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

# Demo wired to the M7.1 platform — preparation (2026-10-07)

> **Status**: steps 4 and 5 have been run through (2026-10-08). Story C's cluster footage is the kind cluster `as-m71` (five simulated Deployments in `ims-sim`; `as-sut`'s translation, Redis, config-service; anti-fraud is not started), still L1. 7.2d stays on `kind-as-m5` and is skipped in this run. The Story D narration adds that Redis in `as-sut` is not REQ-NF-1 on the customer's K8s. The Story E narration adds that the few-second count on the test page does not enter the O1 report. The measurement script is unchanged. M8 is still on hold.
> **Upstream**: §11 of [`2026-10-07-m7.1-sim-platform-plan.md`](2026-10-07-m7.1-sim-platform-plan.md); evidence [`../acceptance/m71-sim-platform-evidence.md`](../acceptance/m71-sim-platform-evidence.md).
> **Not in this document**: reopening M8; modifying `deploy/docker/Dockerfile` (SIP listening is deferred until just before M8 reopens); signing REQ-S-2 / REQ-S-3 / REQ-S-4; writing the counts out as capacity commitments.

The customer demo is still the five stories of [`pre-m8-demo-review-plan.md`](pre-m8-demo-review-plan.md). What changes is which network the signaling runs on, and where Story A's rules come from.

---

## 1. The two networks now

| | Existing script | What this run wires it to |
|---|---|---|
| Signaling | loopback, contract tests, `AS_CONFIG_BUNDLE_PATH` narration | kind `as-m71`: call load → simulated S-CSCF → simulated northbound S-SBC → product Helm AS → simulated southbound S-SBC → callee |
| Cluster | Story C looks at `kind-as-m5` | The same run now looks at `ims-sim` and `as-sut` in `as-m71` |
| Rules | Story A uses the integration test against the local compose Postgres; the product process uses `AS_RULESET_JSON` | Story A goes through config-service on this cluster: proposal, approval, compilation; the translation process consumes the compiled result |
| Console | `https://localhost:8443` (compose) | Still the product console. The `ims-sim` test page is not the console: no login, no product Ingress attached |

The test page is only used to select the call type, set the load, and view the result of this one run. The page states plainly that it is not the operator PKI.

---

## 2. What the narration does not change

- The test CA is not the operator PKI. Does not sign REQ-S-2 / REQ-S-3.
- The test page has no login, does not sign REQ-S-4. Login on the product console is still only covered in the control plane in Story A.
- The counts and latencies on the result page are for this one run, not capacity commitments. Story E is still a research method.
- F2 on this product path is **603**, not stated as 608. 608 belongs only to the separate anti-fraud process; that process does not contend for 5060 with translation this time.
- Story C is still L1: it does not say M5 full chain is accepted, and does not say production alerting or downscaling is closed.
- Story D is not REQ-NF-1 on the customer's K8s. That kind of evidence is not collected before Close.
- Cleartext 5060 is still an optional transport. There is no demo of "reject cleartext when TLS is required".
- Call load going straight at the product SIP is dropped by the network policy; that is a limitation to show the audience, not a fault.

---

## 3. How the five stories are wired

### Story A — Provision a translation number range

The control plane and the signaling are split apart, and both must be present.

1. The console still covers the dual role, callee + prefix, change order, and approval. compose's `https://localhost:8443` can continue to serve as the console footage.
2. Already wired to `as-sut` (2026-10-08): `scripts/demo-review/publish-m71-bundle.sh` runs proposal → a second person approves → distribution report → activation against the cluster Postgres, and the four verdicts are compiled into the repository. The translation process reads `AS_CONFIG_BUNDLE_PATH` and no longer reads `AS_RULESET_JSON`. Removing `+86` and adding `0` is still `AS_TRANSLATION_RULES_JSON`. The process does not pull the bundle; the script mounts the activated JSON into the Pod. The production default `services.configService.enabled` is still false. Console HTTPS login is not in this cluster.
3. Signaling verification now goes through the test page; `test_e1_s2_*` and the two-leg integration test are no longer treated as the on-site demo. The audience sees: after the T1 number change, 200; for T4, 404. The outbound user is `013800138000`.

The config-service image, Secret, and runtime role are wired per the chart's existing conventions; simulation switches are not written into the production default values. Lab material still lives in `testbed/sim-platform/`.

### Story B — Block a fraudulent number range

On site it now goes through the test page, the same product path:

| Type | What the audience sees |
|---|---|
| T5 | 200 |
| T4 | 404 |
| F2 | 603, not 608 |
| T1 | 200, the callee number has been changed |

The 608 in the anti-fraud unit tests may stay in the second half of the script; the narration says that is another process and it is not started on this network. BYE must be able to end with a 2xx, and the outbound leg is also torn down. UDP, TCP, and TLS each run at least one short round; this is not turned into a capacity scenario.

### Story C — The platform can be operated

`chart-check`, the metrics/draining unit tests, and the shape of the alert YAML are retained. The cluster footage has moved to `as-m71` (2026-10-08):

- `ims-sim`: S-CSCF, northbound/southbound S-SBC, callee, call-load
- `as-sut`: `as-sut-translation`, Redis, config-service. The anti-fraud process is stopped, because it would contend with translation for 5060

The 7.2d Ingress login stays on the original M5 cluster evidence; it is not moved into `as-m71`, and the test page is not described as that login. F10's L1 boundary is retained.

### Story D — Calls are not dropped arbitrarily

The script is unchanged: Redis, the recovery build, and the engineering harness are the original ones. The narration now adds: Redis is running in `as-sut`, but this is not kill-Pod acceptance on a customer cluster.

### Story E — How much load we can carry

The O1 report and the "this is not an SLA" narration are retained. The measurement script does not add a test-page short run. The narration now states: the few-second count on `as-m71` does not enter the O1 report.

---

## 4. Order

| # | What is visible once this is done | What still does not change |
|---|---|---|
| 1 | This document is used as the run sheet. The header of `pre-m8-demo-review-plan.md` points here | the script |
| 2 | Run through (2026-10-08). Story B and Story A's signaling step go through the `as-m71` test page, T1/T4/T5/F1/F2, BYE 2xx | config-service |
| 3 | Run through (2026-10-08). The verdict rules come from the config-service compiled bundle, and the process reads `AS_CONFIG_BUNDLE_PATH`. The number-change table is still `AS_TRANSLATION_RULES_JSON` | production default values, the published Dockerfile, moving console login into `as-m71` |
| 4 | Run through (2026-10-08). Story C looks at the two namespaces in `as-m71`, and the L1 framing is still there. `as_active_calls` is read from the translation Pod | moving 7.2d to another cluster, M8 |
| 5 | Narration changed (2026-10-08). D: Redis in `as-sut` is not REQ-NF-1 on customer K8s. E: the test page counts do not enter O1 | the measurement script and the harness |

The narration must not describe the number-change table as a field in the bundle, and must not say the SIP process pulled the bundle itself. The console web page is still compose's `https://localhost:8443`.

---

## 5. What "preparation complete" looks like

- The step table for the five stories and `scripts/demo-review/README.md` describe the `as-m71` path, not loopback / `kind-as-m5` as the signaling site.
- Story A can produce the T1 number change from the approved bundle on this cluster.
- Story B's on-site response codes are 200 / 404 / 603.
- Story C still cannot be heard as an M5 full-chain sign-off.
- Evidence lands in `artifacts/demo-review/<date>/`; do not commit pcaps, private keys, or long-term test CA keys.
- Hands-on acceptance follows §4 of [`pre-m8-demo-review-plan.md`](pre-m8-demo-review-plan.md). Each step separates "what to do / what to look at / what to explain".
