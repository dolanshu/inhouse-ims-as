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

# ADR-0010: Autoscaling — custom-metric HPA + downscale guard controller

- **Status**: accepted
- **Date**: 2026-09-28
- **Decides**: §0 ledger entry 15 — autoscaling: custom-metric HPA + downscale guard controller
- **Responds to REQ**: REQ-NF-1, REQ-NF-3, REQ-NF-4

---

## Context

ADR-0002 established "one process per use case + session state externalized to Redis", making processes stateless — this is the precondition for horizontal autoscaling to be possible: scaling out requires no state migration, and any replica can take any new call.

But "stateless" does not equal "can scale down at any moment". No state in the process does not mean no in-flight calls on the process: as long as an instance still carries calls, removing it drops those calls. REQ-NF-3 writes this as the other half of the requirement — "capacity can be reduced **safely** when traffic decreases"; REQ-NF-1 (process restart does not lose sessions) and REQ-NF-4 (ISSU does not drop calls) require the same kind of protection: as long as there are in-flight calls, this instance must not be touched.

HPA itself cannot answer this question. It looks at **aggregate** metrics (average `active_calls` per Pod), while dropped calls are a **single-instance** matter: when the average is low, a distribution of "some instances still have calls" can entirely exist. Driving downscaling directly with aggregate metrics is equivalent to handing the per-instance question "is any instance carrying calls at this moment" to a controller that only looks at the average to guess. Architecture doc §6.3 has already written this judgment down hard — the downscale guard controller is a necessity, not an optimization.

On the other hand, O1 (capacity target) has not yet been measured, and open items have their own independent research milestone M6 (`AGENT.md` §2, the last item of the §2 non-goals: no capacity figures are published before M6 measures them). This means **no autoscaling threshold is fit for publication**: target utilization, target `active_calls`, and replica min/max are all capacity conclusions, and writing them out before M6 is fabricating figures. This ADR therefore gives no threshold at all, only the **shape of the criterion** and **where it lands**.

At the same time, ADR-0009 established that ISSU's semantics is draining — traffic removal first, waiting for existing calls to reach zero, then deletion. Downscaling is a planned disappearance of an instance, facing the same constraint as ISSU, so it must follow the same path: the instance selected by the controller can only be drained, not force-killed.

## Decision

- **Scale-out follows HPA (custom metrics `active_calls` / `cps`); thresholds and replica min/max are not given in this ADR.** They are capacity conclusions, to be filled into `deploy/helm/values.yaml` after M6 measures them. The file's `autoscaling` section is already guarded with `required`: if thresholds are not filled, installation fails, rather than running with a guessed default. The `minReplicas` that underpins capacity planning is likewise.
- **The downscale guard controller is an independent decision layer.** HPA decides "whether to scale down", the controller decides "which ones can be scaled down": when HPA judges that downscaling is needed, check each instance's `active_calls` one by one, and only allow removing instances with "in-flight calls ≤ the guard threshold". If enough are available, let them pass; if not, **block** and give the already-available partial set of instances (operations can remove this part first, rather than waiting idly).
- **The controller only produces verdicts; it does not call K8s APIs directly.** It is a set of pure functions: input each instance's load and the desired replica count, output the list of removable instances and reasons. Execution is done by the operations layer (Helm / standard controllers). Separating verdict from execution allows the verdict to be tested in a cluster-less environment.
- **The removal action must use draining (ADR-0009).** Traffic removal first → wait for in-flight calls to reach zero → then delete. Instances already draining are not repeatedly selected as candidates, avoiding dispatching the same removal twice.
- **The guard threshold is a safety criterion, not a capacity figure.** Default 0 — non-zero means protected (protect an instance that still has even one call). The value can be adjusted in values, but the justification must be written as "accepting the risk of dropping calls", not "measured capacity allows". Any change that writes the threshold as a capacity conclusion is a violation of this ADR.
- **Coordinated as a belt-and-suspenders with affinity (ADR-0002).** The precondition for an instance to be removable is that its session state is in Redis, not in this process's memory; and precisely for this reason, an instance with zero in-flight calls can be removed cleanly, without migrating any state.

## Consequences

### Positive

- **Downscaling no longer drops calls.** The condition for dropping calls changes from "aggregate metric is low" to "there are indeed no in-flight calls on that instance", and the per-instance criterion directly targets the harm to be prevented.
- **Scale-out policy and downscale safety are decoupled.** HPA only handles "whether to scale down" (capacity-perspective elasticity), the controller only handles "whether it can scale down" (safety-perspective gating); adjusting thresholds after M6 will not disturb the safety criterion, and vice versa.
- **The verdict is testable.** The controller is a pure function, not reading the clock, not opening sockets, not touching K8s, and downscale guard behavior can be covered in cluster-less gates (`platform/tests/test_downscale_guard.py`).
- **Progress is possible even without figures.** Thresholds are operations parameters rather than design premises, and the `required` guard ensures that before M6 it is only "not filled", not "guessed wrong and nobody noticed".

### Negative / accepted

- **Downscaling may be blocked for a long time.** As long as some instances always have calls, downscaling never meets the condition — especially obvious in scenarios with a high proportion of long calls. A timeout and forced policy are needed as a fallback; the timeout value is an operations parameter, not decided here (same as thresholds, goes into `values.yaml`).
- **The controller needs per-instance `active_calls` metrics.** This is finer-grained than the aggregate metrics HPA uses; the metrics side must be able to distinguish by Pod (the `MetricsRegistry` extension has been proposed in architecture §6.3). Aggregate metrics are insufficient to support this criterion; this is the cost of decoupling.
- **No autoscaling threshold can be given before M6.** Operations cannot complete the elasticity configuration before obtaining the O1 conclusion, and `autoscaling.enabled` is off by default. Accepted: fabricating a figure is worse than having none.
- **The controller only gives verdicts; execution remains in the operations layer.** The wiring between criterion and execution (who hands candidates to whom, how to mark draining) is not within this ADR's scope; it belongs to M5 operations wiring work.

## Alternatives considered

| Option | Why not |
|---|---|
| Let HPA downscale directly (native CPU / memory HPA or custom metrics) | Aggregate metrics mask that some instances still have calls: a low average does not mean no instance is carrying calls, so downscaling inevitably drops calls; CPU / memory correlates poorly with real SIP load (architecture §6.3) |
| Forbid downscaling (scale out only) | Loses elasticity. Under tidal traffic, resident peak replica counts mean costs borne by the operator; REQ-NF-3 requires "can scale down safely", not "no downscaling" |
| Judge by connection count (SIP signaling connection count) | SIP signaling connections and in-flight calls are not the same thing: a connection can be long-lived and idle, and in-flight calls can exist outside connections. The criterion must directly target `active_calls` |
| In-process suicide exit (exit upon receiving a downscale signal) | Violates the draining semantics (ADR-0009): exiting before existing calls reach zero equals actively dropping calls |
| Build the guard into HPA (exclude Pods with calls in the custom metric) | HPA's aggregate semantics has no expressive power for "per-Pod exclusion", and it would mix the safety criterion into the capacity strategy, making it easy to break the safety line when adjusting thresholds in M6 |

## Evidence

- [ADR-0002](0002-per-usecase-process-state-redis.md): stateless processes + Redis session tables allow any instance to be removed when it has zero in-flight calls; affinity is the belt-and-suspenders.
- The `autoscaling` section of `deploy/helm/values.yaml` has landed, with thresholds and replica min/max all `null` and guarded by `hpa.yaml`'s `required`: unfilled values cause installation to fail, and guessing is not allowed.
- Implementation evidence: `platform/src/as_platform/ops/downscale_guard.py` (pure-function verdicts, landed in this same change) and `platform/tests/test_downscale_guard.py` (10 unit cases: pass on zero calls, partial block gives partial candidates, draining not repeatedly selected, reproducible ordering, illegal thresholds not widened, purity).
- Architecture doc §6.3 "Dynamic autoscaling": the downscale guard controller is characterized as a necessity, with the criterion being `active_calls`.

## Related

- [ADR-0002](0002-per-usecase-process-state-redis.md) Runtime model: stateless + state externalization + affinity belt-and-suspenders
- [ADR-0007](0007-data-plane-split.md) Runtime state in Redis: the state precondition for an instance to be removable
- [ADR-0009](0009-issu-draining.md) ISSU is draining, not in-flight state migration — this ADR's removal action depends on its semantics
- [`../system-architecture.md`](../system-architecture.md) §6.3 Dynamic autoscaling
- [`../../../deploy/helm/README.md`](../../../deploy/helm/README.md) Where thresholds and replica min/max land
- Open item O1 (capacity target, M6): before that, this ADR publishes no threshold
