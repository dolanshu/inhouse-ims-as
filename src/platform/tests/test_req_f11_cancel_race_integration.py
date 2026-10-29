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

"""REQ-F-11 engineering: CANCEL race on the product runtime forward path.

Branch 1 (RFC 3261 valid path): the upstream CANCEL arrives before the
downstream peer's final response. The AS must forward the CANCEL to the
downstream leg (not create a new dialog, not drop it), the peer answers 487,
and the AS propagates 487 upstream with an ACK.

Branch 2 (final response already arrived) is timing-sensitive and is registered
as a gap; see the FAILCLOSED artifact for S11.
"""

from __future__ import annotations

import importlib.util
import re
import time
import uuid
from pathlib import Path

import pytest
from native_extensions import require_resip_runtime_extension

from as_platform.decision import Rule, RuleSet
from as_platform.decision.rules import Action
from as_platform.sip.ingress import TransportIngressGate
from as_platform.sip.resip_runtime import ResipRuntimeListener
from as_platform.sip.transport import PeerPolicy, TlsConfig, TransportSeam

_FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "two_leg_udp_peer.py"
_spec = importlib.util.spec_from_file_location("two_leg_udp_peer", _FIXTURE_PATH)
assert _spec is not None and _spec.loader is not None
_peer = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_peer)
bind_udp = _peer.bind_udp
parse_sip_message = _peer.parse_sip_message
required_header = _peer.required_header

pytestmark = pytest.mark.integration

_HOST = "127.0.0.1"
_TIMEOUT = 8.0
_TLS = TlsConfig(
    certificate_path="",
    private_key_path="",
    require_client_certificate=False,
)

_OFFER_SDP = (
    b"v=0\r\n"
    b"o=- 0 0 IN IP4 127.0.0.1\r\n"
    b"s=-\r\n"
    b"c=IN IP4 127.0.0.1\r\n"
    b"t=0 0\r\n"
    b"m=audio 9 RTP/AVP 0\r\n"
    b"a=rtpmap:0 PCMU/8000\r\n"
)


def _require_extension() -> object:
    return require_resip_runtime_extension()


def _invite(server_port: int, caller_port: int, call_id: str, branch: str) -> bytes:
    lines = (
        f"INVITE sip:+15558675309@{_HOST}:{server_port} SIP/2.0",
        f"Via: SIP/2.0/UDP {_HOST}:{caller_port};branch={branch};rport",
        "Max-Forwards: 70",
        f"From: <sip:+15551230001@{_HOST}>;tag=cancel-test",
        f"To: <sip:+15558675309@{_HOST}>",
        f"Call-ID: {call_id}",
        "CSeq: 1 INVITE",
        f"Contact: <sip:+15551230001@{_HOST}:{caller_port}>",
        "Content-Type: application/sdp",
        f"Content-Length: {len(_OFFER_SDP)}",
        "",
        "",
    )
    return "\r\n".join(lines).encode("ascii") + _OFFER_SDP


def _cancel(server_port: int, caller_port: int, call_id: str, branch: str) -> bytes:
    """Build a CANCEL matching the INVITE's Call-ID, From tag, and Via branch."""
    lines = (
        f"CANCEL sip:+15558675309@{_HOST}:{server_port} SIP/2.0",
        f"Via: SIP/2.0/UDP {_HOST}:{caller_port};branch={branch};rport",
        "Max-Forwards: 70",
        f"From: <sip:+15551230001@{_HOST}>;tag=cancel-test",
        f"To: <sip:+15558675309@{_HOST}>",
        f"Call-ID: {call_id}",
        "CSeq: 1 CANCEL",
        "Content-Length: 0",
        "",
        "",
    )
    return "\r\n".join(lines).encode("ascii")


def _response(request: bytes, status: int, reason: str) -> bytes:
    _, headers = parse_sip_message(request)
    vias = _header_values(headers, "via")
    from_value = required_header(headers, "from")
    to_value = required_header(headers, "to")
    call_id = required_header(headers, "call-id")
    cseq = required_header(headers, "cseq")
    # 100 Trying never carries a To tag; any other response establishes or
    # confirms a dialog and must carry one so reSIProcate can build the
    # outbound dialog set (required for CANCEL forwarding).
    if status != 100 and not re.search(r"(?:^|;)\s*tag\s*=", to_value, flags=re.IGNORECASE):
        to_value = f"{to_value};tag=peer-resp"
    lines = [f"SIP/2.0 {status} {reason}"]
    lines.extend(f"Via: {via}" for via in vias)
    lines.extend(
        (
            f"From: {from_value}",
            f"To: {to_value}",
            f"Call-ID: {call_id}",
            f"CSeq: {cseq}",
        )
    )
    # Dialog-establishing responses need a Contact header so reSIProcate can
    # set the remote target for the early/confirmed dialog. Derive the peer's
    # host:port from the To URI (the outbound INVITE's destination).
    if status != 100:
        uri_match = re.search(r"<sip:[^>]*@([^:;>]+):(\d+)[^>]*>", to_value)
        if uri_match:
            lines.append(f"Contact: <sip:peer@{uri_match.group(1)}:{uri_match.group(2)}>")
    lines.extend(
        (
            "Content-Length: 0",
            "",
            "",
        )
    )
    return "\r\n".join(lines).encode("latin-1")


def _header_values(headers: dict[str, list[str]], name: str) -> list[str]:
    compact = {"via": ("via", "v")}
    values: list[str] = []
    for candidate in compact.get(name, (name,)):
        values.extend(headers.get(candidate, ()))
    return values


def _recv_until(sock, predicate, timeout: float = _TIMEOUT) -> bytes:
    deadline = time.monotonic() + timeout
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            pytest.fail("timed out waiting for matching message")
        sock.settimeout(remaining)
        data, _ = sock.recvfrom(65535)
        if predicate(data):
            return data


def test_cancel_before_downstream_final_is_forwarded() -> None:
    """REQ-F-11 branch 1: upstream CANCEL before peer final response.

    The peer sends 180 Ringing (establishing an early dialog) but no final
    response, so when CANCEL arrives the AS must forward it downstream. The
    peer answers 487 to the CANCEL and the AS propagates 487 upstream.
    """
    _require_extension()
    upstream = bind_udp("upstream")
    downstream = bind_udp("downstream")
    downstream_port = downstream.getsockname()[1]
    route_uri = f"sip:peer@{_HOST}:{downstream_port};transport=udp"
    rules = RuleSet(
        rules=(
            Rule(
                rule_id="cancel-forward",
                prefix="+15558675309",
                action=Action.FORWARD,
                target=route_uri,
            ),
        )
    )
    gate = TransportIngressGate(
        TransportSeam(
            tls=_TLS,
            peer_policy=PeerPolicy(
                allowed_addresses=frozenset({_HOST}),
                allowed_certificate_ids=frozenset(),
            ),
            config_version=1,
        )
    )
    listener = ResipRuntimeListener(gate, rules)
    call_id = f"cancel-race-{uuid.uuid4()}@{_HOST}"
    branch = "z9hG4bK-" + uuid.uuid4().hex
    try:
        listener.start()
        # 1. Upstream INVITE
        upstream.sendto(
            _invite(listener.port, upstream.getsockname()[1], call_id, branch),
            (_HOST, listener.port),
        )

        # 2. Downstream receives INVITE and answers 180 Ringing (establishes the
        #    early dialog so the outbound dialog set exists). The CANCEL then
        #    arrives before any *final* response, exercising the cancel-forward
        #    path of REQ-F-11 branch 1.
        downstream.settimeout(_TIMEOUT)
        outbound_invite, dum_addr = downstream.recvfrom(65535)
        assert parse_sip_message(outbound_invite)[0].startswith("INVITE ")
        downstream.sendto(_response(outbound_invite, 180, "Ringing"), dum_addr)
        # Let reSIProcate process the 180 and create the outbound dialog set.
        time.sleep(0.3)

        # 3. Upstream CANCEL (before any downstream *final* response)
        upstream.sendto(
            _cancel(listener.port, upstream.getsockname()[1], call_id, branch),
            (_HOST, listener.port),
        )

        # 4. Downstream receives CANCEL, not BYE (early dialog cancellation)
        downstream_cancel = _recv_until(
            downstream,
            lambda data: parse_sip_message(data)[0].startswith("CANCEL "),
        )

        # 5. Peer answers 487 to the CANCEL
        downstream.sendto(_response(downstream_cancel, 487, "Request Terminated"), dum_addr)

        # 6. Upstream receives 487 (propagated, not rewritten)
        upstream_487 = _recv_until(
            upstream,
            lambda data: parse_sip_message(data)[0].startswith("SIP/2.0 487"),
        )
        assert required_header(parse_sip_message(upstream_487)[1], "call-id") == call_id
    finally:
        listener.stop()
        upstream.close()
        downstream.close()
