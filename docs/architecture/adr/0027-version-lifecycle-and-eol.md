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

# ADR-0027: Version Lifecycle and EOL Policy

- **Status**: accepted
- **Date**: 2026-10-09
- **Decides**: version lifecycle and EOL policy
- **Responds to REQ**: REQ-NF-16

---

## Context

ADR-0018 resolved "where the version number comes from" (the root VERSION is the single source of release, component interface versions live in `pyproject.toml`), but did not answer "once a version is released, how long is it supported, when does support stop, and how is it upgraded."

For carrier customers (especially Hong Kong telecom operators), the version lifecycle is a basic threshold for procurement review:
- Operations teams need to know how long the current version remains usable, so they can plan upgrade windows.
- Commercial teams need the EOL commitment, so they can sign SLAs.
- Security teams need to know whether security patches are still provided after EOL.

The project is currently at the v0.2.0 stage and has not formally released a GA version. Before v1.0 GA, a clear version lifecycle policy must be defined; otherwise the carrier internal review cannot be passed.

## Decision

**Support period**: each minor version (e.g. 1.0, 1.1, 1.2) is supported for **at least 12 months** from GA, providing bug fixes and security patches during the support period.

**EOL advance-notice period**: at least **6 months** before a version's EOL, an EOL announcement is published, giving customers an upgrade window.

**Upgrade path**:
- Adjacent minor versions (e.g. 1.0 → 1.1 → 1.2) must support direct upgrade without service interruption (ISSU, see ADR-0009).
- Cross-major versions (e.g. 1.x → 2.0) require a migration guide and data-migration tooling.

**LTS versions**: no LTS version is defined at this time. If a future carrier customer explicitly requires LTS, a new ADR must be added to define the LTS policy (support period, upgrade path, maintenance-cost sharing).

**Security patches**: after EOL, no further security patches are provided. Customers must upgrade to a supported version.

**Scope**: this policy applies only to GA versions (`major.minor.0`). Development versions (`0.x.y`) and pre-releases are not covered by the lifecycle commitment.

## Consequences

### Positive

- **Carrier review can pass**: version lifecycle is a basic threshold for procurement review; with a clear policy, the question "how long is it unsupported" will not be raised.
- **Operations can plan**: the customer operations team can plan upgrade windows based on the support period, avoiding passive exposure to a sudden EOL.
- **Commercial can commit**: SLAs and maintenance contracts can be priced based on the support period.

### Negative / accepted

- **Increased maintenance cost**: a 12-month support period means each minor version must be maintained (bug-fix and security-patch branches) for at least 12 months after release. For a small team, this may increase the maintenance burden.
- **No LTS defined**: some carrier customers may require LTS (e.g. 3–5 years of support); the current policy does not satisfy this. If needed in the future, a new ADR must be added and maintenance costs evaluated.
- **No security patches after EOL**: for security-sensitive customers, no patches after EOL may be unacceptable. This must be communicated clearly during the pre-sales stage.

## Alternatives considered

| Option | Why not |
|---|---|
| Define LTS version (3–5 year support) | Current team size and maintenance cost do not support LTS. If a future carrier customer explicitly requires it, a new ADR must be added to evaluate cost sharing |
| 6-month support period | 6 months is too short for carrier customers and cannot pass procurement review. Industry practice is 12–24 months |
| Continue providing security patches after EOL | Maintenance cost is too high and contradicts the "no LTS" policy. EOL means all support stops |

## Evidence

- `docs/product-packaging-plan.md` §3.5 explicitly lists "version lifecycle and EOL policy" as a third-batch deliverable, requiring a new requirement + ADR.
- `docs/reviews/product-packaging-plan-review-2026-10-09.md` G-P1-4 / G-P1-9 points out that ADR-0018 only covers version-number semantics; lifecycle/EOL is a new decision.
- Hong Kong telecom operator procurement reviews typically require a version-lifecycle commitment (industry practice).

## Related

- [ADR-0018](0018-release-versioning.md) unified product release version + independent component interface versions
- [`../system-architecture.md`](../system-architecture.md) §11.3 development model —— version-governance section
- [`docs/product-packaging-plan.md`](../../product-packaging-plan.md) §3.5 version lifecycle and EOL policy
