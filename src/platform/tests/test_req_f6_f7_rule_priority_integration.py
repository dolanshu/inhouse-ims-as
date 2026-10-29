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

"""REQ-F-6 / REQ-F-7 engineering: multi-rule priority on the runtime path.

These integration cases exercise the production decision seam through
``ResipRuntimeListener`` with a rule set built from **overlapping** prefixes, so
the winner-selection logic (action rank first, then longest prefix) is actually
exercised end-to-end rather than only at the unit level.

Coverage:
* REQ-F-7: a ``BLOCK`` rule outranks a ``TRANSLATE`` rule whose prefix also
  matches, even when the translate prefix is shorter (action rank dominates).
* REQ-F-6: within one action, the longest matching prefix wins and *its*
  translation rule is the one applied to the outbound user.
* REQ-F-6: a number that matches no prefix yields 404 and no downstream INVITE.
"""

from __future__ import annotations

import importlib.util
import json
import re
import socket
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
header_values = _peer.header_values
required_header = _peer.required_header

pytestmark = pytest.mark.integration

_HOST = "127.0.0.1"
_TIMEOUT = 8.0
_NO_DOWNSTREAM_TIMEOUT = 1.5
_TLS = TlsConfig(
    certificate_path="",
    private_key_path="",
    require_client_certificate=False,
)

# Translation rules keyed by routing rule_id. The two TRANSLATE rules produce
# distinguishable user parts so the test can tell which prefix length won.
_PRIORITY_TRANSLATION_RULES = json.dumps(
    [
        {
            "rule_id": "t-short",
            "prefix": "+86755",
            "strip_prefix": "+86",
            "add_prefix": "0",
        },
        {
            "rule_id": "t-long",
            "prefix": "+8675512",
            "strip_prefix": "+8675512",
            "add_prefix": "9",
        },
    ]
)


def _require_extension() -> object:
    return require_resip_runtime_extension()


def _build_rules(downstream_port: int) -> RuleSet:
    """Overlapping-prefix rule set that forces real winner selection.

    * ``b-168`` (BLOCK, +86168) and ``t-16`` (TRANSLATE, +8616) both match
      +86168xxxxxx: the block must win (REQ-F-7).
    * ``t-short`` (TRANSLATE, +86755) and ``t-long`` (TRANSLATE, +8675512) both
      match +8675512xxxx: the longer prefix must win (REQ-F-6).
    """
    route_uri = f"sip:peer@{_HOST}:{downstream_port};transport=udp"
    return RuleSet(
        rules=(
            Rule(rule_id="b-168", prefix="+86168", action=Action.BLOCK, target=None),
            Rule(rule_id="t-16", prefix="+8616", action=Action.TRANSLATE, target=route_uri),
            Rule(rule_id="t-short", prefix="+86755", action=Action.TRANSLATE, target=route_uri),
            Rule(rule_id="t-long", prefix="+8675512", action=Action.TRANSLATE, target=route_uri),
        )
    )


def _invite(called: str, server_port: int, caller_port: int, call_id: str) -> bytes:
    branch = "z9hG4bK-" + uuid.uuid4().hex
    sdp = (
        "v=0\r\n"
        "o=- 0 0 IN IP4 127.0.0.1\r\n"
        "s=-\r\n"
        "c=IN IP4 127.0.0.1\r\n"
        "t=0 0\r\n"
        "m=audio 9 RTP/AVP 0\r\n"
        "a=rtpmap:0 PCMU/8000\r\n"
    )
    lines = (
        f"INVITE sip:{called}@{_HOST}:{server_port} SIP/2.0",
        f"Via: SIP/2.0/UDP {_HOST}:{caller_port};branch={branch};rport",
        "Max-Forwards: 70",
        f"From: <sip:+8613911111111@{_HOST}>;tag=priority",
        f"To: <sip:{called}@{_HOST}>",
        f"Call-ID: {call_id}",
        "CSeq: 1 INVITE",
        f"Contact: <sip:+8613911111111@{_HOST}:{caller_port}>",
        "Content-Type: application/sdp",
        f"Content-Length: {len(sdp)}",
        "",
        sdp,
    )
    return "\r\n".join(lines).encode("ascii")


def _recv_with_timeout(sock: socket.socket, timeout: float) -> bytes | None:
    sock.settimeout(timeout)
    try:
        data, _ = sock.recvfrom(65535)
        return data
    except TimeoutError:
        return None


def _recv_final_response(sock: socket.socket) -> bytes:
    """Read SIP responses until a final (non-1xx) one arrives."""
    while True:
        data = _recv_with_timeout(sock, _TIMEOUT)
        if data is None:
            pytest.fail("timed out waiting for final SIP response")
        start_line, _ = parse_sip_message(data)
        fields = start_line.split(" ", 2)
        if len(fields) >= 2 and not fields[1].startswith("1"):
            return data


def _status_code(message: bytes) -> str:
    start_line, _ = parse_sip_message(message)
    return start_line.split(" ", 2)[1]


def _request_uri_user(request: bytes) -> str:
    """Return the user part of a SIP request's Request-URI."""
    start_line, _ = parse_sip_message(request)
    uri = start_line.split(" ", 2)[1]
    body = uri.split(":", 1)[1] if ":" in uri else uri
    user = body.split("@", 1)[0]
    user = user.split(";", 1)[0]
    return user


def _make_ok_response(request: bytes) -> bytes:
    _, headers = parse_sip_message(request)
    vias = header_values(headers, "via")
    from_value = required_header(headers, "from")
    to_value = required_header(headers, "to")
    call_id = required_header(headers, "call-id")
    cseq = required_header(headers, "cseq")
    if not re.search(r"(?:^|;)\s*tag\s*=", to_value, flags=re.IGNORECASE):
        to_value = f"{to_value};tag=priority-peer"
    sdp = (
        "v=0\r\n"
        "o=- 0 0 IN IP4 127.0.0.1\r\n"
        "s=-\r\n"
        "c=IN IP4 127.0.0.1\r\n"
        "t=0 0\r\n"
        "m=audio 9 RTP/AVP 0\r\n"
        "a=rtpmap:0 PCMU/8000\r\n"
    )
    lines = ["SIP/2.0 200 OK"]
    lines.extend(f"Via: {via}" for via in vias)
    lines.extend(
        (
            f"From: {from_value}",
            f"To: {to_value}",
            f"Call-ID: {call_id}",
            f"CSeq: {cseq}",
            "Content-Type: application/sdp",
            f"Content-Length: {len(sdp)}",
            "",
            sdp,
        )
    )
    return "\r\n".join(lines).encode("latin-1")


def _start_listener(rules: RuleSet) -> ResipRuntimeListener:
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
    return ResipRuntimeListener(gate, rules)


def test_block_outranks_translate_on_runtime_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """REQ-F-7: BLOCK beats TRANSLATE even when both prefixes match.

    +861681000000 matches b-168 (BLOCK) and t-16 (TRANSLATE). The block rule
    must win: the AS answers 603 and never sends a downstream INVITE.
    """
    _require_extension()
    monkeypatch.setenv("AS_SIP_ROUTE_HOOK", "as_translation.outbound")
    monkeypatch.setenv("AS_TRANSLATION_RULES_JSON", _PRIORITY_TRANSLATION_RULES)

    upstream = bind_udp("upstream")
    downstream = bind_udp("downstream")
    rules = _build_rules(downstream.getsockname()[1])
    listener = _start_listener(rules)
    call_id = f"block-priority-{uuid.uuid4()}@{_HOST}"
    try:
        listener.start()
        invite = _invite("+861681000000", listener.port, upstream.getsockname()[1], call_id)
        upstream.sendto(invite, (_HOST, listener.port))

        response = _recv_final_response(upstream)
        assert _status_code(response) == "603"

        # No B2BUA dialog is created: nothing reaches the peer.
        assert _recv_with_timeout(downstream, _NO_DOWNSTREAM_TIMEOUT) is None
    finally:
        listener.stop()
        upstream.close()
        downstream.close()


def test_longest_translate_prefix_wins_on_runtime_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """REQ-F-6: within TRANSLATE the longest prefix wins and its rule translates.

    +867551234567 matches t-short (+86755) and t-long (+8675512). t-long must
    win, so the outbound user is ``934567`` (t-long strips +8675512, adds 9),
    not ``07551234567`` (t-short would produce). The downstream INVITE's
    Request-URI user proves both the longest-prefix selection and that the
    winning rule's translation was applied.
    """
    _require_extension()

    upstream = bind_udp("upstream")
    downstream = bind_udp("downstream")
    downstream_port = downstream.getsockname()[1]

    monkeypatch.setenv("AS_SIP_ROUTE_HOOK", "as_translation.outbound")
    monkeypatch.setenv("AS_SIP_NEXT_HOP", _HOST)
    monkeypatch.setenv("AS_SIP_NEXT_HOP_PORT", str(downstream_port))
    monkeypatch.setenv("AS_TRANSLATION_RULES_JSON", _PRIORITY_TRANSLATION_RULES)

    rules = _build_rules(downstream_port)
    listener = _start_listener(rules)
    call_id = f"longest-prefix-{uuid.uuid4()}@{_HOST}"
    try:
        listener.start()
        invite = _invite("+867551234567", listener.port, upstream.getsockname()[1], call_id)
        upstream.sendto(invite, (_HOST, listener.port))

        downstream.settimeout(_TIMEOUT)
        downstream_request, downstream_src = downstream.recvfrom(65535)
        start_line, _ = parse_sip_message(downstream_request)
        assert start_line.startswith("INVITE ")
        # t-long wins: strip +8675512, add 9 -> "934567".
        # t-short would produce "07551234567", so this also proves
        # longest-prefix-first rather than first-match.
        assert _request_uri_user(downstream_request) == "934567"

        # Answer the downstream leg so the B2BUA does not leave a dangling
        # transaction; the REQ-F-6 assertion above is the proof we need.
        downstream.sendto(_make_ok_response(downstream_request), downstream_src)
    finally:
        listener.stop()
        upstream.close()
        downstream.close()


def test_no_match_returns_404_on_runtime_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """REQ-F-6: a number outside every prefix yields 404 and no downstream INVITE."""
    _require_extension()
    monkeypatch.setenv("AS_SIP_ROUTE_HOOK", "as_translation.outbound")
    monkeypatch.setenv("AS_TRANSLATION_RULES_JSON", _PRIORITY_TRANSLATION_RULES)

    upstream = bind_udp("upstream")
    downstream = bind_udp("downstream")
    rules = _build_rules(downstream.getsockname()[1])
    listener = _start_listener(rules)
    call_id = f"no-match-{uuid.uuid4()}@{_HOST}"
    try:
        listener.start()
        invite = _invite("+999999999999", listener.port, upstream.getsockname()[1], call_id)
        upstream.sendto(invite, (_HOST, listener.port))

        response = _recv_final_response(upstream)
        assert _status_code(response) == "404"

        assert _recv_with_timeout(downstream, _NO_DOWNSTREAM_TIMEOUT) is None
    finally:
        listener.stop()
        upstream.close()
        downstream.close()
