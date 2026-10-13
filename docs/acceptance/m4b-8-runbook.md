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

# M4b-8 browser acceptance runbook (dev HTTPS same-origin stack)

**Mapping**: [`test-plan.md`](test-plan.md) §1.4 "M4b-8 browser acceptance procedure" steps 1–5.  
**Stack**: [`deploy/compose/README.md`](../../deploy/compose/README.md) (PostgreSQL 12.22 + config-service + Caddy self-signed TLS).  
**Status**: engineering/AI-executable checklist; **does not** constitute M4b/M4/REQ acceptance pass; maintainer sign-off see [`report.md`](report.md) M4b-8 section (recorded 2026-10-04).

## 0. Preparation

- [ ] Docker available on WSL2/Linux
- [ ] Complete compose README quick start: `gen-certs` → `postgres` → `migrate` → `bootstrap-admin` → `up` → `smoke-https.sh` passes
- [ ] Record environment: git commit, `docker compose images`, **non-secret** items in `.env` (do not commit passwords/HMAC)
- [ ] Prepare a second account (approver): after the first admin logs in, create it via the user-management API/UI (use API if the UI is not ready); record role assignment
- [ ] 7.2d production ingress preflight: not covered by this runbook; keep **BLOCKED** (see test-plan §1.4)

## 1. Step 1 — operator rule CRUD → approval request

**Acceptance intent**: create/edit/disable/delete test rules; each submitted for approval; after refresh the live status is consistent with the queue; no fixture fallback.

| Check | Result | Note |
|---|---|---|
| Log in as operator over HTTPS | ☐ PASS / ☐ FAIL / ☑ **BLOCKED** | testable once stack is ready; rule write path below |
| Create/edit/disable/delete rule and submit approval (**called-party + prefix**) | ☐ PASS / ☐ FAIL | adjudication accepted; live console only exposes called-party + prefix; PG E2E `test_postgres_managed_rule_pipeline_integration.py` |
| Calling-party / regex rules | **N/A (v1.1)** | not in M4; see [`m4-req-calling-regex-lossless-adjudication-2026-10-03.md`](../reviews/m4-req-calling-regex-lossless-adjudication-2026-10-03.md) |
| Approval queue consistent with live table | ☐ PASS / ☐ FAIL | depends on called-party + prefix rule change path |

**Evidence**: redacted screenshots, HTTPS API calls in Network (no plaintext cookie/token).

## 2. Step 2 — approver approve/reject

**Acceptance intent**: different approver; approve valid changes; rejection requires a reason; creator must not self-approve/self-reject; status consistent with audit.

| Check | Result | Note |
|---|---|---|
| approver login | ☐ PASS / ☐ FAIL | requires the second account from step 0 |
| Approve/reject existing ChangeOrder (7.3a scope) | ☐ PASS / ☐ FAIL | can verify submit/approve/reject against an existing draft/submitted order in the DB |
| Creator self-approve/self-reject rejected | ☐ PASS / ☐ FAIL | API already has regression; confirm again in browser |
| Empty rejection reason rejected | ☐ PASS / ☐ FAIL | |

**Evidence**: redacted screenshots, order status before/after comparison.

## 3. Step 3 — Call-ID live trace

**Acceptance intent**: query live trace by a known Call-ID, verify SIP fields and rule hit.

| Check | Result | Note |
|---|---|---|
| Console trace query | ☑ **BLOCKED** | **REQ-F-13 / M4b-7.4**: M4 close adjudication deferred; no live trace source/API |
| Field and rule-hit verification | ☑ **BLOCKED** | same as above |

**Evidence**: N/A (annotate `BLOCKED: missing backend` when backend is absent).

## 4. Step 4 — batched distribution / health / rollback

**Acceptance intent**: batched notify, version load, health check; failed batch auto-rollback; manual rollback.

| Check | Result | Note |
|---|---|---|
| Register testbed instance (health URL) | ☐ PASS / ☐ FAIL | use compose `testbed-health` (`AS_TESTBED_HEALTH_URL`) |
| Operations fleet inventory (instance CRUD) | ☐ PASS / ☐ FAIL | M4b-7.5 console UI (notify/health URL) |
| Start / report / rollback inside Change order | ☐ PASS / ☐ FAIL | M4b-7.6 modal UI; requires enabled fleet instance and health probe |
| API-level notify + health probe (7.5 slice) | ☐ PASS / ☐ FAIL | use internal API + curl; not the full step-4 browser acceptance |
| Inject health failure → auto-rollback | ☐ PASS / ☐ FAIL / ☑ **BLOCKED** | depends on full distribution chain and AS stack |
| Manual rollback | ☐ PASS / ☐ FAIL / ☑ **BLOCKED** | same as above |

**Evidence**: distribution report JSON (redacted), health probe logs.

## 5. Step 5 — audit and fail-closed

**Acceptance intent**: §3 audit fields; redaction; append-only; explicit write of rejections; fail-closed on failure paths.

| Check | Result | Note |
|---|---|---|
| Login/logout/ChangeOrder operations produce audit | ☐ PASS / ☐ FAIL | verify within step 2 operable scope |
| Export/query audit has no password/token | ☐ PASS / ☐ FAIL | |
| Runtime role denies INSERT/UPDATE/DELETE/TRUNCATE on audit | ☐ PASS / ☐ FAIL | use `psql` with `as_config_web` + `SET ROLE` to verify |
| audit unavailable etc. fail-closed | ☐ PASS / ☐ FAIL | inject as needed; operate with care |

**Evidence**: redacted audit rows, psql denial output.

## 6. Artifact archiving

Place redacted materials into the maintainer-specified directory (placeholder):

```
artifacts/m4b-8/<YYYY-MM-DD>/
```

In [`report.md`](report.md) § M4b-8 fill in path, commit, and blocker summary; maintainer sign-off already recorded (2026-10-04).

## 7. Playwright automation (optional)

```sh
cd deploy/compose
export M4B8_E2E_PASSWORD='<12+ chars, dev-only>'   # script syncs admin / ops-e2e / mgr-e2e via the owner DSN
./scripts/m4b-8-browser-evidence.sh
```

Artifacts default to `artifacts/m4b-8/<date>/` (screenshots + JSON log). On Ubuntu 20.04, if `playwright install chromium` fails, the script falls back to the `mcr.microsoft.com/playwright` container (`--network host`).

## 8. Manual browser notes (when no automation)

1. Open `https://localhost:8443/` → accept self-signed cert → confirm no mixed-content.
2. DevTools → Network: confirm APIs are on the **same origin** `https://localhost:8443/internal/v1/...`.
3. Login failure/success still uses HTTPS scheme; do not access via `http://`.
4. Cover cookie, session, CSRF, and password fields before saving screenshots.
