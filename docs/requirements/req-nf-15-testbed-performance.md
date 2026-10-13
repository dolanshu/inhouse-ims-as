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

# REQ-NF-15: three-layer testbed and real-socket capacity research

> **Status:** reviewed (2026-10-05, D8 closed)  
> **Carried ADR:** [ADR-0014](../architecture/adr/0014-three-layer-testbed.md)  
> **PRD index:** [prd.md](prd.md) §3 REQ-NF-15

## Business description

The product deliverable does not include testbed; testbed is an R&D asset, with direction testbed → platform, and runtime must not depend on testbed. The testbed has three layers, and the responsibilities of each layer must not be impersonated by another:

| Layer | Path | Question answered |
|---|---|---|
| Contracts | `testbed/contracts/` | Decision and cross-implementation consistency (ADR-0012) |
| Simulation | `testbed/simulators/`, `testbed/probe/` | Whether the AS can work against something that behaves like an operator peer |
| Performance | `testbed/load/` | Observe capacity boundaries and runtime profile on the **real-socket** path |

Capacity and O1 research **must** use real-socket load testing only (UDP/TCP/TLS through the network stack and event loop); driving callbacks to impersonate system capacity measurement is forbidden. GPL tools (such as SIPp) are for internal testing only and must not be distributed with the product.

This REQ does **not** prescribe external SLA, marketing CPS/concurrency commitments, or final HPA thresholds; those are handled separately by the O1 maintainer adjudication and the M8 acceptance chain (`AGENT.md` §2).

## Acceptance criteria

See [../acceptance/test-plan.md](../acceptance/test-plan.md) §2-REQ-NF-15.

## Evidence and reports

- Harness and scripts: `testbed/load/`, `testbed/load/scripts/m6-*.sh`
- M6 O1 internal measurement report (dev host, not SLA): [../acceptance/m6-o1-measurement-report-2026-10-05.md](../acceptance/m6-o1-measurement-report-2026-10-05.md)
- D8 review: [../reviews/d8-req-nf-15-review-2026-10-05.md](../reviews/d8-req-nf-15-review-2026-10-05.md)
