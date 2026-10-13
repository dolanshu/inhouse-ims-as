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

"""REQ-F-9 engineering: in-dialog BYE routing on the product runtime path.

After a dialog is established (200 OK with SDP offer/answer), an upstream BYE
must be forwarded to the downstream peer rather than creating a new dialog or
being dropped. The peer's 200 OK to BYE completes teardown on both legs.

re-INVITE and UPDATE in-dialog forwarding are not implemented in the native
forward-mode runtime; this case covers the BYE branch of REQ-F-9.
"""

from __future__ import annotations

import importlib.util
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

# Minimal SDP answer so the product B2BUA can complete offer/answer. The AS
# does not process media (SDP pass-through only); this body is relayed verbatim.
_ANSWER_SDP = (
    b"v=0\r\n"
    b"o=- 0 0 IN IP4 127.0.0.1\r\n"
    b"s=-\r\n"
    b"c=IN IP4 127.0.0.1\r\n"
    b"t=0 0\r\n"
    b"m=audio 9 RTP/AVP 0\r\n"
    b"a=rtpmap:0 PCMU/8000\r\n"
)

# Minimal SDP offer sent on the inbound INVITE so the B2BUA can perform
# offer/answer and relay the downstream 200 OK answer upstream.
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


def _invite(server_port: int, caller_port: int, call_id: str) -> bytes:
    branch = "z9hG4bK-" + uuid.uuid4().hex
    lines = (
        f"INVITE sip:+15558675309@{_HOST}:{server_port} SIP/2.0",
        f"Via: SIP/2.0/UDP {_HOST}:{caller_port};branch={branch};rport",
        "Max-Forwards: 70",
        f"From: <sip:+15551230001@{_HOST}>;tag=bye-test",
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


def _ok_with_sdp(request: bytes, contact_port: int) -> bytes:
    """Build a 200 OK that copies transaction headers and carries an SDP answer."""
    _, headers = parse_sip_message(request)
    vias = _header_values(headers, "via")
    from_value = required_header(headers, "from")
    to_value = required_header(headers, "to")
    call_id = required_header(headers, "call-id")
    cseq = required_header(headers, "cseq")
    if "tag=" not in to_value.lower():
        to_value = f"{to_value};tag=peer-answer"
    lines = ["SIP/2.0 200 OK"]
    lines.extend(f"Via: {via}" for via in vias)
    lines.extend(
        (
            f"From: {from_value}",
            f"To: {to_value}",
            f"Call-ID: {call_id}",
            f"CSeq: {cseq}",
            f"Contact: <sip:peer@127.0.0.1:{contact_port}>",
            "Content-Type: application/sdp",
            f"Content-Length: {len(_ANSWER_SDP)}",
            "",
            "",
        )
    )
    return "\r\n".join(lines).encode("latin-1") + _ANSWER_SDP


def _ok_response(request: bytes) -> bytes:
    """Build a 200 OK with no body (for BYE responses)."""
    _, headers = parse_sip_message(request)
    vias = _header_values(headers, "via")
    from_value = required_header(headers, "from")
    to_value = required_header(headers, "to")
    call_id = required_header(headers, "call-id")
    cseq = required_header(headers, "cseq")
    lines = ["SIP/2.0 200 OK"]
    lines.extend(f"Via: {via}" for via in vias)
    lines.extend(
        (
            f"From: {from_value}",
            f"To: {to_value}",
            f"Call-ID: {call_id}",
            f"CSeq: {cseq}",
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


def _recv_final(sock, timeout: float = _TIMEOUT) -> bytes:
    deadline = time.monotonic() + timeout
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            pytest.fail("timed out waiting for final response")
        sock.settimeout(remaining)
        data, _ = sock.recvfrom(65535)
        start_line, _ = parse_sip_message(data)
        if start_line.startswith("ACK "):
            continue
        status = start_line.split(" ", 2)[1] if len(start_line.split(" ", 2)) >= 2 else ""
        if not status.startswith("1"):
            return data


def test_in_dialog_bye_is_forwarded_to_peer() -> None:
    """REQ-F-9 (BYE branch): an upstream BYE on an established dialog reaches the peer.

    Flow: INVITE -> downstream INVITE -> 200 OK (SDP) -> upstream 200 OK ->
    ACK -> upstream BYE -> downstream BYE -> 200 OK -> upstream 200 OK.
    """
    _require_extension()
    upstream = bind_udp("upstream")
    downstream = bind_udp("downstream")
    downstream_port = downstream.getsockname()[1]
    route_uri = f"sip:peer@{_HOST}:{downstream_port};transport=udp"
    rules = RuleSet(
        rules=(
            Rule(
                rule_id="bye-forward",
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
    call_id = f"bye-dialog-{uuid.uuid4()}@{_HOST}"
    try:
        listener.start()
        # 1. Upstream INVITE
        upstream.sendto(
            _invite(listener.port, upstream.getsockname()[1], call_id),
            (_HOST, listener.port),
        )

        # 2. Downstream receives INVITE
        downstream.settimeout(_TIMEOUT)
        outbound_invite, dum_addr = downstream.recvfrom(65535)
        assert parse_sip_message(outbound_invite)[0].startswith("INVITE ")

        # 3. Peer answers 200 OK with SDP
        downstream.sendto(_ok_with_sdp(outbound_invite, downstream_port), dum_addr)

        # 4. Upstream receives 200 OK (answer relayed)
        upstream_ok = _recv_final(upstream)
        assert parse_sip_message(upstream_ok)[0].startswith("SIP/2.0 200")

        # 5. Upstream sends ACK
        _, ok_headers = parse_sip_message(upstream_ok)
        ack_lines = [
            f"ACK sip:+15558675309@{_HOST}:{listener.port} SIP/2.0",
            f"Via: SIP/2.0/UDP {_HOST}:{upstream.getsockname()[1]};branch=z9hG4bK-ack;rport",
            "Max-Forwards: 70",
            f"From: {required_header(ok_headers, 'from')}",
            f"To: {required_header(ok_headers, 'to')}",
            f"Call-ID: {call_id}",
            "CSeq: 1 ACK",
            "Content-Length: 0",
            "",
            "",
        ]
        upstream.sendto("\r\n".join(ack_lines).encode("ascii"), (_HOST, listener.port))

        # 6. Upstream sends BYE (in-dialog)
        bye_lines = [
            f"BYE sip:+15558675309@{_HOST}:{listener.port} SIP/2.0",
            f"Via: SIP/2.0/UDP {_HOST}:{upstream.getsockname()[1]};branch=z9hG4bK-bye;rport",
            "Max-Forwards: 70",
            f"From: {required_header(ok_headers, 'from')}",
            f"To: {required_header(ok_headers, 'to')}",
            f"Call-ID: {call_id}",
            "CSeq: 2 BYE",
            "Content-Length: 0",
            "",
            "",
        ]
        upstream.sendto("\r\n".join(bye_lines).encode("ascii"), (_HOST, listener.port))

        # 7. Downstream receives BYE (proves in-dialog routing, not new dialog)
        downstream_bye = _recv_final(downstream)
        assert parse_sip_message(downstream_bye)[0].startswith("BYE ")

        # 8. Peer answers 200 OK to BYE
        downstream.sendto(_ok_response(downstream_bye), dum_addr)

        # 9. Upstream receives 200 OK to BYE
        upstream_bye_ok = _recv_final(upstream)
        assert parse_sip_message(upstream_bye_ok)[0].startswith("SIP/2.0 200")
    finally:
        listener.stop()
        upstream.close()
        downstream.close()
