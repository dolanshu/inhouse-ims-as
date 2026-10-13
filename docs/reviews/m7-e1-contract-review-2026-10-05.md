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

# M7 E1 contract smoke — second-pass review (2026-10-05)

> **Subject:** `test_e1_contract_resip_runtime.py` and M7 tail wiring  
> **Cross-ref:** [`m7-milestone-engineering-closure-adjudication-2026-10-05.md`](m7-milestone-engineering-closure-adjudication-2026-10-05.md)

## Scope

| Item | Assessment |
|------|------------|
| `test_e1_s2_no_match_empty_rules_returns_404` | **Accept** — UDP INVITE with S2 called `+99912345678`, empty `RuleSet`, final ≥200 is 404; `active_call_count() == 0` (no outbound leg) |
| `test_e1_s3_block_rule_returns_603` | **Accept** — S3 called `+8616800000000` with block prefix rule → 603; no outbound leg |
| `test_e1_s4_caller_cancel_path` | **Skip** — documented in test file; native binding has no CANCEL/B2BUA forward path |
| REQ / contract trace | **Partial** — maps to REQ-F-6 and `testbed/contracts/sip-baseline/S2-no-match-404`; not full S2 header-by-header replay |
| Skip when `_resip_runtime` missing | **Pass** — matches `test_resip_runtime_integration.py` pattern |
| `AS_RESIP_RECOVERY_CHECKPOINT_FILE` on `on_process_start_restore` | **Accept** (test-only) — spawns `RecoveryStackSession.start_from_adapter_file`; `NATIVE_ON_PROCESS_START_RESTORE_IMPLEMENTED` stays **`False`** |
| Production process restart | **Deny** — env hook does not replace process shell wiring |

## Verification

| Command | Expected |
|---------|----------|
| `make gate` | Green (contract test skip or pass per native build) |

## Recommendation

**Accept** as M7 **engineering** tail only. **Deny** E1 milestone credit and M7 exit.
