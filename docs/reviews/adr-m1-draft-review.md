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

# ADR-0001/0002/0003/0018 M1 Draft Review Record

> Reviewer: AI agent (grilling session)
> Date: 2026-09-28
> Scope: the 4 draft ADRs newly written during the M1 phase
> Status: **batch draft review passed; may be converted to accepted**

## Review Method

Checked one by one against:
1. the decision mapping in the ADR registry README (§0 ledger numbering match)
2. the architecture document §0 decision ledger (consistency of decision content)
3. the dependency relationships in ADR-0019 (whether decisions referenced by ADR-0019 are correctly placed as prerequisites)
4. whether each ADR's Context/Decision/Consequences are complete

---

## 1. ADR-0001: Single monorepo + uv workspace

- **Decides ledger**: decision 3 ✅
- **Context**: the three POC hard problems (cross-repo clone, Docker context, version drift) are described accurately
- **Decision**: uv workspace + AST scan guard, consistent with the architecture document
- **Consequences**: 4 positive, 2 accepted, non-empty
- **Evidence**: test_workspace_layout.py / test_library_independence.py exist and pass
- **Review conclusion**: ✅ **Pass**

## 2. ADR-0002: One process per test case + Redis with externalized state

- **Decides ledger**: decision 2 ✅
- **Context**: POC sippy blocking model + InMemoryStateStore loses sessions on restart
- **Decision**: processes are stateless, all state externalized to Redis (StateStore seam)
- **Consequences**: positive — process boundary = failure domain; accepted — hard dependency on Redis Sentinel
- **Review conclusion**: ✅ **Pass**

## 3. ADR-0003: Single ISC access semantics

- **Decides ledger**: decision 10 ✅
- **Context**: S-SBC transparent bridging → the AS only needs to implement ISC
- **Decision**: the off-network AS does not implement dual-mode adaptation; the testbed needs an S-SBC emulator
- **Consequences**: positive — only one semantics is implemented; accepted — dependency on the carrier's S-SBC bridging correctly
- **Review conclusion**: ✅ **Pass**

## 4. ADR-0018: Unified product release version + independently versioned component interfaces

- **Decides ledger**: §11.3 ✅ (cross-ledger section)
- **Context**: POC VERSION vs pyproject drift
- **Decision**: the root VERSION is the single release source; components declare interface versions
- **Consequences**: positive — drift eliminated; accepted — version governance slightly more complex, but guarded by tests/test_version_consistency.py
- **Review conclusion**: ✅ **Pass**

---

## Adjudication

| ADR | Source | Issue summary | Adjudication | State | Verification method |
|---|---|---|---|---|---|
| ADR-0001 | draft → accepted | No issues, content complete | Accept | Closed | Consistent with registry §3 decision |
| ADR-0002 | draft → accepted | No issues, Consequences non-empty | Accept | Closed | Consistent with registry §2 decision |
| ADR-0003 | draft → accepted | No issues, Context clear | Accept | Closed | Consistent with registry §10 decision |
| ADR-0018 | draft → accepted | No issues, echoes ADR-0002 | Accept | Closed | Consistent with §11.3 |

## Follow-ups

- Change the Status of the 4 ADRs from `draft` to `accepted`
- Update the `docs/architecture/adr/README.md` registry (4 status rows + the note "includes M1 draft review record")
