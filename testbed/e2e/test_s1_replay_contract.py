"""Wave 2: S1-basic-call replay comparison on the Wave 1 topology.

Scope: ``docs/acceptance/2026-10-09-e2e-test-plan.md`` Wave 2, tracked by
[``../acceptance/2026-10-11-wave2-replay-register.md``](../acceptance/2026-10-11-wave2-replay-register.md)
— the in-repo carrier that stands in for the "separate issue" the A4-3 adjudication
refers to.

What this file asserts, and only that:

1. **Normalised sequence** of the inbound leg and of the outbound leg of a T1 call,
   compared against the ``S1-basic-call`` baseline (``testbed/contracts/sip-baseline/``).
   "Normalised" has one precise meaning here, taken from the e2e plan's
   "method + **final** response code sequence": **1xx provisional responses are dropped**.
   The baseline's non-provisional skeleton is, per leg, ``INVITE → 200 → ACK → BYE → 200``.
2. **C_in ≠ C_out** (REQ-F-2 subset): the Call-ID of an inbound INVITE differs from the
   Call-ID of any outbound INVITE — the B2BUA starts a new dialog on the second leg.
3. **SDP offer byte-identity** (REQ-F-4): the body put on the outbound INVITE is
   byte-identical to the body of the inbound INVITE.

How the messages are collected, and why that is legitimate:

* the observation points are the two ``TransparentBridge`` hops that sit **either side of
  the AS** — ``north`` (trunk side / inbound leg) and ``south`` (core side / outbound leg);
* a hop's ``_on_message`` sees what arrives at that hop from **upstream**, i.e. the leg's
  **requests**; its ``_forward_response`` sees what comes back from the **next hop**
  toward the AS, i.e. the leg's **responses**;
* both are wrapped with ``monkeypatch`` **inside this test module only**. No product and
  no simulator source is modified. Two consequences worth stating plainly: the wrapped
  names are private API, so a rename in ``as_simulators`` breaks this file; and the patch
  is installed **before** the bridges are constructed, because ``SipServer`` binds
  ``self._on_message`` during ``TransparentBridge.__init__``.

The number of calls inside the load window is timing-dependent, so nothing here assumes
a single call: messages are grouped per Call-ID and **every** complete call is asserted,
provided at least one completed.

Native extension policy: same as Wave 1 and per A4-2 — a missing ``_resip_runtime``
**fails**, it does not skip.

Deliberately **not** covered here (still open, tracked in the register):

* header-by-header comparison of all 14 baseline messages — this file compares the
  normalised skeleton, which is what Wave 2's definition asks for;
* the console, kind, and any capacity number.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar

import pytest

from as_load.harness import LoadConfig, run_load
from as_platform.sip.ingress import TransportIngressGate
from as_platform.sip.message import header, is_request, parse_message, status_code
from as_platform.sip.resip_runtime import ResipRuntimeListener, load_resip_runtime_extension
from as_platform.sip.transport import PeerPolicy, TlsConfig, TransportSeam
from as_simulators.bridge import TransparentBridge
from as_simulators.demo_rules import demo_rules
from as_simulators.uas import PeerUas
from as_simulators.wire import method_of

pytestmark = pytest.mark.e2e

_T = TypeVar("_T")

_HOST = "127.0.0.1"

# The normalised skeleton of the S1-basic-call baseline: after dropping the 1xx
# provisional responses (02/04/05 in the baseline's numbering), each leg is
# INVITE -> 200 -> ACK -> BYE -> 200. Requests and responses are asserted as two
# separate lists: they travel on different code paths inside the bridge, so their
# interleaving is timing-dependent and must not be frozen into an assertion.
_BASELINE_LEG_REQUESTS = ("INVITE", "ACK", "BYE")
_BASELINE_LEG_FINAL_RESPONSES = (200, 200)

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


@dataclass(frozen=True)
class _Observation:
    """One message seen at an observed hop."""

    hop: str
    kind: str  # "request" | "response"
    call_id: str | None
    cseq: str | None  # the CSeq header (e.g. "2 BYE"): identifies the SIP transaction
    method: str | None
    status: int | None
    payload: bytes | None


def _dedupe(pairs: list[tuple[str | None, _T]]) -> tuple[_T, ...]:
    """Fold retransmissions: drop later entries repeating an earlier CSeq, keep the order."""
    seen: set[str | None] = set()
    result: list[_T] = []
    for cseq, value in pairs:
        if cseq in seen:
            continue
        seen.add(cseq)
        result.append(value)
    return tuple(result)


def _body_of(payload: bytes) -> bytes:
    """Return the SDP body of a SIP message: everything after the first blank line."""
    separator = b"\r\n\r\n"
    index = payload.find(separator)
    if index < 0:
        return b""
    return payload[index + len(separator) :]


class _LegRecorder:
    """Collects the messages the two hops either side of the AS observe.

    ``north`` is the trunk-side hop (inbound leg of the AS); ``south`` is the core-side
    hop (outbound leg). A hop's ``_on_message`` carries the leg's requests, its
    ``_forward_response`` carries the leg's responses.
    """

    def __init__(self) -> None:
        self.observations: list[_Observation] = []
        self._hops: dict[int, str] = {}

    def watch(self, hop: str, bridge: TransparentBridge) -> None:
        """Register ``bridge`` as the observation point named ``hop``."""
        self._hops[id(bridge)] = hop

    def install(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Wrap the two bridge entry points. Must run before the bridges are built."""
        recorder = self
        original_on_message = TransparentBridge._on_message
        original_forward_response = TransparentBridge._forward_response

        def on_message(
            bridge: TransparentBridge,
            server: object,
            payload: bytes,
            peer: tuple[str, int],
            connection: object,
        ) -> None:
            if id(bridge) in recorder._hops:
                recorder._record_payload(bridge, "request", payload)
            original_on_message(bridge, server, payload, peer, connection)

        def forward_response(bridge: TransparentBridge, server: object, message: object) -> None:
            if id(bridge) in recorder._hops:
                recorder._record_message(bridge, "response", message)
            original_forward_response(bridge, server, message)

        monkeypatch.setattr(TransparentBridge, "_on_message", on_message)
        monkeypatch.setattr(TransparentBridge, "_forward_response", forward_response)

    def _record_payload(self, bridge: TransparentBridge, kind: str, payload: bytes) -> None:
        hop = self._hops[id(bridge)]
        try:
            message = parse_message(payload)
        except ValueError:
            self.observations.append(_Observation(hop, kind, None, None, None, None, payload))
            return
        self.observations.append(
            _Observation(
                hop=hop,
                kind=kind,
                call_id=header(message, "Call-ID"),
                cseq=header(message, "CSeq"),
                method=method_of(message) if is_request(message) else None,
                status=None if is_request(message) else status_code(message),
                payload=payload,
            )
        )

    def _record_message(self, bridge: TransparentBridge, kind: str, message: object) -> None:
        hop = self._hops[id(bridge)]
        self.observations.append(
            _Observation(
                hop=hop,
                kind=kind,
                call_id=header(message, "Call-ID"),  # type: ignore[arg-type]
                cseq=header(message, "CSeq"),  # type: ignore[arg-type]
                method=None,
                status=status_code(message),  # type: ignore[arg-type]
                payload=None,
            )
        )

    def _per_call(self, hop: str) -> dict[str, list[_Observation]]:
        grouped: dict[str, list[_Observation]] = {}
        for item in self.observations:
            if item.hop != hop or item.call_id is None:
                continue
            grouped.setdefault(item.call_id, []).append(item)
        return grouped

    def request_sequences(self, hop: str) -> list[tuple[str, ...]]:
        """Per-call request-method sequences observed at ``hop``, retransmissions folded.

        A request that reaches the hop twice under the same CSeq is a retransmission of
        one transaction, not two messages, so it is counted once.
        """
        return [
            _dedupe([(item.cseq, item.method) for item in items if item.method is not None])
            for items in self._per_call(hop).values()
        ]

    def final_response_sequences(self, hop: str) -> list[tuple[int, ...]]:
        """Per-call final (>= 200) response-code sequences observed at ``hop``, 1xx dropped.

        Same folding as :meth:`request_sequences`: a final response retransmitted until
        its ACK arrives is one transaction.
        """
        return [
            _dedupe(
                [
                    (item.cseq, item.status)
                    for item in items
                    if item.status is not None and item.status >= 200
                ]
            )
            for items in self._per_call(hop).values()
        ]

    def invite_call_ids(self, hop: str) -> tuple[str, ...]:
        """Distinct Call-IDs of the INVITEs observed at ``hop``."""
        return tuple(
            {
                item.call_id
                for item in self.observations
                if item.hop == hop and item.method == "INVITE" and item.call_id is not None
            }
        )

    def invite_bodies(self, hop: str) -> tuple[bytes, ...]:
        """Bodies of the INVITEs observed at ``hop``."""
        return tuple(
            _body_of(item.payload)
            for item in self.observations
            if item.hop == hop and item.method == "INVITE" and item.payload is not None
        )

    def leg_call_id_map(self, hop: str) -> list[dict[str, object]]:
        """Per-call Call-ID stability evidence at ``hop``.

        For each Call-ID group observed at ``hop``, return the Call-ID seen on
        the INVITE, the ACK, the BYE, and on every 200 OK response.  A complete
        leg has all four populated; an incomplete one leaves the missing slots
        as ``None`` so the caller can tell them apart from a present-but-empty
        value.
        """
        result: list[dict[str, object]] = []
        for items in self._per_call(hop).values():
            invite_cid = next((item.call_id for item in items if item.method == "INVITE"), None)
            ack_cid = next((item.call_id for item in items if item.method == "ACK"), None)
            bye_cid = next((item.call_id for item in items if item.method == "BYE"), None)
            response_cids = [item.call_id for item in items if item.status == 200]
            result.append(
                {
                    "invite": invite_cid,
                    "ack": ack_cid,
                    "bye": bye_cid,
                    "responses": response_cids,
                }
            )
        return result


def _require_product_stack() -> object:
    """Return the native runtime, or fail: e2e without the product stack is not e2e."""
    extension = load_resip_runtime_extension()
    if extension is None:
        pytest.fail(
            "platform _resip_runtime extension not built; run make m2-platform-resip-build. "
            "e2e never skips for a missing native extension (A4-2)."
        )
    return extension


def _drive_recorded_first_edition(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    recorder: _LegRecorder,
) -> None:
    """Run T1 calls through S-CSCF → S-SBC → AS → peer UAS, recording both legs.

    The topology is the Wave 1 one (``test_sip_first_edition.py``); it is repeated here
    rather than imported so the two waves stay independently reviewable and so this file
    can install its own observation hooks around the hops it cares about.
    """
    _require_product_stack()
    transport = "udp"

    # The patch has to be live before TransparentBridge.__init__ binds _on_message.
    recorder.install(monkeypatch)

    rules, _translations = demo_rules()
    uas = PeerUas(_HOST, transport, tls_certificate=None, tls_private_key=None)
    south = TransparentBridge(
        advertised_host=_HOST,
        next_hop=(_HOST, uas.port),
        transport=transport,
        tls_certificate=None,
        tls_private_key=None,
        tls_ca_file=None,
    )
    monkeypatch.setenv("AS_SIP_ROUTE_HOOK", "as_translation.outbound")
    monkeypatch.setenv("AS_SIP_NEXT_HOP", _HOST)
    monkeypatch.setenv("AS_SIP_NEXT_HOP_PORT", str(south.port))
    monkeypatch.setenv("AS_SIP_NEXT_HOP_TLS_PORT", str(south.port))
    monkeypatch.setenv("AS_TRANSLATION_RULES_JSON", _TRANSLATION_RULES)

    tls = TlsConfig(
        certificate_path="",
        private_key_path="",
        ca_path=None,
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
        enable_udp=True,
        enable_tcp=False,
        tls_only=False,
        bind_address=_HOST,
        advertised_address=_HOST,
    )
    listener.start()
    product_port = listener.port
    assert product_port is not None
    north = TransparentBridge(
        advertised_host=_HOST,
        next_hop=(_HOST, product_port),
        transport=transport,
        tls_certificate=None,
        tls_private_key=None,
        tls_ca_file=None,
    )
    scscf = TransparentBridge(
        advertised_host=_HOST,
        next_hop=(_HOST, north.port),
        transport=transport,
        tls_certificate=None,
        tls_private_key=None,
        tls_ca_file=None,
    )

    recorder.watch("north", north)
    recorder.watch("south", south)

    hops = (uas, south, north, scscf)
    for hop in hops:
        hop.start()
    try:
        run_load(
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
                tls_ca_file=None,
                scenarios=("T1",),
            )
        )
    finally:
        for hop in reversed(hops):
            hop.stop()
        listener.stop()


def test_e2e_s1_replay_both_legs_match_the_normalised_baseline(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Both legs of every complete T1 call reduce to the baseline skeleton once 1xx is dropped."""
    recorder = _LegRecorder()
    _drive_recorded_first_edition(tmp_path, monkeypatch, recorder)

    for hop in ("north", "south"):
        requests = recorder.request_sequences(hop)
        responses = recorder.final_response_sequences(hop)
        assert requests, f"no Call-ID-grouped requests observed at the {hop} hop"
        for sequence in requests:
            assert sequence == _BASELINE_LEG_REQUESTS, (
                f"{hop} leg request sequence {sequence} != baseline {_BASELINE_LEG_REQUESTS}"
            )
        for sequence in responses:
            assert sequence == _BASELINE_LEG_FINAL_RESPONSES, (
                f"{hop} leg final response sequence {sequence} != "
                f"baseline {_BASELINE_LEG_FINAL_RESPONSES}"
            )


def test_e2e_s1_replay_second_leg_starts_a_new_call_id(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """REQ-F-2 subset: C_in ≠ C_out — the B2BUA never reuses an inbound Call-ID outbound."""
    recorder = _LegRecorder()
    _drive_recorded_first_edition(tmp_path, monkeypatch, recorder)

    inbound_ids = set(recorder.invite_call_ids("north"))
    outbound_ids = set(recorder.invite_call_ids("south"))
    assert inbound_ids, "no inbound INVITE Call-ID observed on the trunk-side hop"
    assert outbound_ids, "no outbound INVITE Call-ID observed on the core-side hop"
    reused = inbound_ids & outbound_ids
    assert not reused, f"the second leg reused inbound Call-ID(s): {sorted(reused)}"


def test_e2e_s1_replay_sdp_offer_is_byte_identical_across_legs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """REQ-F-4: the SDP offer the AS puts on the second leg is byte-identical."""
    recorder = _LegRecorder()
    _drive_recorded_first_edition(tmp_path, monkeypatch, recorder)

    inbound = recorder.invite_bodies("north")
    outbound = recorder.invite_bodies("south")
    assert inbound, "no inbound INVITE body observed on the trunk-side hop"
    assert outbound, "no outbound INVITE body observed on the core-side hop"
    assert all(body for body in inbound), "an inbound INVITE carried an empty body"
    assert set(outbound) == set(inbound), (
        "the outbound SDP offer(s) are not byte-identical to the inbound offer(s): "
        f"inbound={sorted(inbound)!r} outbound={sorted(outbound)!r}"
    )


def test_e2e_s1_replay_call_id_is_stable_within_each_leg(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """REQ-F-2 items 5-6: within each leg, every message keeps the INVITE's Call-ID.

    RFC 3261 §8.1.1.4 fixes the Call-ID for the whole dialog, so the ACK and
    BYE of a leg, and the 200 OK responses, must all carry the same Call-ID
    as that leg's INVITE.  Asserts this for every complete call on both the
    trunk-facing (north) and core-facing (south) legs.
    """
    recorder = _LegRecorder()
    _drive_recorded_first_edition(tmp_path, monkeypatch, recorder)

    for hop in ("north", "south"):
        calls = recorder.leg_call_id_map(hop)
        complete = [
            call
            for call in calls
            if call["invite"] is not None
            and call["ack"] is not None
            and call["bye"] is not None
            and call["responses"]
        ]
        assert complete, f"no complete call (INVITE+ACK+BYE+200 OK) observed at the {hop} hop"
        for call in complete:
            leg_cid = call["invite"]
            assert call["ack"] == leg_cid, (
                f"{hop} ACK changed Call-ID: INVITE had {leg_cid}, ACK had {call['ack']}"
            )
            assert call["bye"] == leg_cid, (
                f"{hop} BYE changed Call-ID: INVITE had {leg_cid}, BYE had {call['bye']}"
            )
            assert all(cid == leg_cid for cid in call["responses"]), (
                f"{hop} 200 OK changed Call-ID: INVITE had {leg_cid}, "
                f"responses had {call['responses']}"
            )
