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

# Execution Record: W0 Real-Stack Build Normalization + A3 Re-verification + A4 Wave 1 e2e Landing

> **Status: executed, awaiting maintainer review; signs off no REQ / milestone.**
> This document is the execution record for the **locally executable portion** of §0-A.1 (the three authorized items) and §5 W0 of
> [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md);
> the original plan text was not backfilled, and this document is **append-only** throughout.
> Basis: G1–G8 in §0-A.6 of that document were all landed as adjudication records on 2026-10-10, so W0's A2 / A3 **depend on no pending adjudication**;
> the maintainer's 2026-10-10 stance of "review approval is not execution authorization" **remains in effect**, and the records here do not replace per-instance approval.
>
> **This document signs off no REQ and no milestone, constitutes no external acceptance pass, and lifts no hold**
> (the external IOT / real-environment evidence collection hold and the deferred M8 exit signature remain in effect).
> **No git write operation was performed this time**: no `commit` / `add` / `push` / `tag` / branch creation / remote change;
> all changes stay in the work tree, and the commit split is the maintainer's decision.

**Execution environment**: registered environment **`dev-win03ib7niepf0`** (host `WIN-03IB7NIEPF0`, Ubuntu 22.04.5 LTS / WSL2 / x86_64,
user `shudong`, never root throughout). Execution date: 2026-10-11.

---

## 0. Quick Conclusion Overview

| Item | Result | Triple / basis |
|---|---|---|
| **A2 · Real-stack build normalization** | ✅ Done. `make m2-platform-resip-build` succeeded; `make gate-native` exit 0, **1068 passed / 2 skipped / 206 deselected**; the original 7 `native_extensions.py` skips and 1 `_resip_recovery` skip **all disappeared (real execution)** | `(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-gate-native-2026-10-11.txt, 2026-10-11)` |
| **A3 · Phase A real-stack re-verification** | ✅ Done. 7 contract + 1 integration **all green** (previously there had never been a real-stack re-verification record) | `(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-phase-a-revalidation-2026-10-11.txt, 2026-10-11)` |
| **A5 · Alert rule syntax validation** | ✅ Re-run locally. `make alert-check` (local promtool **2.55.1**) → `SUCCESS: 10 rules found` (3 groups, 10 rules); `make chart-check` → `chart-check: OK` | see §6; the pre-existing closure of P4 (2026-10-11) was not reopened |
| **A4 · e2e Wave 1 landing** | ✅ Done. Created `testbed/e2e/test_sip_first_edition.py`; `pytest -m e2e` went from **0 collected** to **5 collected and green 3 consecutive times**; when native is missing it **fails instead of skipping** (verified by measurement) | `(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-e2e-2026-10-11.txt, 2026-10-11)` |
| **Local real-stack smoke (local portion of E1 / E4 / E5)** | ✅ All four passed: S1 UDP, S1 TCP, TCP runtime (1 passed), TLS runtime (3 passed) | `(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-native-smoke-2026-10-11.txt, 2026-10-11)` |
| **M7 extensions (the "if needed" item in the W0 table)** | ✅ Done incidentally: both `_resip_recovery` and `_resip_two_leg` were built | see §3.2 |
| **Pre-existing defect exposed by A2** | ⚠️ Discovered and **fixed**: the `RESIP_RUNTIME_LISTENING` port regex does not include the `advertised=` field, in **5 places**; it had never matched since it landed in commit `139d299` (it kept skipping because the `.so` was missing). After the fix, `testbed/load` smoke is 1 passed and `m6-product-runtime-smoke.sh` exits 0 | see §11. **No capacity or performance number was produced** |
| **Root guard `uv run pytest tests/ -q`** | ✅ **115 passed** | see §8 |
| **Plain `make gate` (non-native mode)** | ✅ exit 0, **1084 passed / 2 skipped / 211 deselected** | see §8 (211 = 206 + the 5 new e2e cases this round, all deselected by `-m "unit or contract"`) |

**Not done / out of scope this round**: W1 (the **execution** of the A6 version stance), W2 (B1–B6, maintainer adjudication / review, where the B1 value is still open),
W3 (C1–C5, needs an external environment, §0 item 2 hold), the 14 Wave 2 replays of A4-3 (the carrier has been taken over by
[`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md),
with implementation waiting for a later A4 batch), and A5's **capture wiring** (X1, still awaiting the carrier's monitoring-integration standard input).
Details in §9.

---

## 1. Key Fact: This Machine Had Never Built a Native Extension Before

`make gate-native` is the "largest gap" precisely because this machine previously had **no** `_resip_*.so` at all:

| Check | Measured before execution on 2026-10-11 |
|---|---|
| `find . -name "_resip*.so"` | **no hits at all** |
| `.cache/` directory | **does not exist** (the reSIProcate source and build tree were never restored / compiled on this machine) |
| Consequence | 7 cases in `platform/tests/native_extensions.py:24` + 1 in `test_sip_recovery.py:69` were **skips, not passes** |

This round is the **first** time this machine has produced a real-stack gate run since [`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md) was landed on 2026-10-09.

---

## 2. Prerequisite: The Root-Free Route to the Native Build Dependencies (This Machine Was Missing Two dev Packages)

The `check_native_build_deps()` in `testbed/simulators/resip-probe/scripts/m2-native.sh` requires
three pkg-config packages: `popt` / `libcares` / `openssl`. Measured on this machine: **openssl ✅, popt ❌, libcares ❌**
(the two runtime libraries `libpopt.so.0` / `libcares.so.2` exist in `/usr/lib/x86_64-linux-gnu/`, but the **dev packages are not installed**,
so there is no `.pc` and no headers). `sudo` on this machine **requires a password** and there was never root, so the route taken was "download .deb → unpack into the repo-internal `.cache/` (gitignored) →
point cmake at it via environment variables", **without modifying the system**.

### 2.1 Why the Prebuilt Tarball in vendor Was Not Used

`testbed/simulators/resip-probe/vendor/resiprocate-m2-ubuntu20.04-x86_64-prebuilt-20261004.tar.gz`
is a build artifact for **Ubuntu 20.04 / OpenSSL 1.1**; this machine is **Ubuntu 22.04 / OpenSSL 3**
(`libssl.so.3` / `libcrypto.so.3`). Per the explicit requirement in that vendor directory's `README.md`
("Reuse the binaries only when `ldd` resolves every dependency … Newer Ubuntu releases commonly
provide OpenSSL 3 instead; in that case rebuild from the bundled source"),
the **prebuilt route does not hold**, so this round switched to **building from the bundled source**.

### 2.2 Commands Actually Executed (reproducible)

```bash
# 1) 随仓源码恢复（sha256 由脚本校验）
make m2-native-restore
# 实测输出：resiprocate-1.14.0-632e215c-source.tar.gz: OK ；prebuilt: OK
#          extracting ... -> .cache/m2-resiprocate/source

# 2) 取两个 dev 包（apt-get download 不需要 root）
mkdir -p /tmp/depdl && cd /tmp/depdl
apt-get download libpopt-dev libc-ares-dev
dpkg-deb -x libc-ares-dev_*_amd64.deb x-libc-ares-dev
dpkg-deb -x libpopt-dev_*_amd64.deb    x-libpopt-dev

# 3) 装进仓库内 .cache/native-deps/（gitignored，不入库）
cd /home/shudong/project/3rdparty-as
mkdir -p .cache/native-deps/usr
cp -a /tmp/depdl/x-libc-ares-dev/usr/. .cache/native-deps/usr/
cp -a /tmp/depdl/x-libpopt-dev/usr/.    .cache/native-deps/usr/
LIB=.cache/native-deps/usr/lib/x86_64-linux-gnu
# dev 包里的 .so 是指向 .so.N 的符号链接，指回系统运行时库（链接期用，运行期仍由系统解析）
ln -sf /usr/lib/x86_64-linux-gnu/libcares.so.2 $LIB/libcares.so
ln -sf /usr/lib/x86_64-linux-gnu/libpopt.so.0  $LIB/libpopt.so

# 4) 构建期环境变量（每条 make 命令前都要带上）
export PKG_CONFIG_PATH="$PWD/.cache/native-deps/usr/lib/x86_64-linux-gnu/pkgconfig"
export CMAKE_PREFIX_PATH="$PWD/.cache/native-deps/usr"
export CMAKE_LIBRARY_PATH="$PWD/.cache/native-deps/usr/lib/x86_64-linux-gnu"
export CPLUS_INCLUDE_PATH="$PWD/.cache/native-deps/usr/include"
export C_INCLUDE_PATH="$PWD/.cache/native-deps/usr/include"
```

**One measured pitfall (recorded so it is not stepped on again)**: when only `PKG_CONFIG_PATH` + `CMAKE_PREFIX_PATH` are set, the cmake configure passes,
but compiling `rutil` reports `fatal error: ares.h: No such file or directory`
— reSIProcate's `WITH_C_ARES=ON` only attaches `PkgConfig::cares` to the link libraries and **does not add its include directory to the compile targets**,
so the header path must additionally be supplied via `CPLUS_INCLUDE_PATH` / `C_INCLUDE_PATH`.

**Toolchain on this machine**: `cmake 3.22.1`, `g++ 11.4.0`, `pkg-config`, `nproc 12`.

---

## 3. A2 · Real-Stack Build Normalization

### 3.1 Building reSIProcate and the Probe

```bash
make m2-native-build        # = build-resip + build-probe
```
Measured: exit 0; `reSIProcate build OK: .cache/m2-resiprocate/build`;
`resip_probe OK: .cache/m2-resiprocate/probe-build/resip_probe`.

### 3.2 Building the Three Platform Extensions

| Command | Artifact | Result |
|---|---|---|
| `make m2-platform-resip-build` | `platform/native/resip_runtime/build/_resip_runtime.cpython-310-x86_64-linux-gnu.so` | ✅ |
| `make m7-platform-recovery-build` | `platform/native/resip_recovery/build/_resip_recovery.cpython-310-x86_64-linux-gnu.so` | ✅ |
| `make m7-platform-two-leg-build` | `platform/native/resip_two_leg/build/_resip_two_leg.cpython-310-x86_64-linux-gnu.so` | ✅ |

The latter two belong to the "M7 extensions (if needed)" row of the W0 table: this round **needed** them — only with those in place does the
`test_sip_recovery.py:69` skip disappear.

### 3.3 Measured Result of `make gate-native`

| Run | Result | Explanation |
|---|---|---|
| When only `_resip_runtime` was built | **1067 passed / 3 skipped / 206 deselected / 11 warnings**, exit 0 | 1 `_resip_recovery` skip + 2 `test_derived_baseline` skips remain |
| After all three extensions were present (closing value) | **1068 passed / 2 skipped / 206 deselected / 11 warnings**, exit 0 | see below |

**A2 exit criteria checked item by item:**

| Exit criterion | Measured |
|---|---|
| `make m2-platform-resip-build` succeeds | ✅ §3.2 |
| `AS_REQUIRE_NATIVE_EXTENSIONS=1 make gate` (equivalent to `make gate-native`) runs through | ✅ exit 0 |
| The original 7 `native_extensions.py` skips **disappear** | ✅ the `SKIPPED` section of the closing run **has only 2 entries**, both from `testbed/simulators/tests/test_derived_baseline.py:245` / `:279` (S1-basic-call does not construct Route / Record-Route headers, which requires a dedicated M2 probe capture) — **not one** comes from a missing native extension |
| One complete run result is archived | ✅ `PASS-gate-native-2026-10-11.txt` |

> **On the relationship between 1068 and historical counts**: this document does not explain it by subtracting the 2026-10-10 `1002 passed / 10 skipped` —
> the two are several sessions apart, and the guards and test cases themselves grew continuously (earlier on 2026-10-11 the plain `make gate`
> on this machine was already `1037 passed / 10 skipped`). The criterion of A2 is **"whether the native-related skips disappear"**, which is directly proven by the
> `SKIPPED` section of the closing run and is unrelated to the absolute count.

---

## 4. A3 · Phase A Re-verification of the SIP native plan

```bash
uv run pytest platform/tests/test_e1_contract_resip_runtime.py \
              platform/tests/test_e1_contract_resip_runtime_full.py -m contract -q
# → 7 passed in 0.73s

uv run pytest platform/tests/test_resip_runtime_integration.py::test_accept_all_invites_harness_mode_returns_200 -q
# → 1 passed in 0.12s
```

**A3 exit criteria checked item by item:**

| Exit criterion | Measured |
|---|---|
| ① The two E1 contract files (including `test_e1_s1_accept_all_harness_returns_200`, `test_e1_s1_accept_all_from_contract_invite`) have real execution results | ✅ `7 passed`; S1–S4 all green at the contract layer (previously there were only changes and **no real-stack re-verification record**) |
| ② `test_resip_runtime_integration.py::test_accept_all_invites_harness_mode_returns_200` (`integration` marker, **not** collected by `-m "unit or contract"`, must be specified explicitly) | ✅ `1 passed` |
| Phase D's scope and batches are scheduled | ⚠️ **Not completed by this round** — the scheduling of that plan's Phase D (the 14 S1 replays, the S5–S11 real-stack cases) needs the maintainer to confirm priorities; of these, "the 14 S1 replays" has been taken over by the in-repo carrier [`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md) of A4-3 |
| The handling of the three Sign-off boxes at the end of that plan is made explicit | ✅ **appended** at the end of [`2026-10-09-sip-native-testing-plan.md`](2026-10-09-sip-native-testing-plan.md): box 1 (Phase A) ticked; box 2 (Phase C native build job) and box 3 (Phase D) marked not completed with the basis written out |

> **The §0 "2 failed when this machine has .so files" of the 2026-10-09 plan did not recur** in this real-stack re-verification:
> both `test_e1_s1_accept_all_harness_returns_200` and `test_e1_s1_accept_all_from_contract_invite` passed.
> This signs off nothing on any REQ; it only shows that Phase A **is green under real-stack re-verification** for the changes after commit `18f2bb7`.

---

## 5. Local Real-Stack Smoke (Local Portion of E1 / E4 / E5, Not External IOT)

Per the exception paragraph of §0.1 and §5 "W0 scope adjustment" of
[`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md):
the S1–S4 harness and the **self-signed-certificate** TLS smoke **are not external IOT**,
are not deferred by the §0 item 2 adjudication, and proceed in W0 together with A2 / A3.

| Command | Measured |
|---|---|
| `make m2-native-smoke` (S1 UDP, `resip_probe` runs through to `RemoteBye`) | exit 0, `smoke passed (S1 UDP)` |
| `make m2-native-smoke-tcp` (S1 TCP loopback) | exit 0, `smoke passed (S1 TCP)` |
| `make m2-native-smoke-tcp-runtime` (product TCP runtime integration) | exit 0, `1 passed` |
| `make m2-native-smoke-tls-runtime` (product TLS runtime integration, **test CA / self-signed**) | exit 0, `3 passed` (21.57s) |

**Boundary (must not be exaggerated)**: the TLS test uses a **test CA generated together with the test**,
and per the pre-existing stance **does not sign off REQ-S-2 / REQ-S-3** (those require a carrier PKI and a public-network S-SBC, which belong to the deferred external evidence collection).

---

## 6. A5 · Alert Rule Syntax Validation and Chart Shape Gate (local re-run)

The 2026-10-11 infra bootstrap on this machine installed `helm` / `promtool` into `tools/bin/` (not committed),
so `tools/bin` must be in `PATH`:

```bash
export PATH="$PWD/tools/bin:$PATH"
make chart-check   # → chart-check: OK（1 chart(s) linted, 0 chart(s) failed），exit 0
make alert-check   # → Checking deploy/alerts/as-alerts.yaml / SUCCESS: 10 rules found，exit 0
```

- `alert-check` uses local **promtool 2.55.1**, the **same version** as the historical alert evidence of 2026-10-05;
  the 10 rules = `as.call-path` 5 + `as.runtime` 3 + `as.platform` 2 (3 groups).
- This is **the same thing on a different evidence basis** as the pre-existing closure of register §2 P4; this document **does not reopen** P4.
- **`promtool` is only syntax validation**: X1 (capture-wiring annotation vs ServiceMonitor/PodMonitor) still awaits the carrier's
  monitoring-integration standard input, and **syntax passing ≠ wiring closure**.

---

## 7. A4 · e2e Wave 1 Landing

### 7.1 Landed According to Adjudication (all four adjudications were landed on 2026-10-10)

| Adjudication | How it was landed | Measured |
|---|---|---|
| **A4-1** create a separate new file | Created `testbed/e2e/test_sip_first_edition.py`; the `integration` marker of `testbed/simulators/tests/test_product_path.py` is **untouched** | ✅ the integration layer is preserved as-is |
| **A4-2** **fail** when native is missing | In-case `_require_product_stack()`: **fails unconditionally**, no env branch, no skip | ✅ measured: after temporarily moving `_resip_runtime*.so` away, `-m e2e` → **5 failed, 0 skipped** (failure message `e2e never skips for a missing native extension (A4-2)`); the `.so` was then restored and a re-run confirmed recovery |
| **A4-3** the 14 Wave 2 items are deferred to a separate carrier | Carrier = [`../acceptance/2026-10-11-wave2-replay-register.md`](../acceptance/2026-10-11-wave2-replay-register.md) (register §2 P5 closed) | ✅ the 14 replays are **not implemented** this round, and Wave 1 did not contain them either (the plan's Wave 1 "explicitly not doing" row already states that the 14 per-header replays are not in Wave 1) |
| **A4-4** kind e2e enters the PR-required E2E policy | The adjudication text states "**this direction is only a policy direction registration, and does not constitute authorization for any configuration change; this task changes no configuration file**" | ✅ **no** CI / gate configuration was changed this round; what was created is a locally runnable **non-kind** e2e |

### 7.2 Cases and Measurements

| Case ID (that plan's §3) | Test | Assertion essentials |
|---|---|---|
| E2E-SIP-1 | `test_e2e_sip_1_udp_t1_translated_call_completes` | the final state of UDP T1 is **200**; the outbound leg user is the translation result `013800138000` (and the inbound caller `+8613800138000` does not reach the peer directly); BYE count == answered count; `unresolved_sessions == 0`; no `bye_*` errors |
| E2E-SIP-2 | `test_e2e_sip_2_udp_t4_no_match_returns_404` | the final state of UDP T4 is **404**; `+155500030003` does not reach the peer UAS; BYE count == 0 |
| E2E-SIP-3 | `test_e2e_sip_3_udp_f2_blocked_returns_603` | the final state of UDP F2 is **603**; no service leg goes out; BYE count == 0 |
| E2E-SIP-4 | `test_e2e_sip_4_stream_transport_t1_completes[tcp\|tls]` | one T1 sub-case each for TCP and TLS; TLS uses the **test CA**, and the docstring explicitly states "does not sign off REQ-S-2 / REQ-S-3" |

```
uv run pytest -m e2e -q
→ 5 passed, 1292 deselected, 1 warning      （连续 4 次：4.85s / 4.76s / 4.51s / 4.81s，均 5 passed）

> **deselected 计数说明**：同一命令在收尾复跑时为 `1292`（全仓收集 1297）。
> 差额 16 来自根守卫 `tests/test_evidence_discipline.py` 对证据文件的逐文件参数化 ——
> 本次新增的 8 个证据文件使守卫用例 +16（99 → 115），全仓收集数随之上升。
> 两次都是同一命令的真实输出，**不是** e2e 用例数的变化：e2e 恒为 5 条。
```

**The three properties that make this e2e rather than integration** (written into the case module docstring): the AS under test is the **product stack**
(`_resip_runtime` + `ResipRuntimeListener`); the decision goes through the **production seam** (`decide()` over `demo_rules()`,
with `accept_all_invites` kept off); the path **crosses a network-element boundary** (load generator → simulated S-CSCF → simulated S-SBC → AS → peer UAS).

**One implementation trade-off (recorded)**: the **call count** inside the load window of `run_load` varies with `duration_seconds` / `workers`
and with whether the scenario terminates immediately (measured with `workers=1` for a single scenario: T1 is 1 call, T4 / F2 are 3).
Therefore the assertions take values **only from the set of final response codes and from invariants such as "BYE count == answered count"**,
and do not hardcode the count as `== 1`, so that timing jitter is not frozen into a flaky assertion.

### 7.3 Relationship to S1 Item 4 (no behaviour change, only an annotation added)

The first S1 batch moved `-m e2e` out of `make test` because at that time `-m e2e` collected nothing and was guaranteed to exit 5.
Now that e2e is non-empty, the factual premise of that comment has changed, so **a single annotation sentence was appended** to
the comment on the `test` target in the `Makefile` to describe the current state; **not one character of the actual behaviour of `make test` was changed** — whether to bring the e2e layer back into `make test`
is a gate configuration change and, like A4-4, belongs to the **maintainer adjudication** scope (A4-4's adjudication explicitly "constitutes no authorization for any configuration change").

---

## 8. Evidence List (Always Expressed as Triples)

| Triple | Content |
|---|---|
| `(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-gate-native-2026-10-11.txt, 2026-10-11)` | `make gate-native` → `1068 passed, 2 skipped, 206 deselected, 11 warnings`, exit 0; **contains 2 SKIPPED** (both from `test_derived_baseline.py:245` / `:279`, not from a missing native extension) |
| `(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-phase-a-revalidation-2026-10-11.txt, 2026-10-11)` | A3 re-verification: contract 7 passed + integration 1 passed |
| `(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-e2e-2026-10-11.txt, 2026-10-11)` | `uv run pytest -m e2e -q` → `5 passed, 1292 deselected` (closing re-run value; an earlier run the same day was `1276 deselected`, the 16 difference coming from the new evidence files adding +16 parameterized root-guard cases; e2e stays at 5, see §7.2) |
| `(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-native-smoke-2026-10-11.txt, 2026-10-11)` | the four local real-stack smokes, each `exit=0` |

There are also local re-runs (the same items under verification as the earlier bootstrap round of 2026-10-11, not new conclusions):
`make chart-check` → `chart-check: OK`; `make alert-check` → `SUCCESS: 10 rules found`.

**Root guard**: `uv run pytest tests/ -q` → **115 passed** (measured at the close of 2026-10-11).
This count varies as guard cases grow: the 8 new evidence files of this round are covered file-by-file by the parameterized
`tests/test_evidence_discipline.py::test_evidence_filename_states_its_verdict`,
so the guard count rises accordingly; it does not conflict with the 62 / 68 / 76 / 94 / 99 recorded in the register, which are measured facts of different sessions.

**`make gate` (plain mode, non-native)**: exit 0, **1084 passed / 2 skipped / 211 deselected**.
The `211 deselected` is 5 more than the pre-native-mode `206` — that is, the 5 new e2e cases of this round (excluded by `-m "unit or contract"`).

**Static checks**: `uv run ruff check testbed/e2e/` → `All checks passed!`;
`uv run ruff format --check testbed/e2e/` → `1 file already formatted`;
the `ruff format --check .` / `ruff check .` / `mypy` inside `make gate` all passed.

---

## 9. Out-of-Scope / Not-Done Items (Written Item by Item, No Ambiguity)

| Not done | Reason / ownership |
|---|---|
| **Execution of the A6 version stance** (syncing `Chart.yaml` version / appVersion, declaring `kubeVersion`) | The G4 adjudication states "currently do not modify `VERSION` and `Chart.yaml`"; the `kubeVersion` minimum is "derived backwards from the APIs used, no numeric adjudication is made this time". **`VERSION` / `Chart.yaml` were not changed** this round |
| **A5 capture wiring** (annotation vs ServiceMonitor/PodMonitor) | **X1 still awaits the carrier's monitoring-integration standard input**; the adjudication states "do not change the chart for now". Not a single byte of `deploy/helm/` was touched |
| **The 14 Wave 2 replays of A4** | The carrier is in place (wave2-replay-register), implementation waits for a later A4 batch; **REQ-F-1 is not signed off**, and all 14 of its items remain open |
| **Phase C (native build in CI and required)** | It is a CI configuration change and needs maintainer authorization; this round only normalizes it **on this machine** |
| **Scheduling of Phase D (S5–S11 real-stack cases)** | The maintainer must confirm priorities |
| **W2 · B1–B6** | B1 (O1) **value still open**; the values of B2 / B3 / B4 are adjudicated but **not implemented / not authorized**; B5 (the nine M8 N2 items + signature) and B6 (the review of 16 packaging documents) are **maintainer** actions |
| **W3 · C1–C5** | They need an external environment, and the §0 item 2 hold remains in effect. **The local real-stack green does not substitute for any of them** |
| **Any change under `deploy/`** | Not a single byte of chart / alerts / kind scripts was touched |
| **git write operations** | No `commit` / `add` / `push` / `tag` / branch creation / remote change |

---

## 10. Three Things the Maintainer Needs to Note

1. **The native build on this machine depends on a temporary directory outside the repo** (`.cache/native-deps/`, gitignored, not committed).
   On another machine (or after clearing `.cache/`), `make m2-platform-resip-build` falls back to the "missing dev packages" state
   and §2.2 must be redone, or `apt-get install libpopt-dev libc-ares-dev` can be run directly on a machine that has root.
   **This is a new machine-capability fact** and has not yet been written into the registration row of [`../environments.md`](../environments.md)
   (that table is generated by `tools/env-probe.sh` and must not be hand-edited, so it is only recorded in this document for now; **whether to fold it into the probe script is for the maintainer to decide**).
2. **A4-4 and "does e2e go back into `make test`" are the same pending item**, and this round **did not adjudicate on the maintainer's behalf**:
   the behaviour of `make test` remains as it was in the first S1 batch (unit/contract + integration only).
3. **Real-stack green does not mean REQ-level acceptance passed**: all conclusions of this round are **engineering gate layer** evidence,
   the open 24 / blocked 12 of `report.md` §0.5 were **not changed by a single character**, no REQ is signed off, and no milestone is signed off.

---

## 11. A Pre-existing Defect Exposed by A2 (Fixed, Needs Maintainer Confirmation)

**This is precisely where the value of A2 lies**: once skips became real execution, a defect that had **never been discovered before** immediately became visible.

### 11.1 Symptom

`testbed/load/tests/test_product_runtime_smoke.py::test_product_resip_runtime_uas_smoke`
failed on the **very first real run** after the real stack was in place:

```
Failed: timed out waiting for RESIP_RUNTIME_LISTENING:
RESIP_RUNTIME_LISTENING address=127.0.0.1 advertised=127.0.0.1 udp_port=45749
```

### 11.2 Root Cause (Not a Problem with This Machine's Environment)

- The C++ side (`platform/native/resip_runtime/runtime_module.cxx:1478-1480`) actually outputs
  `address=… advertised=… udp_port=…` — which is **consistent** with the line format recorded in
  [`../acceptance/m8-resip-runtime-log-contract.md`](../acceptance/m8-resip-runtime-log-contract.md) §3
  (that document's sample line itself contains `advertised=`).
- But the consumer uses the **old regex without `advertised=`**,
  `RESIP_RUNTIME_LISTENING address=127\.0\.0\.1 udp_port=(\d+)` — it can never match and will always time out.
- `git log -S` shows: the printing of `advertised=` and that smoke case **landed in the same commit `139d299`**,
  meaning **this case has never matched since it landed**; it stayed green only because this machine (and every recorded run)
  never had a `.so`, so the case was **skipping** all along.

**The same defect exists in 5 places**: `_LISTEN_RE` in `testbed/load/tests/test_product_runtime_smoke.py`,
and the `_UAS_UDP_RE` of the 4 M6 scripts under `testbed/load/scripts/`
(`m6-product-runtime-smoke.sh`, `m6-product-runtime-micro-measure.sh`,
`m6-product-runtime-measure-60s.sh`, `m6-o1-formal-report.sh`) —
the latter four extract the port with `sed -nE` and would likewise never obtain the port and then `die`.

### 11.3 Fix (backward compatible, introduces no capacity numbers)

The regex is changed to **treat `advertised=` as an optional field**:

| Location | Change |
|---|---|
| `testbed/load/tests/test_product_runtime_smoke.py` | `_LISTEN_RE` → `RESIP_RUNTIME_LISTENING address=127\.0\.0\.1 (?:advertised=\S+ )?udp_port=(\d+)` (Python `re`, capture group numbering unchanged) |
| `testbed/load/scripts/m6-*.sh` (4 files) | `_UAS_UDP_RE` → `… address=127\.0\.0\.1 (advertised=[^ ]+ )?udp_port=([0-9]+)`, `sed` backreference `\1` → `\2` (ERE **does not support** `(?:…)`, hence a capture group is used and the port becomes `\2`) |

**Verification**:
- `uv run pytest testbed/load/tests/test_product_runtime_smoke.py -q` → **1 passed** (previously failed with a 60s timeout)
- `bash testbed/load/scripts/m6-product-runtime-smoke.sh` → exit 0,
  `smoke passed (established_sessions=1)`, `UAS UDP port: 45662` (previously it would `die` at the port extraction step)
- Both regex forms measured: the port is obtained **both** with and without `advertised=` (45749 / 5060)
- `uv run ruff check testbed/load/` → `All checks passed!`; `ruff format --check` → `12 files already formatted`;
  the 4 shell scripts pass `bash -n`

**Boundary**: this round **neither produced nor rewrote** any capacity or performance number; what was fixed is the **port-extraction regex**,
and M6's historical measurement reports and O1 conclusions are **out of scope this round**.

### 11.4 Another Measured Fact (Not Fixed, Environment-Dependent)

The integration layer of `make test` **cannot run fully** on this machine: the Postgres integration cases of `services/config-service` need
a PostgreSQL at `127.0.0.1:55432` (provided by compose), and that service is not started on this machine ⇒
**113 errors + 1 failed (PG-related) + 11 skipped**; `make test` ultimately exits 2.
This is **unrelated** to this round's changes (the same situation occurs on any machine without compose PG running),
and is **not** an exit criterion of A2 / A3 / A4. Starting compose PG is a container action, **not done this round**, and is registered faithfully.

---

**Landed: 2026-10-11. Status: executed, awaiting maintainer review.**
(Corresponding plan: [`2026-10-10-unfinished-assessment-and-next-plan.md`](2026-10-10-unfinished-assessment-and-next-plan.md)
§0-A.1 / §5 W0; environment registration: [`../environments.md`](../environments.md);
evidence index: [`../acceptance/artifacts/m5/README.md`](../acceptance/artifacts/m5/README.md).)
