# Inhouse-IMS-AS — Copyright 2026 Dolan Shu <dolan.d.shu@gmail.com>, Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

"""REQ-S-4 role/permission matrix at the HTTP boundary, against real PostgreSQL.

``services/console/tests/test_access.py`` already proves the matrix as a pure
function: for every role and every permission it asserts what ``authorize``
returns. What it cannot prove is that a request actually meets that decision —
that the endpoint carrying a write operation calls the matching
``require_*_permission`` before it does anything else, and that a refusal is
still written to the audit trail.

This module closes that gap from the outside: it logs in as each role, issues
the real HTTP request, and asserts the status code and the persisted audit
line. It reuses the application, session and login helpers from
``test_postgres_auth_api_integration`` so the wiring under test is the same
wiring that module exercises.

Covered operations and their enforcement point in
``services/config-service/src/as_config_service/api.py``:

* ``read``          — router dependency ``require_config_read`` (READ_CONFIG)
* ``submit``        — ``require_submit_permission``   (SUBMIT_CHANGE)
* ``approve``       — ``require_approve_permission``  (APPROVE_CHANGE)
* ``rollback``      — ``require_rollback_permission`` (ROLLBACK_CHANGE)
* ``manage_users``  — ``require_manage_users``        (MANAGE_USERS)

The two-person rule is *not* part of the matrix rows: whoever submitted a
change may not approve it, which would otherwise read as "APPROVER gets 403 on
approve" and be counted as a missing permission. Every change order the matrix
acts on is therefore drafted and submitted by ``matrix-submitter`` — a
principal that is never the role under test — so a 403 on approve can only come
from the permission check. The rule itself is asserted separately in
``test_creator_may_not_approve_their_own_change``.
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient
from test_postgres_auth_api_integration import (
    PgHarness,
    _app,
    _audit_events,
    _bootstrap,
    _change_order_payload,
    _login,
    _only_new_audit_event,
)

# Re-exported so pytest collects it as this module's harness fixture. No static
# checker can see a fixture request: it is resolved from the parameter name.
from test_postgres_auth_api_integration import pg as pg_harness  # noqa: F401

from as_console.access import AuditOutcome, Role

pytestmark = pytest.mark.integration

_ADMIN_ID = "admin-1"
_ADMIN_PASSWORD = "admin-password-long"

_ROLE_CREDENTIALS: dict[str, tuple[str, str]] = {
    "viewer": ("matrix-viewer", "matrix-viewer-password-long"),
    "operator": ("matrix-operator", "matrix-operator-password-long"),
    "approver": ("matrix-approver", "matrix-approver-password-long"),
    "submitter": ("matrix-submitter", "matrix-submitter-password-long"),
    "admin": (_ADMIN_ID, _ADMIN_PASSWORD),
}

# `matrix-submitter` is never a role under test: it only drafts and submits the
# change orders the matrix rows act on, so a 403 on approve cannot come from the
# two-person rule and must come from the permission check.
_NON_ADMIN_ROLES: tuple[tuple[str, str, Role], ...] = (
    ("matrix-viewer", "matrix-viewer-password-long", Role.VIEWER),
    ("matrix-operator", "matrix-operator-password-long", Role.OPERATOR),
    ("matrix-approver", "matrix-approver-password-long", Role.APPROVER),
    ("matrix-submitter", "matrix-submitter-password-long", Role.OPERATOR),
)

# (operation, role, expected status). The permission column of ROLE_PERMISSIONS
# in services/console/src/as_console/access.py, read as an HTTP status.
_MATRIX: tuple[tuple[str, str, int], ...] = (
    ("read", "viewer", 200),
    ("read", "operator", 200),
    ("read", "approver", 200),
    ("read", "admin", 200),
    ("submit", "viewer", 403),
    ("submit", "operator", 201),
    ("submit", "approver", 201),
    ("submit", "admin", 201),
    ("approve", "viewer", 403),
    ("approve", "operator", 403),
    ("approve", "approver", 200),
    ("approve", "admin", 200),
    ("rollback", "viewer", 403),
    ("rollback", "operator", 403),
    ("rollback", "approver", 200),
    ("rollback", "admin", 200),
    ("manage_users", "viewer", 403),
    ("manage_users", "operator", 403),
    ("manage_users", "approver", 403),
    ("manage_users", "admin", 200),
)

# The 403 detail every denial carries. Asserting it keeps a row from being
# satisfied by some other 403 (CSRF, the two-person rule, a missing resource).
_DENIAL_DETAIL: dict[str, str] = {
    "submit": "change submission denied",
    "approve": "change approval denied",
    "rollback": "change rollback denied",
    "manage_users": "user management denied",
}


def _proposal_payload(rule_id: str) -> dict[str, object]:
    return {
        "bundle": {"version": "v1", "rules": [], "toggles": []},
        "managed_rule_change": {
            "action": "create",
            "rule_id": rule_id,
            "proposed_rule": {
                "rule_id": rule_id,
                "name": "RBAC matrix rule",
                "match_field": "called",
                "match_mode": "prefix",
                "match_value": "+8613",
                "target_service": "translation",
                "enabled": True,
                "target_detail": "return-uas",
            },
        },
    }


def _prepare(pg: PgHarness) -> None:
    """Bootstrap the admin and add one user per non-admin role."""
    _bootstrap(pg)
    for user_id, password, role in _NON_ADMIN_ROLES:
        pg.auth_store.create_user(user_id, password, {role}, pg.clock[0])


def _client_for(pg: PgHarness, role: str) -> tuple[TestClient, str]:
    user_id, password = _ROLE_CREDENTIALS[role]
    client = TestClient(_app(pg), base_url="https://testserver")
    csrf = _login(client, user_id, password)
    return client, csrf


def _submitted_change_order(pg: PgHarness, rule_id: str) -> str:
    """A change order drafted and submitted by a principal that is never under test."""
    submitter, submitter_csrf = _client_for(pg, "submitter")
    created = submitter.post(
        "/internal/v1/change-orders",
        json=_proposal_payload(rule_id),
        headers={"X-CSRF-Token": submitter_csrf},
    )
    assert created.status_code == 201, created.text
    change_id = created.json()["record"]["order"]["change_id"]
    submitted = submitter.post(
        f"/internal/v1/change-orders/{change_id}/submit",
        headers={"X-CSRF-Token": submitter_csrf},
    )
    assert submitted.status_code == 200, submitted.text
    return change_id


def _distributing_change_order(pg: PgHarness, rule_id: str, version: int) -> tuple[str, int, int]:
    """A change order whose distribution is in progress, ready to be rolled back."""
    change_id = _submitted_change_order(pg, rule_id)
    approver, approver_csrf = _client_for(pg, "approver")
    approved = approver.post(
        f"/internal/v1/change-orders/{change_id}/approve",
        headers={"X-CSRF-Token": approver_csrf},
    )
    assert approved.status_code == 200, approved.text
    order_revision = approved.json()["revision"]
    started = approver.post(
        f"/internal/v1/change-orders/{change_id}/distribution",
        json={
            "version": version,
            "batches": [["as-1"], ["as-2"]],
            "expected_change_order_revision": order_revision,
        },
        headers={"X-CSRF-Token": approver_csrf},
    )
    assert started.status_code == 201, started.text
    payload = started.json()
    return change_id, payload["distribution"]["revision"], payload["change_order"]["revision"]


def _issue(pg: PgHarness, operation: str, role: str, client: TestClient, csrf: str) -> Any:
    if operation == "read":
        return client.get("/internal/v1/managed-rules")
    if operation == "submit":
        return client.post(
            "/internal/v1/change-orders",
            json=_change_order_payload(),
            headers={"X-CSRF-Token": csrf},
        )
    if operation == "approve":
        change_id = _submitted_change_order(pg, f"rule-approve-{role}")
        return client.post(
            f"/internal/v1/change-orders/{change_id}/approve",
            headers={"X-CSRF-Token": csrf},
        )
    if operation == "rollback":
        change_id, distribution_revision, change_order_revision = _distributing_change_order(
            pg, f"rule-rollback-{role}", 21
        )
        return client.post(
            f"/internal/v1/change-orders/{change_id}/distribution/rollback",
            json={
                "expected_distribution_revision": distribution_revision,
                "expected_change_order_revision": change_order_revision,
                "reason": "rbac matrix rollback probe",
            },
            headers={"X-CSRF-Token": csrf},
        )
    if operation == "manage_users":
        return client.get("/internal/v1/auth/users")
    raise AssertionError(f"unknown matrix operation: {operation}")


@pytest.mark.parametrize(("operation", "role", "expected_status"), _MATRIX)
def test_http_boundary_enforces_the_role_permission_matrix(
    pg_harness: PgHarness,  # noqa: F811 - the fixture request, not a redefinition
    operation: str,
    role: str,
    expected_status: int,
) -> None:
    """Every role meets the same endpoint; only the permission decides the status."""
    _prepare(pg_harness)
    client, csrf = _client_for(pg_harness, role)

    response = _issue(pg_harness, operation, role, client, csrf)

    assert response.status_code == expected_status, response.text
    if expected_status == 403:
        # A CSRF refusal, the two-person rule and a missing resource are all 403
        # too; the detail pins this row to the permission check itself.
        assert response.json()["detail"] == _DENIAL_DETAIL[operation], response.text


def test_denied_write_at_the_http_boundary_persists_a_denied_audit_row(
    pg_harness: PgHarness,  # noqa: F811 - the fixture request, not a redefinition
) -> None:
    """A 403 must leave a trail: the refusal itself is what REQ-S-4 asks to record."""
    _prepare(pg_harness)
    client, csrf = _client_for(pg_harness, "viewer")

    before = len(_audit_events(pg_harness))
    denied = client.post(
        "/internal/v1/change-orders",
        json=_change_order_payload(),
        headers={"X-CSRF-Token": csrf},
    )

    assert denied.status_code == 403
    # "change submission denied" is require_submit_permission; a CSRF refusal
    # would say "CSRF validation failed", so this pins the 403 to the permission.
    assert denied.json()["detail"] == "change submission denied"
    record = _only_new_audit_event(pg_harness, before)
    assert record.actor == "matrix-viewer"
    assert record.outcome is AuditOutcome.DENIED
    assert record.action == "POST /internal/v1/change-orders"
    assert record.resource == "/internal/v1/change-orders"
    assert record.before_value is record.after_value is None

    # The same line, read straight out of the append-only table this time, so
    # the assertion names the table and the columns it depends on:
    # <audit schema>.<prefix>_audit_events(actor, action, resource, outcome).
    table = pg_harness.audit_store.qualified_table
    cursor = pg_harness.connection.cursor()
    cursor.execute(f"SELECT actor, action, resource, outcome FROM {table} ORDER BY id")
    rows = cursor.fetchall()
    pg_harness.connection.rollback()
    assert (
        "matrix-viewer",
        "POST /internal/v1/change-orders",
        "/internal/v1/change-orders",
        "denied",
    ) in rows


def test_creator_may_not_approve_their_own_change(
    pg_harness: PgHarness,  # noqa: F811 - the fixture request, not a redefinition
) -> None:
    """The two-person rule, so it is never read as a missing APPROVE_CHANGE grant."""
    _prepare(pg_harness)
    approver, approver_csrf = _client_for(pg_harness, "approver")
    created = approver.post(
        "/internal/v1/change-orders",
        json=_proposal_payload("rule-self-approval"),
        headers={"X-CSRF-Token": approver_csrf},
    )
    assert created.status_code == 201, created.text
    change_id = created.json()["record"]["order"]["change_id"]
    submitted = approver.post(
        f"/internal/v1/change-orders/{change_id}/submit",
        headers={"X-CSRF-Token": approver_csrf},
    )
    assert submitted.status_code == 200, submitted.text

    before = len(_audit_events(pg_harness))
    self_approval = approver.post(
        f"/internal/v1/change-orders/{change_id}/approve",
        headers={"X-CSRF-Token": approver_csrf},
    )

    assert self_approval.status_code == 403
    assert self_approval.json()["detail"] == "creator may not approve this change"
    record = _only_new_audit_event(pg_harness, before)
    assert record.actor == "matrix-approver"
    assert record.outcome is AuditOutcome.DENIED
    assert record.action == "POST /internal/v1/change-orders/{change_id}/approve"
