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

# M8 batch 5 "Performance and capacity (kind)" review record (2026-10-12)

## Current Status

All four engineering goals of batch 5 have landed: 3 PASS (NF-15 multi-replica measurement, O1 loopback 1280 internal re-measurement, HPA threshold filling) plus 1 FAILCLOSED (performance-tier gate terminal state, registered and pending maintainer adjudication). No REQ is signed off, the matrix NF-15 row stays open, and report.md counts are untouched. `make gate` is fully green (1150 passed, 227 deselected), the evidence discipline test is 127 passed, `make chart-check` is OK. No new capacity-type alerts were added; ne-datasheet capacity values and the 4.1 formal report remain blocked. The only item pending the maintainer = performance-tier gate terminal state (B5-04).

**2026-10-13 maintainer additional adjudication: batch 5 judged pass.** This is batch-level engineering acceptance (3 PASS engineering goals + 1 FAILCLOSED registered faithfully), **not a REQ-NF-15 sign-off**; the matrix NF-15 row stays open and report.md counts stay unchanged. The maintainer additionally instructed: measurement evidence must carry a plain-language explanation (already appended to the end of both measurement evidence files), and the next release enhancement direction must be registered — disable accept_all_invites, stand up a real downstream UAS, and run real socket load tests over the full B2BUA two-leg path (see B5-08/B5-09). B5-04 (performance-tier gate terminal state) is not covered by this pass and still awaits the M8 final review adjudication.

## 1. Review target

- Evidence-gathering scope: the four evidence items of `docs/handoff/2026-10-12-m8-batch5-prompt.md` (NF-15 kind multi-replica measurement, O1 loopback 1280 internal re-measurement, HPA threshold filling, performance-tier gate terminal state registration).
- All outputs: 4 evidence files (see §4), `deploy/helm/values-onprem.example.yaml` change (+37 lines in the autoscaling section), evidence index `docs/acceptance/artifacts/m5/README.md` (+4 lines).
- Execution basis: `docs/handoff/2026-10-12-m8-scope-revision-internal-release-plan.md` §2.5.
- Execution environment: dev-win03ib7niepf0, cluster kind-as-m5, namespace nf15-perf.

## 2. Review date and reviewer

- Review date: 2026-10-12.
- Reviewer: AI agent engineering self-review (AGENT.md §3.3); maintainer sign-off listed separately (see end of document).

## 3. Review conclusion

**Conditional pass.** All four engineering goals and their evidence triples are complete, and the gate is fully green (`make gate` exit 0, evidence discipline 127 passed, chart-check OK). Pass conditions:

1. B5-04 (performance-tier gate terminal state) awaits maintainer adjudication; the agent neither implemented the blocking tier nor accepted the risk on the maintainer's behalf;
2. Commit splitting is the maintainer's decision; this batch executed no git write operations.

## 4. Evidence triple list

| Item | Triple (conclusion, evidence, date) |
| --- | --- |
| NF-15 multi-replica measurement | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-nf15-multi-replica-measurement-2026-10-12.txt, 2026-10-12) |
| O1 loopback 1280 (internal) | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-o1-loopback-cps-1280-2026-10-12.txt, 2026-10-12) |
| HPA threshold filling | (verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-hpa-threshold-filled-2026-10-12.txt, 2026-10-12) |
| performance gate terminal state | (failed-registered-pending-adjudication, docs/acceptance/artifacts/m5/2026-10-12/FAILCLOSED-performance-gate-terminal-state-2026-10-12.txt, 2026-10-12) |

## 5. Key result re-check

- Site: new namespace nf15-perf added to the kind-as-m5 cluster; helm release `nf15` (anti-fraud 2 replicas, requests 200m/256Mi, bundled PG/Redis + config-service) + temporary `sut-direct` Deployment (2/4 replicas, podIP broadcast bypassing Service) + as-load-gen Pod; tier model accept-all / UDP / hold=0 / 15s per tier.
- NF-15 2 replicas, five tiers (20/80/320/640/1280 CPS) all zero failures: established=300/1200/4800/9600/19200, unresolved=0.
- per-pod CPU (with the 200m request as denominator): ~160 CPS/Pod about 50% of request, ~320 CPS/Pod about 105%, ~640 CPS/Pod about 214%; memory peak about 59% at the top tier.
- Establishment latency p95: from 8.3ms (80 CPS) to 29-36ms (1280 CPS).
- 4 replicas@1280: perfectly balanced via direct podIP connections (14400 UDP packets each), with linear-consistent resource usage.
- O1 loopback 1280: 19200/19200 established, unresolved=0, p95 12.79ms.
- HPA example: enabled / minReplicas 2 / maxReplicas 4 / CPU 70 / MEM 70; default values.yaml and hpa.yaml guards zero changes; example renders 2 HPAs and default renders 0 HPAs, both guards verified effective, chart-check OK.
- Architecture finding: ClusterIP UDP short flows get pinned to a single endpoint by conntrack (2400 calls used only about 10 distinct client source ports); SIP UDP multi-replica balancing cannot rely on ClusterIP random distribution.

## 6. Issue list (gaps)

- **B5-01 ClusterIP UDP endpoint pinning**: architecture finding; real deployment requires a per-replica independently reachable design; not raised as an item in this batch, recommended to be handled at the target environment design stage.
- **B5-02 measurement model limitations**: accept-all / hold=0 / single-node kind — not the business decision path, not S-SBC, not a saturation point; the maintainer has fixed the framing as symbolic numbers and architecture exploration; no external numbers are published.
- **B5-03 high latency at the 4-replica tier (p95 79-88ms)**: root cause is 512-thread contention on the single load-generator pod; SUT had zero failures; the clean latency curve is the 2-replica one.
- **B5-04 performance-tier gate terminal state**: either (a) add a blocking tier to `make gate`, or (b) written risk acceptance by the M8 final review — awaiting maintainer adjudication; the agent neither implemented it nor accepted on the maintainer's behalf.
- **B5-05 first tier 20 CPS p50≈52ms**: cold-start warm-up, already explained in the evidence, not a regression.
- **B5-06 onprem example enables HPA but gives no useCases[].resources numbers**: comments now mandatorily require balancing requests against a measurement in the target environment first; the example file stays symbolic, no new capacity numbers.
- **B5-07 raw data stored on the execution machine at /tmp/m8b5/, not committed**: follows the batch 3 convention; key configuration and all derived numbers have been written verbatim into the evidence files.

## 7. Boundaries and non-claims

- Does not claim M8 is fully green; does not constitute M8 exit sign-off.
- Does not sign off REQ-NF-15; the matrix NF-15 row stays open.
- No external capacity numbers; internal engineering target values must not be written into external materials.
- No new capacity-type alerts; ne-datasheet capacity values and the 4.1 formal report remain blocked.
- No git write operations were executed (no add/commit/tag/push/branch).

## Adjudication

| ID | Source | Issue summary | Verdict | Fix plan | Status | Verification method | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B5-01 | This batch's NF-15 measurement | ClusterIP UDP short-flow conntrack pins a single endpoint, so multi-replica balancing does not hold on that path | Accept (architecture finding registered, not raised as an item) | Evidence file records the mechanism and meaning; target environment design adopts per-replica independent reachability | Closed | Behaviour observation (per-pod UDP counts 57604 vs 4 + conntrack source port sampling) | Input for future release target environment design |
| B5-02 | This batch's NF-15/O1 measurement | Limitations of the accept-all/hold=0/single-node kind model | Accept (maintainer has fixed the symbolic framing) | Boundary section written in the evidence file; not cited in external materials | Closed | Documentation update | AGENT.md §2 |
| B5-03 | This batch's NF-15 measurement | 4-replica tier latency polluted by load generator thread contention | Partially accepted | Evidence file annotates the pollution source; latency conclusions use the 2-replica curve | Modified | Behaviour observation + documentation update | Can be re-run later with a separate load pod if needed |
| B5-04 | RC plan A-6 / scope §2.5 | Whether the performance tier enters the `make gate` blocking set | Pending adjudication | Either/or: implement the blocking tier, or written risk acceptance by the M8 final review | Pending modification | Maintainer confirmation | FAILCLOSED-performance-gate-terminal-state-2026-10-12.txt |
| B5-05 | This batch's NF-15 measurement | Cold-start latency anomaly on the first tier | Accept (measurement artefact) | Explained in the evidence file, no re-run | Closed | Documentation update | — |
| B5-06 | This batch's HPA measurement | Example HPA lacks accompanying numeric resources | Partially accepted | Comments mandate "measure and balance requests before enabling"; no new numbers added | Modified | helm template + chart-check + documentation update | Re-measure in the target environment before go-live |
| B5-07 | This batch's evidence discipline measurement | Raw data only in /tmp, not committed | Accept (follows the batch 3 convention) | Key configuration and derived numbers entered verbatim into evidence | Closed | Documentation update | /tmp/m8b5/ retained until the maintainer cleans it up |
| B5-08 | 2026-10-13 maintainer adjudication | Overall batch 5 verdict | Accept (batch 5 judged pass; not a REQ-NF-15 sign-off, matrix row stays open) | Plain-language explanation section appended to both measurement evidence files; B5-04 still listed separately pending the M8 final review | Closed | Maintainer confirmation (2026-10-13 verbal adjudication, recorded by the agent) | Batch-level engineering acceptance; no M8 exit sign-off claimed |
| B5-09 | 2026-10-13 maintainer adjudication | Capacity measurement to use a real two-leg path: disable accept_all_invites, real downstream UAS, real socket load test over B2BUA inbound + outbound legs | Accept (listed as a next-release enhancement, not raised as an item in this version) | This version only registers the direction in evidence/review/handoff; implementation goes through the next release's new-feature process | Closed | Maintainer confirmation (2026-10-13 verbal adjudication, recorded by the agent) | Covers the business decision and forwarding paths; corresponds to the accept-all model limitations (B5-02) |

**Sign-off:** the maintainer judged batch 5 pass on 2026-10-13 (B5-08/B5-09 adjudicated; B5-04 still awaits the M8 final review); the AI agent engineering self-review was completed on 2026-10-12, with the adjudication recorded on disk on 2026-10-13.

---

This review signs off no REQ, changes no matrix status or report.md counts, and does not constitute an external capacity commitment; no git write operations were executed.
