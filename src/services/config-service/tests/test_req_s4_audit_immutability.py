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

"""Structural evidence that the audit store is append-only. REQ-S-4.

Everything here reads the programmatic schema bootstrap of
``PostgresAuditStore.ensure_schema``: the trigger DDL it declares and the guard
functions it installs. It proves that the bootstrap *declares* a row-level
``BEFORE UPDATE OR DELETE`` trigger and a statement-level ``BEFORE TRUNCATE``
trigger, and that both guards raise SQLSTATE ``23514`` (check_violation).

This is deliberately **not** the same thing as proving the database refuses a
mutation: a declared trigger is text until a server has fired it. The
database-side measurement — the least-privilege runtime role being refused
UPDATE / DELETE / TRUNCATE with ``InsufficientPrivilege``, and the table owner
being stopped by the trigger with ``CheckViolation`` — lives in
``src/services/config-service/tests/test_postgres_audit_store_integration.py``
(``test_runtime_role_can_append_and_read_only_with_effective_grants``), which
needs a real PostgreSQL server and therefore runs under ``-m integration``,
outside ``make gate``. Both layers are needed; neither replaces the other.
"""

from __future__ import annotations

import ast
import inspect
import textwrap
from typing import Any

import pytest

from as_config_service.audit_store import _AUDIT_GUARD_FUNCTION_BODIES, PostgresAuditStore

pytestmark = pytest.mark.unit

# pg_trigger.tgtype is a bitmask: bit 0 row-level, bit 1 before, bit 2 insert,
# bit 3 delete, bit 4 update, bit 5 truncate. Decoding it here rather than
# hard-coding 27 / 34 keeps the assertion meaningful: the number in the source
# has to be the number these events actually add up to.
_TGTYPE_ROW = 1
_TGTYPE_BEFORE = 2
_TGTYPE_DELETE = 8
_TGTYPE_UPDATE = 16
_TGTYPE_TRUNCATE = 32

ROW_TRIGGER_TYPE = _TGTYPE_ROW | _TGTYPE_BEFORE | _TGTYPE_DELETE | _TGTYPE_UPDATE
TRUNCATE_TRIGGER_TYPE = _TGTYPE_BEFORE | _TGTYPE_TRUNCATE

_UNRESOLVED = "<not a literal>"

_MUTATION_NAMES = (
    "update",
    "delete",
    "truncate",
    "purge",
    "remove",
    "clear",
    "rewrite",
    "modify",
)


def _ensure_schema_source() -> str:
    return textwrap.dedent(inspect.getsource(PostgresAuditStore.ensure_schema))


def _string_literals() -> tuple[str, ...]:
    """Every string literal the schema bootstrap emits as SQL."""
    tree = ast.parse(_ensure_schema_source())
    return tuple(
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    )


def _declared_triggers() -> dict[str, tuple[object, ...]]:
    """The ``expected_triggers`` table inside ``ensure_schema``, by trigger name."""
    tree = ast.parse(_ensure_schema_source())
    declared: dict[str, tuple[object, ...]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == "expected_triggers"
            for target in node.targets
        ):
            continue
        if not isinstance(node.value, ast.Dict):
            continue
        for key, value in zip(node.value.keys, node.value.values, strict=False):
            if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
                continue
            if not isinstance(value, ast.Tuple):
                continue
            declared[key.value] = tuple(
                element.value if isinstance(element, ast.Constant) else _UNRESOLVED
                for element in value.elts
            )
    return declared


def test_bootstrap_declares_a_row_level_update_and_delete_trigger() -> None:
    literals = _string_literals()
    assert "CREATE TRIGGER audit_row_immutable BEFORE UPDATE OR DELETE ON " in literals
    assert " FOR EACH ROW EXECUTE FUNCTION " in literals


def test_bootstrap_declares_a_statement_level_truncate_trigger() -> None:
    literals = _string_literals()
    assert "CREATE TRIGGER audit_table_immutable BEFORE TRUNCATE ON " in literals
    assert " FOR EACH STATEMENT EXECUTE FUNCTION " in literals


def test_declared_trigger_types_are_row_level_and_statement_level() -> None:
    declared = _declared_triggers()
    assert ROW_TRIGGER_TYPE == 27
    assert TRUNCATE_TRIGGER_TYPE == 34
    assert ROW_TRIGGER_TYPE & _TGTYPE_ROW
    assert TRUNCATE_TRIGGER_TYPE & _TGTYPE_ROW == 0
    assert declared["audit_row_immutable"][0] == ROW_TRIGGER_TYPE
    assert declared["audit_table_immutable"][0] == TRUNCATE_TRIGGER_TYPE
    # "O" is pg_trigger.tgenabled: the trigger fires in the default origin mode.
    assert declared["audit_row_immutable"][1] == "O"
    assert declared["audit_table_immutable"][1] == "O"


def test_guard_function_bodies_raise_check_violation() -> None:
    assert set(_AUDIT_GUARD_FUNCTION_BODIES) == {"row", "truncate"}
    for body in _AUDIT_GUARD_FUNCTION_BODIES.values():
        assert "RAISE EXCEPTION" in body
        assert "USING ERRCODE = '23514'" in body
    assert "audit rows are immutable" in _AUDIT_GUARD_FUNCTION_BODIES["row"]
    assert "audit table is append-only" in _AUDIT_GUARD_FUNCTION_BODIES["truncate"]


def test_bootstrap_installs_the_guard_functions_with_the_declared_bodies() -> None:
    literals = _string_literals()
    for body in _AUDIT_GUARD_FUNCTION_BODIES.values():
        assert any(body in literal for literal in literals), (
            f"no CREATE FUNCTION statement carries the guard body {body!r}"
        )
    assert "CREATE FUNCTION " in literals
    assert any(
        literal.startswith(
            "() RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS $audit_guard$"
        )
        for literal in literals
    )


def test_bootstrap_takes_an_access_exclusive_lock_before_granting() -> None:
    assert " IN ACCESS EXCLUSIVE MODE" in _string_literals()


def test_store_exposes_no_mutation_api() -> None:
    store = PostgresAuditStore(_NoConnection())
    for name in _MUTATION_NAMES:
        assert not hasattr(store, name), f"audit store gained a {name}() operation"
    public_api = sorted(name for name in dir(store) if not name.startswith("_"))
    assert public_api == [
        "append",
        "connection",
        "ensure_schema",
        "list_events",
        "prefix",
        "qualified_sequence",
        "qualified_table",
        "schema",
        "sequence",
        "table",
        "validate_runtime_connection",
    ]


class _NoConnection:
    """A connection placeholder: these assertions never reach the database."""

    def cursor(self) -> Any:  # pragma: no cover - never called
        raise AssertionError("structural assertions must not execute SQL")

    def commit(self) -> None:  # pragma: no cover - never called
        raise AssertionError("structural assertions must not execute SQL")

    def rollback(self) -> None:  # pragma: no cover - never called
        raise AssertionError("structural assertions must not execute SQL")
