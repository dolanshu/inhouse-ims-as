<!--
Inhouse-IMS-AS — Copyright 2026 Dolan Shu <dolan.d.shu@gmail.com>, Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-->

# ADR-0004: No media; keep one media seam and write down its trigger conditions

- **Status**: accepted
- **Date**: 2026-09-30
- **Decides**: §0 ledger entry 11 — media: do not touch media; keep the seam and trigger conditions
- **Responds to REQ**: REQ-NF-6, REQ-F-4

---

## Context

`AGENT.md` §2 lists "no media" directly as a non-goal, in exhaustive phrasing that
leaves no room for interpretation: **"No media. No RTP, no transcoding, no DTMF,
no MRF, no media anchoring. Keep one seam and write down its trigger conditions
(ADR-0004)."** The five negatives cover every capability of the media plane:
transport (RTP), processing (transcoding), interaction (DTMF), resources (MRF),
topology (anchoring). This is not "not implemented yet" but a boundary drawn —
every item in §2 is a decided outcome, not an omission.

This boundary is decided by two things, both stemming from the same fact: we are
deployed **outside** the operator network (`AGENT.md` §1, architecture document
§1.1).

**First, the triangular route.** Media flows naturally along the shortest path: the
caller-side network element's RTP flows directly to the callee-side network
element. Once we act as a media relay, the media must route out of the network to
our node and then back into the network — out once, in once. The cost is doubled:
in bandwidth, the same voice stream crosses the operator's network boundary twice,
directly doubling the inter-network link bandwidth cost; in latency, the extra two
hops (out, in) stack queuing and processing latency directly onto the end-to-end
voice latency budget. Voice tolerates latency far less than signaling does: a
call's SIP setup can tolerate hundreds of milliseconds, but extra media latency is
something the user hears directly. Worsening voice quality for a capability we do
not even need is negative-return.

**Second, compliance.** An out-of-network node processing user voice touches the
boundary of lawful interception and privacy compliance. Voice content
(communication content) has a clear statutory collection subject and procedure
within the network; letting an out-of-network third-party AS carry the voice stream
moves a compliance problem that should stay closed within the network out to
outside it, introducing a cross-subject, cross-jurisdiction exposure surface. This
point is the same kind of judgment as another non-goal in `AGENT.md` §2 — "no
lawful interception (LI). IRI belongs to in-network network elements; letting a
third-party AS get involved would introduce cross-jurisdiction exposure (ADR-0016)":
where the capability sits determines where the compliance responsibility sits, and
no encryption or audit measure can offset that.

But "no media" does not mean "no media need exists". The most typical case in
anti-fraud is **playing a prompt**: after judging a call to be fraud, play a
prompt tone to the caller. This need is real; it just isn't ours to carry — architecture
document §9.1 has already nailed it down: **it should be played by the in-network
MRF (Media Resource Function); we only give the decision.** The MRF is in-network,
so there is no triangular route and no out-of-network compliance problem; all we
do is tell the operator side via signaling (608 / routing indication), and the
in-network network element triggers the prompt playback. Our output is a decision,
not a sound wave.

Thus "no media" and "media needs may appear in future" must be expressed together:
we do not build the capability, but **the conditions that would trigger it must be
written down** — otherwise it will either be quietly implemented in future
(bypassing the ADR and requirements process) or re-argued from scratch (the
decision was not crystallized). This is the whole meaning of the seam — it is not a
piece of code waiting to be implemented, but a boundary statement with its switch
conditions written down.

## Decision

- **The kernel implements no media capability whatsoever.** No RTP transport or
  send/receive, no codec conversion (transcoding), no DTMF capture or generation,
  no media anchoring (not becoming an intermediate RTP node), no deployment or
  implementation of MRF. This is a capability-list exclusion, not a priority
  ordering — they are not on the to-do list.
- **SDP must pass through byte-for-byte (REQ-F-4).** The SDP offer carried by the
  upstream INVITE is passed verbatim to the downstream peer; the SDP answer carried
  by the downstream 200 OK is passed verbatim back to the upstream. We rewrite no
  field in the offer/answer: no add/remove codecs, no change to ports and
  addresses, no change to `o=` / `c=` lines. Transparency is the verifiable form of
  "no media" on the signaling side — once we start rewriting SDP, we are
  participating in media negotiation.
- **Keep one media seam: an interface definition + trigger conditions, with the
  production implementation being an empty shell.** Both parts of the seam are
  equally important; lose either half and it degrades into "left a hole anyone can
  slip through":
  - **Trigger conditions** (the only enablement condition): the appearance of a
    **playback / recording / transcoding / DTMF** need. Nothing outside these four
    categories (performance optimization, topology simplification, "just do it
    while we're at it") constitutes a trigger.
  - **How to enable**: when the trigger condition holds, one **must re-run the ADR
    and requirements process** — write a new ADR for the decision, add the
    requirement item to the PRD, and walk the full document chain of `AGENT.md` §3.
    Do not quietly enable it in the implementation, and do not treat "the seam is
    already there" as pre-existing authorization. The seam is a **reserved
    argumentation entry point, not a reserved permission**.
- **Playback / recording and other media actions are performed by the operator's
  in-network MRF; we only give the decision via signaling.** We do not orchestrate
  the MRF, do not proxy media, do not hold media resources. When playback is needed,
  the AS's output is the decision document and the signaling indication (e.g., 608 /
  routing), and the in-network network element decides how to find the MRF.

## Consequences

### Positive

- **Avoid the triangular route.** The media stream stays on the in-network shortest
  path, paying no double bandwidth or extra latency for our existence. This is not
  a performance optimization — it is "do not introduce a cost we cannot bear".
- **Avoid out-of-network voice compliance risk.** User voice does not pass through
  our nodes; the lawful-interception and privacy-compliance boundary stays closed
  within the network and is not reopened by our deployment position.
- **Keep the kernel simple and testable.** The media plane (RTP send/receive,
  jitter buffer, codec, DTMF, resource scheduling) is the largest and hardest part
  of a SIP AS to verify without a real network. Excluding it leaves the kernel with
  only signaling and decision; tests can be completed without real media equipment.
  This is also one of the premises that lets `AGENT.md` §5 write "the decision
  module is a pure function" as a hard rule.
- **SDP transparency is verifiable.** Byte-for-byte pass-through can be written as
  an assertion, not an unverifiable promise like "basically unchanged".

### Negative / accepted

- **We cannot satisfy playback / recording scenarios on our own.** The anti-fraud
  prompt tone is the most typical example: the decision is ours, the sound is not.
  Such scenarios must rely on the operator's in-network MRF, and we have only a
  signaling relationship with the MRF. This dependency must be written into the
  interface agreement with the operator — it is a **delivery boundary**, not a
  "feature we'll fill in later". If a customer's solution has no usable in-network
  MRF, then playback-type needs are unsatisfiable in that delivery; this conclusion
  should be stated at the solution stage, not discovered at the implementation
  stage.
- **A long-idle seam has the cost of "no one dares delete it".** An interface
  definition reserved only for the future produces only maintenance cost (readers
  must understand it, reviewers must judge whether it is misused) for the years it
  has no trigger condition, yet yields no benefit. Accepted: this cost is lower than
  the cost of "quietly implementing it in future" or "re-arguing it in future".
  Deleting the seam also requires walking the ADR process — since it is part of the
  decision, it cannot be silently removed.
- **The seam currently exists only as documentation.** As of now there is no
  media-related module in the kernel code; this ADR establishes semantics and
  trigger conditions, and does not fabricate an already-existing interface
  implementation.

## Alternatives considered

| Option | Why not |
|---|---|
| Build our own MRF / media relay (we anchor RTP) | Triangular route: media routes out then back, doubling bandwidth + adding latency, directly worsening voice quality; and an out-of-network node processing user voice touches the lawful-interception and privacy-compliance boundary (architecture document §9.1) |
| Borrow the operator's in-network MRF but orchestrate it ourselves (i.e., this decision) | Adopted. The MRF is in-network, with no triangular route and no out-of-network compliance problem; we only give the decision and signaling indication, and hold no media resources |
| Let the business party handle media itself | The business party uses us precisely to avoid touching SIP and media (the value of a third-party AS is to handle protocol and decision on the business party's behalf); pushing media back to the business party negates the product's reason to exist |
| Partially participate in media (only rewrite SDP, do not relay RTP) | Rewriting SDP means participating in media negotiation, directly conflicting with REQ-F-4's byte-for-byte pass-through; and the boundary of "partial participation" would keep eroding — once you start changing the `c=` line, the next step is anchoring |

## Evidence

- `AGENT.md` §2 non-goal original: "No media. No RTP, no transcoding, no DTMF, no
  MRF, no media anchoring. Keep one seam and write down its trigger conditions
  (ADR-0004)."
- Architecture document §9.1 "Media: don't touch, but leave an opening": the seam's
  trigger condition is written as "playback/recording/transcoding/DTMF need
  appears", with the rationale — "an out-of-network third-party AS doing media relay
  is a **triangular route** (media routes out then back, doubling bandwidth + adding
  latency), and an out-of-network node processing user voice touches lawful
  interception and privacy compliance; if anti-fraud needs a playback prompt, it
  should be **played by the in-network MRF**, and the AS only gives the decision."
  Architecture document §2 table also records "Media: no RTP, SDP passed through
  verbatim".
- PRD REQ-NF-6 (no media) original: "Do not implement RTP, do not do transcoding,
  do not process DTMF, do not do media anchoring, do not deploy MRF. Keep one
  extension-interface definition (enabled only when a playback/recording/transcoding/
  DTMF need appears), with the production implementation being an empty shell.
  Rationale: an out-of-network third-party AS doing media relay is a triangular
  route (media routes out then back, doubling bandwidth + adding latency), and an
  out-of-network node processing user voice touches lawful interception and privacy
  compliance."
- PRD REQ-F-4 (SDP fully transparent) original: "The SDP offer carried by the
  upstream INVITE … must be passed verbatim to the downstream peer; the SDP answer
  carried by the downstream 200 OK must be passed verbatim back to the upstream. We
  do not do media anchoring at the application-server layer … keep one
  extension-interface definition (enabled only when a playback/recording/transcoding/
  DTMF need appears), with the production implementation being an empty shell. If
  media anchoring is needed in future for playback/recording/transcoding, it is
  performed by the operator's in-network MRF, and we only tell the operator side via
  signaling to find the MRF."
- PRD §1 non-goal compressed version: "If media processing needs playback/recording/
  transcoding in future, after triggering it is performed by the operator's
  in-network MRF (Media Resource Function); we only give the decision."
- Baseline S1's SDP byte-for-byte pass-through assertions:
  `testbed/simulators/tests/test_derived_baseline.py`'s
  `test_req_f4_invite_body_crosses_unchanged` (INVITE's SDP offer unchanged
  byte-for-byte) and `test_req_f4_answer_body_crosses_unchanged` (200 OK's SDP
  answer unchanged byte-for-byte).
- Implementation evidence (the seam's interface definition, and SDP pass-through
  assertions on the real stack) lands together when the trigger condition holds;
  currently there is no media-related module under `platform/src`.

## Related

- [ADR-0016](0016-in-boundary-security.md) in-boundary security: no LI, no billing — shares with this ADR the origin of "compliance boundary of out-of-network deployment"
- [ADR-0003](0003-s-sbc-transparent-bridge.md) single ISC access semantics: the S-SBC is a transparent bridge; the in-network/out-of-network media difference is absorbed by it
- PRD REQ-F-4 (SDP fully transparent), REQ-NF-6 (no media)
- [`../system-architecture.md`](../system-architecture.md) §9.1 Media: don't touch, but leave an opening
