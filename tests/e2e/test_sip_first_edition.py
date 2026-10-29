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

"""Wave 1 end-to-end SIP coverage of the first edition (signalling only, no console).

Scope: ``docs/acceptance/2026-10-09-e2e-test-plan.md`` Wave 1. Three properties make
these cases e2e rather than integration:

* the AS under test is the **product stack** — ``_resip_runtime`` driven through
  ``ResipRuntimeListener`` — never a hand-assembled Python packet;
* the decision path is the **production seam**: ``decide()`` over ``demo_rules()``, with
  ``accept_all_invites`` left off, so a harness shortcut can never stand in for a policy
  decision;
* the call **crosses network-element boundaries** — load generator → simulated S-CSCF →
  simulated S-SBC → AS → peer UAS — and every case asserts a **terminal state**: the
  final response code, the translated outbound user where one is expected, and that no
  session is left unresolved and no BYE errors occurred.

Native extension policy: a missing ``_resip_runtime`` **fails**, it does not skip. A skip
here would re-open the "skip read as green" hole that A2 closed, and e2e run without the
product stack would not be e2e at all. Build it first with
``make m2-platform-resip-build``.

Deliberately out of scope (Wave 1): the 14-message header-by-header replay of
``S1-basic-call`` (Wave 2, tracked in
``docs/acceptance/2026-10-11-wave2-replay-register.md``), the console, kind, and any
capacity number.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from as_load.harness import LoadConfig, run_load
from as_platform.sip.ingress import TransportIngressGate
from as_platform.sip.resip_runtime import ResipRuntimeListener, load_resip_runtime_extension
from as_platform.sip.transport import PeerPolicy, TlsConfig, TransportSeam
from as_simulators.bridge import TransparentBridge
from as_simulators.ca import generate_test_material
from as_simulators.demo_rules import demo_rules
from as_simulators.uas import PeerUas

pytestmark = pytest.mark.e2e

_HOST = "127.0.0.1"

# T1 in the IMS simulator: +8613800138000 is rewritten by the translation rule below.
_T1_CALLER = "+8613800138000"
_T1_TRANSLATED_OUTBOUND_USER = "013800138000"

_TRANSLATION_RULES = json.dumps(
    [
        {
            "rule_id": "t1-plus86",
            "prefix": "+86138",
            "strip_prefix": "+86",
            "add_prefix": "0",
        }
    ]
)


def _require_product_stack() -> object:
    """Return the native runtime, or fail: e2e without the product stack is not e2e."""
    extension = load_resip_runtime_extension()
    if extension is None:
        pytest.fail(
            "platform _resip_runtime extension not built; run make m2-platform-resip-build. "
            "e2e never skips for a missing native extension (A4-2)."
        )
    return extension


def _drive_first_edition(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    transport: str,
    scenarios: tuple[str, ...],
    *,
    peer_invite_status: int = 200,
) -> tuple[dict[str, Any], PeerUas]:
    """Run ``scenarios`` through S-CSCF → S-SBC → AS → peer UAS and return the outcome.

    Returns the load summary plus the peer UAS, which is the only witness of what the AS
    actually put on the outbound leg.
    """
    _require_product_stack()

    material = generate_test_material(tmp_path / "ca") if transport == "tls" else None
    cert = None if material is None else material.certificate
    key = None if material is None else material.private_key
    ca_file = None if material is None else material.ca_certificate
    rules, _translations = demo_rules()
    uas = PeerUas(
        _HOST,
        transport,
        tls_certificate=cert,
        tls_private_key=key,
        invite_status=peer_invite_status,
    )
    south = TransparentBridge(
        advertised_host=_HOST,
        next_hop=(_HOST, uas.port),
        transport=transport,
        tls_certificate=cert,
        tls_private_key=key,
        tls_ca_file=ca_file,
    )
    monkeypatch.setenv("AS_SIP_ROUTE_HOOK", "as_translation.outbound")
    monkeypatch.setenv("AS_SIP_NEXT_HOP", _HOST)
    monkeypatch.setenv("AS_SIP_NEXT_HOP_PORT", str(south.port))
    monkeypatch.setenv("AS_SIP_NEXT_HOP_TLS_PORT", str(south.port))
    monkeypatch.setenv("AS_TRANSLATION_RULES_JSON", _TRANSLATION_RULES)

    if material is None:
        tls = TlsConfig(
            certificate_path="",
            private_key_path="",
            ca_path=None,
            require_client_certificate=False,
        )
    else:
        tls = TlsConfig(
            certificate_path=str(material.certificate),
            private_key_path=str(material.private_key),
            ca_path=str(material.ca_certificate),
            require_client_certificate=False,
        )
    gate = TransportIngressGate(
        TransportSeam(
            tls=tls,
            peer_policy=PeerPolicy(
                allowed_addresses=frozenset({_HOST}),
                allowed_certificate_ids=frozenset(),
            ),
            config_version=1,
        )
    )
    listener = ResipRuntimeListener(
        gate,
        rules,
        enable_udp=transport == "udp",
        enable_tcp=transport == "tcp",
        tls_only=transport == "tls",
        bind_address=_HOST,
        advertised_address=_HOST,
    )
    listener.start()
    if transport == "tls":
        product_port = listener.tls_port
    elif transport == "tcp":
        product_port = listener.tcp_port
    else:
        product_port = listener.port
    assert product_port is not None
    north = TransparentBridge(
        advertised_host=_HOST,
        next_hop=(_HOST, product_port),
        transport=transport,
        tls_certificate=cert,
        tls_private_key=key,
        tls_ca_file=ca_file,
    )
    scscf = TransparentBridge(
        advertised_host=_HOST,
        next_hop=(_HOST, north.port),
        transport=transport,
        tls_certificate=cert,
        tls_private_key=key,
        tls_ca_file=ca_file,
    )
    hops = (uas, south, north, scscf)
    for hop in hops:
        hop.start()
    try:
        summary = run_load(
            LoadConfig(
                host=_HOST,
                port=scscf.port,
                target_cps=25,
                duration_seconds=0.2,
                hold_seconds=0.05,
                workers=1,
                timeout_seconds=10,
                stack_name="ims-sim",
                stack_version="m7.1",
                output_dir=tmp_path / "load",
                transport=transport,
                tls_ca_file=ca_file,
                scenarios=scenarios,
            )
        )
    finally:
        for hop in reversed(hops):
            hop.stop()
        listener.stop()

    assert isinstance(summary, dict)
    return summary, uas


def _terminal_codes(buckets: dict[str, Any], scenario: str) -> dict[str, int]:
    """Return the ``{final response code: call count}`` map one scenario ended with."""
    bucket = buckets[scenario]
    assert isinstance(bucket, dict)
    codes = bucket["response_codes"]
    assert isinstance(codes, dict)
    return dict(codes)


def _bye_errors(summary: dict[str, Any]) -> dict[str, int]:
    """Return the BYE-related error counters of a load summary."""
    errors = summary["error_distribution"]
    assert isinstance(errors, dict)
    return {
        name: count
        for name, count in errors.items()
        if name.startswith("bye_") or name == "timeout_bye"
    }


def test_e2e_sip_1_udp_t1_translated_call_completes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """E2E-SIP-1: a T1 call is answered 200, rewritten on the outbound leg, and torn down."""
    summary, uas = _drive_first_edition(tmp_path, monkeypatch, "udp", ("T1",))

    buckets = summary["by_scenario"]
    assert isinstance(buckets, dict)
    # The call count inside the load window is timing-dependent; the terminal state is not.
    answered = _terminal_codes(buckets, "T1")
    assert set(answered) == {"200"}
    assert sum(answered.values()) >= 1
    assert _T1_TRANSLATED_OUTBOUND_USER in uas.request_users
    assert _T1_CALLER not in uas.request_users
    assert _bye_errors(summary) == {}
    assert summary["counts"]["unresolved_sessions"] == 0
    # Every answered call must have been torn down: no BYE may be left hanging.
    assert uas.request_methods.count("BYE") == sum(answered.values())


def test_e2e_sip_2_udp_t4_no_match_returns_404(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """E2E-SIP-2: an unmatched T4 is rejected 404 and never reaches the peer UAS."""
    summary, uas = _drive_first_edition(tmp_path, monkeypatch, "udp", ("T4",))

    buckets = summary["by_scenario"]
    assert isinstance(buckets, dict)
    rejected = _terminal_codes(buckets, "T4")
    assert set(rejected) == {"404"}
    assert sum(rejected.values()) >= 1
    assert "+155500030003" not in uas.request_users
    assert _bye_errors(summary) == {}
    assert summary["counts"]["unresolved_sessions"] == 0
    assert uas.request_methods.count("BYE") == 0


def test_e2e_sip_3_udp_f2_blocked_returns_603(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """E2E-SIP-3: a blocked F2 is rejected 603 and never reaches the peer UAS."""
    summary, uas = _drive_first_edition(tmp_path, monkeypatch, "udp", ("F2",))

    buckets = summary["by_scenario"]
    assert isinstance(buckets, dict)
    rejected = _terminal_codes(buckets, "F2")
    assert set(rejected) == {"603"}
    assert sum(rejected.values()) >= 1
    assert _bye_errors(summary) == {}
    assert summary["counts"]["unresolved_sessions"] == 0
    assert uas.request_methods.count("BYE") == 0


@pytest.mark.parametrize("transport", ["tcp", "tls"])
def test_e2e_sip_4_stream_transport_t1_completes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    transport: str,
) -> None:
    """E2E-SIP-4: the T1 subset holds on TCP and TLS (test CA; not REQ-S-2 / REQ-S-3)."""
    summary, uas = _drive_first_edition(tmp_path, monkeypatch, transport, ("T1",))

    buckets = summary["by_scenario"]
    assert isinstance(buckets, dict)
    answered = _terminal_codes(buckets, "T1")
    assert set(answered) == {"200"}
    assert sum(answered.values()) >= 1
    assert _T1_TRANSLATED_OUTBOUND_USER in uas.request_users
    assert _bye_errors(summary) == {}
    assert summary["counts"]["unresolved_sessions"] == 0
    assert uas.request_methods.count("BYE") == sum(answered.values())


@pytest.mark.parametrize("status", [486, 480, 408])
def test_e2e_sip_5_udp_non_2xx_passthrough(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    status: int,
) -> None:
    """E2E-SIP-5 (REQ-F-10): downstream 486/480/408 is forwarded upstream unchanged.

    The peer UAS answers the outbound INVITE with a non-2xx final response. The
    AS must propagate that exact code to the inbound leg (not rewrite to 404 or
    502) and must not establish a dialog, so no BYE reaches the peer.
    """
    summary, uas = _drive_first_edition(
        tmp_path,
        monkeypatch,
        "udp",
        ("T5",),
        peer_invite_status=status,
    )

    buckets = summary["by_scenario"]
    assert isinstance(buckets, dict)
    rejected = _terminal_codes(buckets, "T5")
    assert set(rejected) == {str(status)}
    assert sum(rejected.values()) >= 1
    assert _bye_errors(summary) == {}
    assert summary["counts"]["unresolved_sessions"] == 0
    # A non-2xx final response does not establish a dialog: no BYE on the peer.
    assert uas.request_methods.count("BYE") == 0
