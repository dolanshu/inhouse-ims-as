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

# Execution Record: Integration-Layer Completion + native Reproducibility + O1 Saturation Probe + A4 Wave 2 Landing

> **Status: executed, pending maintainer review; no REQ / milestone is signed off.**
> This document records the **four** items the maintainer authorized on 2026-10-12; the cause is that in the previous round I misstated the nature of two of them:
> ① I wrongly classified "starting compose PostgreSQL to run the integration layer" as "a container action requiring authorization" (there is no such rule, see §2);
> ② I wrongly classified A4 Wave 2 as "a boundary I drew myself" (it is in fact an adjudication already written to disk on 2026-10-10, see §5.1).
> This document **only appends**; it does not rewrite any existing original text.
>
> **This document signs off no REQ, signs off no milestone, does not constitute a pass for external acceptance, and does not lift any hold**
> (deferring external IOT / real-environment evidence gathering and the M8 exit sign-off remains in effect).
> **No git write operation was performed**: no `commit` / `add` / `push` / `tag` / branch creation / remote change.

**Execution environment**: the registered environment **`dev-win03ib7niepf0`** (host `WIN-03IB7NIEPF0`,
Ubuntu 22.04.5 LTS / WSL2 / x86_64, user `shudong`). Execution date: 2026-10-12.

---

## 0. Conclusion Quick View

| Item | Result | Triple / Basis |
|---|---|---|
| **① Integration-layer completion** | ✅ From "113 errors + 2 failed" to **200 passed / 1 skipped / 0 failed / 0 error** (PG 12.22 + `wal_level=logical` + Redis) | `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-integration-pg-logical-2026-10-12.txt, 2026-10-12)` |
| **② New finding: PG 15 incompatibility** | ⚠️ **Truthfully failed**: under PG **15.18** the integration layer has **1 failed / 76 errors**; root cause `defaclobjtype \|\| ':'` → `AmbiguousFunction: operator is not unique: "char" \|\| unknown` (PG 14+ changed that column's type from `char` to `"char"`). **No product code was changed** | `(failed, docs/acceptance/artifacts/m5/2026-10-12/FAIL-integration-pg15-2026-10-12.txt, 2026-10-12)` |
| **③ native reproducibility verification** (B4's suggested first step) | ✅ With an **independent cache directory**, a from-zero `restore` → build reSIProcate + probe → build `_resip_runtime` → `make gate-native` exit 0 (**1100 passed / 2 skipped**). The native build **is reproducible and the artifacts are usable** | see §3 |
| **④ O1 saturation probe** (B1's suggested second step) | ⚠️ **Saturation point not reached**: 20 → 1280 CPS were **all 100% successful with zero errors**; the only degradation signal is `unresolved_sessions` 2 → 13 → 30. **No external capacity value can be set from this** | see §4 |
| **⑤ A4 Wave 2 landing** | ✅ Newly created `testbed/e2e/test_s1_replay_contract.py` (3 cases); `pytest -m e2e` went from 5 → **8 cases**; green across several consecutive runs; with native missing, **8 failed / 0 skipped** | see §5 |
| **Final gate** | ✅ Both `make gate` and `make gate-native` exit 0, **1100 passed / 2 skipped / 214 deselected**; root guard `uv run pytest tests/ -q` → **131 passed** | see §7 |

---

## 1. Correction One: there is no rule saying "container actions require authorization"

In the previous round I wrongly generalized the maintainer's authorization for **one specific command** (`deploy/kind` promtool-equivalent container command, 2026-10-10 §0.2 item 2) into a **ban on a class of actions**. After checking:

| Fact | Location |
|---|---|
| The 2026-10-11 infra bootstrap **actually executed** `docker create` + `docker cp` (extracting promtool from the official quay.io image) | [`2026-10-11-local-infra-bootstrap-execution-record.md`](2026-10-11-local-infra-bootstrap-execution-record.md) §4.3 |
| Likewise, it actually executed `docker pull kindest/node:v1.31.0` (1.49 GB) and `kind create cluster --name as-m5` | same §4.5 / §6 |
| The only thing written as "confirm first" is an **irreversible action**: deleting a kind cluster | same §11 |
| `AGENT.md` has **no** general authorization clause about docker / containers | whole-file search |

Conclusion: starting compose PostgreSQL to run the integration layer is exactly the design purpose of the **repository's own `make test-integration-compose` target**, and it is reversible (`docker compose down`). **The previous round's refusal was my error in drawing the boundary, not a block.**

---

## 2. Integration-Layer Completion

### 2.1 Starting compose PostgreSQL

```bash
# compose 需要 .env；仓库自带 .env.example 的 dev-only 默认值即与 DSN 匹配
cp deploy/compose/.env.example deploy/compose/.env     # 该文件被 .gitignore:44 忽略
docker compose -f deploy/compose/compose.yml up -d postgres
# 注：首次走 compose 时镜像源返回 502；改用 docker pull postgres:12.22 直接拉全后重试成功
# 结果：as-m4b8-dev-postgres-1 / postgres:12.22 / 监听 55432 / wal_level=replica
```

### 2.2 Measured Results Tier by Tier

| Configuration | Command | Result | Triple |
|---|---|---|---|
| PG 12.22 `wal_level=replica`, **no** Redis | `make test-integration-compose` | **196 passed / 5 skipped / 0 failed / 0 error**, exit 0 | `(verified, .../PASS-integration-compose-2026-10-12.txt, 2026-10-12)` |
| Same **+ Redis** | `make test-integration-compose` | **198 passed / 3 skipped**, exit 0 | `(verified, .../PASS-integration-compose-redis-2026-10-12.txt, 2026-10-12)` |
| PG 12.22 **`wal_level=logical`** + Redis (custom DSN `:55433`) | `AS_PG_TEST_DSN=... uv run pytest -m integration -q` | **200 passed / 1 skipped**, exit 0 | `(verified, .../PASS-integration-pg-logical-2026-10-12.txt, 2026-10-12)` |
| PG **15.18** `wal_level=logical` + Redis (custom DSN `:55434`) | same | **1 failed / 124 passed / 76 errors**, exit 1 | `(failed, .../FAIL-integration-pg15-2026-10-12.txt, 2026-10-12)` |

**Cause of the final 1 skip**: `test_postgres_audit_store_integration.py:947`
"schema publication coverage requires PostgreSQL 15 or newer (current server_version_num=120022)"
— i.e. it **necessarily skips under the standard compose environment (PG 12.22)**; this is not a defect.

**Deviation statement (the last two tiers)**: tiers 3 and 4 deviated from the standard `make test-integration-compose`
(using a custom `AS_PG_TEST_DSN` pointing at a container I started separately), in order to eliminate the two skip sources
`wal_level` and the PG version. The PG15 container of tier 4 reused the `deploy/compose/postgres/init` initialization script
(read-only mount); **no file under `deploy/` was modified**.

### 2.3 New finding: `AmbiguousFunction` under PG 15 (not fixed, registered)

```
psycopg.errors.AmbiguousFunction: operator is not unique: "char" || unknown
LINE 1: SELECT defaclobjtype || ':' || defaclrole::text FROM pg_catalog.pg_default_acl ...
HINT:  Could not choose a best candidate operator. You might need to add explicit type casts.
```

- **Impact surface**: 77 places (76 errors + 1 failed share the same root cause), all in the Postgres integration tests of `services/config-service`.
- **Root cause**: starting with PostgreSQL **14**, the type of `pg_default_acl.defaclobjtype` changed from `char` to `"char"`, and combining it with the `||` operator produces an ambiguity that requires an explicit type cast.
- **Why it does not block right now**: the repository's standard environment is the **postgres:12.22** written explicitly in `deploy/compose/compose.yml`.
- **Why it is worth registering**: PostgreSQL **12 went EOL in 2024-11**. This is **the same class of problem** as D1 (Python 3.10 EOL) — the standard environment runs on an already-EOL dependency, and upgrading PG will hit this.
- **Handling this time**: **no product code was changed** (that would be a product code change, requiring the full requirement → ADR → design → review process). Only a truthful `FAIL-` evidence file was written and registered here; **whether to initiate a fix is for the maintainer to decide**.

---

## 3. native Build Reproducibility Verification (B4 / G1's suggested first step)

**Why this step first**: B4's (the Python 3.12 spike) adjudication only fixed the handling options and explicitly states that "whether to execute it bound to the W0 native build is undecided". My recommendation is **not to merge it in**, because if a Python minor migration were bound into the **first** native build, the two conclusions "does the first real-stack gate hold" and "is 3.12 usable" would cross-contaminate and could not be attributed separately. The prerequisite action for that recommendation is first proving that "the native build itself is rebuildable" — otherwise there is nothing to attribute to.

**Method**: rebuild from zero using an **independent cache directory**, without destroying the existing usable build.

```bash
export PKG_CONFIG_PATH="$PWD/.cache/native-deps/usr/lib/x86_64-linux-gnu/pkgconfig"
export CMAKE_PREFIX_PATH="$PWD/.cache/native-deps/usr"
export CPLUS_INCLUDE_PATH="$PWD/.cache/native-deps/usr/include"
export C_INCLUDE_PATH="$PWD/.cache/native-deps/usr/include"
export AS_RESIP_CACHE_ROOT="$PWD/.cache/m2-repro-check"

make m2-native-restore            # exit 0（vendor sha256 校验 + 源码提取到新目录）
make m2-native-build              # exit 0（reSIProcate + resip_probe 从零编译）
make m2-platform-resip-build      # exit 0
make gate-native                  # exit 0，1100 passed / 2 skipped / 211 deselected
```

**Result: the native build is rebuildable, and the artifacts under the new path are usable.**

**Two measured pitfalls (recorded so they are not re-stepped on)**

1. **Missing `restore` fails closed**: running `make m2-native-build` directly errors out because the new cache directory has no source:
   `reSIProcate source not found ... run: m2-native.sh restore`. That is precisely why `make m2-native`
   (restore → build → smoke) exists; the script's error message is effective.
2. **A leftover `AS_RESIP_CACHE_ROOT` makes the artifacts point at the wrong path**: after verification I re-ran
   `make m2-platform-resip-build` in the same shell and the RPATH still pointed at `.cache/m2-repro-check` — this is
   **environment variable residue** (the `export` persists when the shell is reused) plus **cmake caching**
   `-DCMAKE_BUILD_RPATH` (deleting `build/` is needed for it to take effect again).
   Final handling: `unset` the environment variable → delete `platform/native/*/build/` → rebuild → use `readelf -d` to confirm
   the RUNPATH is back to `.cache/m2-resiprocate/build`, then run `make gate-native` to confirm exit 0.

**Conclusion for B4**: since the native build is proven rebuildable, the 3.12 spike can be done as **a single separate change**,
so any failure can be attributed cleanly to 3.12 and will not be confused with "the first build was unstable anyway".

---

## 4. O1 Saturation Probe (B1's suggested second step)

**Background**: the maintainer said the O1 value "cannot just be given any number". My recommendation is **not to invent a number**, but first to add a fact that does not depend on anything external.
Where it landed: the "O1 basis recommendation (appended 2026-10-12)" paragraph below the table in [`../plan.md`](../plan.md) §5.1.

**Probe configuration** (one-off script placed in `/tmp`, **not committed to the repository**; the full command sequence is given here for reproducibility):

```bash
uv run python platform/tests/fixtures/load_uas_runtime.py   # 取 RESIP_RUNTIME_LISTENING udp_port
uv run python -m as_load --host 127.0.0.1 --port "$PORT" \
    --cps "$CPS" --duration 15 --hold 0 --workers "$W" --timeout 5 \
    --stack as-platform-resip-runtime --stack-version 1.14.0-632e215c --out "$OUT"
```

**Measured results** (`workers = max(4, cps/5)`, 15 s per tier):

| CPS | workers | planned | established | peak | unresolved | errors |
|---|---|---|---|---|---|---|
| 20 | 4 | 300 | 300 | 2 | 0 | 0 |
| 40 | 8 | 600 | 600 | 2 | 0 | 0 |
| 80 | 16 | 1200 | 1200 | 2 | 0 | 0 |
| 160 | 32 | 2400 | 2400 | 2 | 0 | 0 |
| 320 | 64 | 4800 | 4800 | 2 | 0 | 0 |
| 640 | 128 | 9600 | 9600 | 13 | 0 | 0 |
| 1280 | 256 | 19200 | 19200 | 30 | 0 | 0 |

**Conclusions (three; none may be exaggerated in the reverse direction)**

1. **No saturation point was observed in the 20 → 1280 CPS range**: `established == planned`, zero errors.
   The saturation point (if it exists) **is above 1280 CPS, outside the range measurable this time**.
2. **The only observable degradation signal** is `unresolved_sessions`: 2 at ≤320 CPS, 13 at 640, 30 at 1280.
   It is a rising count of **sessions that did not converge in time**, and may serve as a candidate metric for future engineering attention, but **it is not a failure rate**.
3. **This result cannot support any external capacity value**. The model is **loopback UDP + accept-all UAS + `hold=0`**,
   with no real network path, no S-SBC, no business processing on the called side, an extremely short session lifetime, and a single process with no multi-replica.

**Actual effect on B1**: it raises the **lower-bound baseline** of the "internal engineering target" from M6's "CPS 20 / concurrency 1200"
to "**CPS 1280 with no failures under this machine's loopback model**" — but that is still a **lower bound**, not a target value and not a committed value.
The external committed value must still wait for an S-SBC path and real-cluster multi-replica measurement.
**No capacity value / HPA threshold / capacity-class alarm was landed this time**; the G5 adjudication sentence "no capacity value is landed before M6 evidence and the maintainer's decision" remains in effect.

---

## 5. A4 Wave 2 Landing

### 5.1 Correction Two: Wave 2 is an adjudication already written to disk, not a boundary I drew myself

In the previous round I described it as "not a blocker, a boundary I drew myself" — **that statement is wrong**. The original text:

> | **G2 / A4-3** | The 14 Wave 2 replay cases are deferred to a separate issue | This iteration only registers them as a gap; this task **does not create an issue**. |
> —— [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md) §0-A.6 (`:57`)

What register §2 **P5** closed is only the gap of "**missing carrier**" (an in-repo doc replacing the issue), and it explicitly writes
"the test case implementation itself still belongs to the A4 e2e batch…… **to be started after Wave 1 completes**".

**Accurate status**: the adjudication is in place (deferred), the carrier is in place ([`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md)),
the **startup prerequisite is satisfied** (Wave 1 landed on 2026-10-11). What is missing is the **authorization to start the next A4 batch**,
which the maintainer granted on 2026-10-12. This section's work is to **execute that authorization**, not to overturn the A4-3 adjudication.

### 5.2 What Was Landed

Newly created **`testbed/e2e/test_s1_replay_contract.py`** (3 e2e cases), following the differential-check definitions in §3 of the carrier:

| Case | Assertion |
|---|---|
| `test_e2e_s1_replay_both_legs_match_the_normalised_baseline` | The **normalized** message sequences of the inbound leg and the outbound leg match the `S1-basic-call` baseline skeleton: each is `INVITE → 200 → ACK → BYE → 200` (1xx are discarded under the "final response code sequence" basis). Requests and responses are **asserted in separate columns**: the two take different code paths inside the bridge, their interleaving order is timing-dependent and must not be frozen |
| `test_e2e_s1_replay_second_leg_starts_a_new_call_id` | **C_in ≠ C_out** (a subset of REQ-F-2): the Call-ID of the inbound INVITE and the Call-ID of the outbound INVITE have **no intersection** |
| `test_e2e_s1_replay_sdp_offer_is_byte_identical_across_legs` | **REQ-F-4**: the body of the outbound INVITE and the body of the inbound INVITE are **byte-for-byte equal** (included **this time**; no separate follow-up was listed) |

**Capture method (truthfully stating the cost)**: the observation point is the `TransparentBridge` on both sides of the AS (`north` = inbound leg / trunk side,
`south` = outbound leg / core side); inside the **test module**, `monkeypatch` wraps `_on_message` (receiving that leg's requests) and
`_forward_response` (receiving that leg's responses). **Not a single byte of the product code or of `as_simulators` was changed**;
the cost is that this case depends on **private APIs**, and renaming anything inside the bridge would break this file.

**Three implementation trade-offs (to avoid writing flaky assertions)**

1. **The patch must be installed before the bridge is constructed** — `SipServer` binds
   `self._on_message` inside `TransparentBridge.__init__`, so patching the class attribute after the instance is constructed has no effect. (The first implementation hit this pitfall, which showed up as "0 messages captured".)
2. **No assumption of "one call"**: the number of calls within the load window is timing-dependent, so the assertions group by **Call-ID**,
   assert the skeleton for **every complete call**, and require at least one.
3. **Retransmissions are collapsed per SIP transaction (CSeq)**: the first version's assertion was turned into `(200, 200, 200, 200)` by 200 OK retransmissions;
   deduplicating by CSeq brought it back to the baseline's `(200, 200)`.

### 5.3 Measurements

```
uv run pytest -m e2e -q                          → 8 passed, 1308 deselected   （Wave 1 的 5 条 + Wave 2 的 3 条）
uv run pytest testbed/e2e/test_s1_replay_contract.py -q  → 3 passed            （连续 4 次稳定）
临时移走 _resip_runtime*.so 后 uv run pytest -m e2e -q  → 8 failed, 0 skipped   （A4-2 成立）
```

### 5.4 Write-back (per the convention in §5 of the carrier)

- [`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md)
  has **appended** §6 "implementation result write-back".
- The REQ-F-1 status in [`../acceptance/test-plan.md`](../acceptance/test-plan.md) has been changed, per the Wave 2 completion criteria in the e2e plan,
  to "**automated subset covered / full text still open**" and linked to the case names; **not a single `- [ ]` was ticked**
  (the 14 item-by-item header differential checks are still open).
- [`../acceptance/2026-10-09-e2e-test-plan.md`](../acceptance/2026-10-09-e2e-test-plan.md) has appended a Wave 2 status correction.

**Boundaries**: the definition of Wave 2 is itself the **normalized skeleton** differential check; it **excludes** the 14 item-by-item headers,
**excludes** the 100/180 provisional response sequence, **excludes** the Via branch pattern, and **excludes** Route consumption.
**REQ-F-1 in full is not signed off, REQ-F-2 / REQ-F-4 are not signed off, no milestone is signed off.**

---

## 6. List of Files Written (files changed in this round)

| File | Nature |
|---|---|
| `testbed/e2e/test_s1_replay_contract.py` | **Newly created** (A4 Wave 2, 3 e2e cases) |
| `docs/handoff/2026-10-12-o1-and-native-reproducibility.md` | **Newly created** (this document) |
| `docs/acceptance/artifacts/m5/2026-10-12/*.txt` | **Newly created** (8 evidence files, including 1 `FAIL-`) |
| `docs/plan.md` | Appended: the "O1 basis recommendation" paragraph below the §5.1 table + 1 row in the §0 decision record table |
| `docs/acceptance/test-plan.md` | Appended: the REQ-F-1 "automated coverage status" paragraph (ticking untouched) |
| `docs/acceptance/2026-10-11-wave2-replay-register.md` | Appended: §6 implementation result write-back |
| `docs/acceptance/2026-10-09-e2e-test-plan.md` | Appended: Wave 2 status correction |
| `docs/acceptance/artifacts/m5/README.md` | Appended: 2026-10-12 evidence index row |
| `docs/handoff/2026-10-10-unfinished-assessment-and-next-plan.md` | Appended: §11.7 / §11.8 / §10.3 B4 scheduling supplement |

---

## 7. Final Gate and Evidence

| Check | Result |
|---|---|
| `make gate` (ruff format --check / ruff check / mypy / `-m "unit or contract"`) | exit 0, **1100 passed / 2 skipped / 214 deselected**; both SKIPPED cases come from `test_derived_baseline.py:245` / `:279` (S1-basic-call does not construct Route / Record-Route headers and needs a dedicated M2 probe capture); **not one** comes from native being missing |
| `make gate-native` | exit 0, same counts |
| `uv run pytest -m e2e -q` | **8 passed, 1308 deselected** |
| `uv run pytest tests/ -q` (root guard) | **131 passed** |
| `uv run ruff check .` | `All checks passed!` |

Triples:

- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-integration-compose-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-integration-compose-redis-2026-10-12.txt, 2026-10-12)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-12/PASS-integration-pg-logical-2026-10-12.txt, 2026-10-12)`
- `(failed, docs/acceptance/artifacts/m5/2026-10-12/FAIL-integration-pg15-2026-10-12.txt, 2026-10-12)`

---

## 8. Local Container and Directory State (not cleaned up, for the maintainer to decide)

All containers started this round for running the integration layer and the probe are **retained undeleted** (deletion is an irreversible action and is not executed unilaterally):

| Container | Image | Port | Purpose |
|---|---|---|---|
| `as-m4b8-dev-postgres-1` (compose) | postgres:12.22 (→ `wal_level=replica`) | 55432 | Standard `make test-integration-compose` |
| `as-redis-test` | redis:7-alpine | 6379 | Eliminating the 2 Redis skips |
| `as-pg-logical-test` | postgres:12.22, `-c wal_level=logical` | 55433 | Eliminating the 3 publication skips |
| `as-pg15-test` | postgres:15-alpine, `-c wal_level=logical` | 55434 | PG15 compatibility probe (produced the `FAIL-` evidence) |
| `as-m5-control-plane` (kind, retained from the previous round) | kindest/node:v1.31.0 | — | The previous round's infra bootstrap |
| `as-pg-test` (leftover from before the previous round, Exited) | postgres:16-alpine | no port mapping | Not started this round, untouched |

Additionally: `deploy/compose/.env` was copied from `.env.example` (ignored by `.gitignore:44`, not committed to the repository),
and its content is the repository's own dev-only defaults; `.cache/m2-repro-check/` is the temporary cache for the reproducibility verification (`.cache/` is ignored).

---

**Write date: 2026-10-12. Status: executed, pending maintainer review.**
(Evidence index: [`../acceptance/artifacts/m5/README.md`](../acceptance/artifacts/m5/README.md);
environment registration: [`../environments.md`](../environments.md).)
