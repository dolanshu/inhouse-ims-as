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

# ADR-0009: ISSU is draining, not in-flight state migration

- **Status**: accepted
- **Date**: 2026-09-30
- **Decides**: §0 ledger §6.2 — ISSU can only use draining: traffic removal → wait for in-flight calls to reach zero → exit, without migrating in-flight state
- **Responds to REQ**: REQ-NF-1, REQ-NF-4

---

## Context

ADR-0002 has already decided the runtime model: **one process per use case, with session state, dialog state, and caller_state all externalized to Redis, and the process itself holding no session-level state that needs persistence**. This decision has a direct corollary, and it is stronger than it looks — since the process holds no session state, an upgrade **does not need** to move in-flight calls' state from the old process to the new process. The entire class of state-movement problems (serialization format, version compatibility, consistency within the movement window) simply does not exist.

But the other half of the corollary must be stated equally clearly, and this half is often omitted: **"not migrating state" does not equal "the process can be killed immediately".** State being in Redis does not mean the calls are not on this process. The process is still carrying a number of in-flight calls right now — their transaction machines, timers, sockets, and dialog contexts all live in this process; only their **recoverable facts** are stored in Redis. Exiting immediately upon receiving `SIGTERM` would break these calls: not "state was lost", but "no one continues sending the next SIP message for this call". The damage of dropping calls is independent of whether state is externalized. ADR-0010 states it bluntly: "no state in the process does not mean no in-flight calls on the process".

ISSU therefore needs a **draining** semantics, not a **migration** semantics:

1. **Stop accepting new requests** (traffic removal) — new requests go to new-version processes;
2. **Existing calls continue to completion on the original process** — they do not need to be moved, only not to be interrupted;
3. **Exit after `active_calls` reaches zero** — there are no calls on the process, and exiting no longer harms anything.

Architecture doc §6.2 writes this conclusion's premise fact down hard: "SIP transaction/dialog state is **all in process memory**, with no serialization or migration interface — therefore 'seamlessly handing in-flight calls over to the new version' is **architecturally untenable**. ISSU can only use **draining**." Note that the two halves of this sentence hold separately: the first half (state is in-process and cannot be migrated) is a **fact about the current stack**, and it may change with the stack selection; the second half (therefore draining) is a **conclusion under the current fact**. This means this decision is not eternal — it carries an explicit re-review trigger condition (see Decision item 5 and ADR-0019 §7 K6).

## Decision

- **① All upgrades / restarts use draining.** Stop accepting new requests → existing calls continue to completion on the original process → exit after `active_calls` reaches zero. There is no path of "replacing in place with the new version and continuing to serve", nor a path of "exiting immediately upon receiving a termination signal". REQ-NF-4's requirement ("new requests are routed to new-version processes, existing calls continue to completion") is exactly the requirements-side expression of this semantics.
- **② The mechanism lands in two places, each covering one half.** Orchestration side: `preStop` hook + extended `terminationGracePeriodSeconds` (already landed in `deploy/helm/templates/deployment.yaml`) — `preStop` first leaves time for Endpoint removal to propagate, avoiding "no longer accepting new traffic but the LB is still sending it here"; `terminationGracePeriodSeconds` bounds the upper limit of this wait, after which K8s sends `SIGKILL` on timeout. Kernel side: draining expressed by `ProcessShell` — `request_terminate()` marks "no longer accepting new requests", `run_until_drained()` polls `active_calls` until it reaches zero or times out. The two are the upper and lower halves of the same semantics: orchestration gives the time window, the process gives the draining behavior.
- **③ Downscaling is subject to the same constraint.** Downscaling is a planned disappearance of an instance, facing the same constraint as ISSU — ADR-0010's downscale guard controller coordinates with it: HPA decides "whether to scale down", while the controller only selects instances with **zero in-flight calls** as candidates, and the removal action itself is still draining. Instances already draining are not repeatedly selected as candidates.
- **④ There must be a hard timeout.** Waiting forever means keeping a Pod alive forever (long calls, zombie calls, and a peer that never hangs up all cause this), so the release process gets permanently stuck. Force exit after the timeout. **The timeout value is an operations parameter; this ADR gives no capacity or time conclusions** — it goes into `values.yaml`, bound to the call duration distribution, not inferred by the architecture. Forced exit on timeout means dropping calls, so it **must be alerted**: this is not a degradation that can happen silently.
- **⑤ Re-review clause: if state becomes serializable, this decision can be overturned, but must not be changed silently.** If the future production stack supports "serialization and recovery of dialog/transaction state" (ADR-0019 §4 E5 probe verification passes), in-flight state migration goes from "architecturally untenable" to "an evaluable alternative", at which point ISSU can be re-evaluated as in-flight state migration. **Overturning this clause requires a new ADR** (per the ADR registry rules: overturning a decision means writing a new ADR and updating the architecture doc in the same change), and it must not be quietly changed to migration semantics in the implementation. ADR-0019 §7 K6 has registered this consequential effect and re-review trigger condition.

## Consequences

### Positive

- **Upgrades do not drop calls.** The condition for dropping calls changes from "the process is terminated" to "the process is terminated when it has no calls", and the per-process criterion directly targets the harm to be prevented. REQ-NF-1 (process restart does not lose sessions) and REQ-NF-4 (ISSU does not drop calls) are both satisfied under this semantics.
- **Consistent with the stateless model, and simple to implement.** Draining requires no serialization format, no version compatibility matrix, and no consistency guarantees within the state-movement window — these are exactly the complexities ADR-0002 eliminated. The kernel side only needs a loop of "refuse new requests + wait for the domain counter to reach zero".
- **The verdict is testable.** `ProcessShell` injects the clock and `active_calls`, and draining's three outcomes (normal zeroing, forced timeout, refusing new requests) can be covered in cluster-less gates.

### Negative / accepted

- **Long calls lengthen the release window.** The lower bound on a rolling upgrade's duration is the longest remaining duration of existing calls. In scenarios with a high proportion of long calls, the release window lengthens significantly. This is the same thing as architecture doc §6.2's "upgrade window ≈ longest existing-call duration" and risk R3 (ISSU window too long); the mitigations (call duration hard cap + forced release policy) are operations strategies, not decided in this ADR.
- **The hard timeout fallback means calls are dropped on timeout.** Timeout is not "graceful degradation"; it is "giving up waiting and accepting the loss". Timeout must therefore be alerted rather than only logged — silently dropping calls is worse than dropping calls itself, because it keeps capacity and experience problems invisible for a long time.
- **Capacity effectively decreases during draining.** Draining replicas no longer accept new traffic but still occupy replica slots; before all new-version replicas are ready, effective capacity is below the nominal replica count. **The specific figures are operations parameters; this ADR involves no capacity conclusions** (`AGENT.md` §2: no capacity figures are published before M6 measures them).
- **This decision carries an undecided re-review trigger condition.** The E5 (state externalization / serialization) probe has not yet been written, and ADR-0019 §7 has made it explicit that "E5 does not even have an executable determination yet". Until then, the question "can upgrades be elevated to in-flight state migration" cannot be answered, so this decision is "a conclusion under the current facts", not a final conclusion.

## Alternatives considered

| Option | Why not |
|---|---|
| In-flight state migration (handing in-flight calls to new-version processes) | The current stack does not support state serialization and migration — the premise fact of architecture doc §6.2; ADR-0019 §4 E5 is still "paper pass / awaiting probe verification", and §7 makes it explicit the E5 probe has not been written. ADR-0002 has already eliminated this complexity. If E5 verification passes in the future, overturn it with a new ADR per Decision ⑤, not adopted at this moment |
| Rolling restart force-kill (exit immediately upon SIGTERM) | Drops in-flight calls. State surviving in Redis only guarantees "state is not lost", not "calls are not broken" — no one continues sending the next SIP message for this call |
| Dual-version parallel, with LB switching traffic but not removing existing traffic | This is not another option, but another phrasing of this decision: traffic switching is responsible for "new requests go to the new version", while the existing part can still only be zeroed via draining, otherwise the old-version process can never exit |
| In-process suicide exit (exit upon receiving a downscale signal) | Already explicitly rejected by ADR-0010: exiting before existing calls reach zero equals actively dropping calls |

## Evidence

- ADR-0002 has already decided the runtime model as "one process per use case + state externalized to Redis", and wrote that "ISSU (In-Service Upgrade) only needs draining (traffic removal, waiting for existing calls to reach zero), without needing state migration" and "graceful shutdown draining requires a preStop hook + extended terminationGracePeriodSeconds".
- Architecture doc §6.2 In-Service Upgrade (ISSU): premise facts (all state in process memory, no serialization or migration interface → seamless handover untenable, only draining); orchestration approach (k8s RollingUpdate + `preStop` draining + extended `terminationGracePeriodSeconds` + PDB); the constraints table records "upgrade window ≈ longest existing-call duration, grace window configurable; a 'forced release on timeout' policy and a call duration hard cap need to be defined". Risk R3 (ISSU window too long) mitigation listed as "call duration hard cap + forced release policy".
- Kernel implementation: `ProcessShell` in `platform/src/as_platform/shell.py` — `ShellConfig.drain_timeout_seconds` (draining upper bound), `request_terminate()` (marks stopping acceptance of new requests), `accepts_new_requests()`, `run_until_drained()` (polls `active_calls` until zero or timeout; comment "Force the exit: waiting forever would keep a Pod alive with calls that will never finish. See ADR-0009.").
- Entry implementation: `platform/src/as_platform/__main__.py` — registers `SIGTERM` / `SIGINT` handlers calling `shell.request_terminate()` (comment "Refuse new work before draining existing calls. See ADR-0009."), returning exit code 0 when draining completes and non-zero on timeout.
- Orchestration implementation: `deploy/helm/templates/deployment.yaml` — `terminationGracePeriodSeconds: {{ $.Values.draining.terminationGracePeriodSeconds }}`, comment "ISSU is draining, not state migration (ADR-0009) …… This window bounds that wait before SIGKILL; it is a timeout, not a capacity figure."; `lifecycle.preStop.exec` executes `sleep {{ $.Values.draining.preStopSleepSeconds }}`, comment "Gives the Endpoint removal time to propagate before the process stops accepting new calls (ADR-0009). The draining wait itself is done by the process shell."
- Measured: `docs/acceptance/report.md` M5 container image section — "`docker stop` inside the container (SIGTERM) → stops accepting new requests → drains → **exit code 0**, ADR-0009's draining really works inside the image"; the Chart renders both `terminationGracePeriodSeconds: 300` and `preStop`. The same section records incomplete items: rolling upgrade and downscale verification on a real Kubernetes cluster (no cluster locally), listed as M5 remaining items.
- Re-review trigger condition: ADR-0019 §7 K6 — "may consequentially reopen ADR-0005 / 0009 / 0010 …… if state becomes serializable, ADR-0009 can be elevated from draining to state migration"; §7 accepted gaps item 3 records E5 as unverified.

## Related

- [ADR-0002](0002-per-usecase-process-state-redis.md) Runtime model: stateless processes make draining possible, without needing state migration
- [ADR-0010](0010-autoscaling-hpa-downscale-guard.md) Autoscaling: the downscale guard controller only selects instances with zero in-flight calls; the removal action follows this ADR's draining
- [ADR-0019](0019-sip-stack-selection.md) §4 E5 (state externalization) and §7 K6 (consequential re-review of ADR-0005/0009/0010) — this decision's re-review trigger condition
- [`../../../deploy/docker/README.md`](../../../deploy/docker/README.md) Container image: entry point and SIGTERM behavior
- [`../system-architecture.md`](../system-architecture.md) §6.2 In-Service Upgrade (ISSU)
