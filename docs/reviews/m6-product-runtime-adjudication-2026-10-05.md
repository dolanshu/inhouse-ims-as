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

# M6 product ResipRuntimeListener adjudication (2026-10-05)

## Object

Engineering adjudication of the M6 **product-path** real-socket smoke (and optional micro-measure script). Cross-ref: [`m6-product-runtime-smoke-review-2026-10-05.md`](m6-product-runtime-smoke-review-2026-10-05.md), [`m2-engineering-closure-adjudication-2026-10-05.md`](m2-engineering-closure-adjudication-2026-10-05.md).

## Adjudication

| Item | Verdict |
|------|---------|
| Product `ResipRuntimeListener` + `accept_all_invites` harness mode | **Accept** (engineering / testbed only) |
| `m6-product-runtime-smoke.sh` + integration test | **Accept** (engineering slice) |
| `m6-product-runtime-micro-measure.sh` (3s, cps 2) | **Accept** (optional precursor; not O1) |
| **M6 milestone exit** | **Deny** — M2 exit still gates milestone credit |
| **O1 publication** | **Deny** — formal capacity numbers remain **open** |
| **D8** (testbed/容量 REQ trace) | **Open** |

## Milestone status

**M6 engineering in progress** against the product listener (post M2 stack-binding closure). **M6 is NOT milestone-complete.** Maintainer sign-off **pending**.

## Limits

Lab smoke/micro-measure only. RSS/CPS from harness runs are not product capacity claims (AGENT.md §2).
