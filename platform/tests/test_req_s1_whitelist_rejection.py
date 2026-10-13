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

"""REQ-S-1 engineering: the product INVITE path answers a whitelist miss with 403.

Why this file exists
--------------------
``platform/src/as_platform/sip/resip_runtime.py`` defines ``_INGRESS_DENIED_STATUS = 403``
and returns it from :meth:`ResipRuntimeListener._on_invite` on two branches
(``:334-335`` plaintext-when-TLS-required, ``:345-346`` ``gate.check_peer`` miss), but
no unit test asserted that status: the only 403 assertions lived in integration tests
(``test_resip_runtime_integration.py:151``, ``test_resip_runtime_tls_policy_integration.py:196``)
and depend on the cmake-built ``_resip_runtime`` extension, so ``make gate`` — layer ①,
``-m "unit or contract"`` — carried no pin on the product reject path at all.

Scope of the stand-in (read before citing this file)
----------------------------------------------------
Each test drives **the real** ``ResipRuntimeListener._on_invite`` — the very callable the
native extension invokes per INVITE — on a listener built by its real ``__init__``
(no ``object.__new__``, no attribute patching, no monkeypatching of the gate). What is
replaced is only what sits *around* it:

* no socket and no native extension — nothing binds, nothing is sent on the wire;
* ``received_at`` is injected as a probe, so "``decide()`` never ran" is asserted
  positively rather than inferred from the status code alone.

What is therefore **not** covered here: the native transport actually emitting a SIP
``403 Forbidden`` response for that return value. That wire behaviour stays covered by
the integration tests named above (UDP / TLS) and is out of scope for layer ①.

See ADR-0016 (in-boundary security: peer whitelist, end-to-end TLS): the entry check is
fail-closed — an unfilled whitelist authorises nobody
(``platform/src/as_platform/sip/transport.py:272-273``).
"""

from __future__ import annotations

from typing import Any

import pytest

from as_platform.decision import RuleSet
from as_platform.sip.ingress import TransportIngressGate
from as_platform.sip.resip_runtime import ResipRuntimeListener
from as_platform.sip.transport import PeerPolicy, TlsConfig, TransportSeam

pytestmark = pytest.mark.unit

# The literal wire status a denied peer must receive. Asserting the literal (rather than
# importing resip_runtime._INGRESS_DENIED_STATUS) is deliberate: the contract that matters
# to the S-SBC is the number on the wire, so a change to the constant must break here.
_DENIED_STATUS = 403

_HOST = "127.0.0.1"

# mTLS-by-default material; ca_path is required by TlsConfig.__post_init__.
_TLS = TlsConfig(
    certificate_path="/etc/as/tls/as.pem",
    private_key_path="/etc/as/tls/as.key",
    ca_path="/etc/as/tls/ca.pem",
)


def _seam(
    allowed_addresses: frozenset[str],
    allowed_certificate_ids: frozenset[str] = frozenset(),
) -> TransportSeam:
    """Build one transport seam carrying the whitelist under test (ADR-0016)."""
    return TransportSeam(
        tls=_TLS,
        peer_policy=PeerPolicy(
            allowed_addresses=allowed_addresses,
            allowed_certificate_ids=allowed_certificate_ids,
        ),
        config_version=1,
    )


def _listener(
    seam: TransportSeam, *, tls_only: bool = False
) -> tuple[ResipRuntimeListener, list[str]]:
    """Build a real listener plus a probe recording whether ``decide()`` was reached.

    ``received_at`` is only consulted inside ``decide()``, so a non-empty probe proves the
    INVITE passed ingress; an empty probe proves it was stopped before the kernel.

    Args:
        seam: The whitelist/TLS configuration in force for this listener.
        tls_only: When ``True``, plaintext transports are rejected at ingress.

    Returns:
        The listener and the shared probe list.
    """
    decide_probe: list[str] = []

    def received_at() -> float:
        decide_probe.append("received_at")
        return 0.0

    listener = ResipRuntimeListener(
        TransportIngressGate(seam),
        RuleSet(rules=()),
        tls_only=tls_only,
        received_at=received_at,
    )
    return listener, decide_probe


def _peer_dict(
    *,
    address: str = _HOST,
    port: int = 5060,
    transport: str = "tls",
    certificate_id: str | None = None,
) -> dict[str, Any]:
    """Shape of the peer dict the native binding hands to ``_on_invite``."""
    peer: dict[str, Any] = {"address": address, "port": port, "transport": transport}
    if certificate_id is not None:
        peer["certificate_id"] = certificate_id
    return peer


def _sip_summary() -> dict[str, Any]:
    """Minimal INVITE summary; fields past ingress are irrelevant to a denial."""
    return {
        "method": "INVITE",
        "request_uri": f"sips:+15558675309@{_HOST}",
        "call_id": "s1-whitelist-rejection@test",
        "calling_number": "+15551230001",
        "called_number": "+15558675309",
        "body": b"",
    }


def test_on_invite_returns_403_when_peer_address_is_not_whitelisted() -> None:
    listener, decide_probe = _listener(_seam(frozenset({"10.0.0.1"})))

    assert listener._on_invite(_peer_dict(), _sip_summary()) == _DENIED_STATUS
    assert decide_probe == []


def test_on_invite_returns_403_when_whitelist_is_empty() -> None:
    """Fail-closed: a whitelist that was never filled in authorises nobody (ADR-0016)."""
    listener, decide_probe = _listener(_seam(frozenset()))

    assert listener._on_invite(_peer_dict(), _sip_summary()) == _DENIED_STATUS
    assert decide_probe == []


def test_on_invite_returns_403_when_certificate_id_is_not_whitelisted() -> None:
    """Certificate-only policy: a token outside ``allowed_certificate_ids`` is denied."""
    listener, decide_probe = _listener(_seam(frozenset(), frozenset({"sha256:" + "a" * 64})))

    assert (
        listener._on_invite(
            _peer_dict(certificate_id="sha256:" + "b" * 64),
            _sip_summary(),
        )
        == _DENIED_STATUS
    )
    assert decide_probe == []


def test_on_invite_allows_a_listed_address_that_presents_an_unknown_certificate() -> None:
    """Pin the OR semantics of :func:`authorize_peer` as they are, not as one might wish.

    ``platform/src/as_platform/sip/transport.py:276-298``: the address dimension and the
    certificate dimension are **OR-ed** — a hit on either authorises the peer. So a peer
    whose address is listed is admitted even when its certificate token is unknown or
    absent. This test records that behaviour so it is never mistaken for mTLS enforcement;
    it is not an endorsement of it, and changing it is a policy decision for a maintainer.
    """
    listener, decide_probe = _listener(_seam(frozenset({_HOST}), frozenset({"sha256:" + "a" * 64})))

    assert (
        listener._on_invite(
            _peer_dict(certificate_id="sha256:" + "b" * 64),
            _sip_summary(),
        )
        == 404
    )
    assert decide_probe == ["received_at"]


def test_on_invite_returns_403_when_peer_port_is_outside_endpoint_whitelist() -> None:
    """Endpoint token ``host:port``: the port is part of the identity."""
    listener, decide_probe = _listener(_seam(frozenset({f"{_HOST}:5060"})))

    assert listener._on_invite(_peer_dict(port=5061), _sip_summary()) == _DENIED_STATUS
    assert decide_probe == []


def test_on_invite_returns_403_when_peer_is_outside_allowed_cidr() -> None:
    listener, decide_probe = _listener(_seam(frozenset({"10.0.0.0/8"})))

    assert listener._on_invite(_peer_dict(), _sip_summary()) == _DENIED_STATUS
    assert decide_probe == []


def test_on_invite_returns_403_for_plaintext_udp_when_tls_is_required() -> None:
    """Even a whitelisted peer is denied on UDP when the trunk mandates TLS."""
    listener, decide_probe = _listener(_seam(frozenset({_HOST})), tls_only=True)

    assert listener._on_invite(_peer_dict(transport="udp"), _sip_summary()) == _DENIED_STATUS
    assert decide_probe == []


def test_on_invite_does_not_deny_a_whitelisted_peer() -> None:
    """Control for the six denials above: 403 is specific to a rejected peer.

    The whitelisted INVITE reaches ``decide()`` (probe non-empty) and an empty rule set
    yields 404, not 403 — so a green run of the denial tests cannot be explained by the
    harness returning 403 unconditionally.
    """
    listener, decide_probe = _listener(_seam(frozenset({_HOST})))

    assert listener._on_invite(_peer_dict(), _sip_summary()) == 404
    assert decide_probe == ["received_at"]


def test_on_invite_accepts_a_matching_certificate_id_without_a_listed_address() -> None:
    """Under mTLS the certificate identifies the peer; a hit on it authorises ingress."""
    fingerprint = "sha256:" + "c" * 64
    listener, decide_probe = _listener(_seam(frozenset(), frozenset({fingerprint})))

    assert listener._on_invite(_peer_dict(certificate_id=fingerprint), _sip_summary()) == 404
    assert decide_probe == ["received_at"]
