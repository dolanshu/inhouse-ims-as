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

# ADR-0022 acceptance adjudication (2026-10-05)

> **Subject:** Maintainer-facing verdict on ADR-0022 acceptance review  
> **Cross-ref:** [`adr-0022-acceptance-review-2026-10-05.md`](adr-0022-acceptance-review-2026-10-05.md)

## Adjudication

| Question | Verdict |
|----------|---------|
| Accept ADR-0022 status **accepted** with 2026-10-05 amendment? | **Accept** (engineering authorization for M7 control layer) |
| ADR selects production Python/C++ bridge API? | **Deny** — still open (D9) |
| D10 / REQ-NF-1 satisfied? | **Deny** — unchanged hard requirement |
| M7 milestone / E1 / REQ acceptance? | **Deny** — not claimed by this acceptance |
| K2 released? | **Deny** |

## Rationale

The September 2026 technical review already conditioned approval on visible blockers (D10, bridge API, E1). M2 delivered a product listener path; the M7 slice adds the **logical** `CallController` and a **minimal** two-leg native experiment under `platform/native/`, distinct from the approved long-term adapter surface. Elevating ADR-0022 to **accepted** records that the product will implement cross-leg control in Python above DUM, not that integration or recovery gates are cleared.

## Maintainer sign-off

**Pending** — acceptance recorded in repo; does not substitute for maintainer signature on milestone or REQ gates.
