# M5 committable evidence (redacted)

Sanitized M5.1 transcripts. Raw kind runs may still land under gitignored `artifacts/m5/<date>/`.

## Filenames are the verdict (since 2026-10-11)

Evidence files in this directory require the mandatory prefixes `PASS-` / `FAIL-` / `FAILCLOSED-`, with the format `<verdict>-<verified-item>-<date>.txt`
(the `-sample` suffix denotes the tail summary of that run). The basis is
[`../../handoff/2026-10-11-open-adjudication-register.md`](../../handoff/2026-10-11-open-adjudication-register.md) §7.4 layer 1.

The three prefixes are not interchangeable; **always treat the filename as authoritative**:

| Prefix | Meaning | Pass evidence? |
|---|---|---|
| `PASS-` | The collected command **exited 0** | Yes |
| `FAIL-` | The collected command **ran but exited non-zero** | **No** |
| `FAILCLOSED-` | Explicitly declined rather than guessed (e.g. `M5_STRICT=1` with no cluster, `exit=1`) | **No** |

> **`FAIL-` is a prefix added on 2026-10-11.** Previously `deploy/kind/m5-record-artifacts.sh` collected with
> `make X 2>&1 | strip_ansi > file`; the pipe's exit code came from `strip_ansi` (always 0) rather than `make`,
> so failed runs were written as `PASS-` files — under "filename is the verdict", this fabricated a green evidence out of nothing.
> The script now splits by `PIPESTATUS[0]`: failures land in `FAIL-`, the script finally exits non-zero, and the file header states the real exit code.

> **`Fail` / `ERROR` strings inside this directory are normal semantics and must not be used to judge a file as failed; always rely on the filename prefix.**

## Index table

| Path | Verdict | Meaning |
|---|---|---|
| `2026-10-05/PASS-gate-2026-10-05.txt` | Pass | full `make gate` (must end in pytest passed). **Contains SKIPPED items**; see item 3 of "Three things easily misread" below |
| `2026-10-05/PASS-gate-sample-2026-10-05.txt` | Pass | last lines of that run (also contains SKIPPED items) |
| `2026-10-05/PASS-chart-check-2026-10-05.txt` | Pass | `make chart-check`, last line `chart-check: OK`; contains `[INFO] Fail:` lines which are expected assertions, see item 2 below |
| `2026-10-05/PASS-chart-check-sample-2026-10-05.txt` | Pass | content copy of the same run |
| `2026-10-05/PASS-alert-check-2026-10-05.txt` | Pass | `promtool check rules` → `SUCCESS: 5 rules found` (**covers only the original 5 rules at that time**) |
| `2026-10-05/PASS-alert-check-sample-2026-10-05.txt` | Pass | content copy of the same run |
| `2026-10-05/FAILCLOSED-m5-strict-context-2026-10-05.txt` | **Not pass evidence** | `M5_STRICT=1` with no `kind-as-m5` (**exit=1**), fail-closed path record |
| `2026-10-11/PASS-alert-check-full-2026-10-11.txt` | Pass | Docker run `promtool check rules` → `SUCCESS: 10 rules found` (**covers all 3 groups of 10 rules**: as.call-path 5 + as.runtime 3 + as.platform 2); image `prom/prometheus:v2.45.0`, host `WIN-03IB7NIEPF0` |
| `2026-10-11/PASS-gate-2026-10-11.txt` | Pass | local host (`dev-win03ib7niepf0`) `make gate` (ruff format --check / ruff check / mypy / pytest unit+contract) → `1037 passed, 10 skipped, 206 deselected`. **Contains SKIPPED items**; when citing you must also state the skip composition, see item 3 below |
| `2026-10-11/PASS-gate-sample-2026-10-11.txt` | Pass | tail summary of the same run (also contains SKIPPED items) |
| `2026-10-11/PASS-chart-check-2026-10-11.txt` | Pass | local host `make chart-check`, last lines `chart-check: OK`, `1 chart(s) linted, 0 chart(s) failed`; semantics identical to the 2026-10-05 row (`[INFO] Fail:` is an expected assertion, see item 2 below); helm 3.16.4 (`tools/bin/`, first local output after infra bootstrap) |
| `2026-10-11/PASS-chart-check-sample-2026-10-11.txt` | Pass | content copy of the same run |
| `2026-10-11/PASS-alert-check-2026-10-11.txt` | Pass | **local** promtool **2.55.1** (`tools/bin/`, **same version** as the 2026-10-05 evidence) `check rules` → `SUCCESS: 10 rules found` (**covers all 3 groups of 10 rules**: as.call-path 5 + as.runtime 3 + as.platform 2); binary provenance is the official image extraction (not a release tarball, GitHub unreachable on install day), see [`../../../handoff/2026-10-11-local-infra-bootstrap-execution-record.md`](../../../handoff/2026-10-11-local-infra-bootstrap-execution-record.md) |
| `2026-10-11/PASS-alert-check-sample-2026-10-11.txt` | Pass | content copy of the same run |
| `2026-10-11/FAILCLOSED-m5-strict-context-2026-10-11.txt` | **Not pass evidence** | `M5_STRICT=1` context check: this run the `kind-as-m5` context was present, the check itself `exit=0`, but per the collection script design this file is **always** recorded as `FAILCLOSED` and never cited as pass evidence (different from the 2026-10-05 row's `exit=1` failure path; neither is pass evidence) |
| `2026-10-11/FAIL-m5-verify-strict-2026-10-11.txt` | **Not pass evidence** | `M5_STRICT=1 bash deploy/kind/m5-verify.sh` **exit=1**: the newly built `as-m5` cluster has only an empty control plane (`No resources found in as-m5 namespace.`, the product AS pod is not deployed), jsonpath assertion out of bounds. **Failed honestly** — confirms "tools and cluster ready ≠ cluster-level product verification passed" |
| `2026-10-11/FAIL-m5-verify-strict-sample-2026-10-11.txt` | **Not pass evidence** | tail summary of the same run |
| `2026-10-11/PASS-gate-native-2026-10-11.txt` | Pass | local host (`dev-win03ib7niepf0`) **first** real-stack gate: `make gate-native` → `1068 passed, 2 skipped, 206 deselected, 11 warnings`, exit 0. **Contains 2 SKIPPED**, both from `testbed/simulators/tests/test_derived_baseline.py:245` / `:279` (S1-basic-call did not construct Route / Record-Route header, requires a dedicated M2 probe capture) — **none from a missing native extension** (the original 7 `native_extensions.py` skips and 1 `_resip_recovery` skip have disappeared). When citing you must also state the skip composition, see item 3 below |
| `2026-10-11/PASS-gate-native-sample-2026-10-11.txt` | Pass | tail summary of the same run (also contains SKIPPED items) |
| `2026-10-11/PASS-phase-a-revalidation-2026-10-11.txt` | Pass | A3 Phase A real-stack revalidation: E1 two contract files `-m contract` → `7 passed`; `test_resip_runtime_integration.py::test_accept_all_invites_harness_mode_returns_200` (`integration` marker, not collected in the default gate) → `1 passed` |
| `2026-10-11/PASS-phase-a-revalidation-sample-2026-10-11.txt` | Pass | content copy of the same run |
| `2026-10-11/PASS-e2e-2026-10-11.txt` | Pass | A4 after Wave 1 landed `uv run pytest -m e2e -q` → `5 passed, 1292 deselected` (`testbed/e2e/test_sip_first_edition.py`; an earlier run the same day was `1276 deselected`, the difference of 16 comes from new evidence files adding +16 parameterized root-guard cases, e2e is always 5). Previously `-m e2e` collected **0 cases** |
| `2026-10-11/PASS-e2e-sample-2026-10-11.txt` | Pass | content copy of the same run |
| `2026-10-11/PASS-native-smoke-2026-10-11.txt` | Pass | four local real-stack smoke checks each `exit=0`: `m2-native-smoke` (S1 UDP), `m2-native-smoke-tcp` (S1 TCP), `m2-native-smoke-tcp-runtime` (1 passed), `m2-native-smoke-tls-runtime` (3 passed, test CA / self-signed, **does not close REQ-S-2 / REQ-S-3**) |
| `2026-10-11/PASS-native-smoke-sample-2026-10-11.txt` | Pass | content copy of the same run |
| `2026-10-12/PASS-integration-compose-2026-10-12.txt` | Pass | local host (`dev-win03ib7niepf0`) started **PostgreSQL 12.22** (`wal_level=replica`) from `deploy/compose` then ran standard `make test-integration-compose` → `196 passed, 5 skipped, 0 failed, 0 error`, exit 0. Previously (no PG) this layer was `2 failed / 113 errors`. The 5 SKIPPED composition: 2 Redis unreachable + 3 `CREATE PUBLICATION requires wal_level=logical` |
| `2026-10-12/PASS-integration-compose-sample-2026-10-12.txt` | Pass | tail summary of the same run |
| `2026-10-12/PASS-integration-compose-redis-2026-10-12.txt` | Pass | same as above + local Redis (`as-redis-test`, 6379) → `198 passed, 3 skipped`, exit 0; the 2 Redis-related skips disappear |
| `2026-10-12/PASS-integration-compose-redis-sample-2026-10-12.txt` | Pass | tail summary of the same run |
| `2026-10-12/PASS-integration-pg-logical-2026-10-12.txt` | Pass | same as above + PG 12.22 with `wal_level=logical` (custom `AS_PG_TEST_DSN` pointing to `:55433`) → `200 passed, 1 skipped`, exit 0. The remaining 1 skip is a PG version gate (`requires PostgreSQL 15 or newer`, standard compose is 12.22), not a defect. **Deviation: this file deviates from standard `make test-integration-compose` (uses a custom DSN)** |
| `2026-10-12/PASS-integration-pg-logical-sample-2026-10-12.txt` | Pass | tail summary of the same run |
| `2026-10-12/FAIL-integration-pg15-2026-10-12.txt` | **Not pass evidence** | **Failed honestly**: under PG **15.18** (custom DSN `:55434`) `-m integration` → `1 failed, 124 passed, 76 errors`, exit 1. Root cause: `SELECT defaclobjtype || ':' || ...` → `AmbiguousFunction: operator is not unique: "char" || unknown` (PG 14+ changed this column type from `char` to `"char"`, requires explicit type cast). **No product code changed**; the repo standard environment (compose) is PG 12.22, so this is not currently blocking, but PG 12 is already EOL and will be hit on upgrade |
| `2026-10-12/FAIL-integration-pg15-sample-2026-10-12.txt` | **Not pass evidence** | tail summary of the same run |
| `2026-10-12/PASS-chart-version-sync-2026-10-12.txt` | Pass | **A6 first chart sync** (maintainer directive on 2026-10-12 "when and to what to sync is decided by the agent"): before sync `--check` honestly showed DRIFT (`version: 0.0.0-skeleton` / `appVersion: "0.0.0"` vs root `VERSION` `0.2.0`, exit 1); action = adopt adjudicated `kubeVersion: ">=1.23.0-0"` + `sync-chart-version.sh --apply`; after sync `--check` exit 0 (`version: 0.2.0` / `appVersion: "0.2.0"`), `make chart-check` (helm 3.16.4, `tools/bin/helm` resolved via `HELM_BIN`) → `chart-check: OK`. Environment `dev-win03ib7niepf0` |
| `2026-10-12/PASS-f15-distribution-lifecycle-rollback-2026-10-12.txt` | Pass | M8 batch 3 F-15 real AS full stack (kind-as-m5/ns as-m5/release `as`): two healthy batches auto applied + idempotent apply, the last unhealthy batch auto rolled_back, manual rollback after the first batch, fleet cluster actually received notify; includes NF-10. fleet is a protocol stub (AS has no notify receiver), does not close REQ |
| `2026-10-12/PASS-nf2-deployment-isolation-2026-10-12.txt` | Pass | NF-2: after deleting the translation Pod and within the rebuild window, anti-fraud /health/live+/ready 42/42 were 200, Pod UID/startTime/restartCount unchanged throughout |
| `2026-10-12/PASS-nf9-namespace-isolation-2026-10-12.txt` | Pass | NF-9: while ns-A stopped bundled PG + deleted the two AS Deployments, independent ns-B (release `asb`) 58/58 were 200, 7 Pod identities checked item-by-item unchanged before and after; ns-A restored via helm upgrade (separately recorded config-service single-connection-no-auto-reconnect observation) |
| `2026-10-12/PASS-nf5-simulator-transport-consistency-2026-10-12.txt` | Pass | NF-5: on the M7.1 simulator S-SBC the product AS verdict distribution per-bucket was identical across UDP/TCP/TLS three rounds for T1/T4/T5/F1/F2 (15 calls: 200x9/404x3/603x3, unresolved=0); TLS is test CA, not operator PKI |
| `2026-10-12/FAILCLOSED-nf4-rolling-restart-inflight-loss-2026-10-12.txt` | **Not pass evidence** | NF-4 rolling zero-loss **not achieved**: during continuous UDP traffic (350 calls/round) a single-replica rollout restart reproduced timeout_invite 3/4, bye_sip_481 6/7, timeout_bye 4/3, unresolved 10 each; root cause headless single-replica switch window + DUM dialog state only in process memory. **2026-10-12 maintainer adjudication accepted this loss, NF-4 signed pass under the accepted interpretation (see next row); this file remains the original failure record, not pass evidence** |
| `2026-10-12/PASS-nf4-rolling-upgrade-accepted-loss-2026-10-12.txt` | Pass (maintainer signed-off, accepts measured call loss; non-zero loss) | NF-4 adjudication evidence: two rounds of measurement (350 calls/round, 13/14 affected, 10 unresolved each) + complete mechanism analysis; current release accepts this call-loss level, rolling zero call-loss is a future release enhancement feature (not scoped for this version) |
| `2026-10-12/PASS-backup-restore-drill-bundled-pg-2026-10-12.txt` | Pass | 2.5 drill: after real bundled PG12 DROP, pg_restore rc=0 (dump 0.259s/restore 0.704s are local measured magnitudes not commitments), 12 counts + three-role consistency, audit append-only 8 guards rejected as designed, console restored, audit continued writing |
| `2026-10-12/PASS-config-service-auth-distribution-409-fix-2026-10-12.txt` | Pass | P0 fix: auth-mode distribution endpoint must return 409 (shared connection polluted by auth SELECT + redundant idle check), removing the check net -10 lines + 2 real PG/HTTPS/CSRF regression tests; file 19 passed, config-service full 629 passed/3 skipped |
| `2026-10-12/PASS-nf15-multi-replica-measurement-2026-10-12.txt` | Pass | M8 batch 5 NF-15: kind-as-m5/ns nf15-perf, 2 replicas across five tiers 20/80/320/640/1280 CPS + 4 replicas at 1280 point, zero failures across all tiers; records per-pod CPU/memory (relative to 200m/256Mi requests) and setup latency p50/p95/p99; separately records ClusterIP UDP short-flow endpoint pinning (conntrack source-port retention) architecture finding. accept-all/kind symbolic model, not external capacity |
| `2026-10-12/PASS-o1-loopback-cps-1280-2026-10-12.txt` | Pass (**internal only, must not be written into external materials**) | O1 internal engineering target retest: loopback/accept-all 1280 CPS×15s, 19200/19200 setups, zero failure/zero unresolved, p95 12.79ms; lower-bound baseline non-saturation point not a committed value |
| `2026-10-12/PASS-hpa-threshold-filled-2026-10-12.txt` | Pass | values-onprem.example.yaml appended autoscaling (enabled/min2/max4/CPU70%/MEM70%, comment includes "measured on kind, not an external commitment, must re-test on target environment before go-live"); default values.yaml and hpa.yaml guards zero-changed; example renders 2 HPAs, default 0, both guards verified effective, make chart-check OK |
| `2026-10-12/FAILCLOSED-performance-gate-terminal-state-2026-10-12.txt` | **Not pass evidence** | performance layer gate terminal state (blocking layer or M8 overall review written acceptance of risk) pending maintainer adjudication; agent neither implemented nor accepted on behalf, registered as FAILCLOSED, not counted in the pass list |
| `2026-10-12/PASS-s1-whitelist-rejection-2026-10-12.txt` | Pass | M8 batch 4 S-1 supplement: added `platform/tests/test_req_s1_whitelist_rejection.py` (9 unit tests) driving the real `ResipRuntimeListener._on_invite`, pinning the product path for whitelist miss / empty policy / cert mismatch / endpoint port / CIDR / plaintext UDP-when-TLS-required returning **403**, and asserting with a `received_at` probe that `decide()` was not executed; pure in-process, no socket no native extension, the 403 frame's wire layer still covered by existing integration. Same-batch measured: `make gate` → `1159 passed, 227 deselected, 11 warnings`, **0 skipped**, exit 0. **Does not close REQ-S-1** |
| `2026-10-12/FAILCLOSED-s1-whitelist-change-approval-not-wired-2026-10-12.txt` | **Not pass evidence** | M8 batch 4 S-1 forensic: **the capability "whitelist change takes effect after approval" does not exist** — `ConfigBundle` (`platform/src/as_platform/api/contract.py:71`, fields :89-91) only has version/rules/toggles; the only approvable proposal `ManagedRuleChange` (`services/config-service/src/as_config_service/change_order.py:68`) only manages rules; `platform/src` `gate.install` / `install_with_overlap` **have no product call site**; `load_transport_seam_from_env` is only read once at construction in `sip_stack_service.py:126`/:156 (= change Helm values + restart). Registered as a gap, requesting the maintainer to adjudicate one of two options (include in change order as a v1.1 new feature / or revise the matrix REQ-S-1 row wording). agent **did not implement** this capability, this file must not be counted in the pass list |
| `2026-10-12/PASS-s4-audit-append-only-2026-10-12.txt` | Pass | M8 batch 4 S-4 supplement (audit append-only): (A1) on the internal environment `dev-win03ib7niepf0` compose PostgreSQL (`as-m4b8-dev-postgres-1`, DSN password redacted to `postgresql://postgres:***@127.0.0.1:55432/as_config`) re-ran `test_postgres_audit_store_integration.py` → `35 passed, 3 skipped`, exit 0, the 3 SKIPPED all are `CREATE PUBLICATION` gates under `wal_level=replica`, **not including** any tamper-proof guard case; the core guard case passed when run alone. (A2) added `services/config-service/tests/test_req_s4_audit_immutability.py` (7 unit tests, into `make gate`) reading `ensure_schema` literals via AST, pinning the row-level `BEFORE UPDATE OR DELETE` / statement-level `BEFORE TRUNCATE` two triggers, guard bodies `audit rows are immutable` / `audit table is append-only` and `ERRCODE = '23514'`, `tgtype` bitmask self-computed 27/34, `LOCK TABLE ... ACCESS EXCLUSIVE MODE`, store has no mutation API and the public name set is closed. **A2 is a structural assertion, not equivalent to database-side measurement** (database-side measurement covered by A1). `make gate` → `1174 passed, 249 deselected`, 0 skipped, exit 0. **Does not close REQ-S-4** |
| `2026-10-12/PASS-s4-rbac-permission-matrix-2026-10-12.txt` | Pass | M8 batch 4 S-4 supplement (RBAC permission matrix): added `services/config-service/tests/test_req_s4_rbac_api_matrix_integration.py` (22 integration tests, real PG, same redacted DSN) pushing the matrix from kernel pure functions to the **HTTP boundary** — 20 parameterized rows covering read / submit / approve / rollback / manage_users × viewer / operator / approver / admin, each cell consistent with `access.py:60-75` `ROLE_PERMISSIONS`; each 403 assertion detail exactly equals the permission-denied copy (excluding CSRF / two-person principle / 404 impersonation). **manage_users has an HTTP enforcement point** (`api.py:746`, endpoints `GET /internal/v1/auth/users` and two others), **no fabricated endpoints, no uncovered permissions**. Additionally verified privilege-escalation trace: viewer submits → 403 and the audit table `<audit_schema>.<prefix>_audit_events(actor, action, resource, outcome)` gains exactly one `denied` row. Two-person principle separately established one (approver self-review → 403). Boundary: each permission takes only one representative endpoint, other endpoints mounting the same `require_*` are not enumerated one-by-one (the list is in the file). `make gate` exit 0. **Does not close REQ-S-4** |
| `2026-10-12/PASS-e6-packaging-recheck-2026-10-12.txt` | Pass | M8 batch 6 / E-6 packaging recheck (executed 2026-10-13, environment `dev-win03ib7niepf0`): `test_version_consistency` 9 passed, `test_evidence_discipline` 135 passed, `make gate` 1174 passed/249 deselected, image rebuild exit 0 (**new digest `sha256:63ba8f4df78d...`, inconsistent with batch 1's `sha256:8f2e1b9465d...`, recorded new digest as required**), redaction recheck found no secrets/certs/captures/password-bearing logs, SIP listen runtime verification `RESIP_RUNTIME_LISTENING ... udp_port=5060`, `make chart-check` OK, AS_SIP_*/AS_TLS_*/AS_PEER_* 16 variables checked one-by-one with no drift |
| `README.md` | — | this index |

## Three things easily misread

1. **`FAILCLOSED-m5-strict-context-2026-10-05.txt` is a failure record with exit=1, not pass evidence.**
   It records the **fail-closed path** when `M5_STRICT=1` and no `kind-as-m5` cluster exists (content is
   `ERROR: kind-as-m5 context missing (M5_STRICT=1)` / `exit=1`). Its value is to prove the behavior "fails explicitly when no cluster"
   exists, and it **must not** be counted in any "passed" list.

2. **`PASS-chart-check-2026-10-05.txt`'s `[INFO] Fail: tls.enabled=true requires tls.secretName`
   is the chart-check's expected assertion for a fail-closed render, normal semantics, does not mean the file failed.**
   The same applies to the nearby `sip.peerAllowlist must be non-empty (ADR-0016 fail-closed)` and
   `[INFO] Chart.yaml: icon is recommended`; the basis for judgment is the last line `chart-check: OK` and
   `1 chart(s) linted, 0 chart(s) failed`.

3. **`PASS-gate-2026-10-05.txt` contains SKIPPED items; per existing discipline "skip is not pass evidence".**
   That run was `878 passed, 2 skipped, 145 deselected`, the two SKIPPED both come from
   `testbed/simulators/tests/test_derived_baseline.py:245` and `:279`
   (S1-basic-call did not construct Route / Record-Route header, requires a dedicated M2 probe capture to assert).
   **When citing this file you must also state the skip composition**, do not just write "gate passed".

## Citation convention

All evidence is expressed as the triple `(verdict, evidence file, date)`, e.g.
`(verified, docs/acceptance/artifacts/m5/2026-10-05/PASS-chart-check-2026-10-05.txt, 2026-10-05)`;
environment names see [`../../environments.md`](../../environments.md) (anonymous "local host" is forbidden to appear again in documents).

Do not store passwords, tokens, DSNs, or cookies.
