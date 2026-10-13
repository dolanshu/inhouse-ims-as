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

# M7.1 product AS joint-debugging record (2026-10-07)

> **Engineering close-out (2026-10-07).** Measured against plan §9. Below is the single kind run used for the close-out.
>
> The path is page / call load → simulated S-CSCF → simulated northbound S-SBC → **product Helm AS** → simulated southbound S-SBC → callee.
> The test CA is not an operator PKI. REQ-S-2 / REQ-S-3 are not signed as pass because of this document. The page has no login, so REQ-S-4 is not signed.
> The counts and latencies below describe only this run; they are not a capacity commitment.
> No certificates, private keys, or pcaps are committed.

## Environment

| Item | Value |
|---|---|
| Cluster | kind `as-m71`, Calico v3.28.2, single node |
| `ims-sim` | Simulated S-CSCF, northbound/southbound S-SBC, callee, call load page. Image `ims-sim:dev` |
| `as-sut` | `deploy/helm` release `as-sut`, Deployment `as-sut-translation`. Image `as-sut:dev` (with `_resip_runtime` compiled locally). Redis `as-sut-redis` is running. Rules come from `AS_RULESET_JSON`, not pushed down by config-service |
| Installation | `bash testbed/sim-platform/kind-up.sh`; product values in `testbed/sim-platform/values-product-as.yaml` (not written into the production default values) |

F1 / F2 go through the product kernel's FORWARD / BLOCK (603), consistent with the first version's call types. Anti-fraud rate limiting is a separate process and would contend for the same SIP port; it was not started for this run.

## Calls

The page API is called from the `call-load` pod. For each transport about 3 seconds, 5 calls/second, three calls for each of the five types. T4 has no matching rule, 404. F2 is 603, not changed to 608. For established dialogs (T1 / T5 / F1) the BYE is 2xx in every case, with `unresolved` = 0. The product forwards the inbound-leg BYE to the outbound leg. 404 / 603 establish no dialog, so there is no BYE.

| Transport | Result | Teardown |
|---|---|---|
| UDP | 200×9, 404×3, 603×3 | BYE 2xx, unresolved 0 |
| TCP | 200×9, 404×3, 603×3 | BYE 2xx, unresolved 0 |
| TLS | 200×9, 404×3, 603×3. T1 outbound leg `sips:013800138000@ssbc-south…:5061` | BYE 2xx, unresolved 0 |

Before the fix: the BYE for UDP / TCP was 415, because the call load put `Content-Type: application/sdp` on the empty ACK / BYE, while the product only accepts that type on INVITE. The TLS BYE timed out because when all three transports were open at once the Contact still pointed at 5060, so the next hop tried to connect over TLS to a cleartext port. The counts are not a capacity commitment.

## Direct calls dropped by network policy

This is expected behaviour, not a defect. `call-load` sends an INVITE to the product Pod's UDP 5060 and gets no SIP response within 2 seconds (`TimeoutError`). The product does not return 403. An INVITE from the northbound S-SBC reaches the product and gets the responses above. The product's inbound policy only allows the northbound S-SBC; the call load's outbound policy only allows the S-CSCF.

## After close-out

1. **Re-evaluate the demo and hook the story to this platform.** The execution ticket is [`../handoff/2026-10-07-demo-on-m71-platform-plan.md`](../handoff/2026-10-07-demo-on-m71-platform-plan.md). At close-out the rules were still `AS_RULESET_JSON`. Step 2 afterwards moved signalling to the test page; step 3 (2026-10-08) changed the decision rules to a config-service compiled bundle, with the process reading `AS_CONFIG_BUNDLE_PATH`. The number-translation table is still `AS_TRANSLATION_RULES_JSON`. Production default values and the release Dockerfile are unchanged.
2. **Ship the image with the SIP listener included, before M8 is reopened.** `deploy/docker/Dockerfile` is still the M5 process shell and does not bind SIP. `as-sut:dev` is only for this kind experiment.
