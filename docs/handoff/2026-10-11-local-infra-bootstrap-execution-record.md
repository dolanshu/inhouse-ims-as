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

# Execution record: local installation of infra (helm / kubectl / kind / promtool)

> **Status: executed, awaiting maintainer review; no REQ / milestone is signed off.**
> This document is the execution record of [`2026-10-11-local-infra-bootstrap-plan.md`](2026-10-11-local-infra-bootstrap-plan.md),
> produced per item 6 of §7 of that plan, writing "command / actual output (key lines) / conclusion" for each one. The original plan text is not back-filled.
> Execution environment: the registered environment **`dev-win03ib7niepf0`** (host `WIN-03IB7NIEPF0`, Ubuntu 22.04.5 LTS / WSL2 / x86_64,
> user `shudong`, no root at any point). Execution date: 2026-10-11 (local time zone).
>
> **This record signs off no REQ, no milestone, and no M5 / M8 closure condition**; none of the changes are committed,
> and the maintainer decides how to split and execute the commit.

## 0. Quick conclusion overview

| Item | Result |
|---|---|
| The four tools are in place | ✅ helm 3.16.4 / kubectl 1.31.4 / kind 0.24.0 / promtool 2.55.1, all in `tools/bin/` (gitignored, not committed) |
| `make chart-check` re-run locally | ✅ exit 0, last line `chart-check: OK` |
| `make alert-check` re-run locally | ✅ exit 0, `SUCCESS: 10 rules found` (3 groups / 10 rules, same promtool 2.55.1 version as the historical evidence) |
| kind cluster `as-m5` | ✅ created, context `kind-as-m5` verified OK |
| Cluster-level product verification | ❌ **not done**: `M5_STRICT=1 m5-verify` fails truthfully on the newly created empty cluster (exit=1, no product AS pod); cluster-level verification is not claimed to have passed on that basis |
| Script fix | ✅ the extraction-path bug in `tools/bootstrap-infra.sh` is fixed (see §3), **not committed** |
| Network deviation | the GitHub object egress returned 0 bytes for a long time and dl.k8s.io was rate-limited single-stream to ~20KB/s; kubectl / promtool / kind used fallback acquisition routes; the provenance and verification of each fallback are in §5 / §10 |

## 1. Prerequisite checks (plan §2, all 8 items pass)

| # | What is checked | Command | Actual output (key lines) | Conclusion |
|---|---|---|---|---|
| 1 | docker daemon | `docker info` | `Server Version: 29.2.1` / `Operating System: Ubuntu 22.04.5 LTS`, exit 0 | ✅ the hard gate passes |
| 2 | location of the docker client | `command -v docker` | `/usr/bin/docker` | ✅ |
| 3 | sudo | `sudo -n true 2>/dev/null && echo yes \|\| echo no` | `no` | ✅ root was never used |
| 4 | current user | `id -un` | `shudong` (non-root) | ✅ |
| 5 | CPU architecture | `uname -m` | `x86_64` | ✅ |
| 6 | available disk | `df -h . \| tail -1` | `1007G 95G 861G 10% /` | ✅ (far above 2 GB) |
| 7 | whether it is WSL | `grep -qi microsoft /proc/version && echo WSL \|\| echo native` | `WSL` (kernel `6.18.40.1-microsoft-standard-WSL2`) | ✅ WSL2 is usable |
| 8 | downloader | `command -v curl` | `/usr/bin/curl` | ✅ |

## 2. env-probe before/after comparison

**Before execution** (measured earlier that day by the main agent): docker / uv / python3.10 / make / git are ✅,
helm / kubectl / kind / promtool are ❌ — not found (neither in tools/bin nor on PATH), and not a single item is "⚠ installed but unusable".

**After execution** (a fresh run of `tools/env-probe.sh` when this record was written, exit 0):

```
✅ 具备  docker      /usr/bin/docker                Docker version 29.2.1, build a5c7197
✅ 具备  uv          /home/shudong/.local/bin/uv    uv 0.12.15 (x86_64-unknown-linux-gnu)
✅ 具备  python3.10  /usr/bin/python3.10            Python 3.10.12
✅ 具备  helm        tools/bin/helm                 v3.16.4+g7877b45
✅ 具备  kubectl     tools/bin/kubectl              clientVersion:
✅ 具备  kind        tools/bin/kind                 kind v0.24.0 go1.22.10 linux/amd64
✅ 具备  promtool    tools/bin/promtool             promtool, version 2.55.1 (branch: HEAD, revision: 6d7569…
✅ 具备  make        /usr/bin/make                  GNU Make 4.3
✅ 具备  git         /usr/bin/git                   git version 2.34.1
✅ 具备：docker, uv, python3.10, helm, kubectl, kind, promtool, make, git
❌ 缺失：（无）
⚠ 装了但不可用：（无）
```

Conclusion: the three checks of plan §6.1 are all satisfied (all four present, versions matching `tools/VERSIONS` verbatim, no "installed but unusable").
Note: the `clientVersion:` on the kubectl line is env-probe's display form — it takes the first line of the YAML produced by `version --client=true -o yaml` for kubectl;
the locked version was confirmed by running it directly:

```
tools/bin/kubectl version --client=true
→ Client Version: v1.31.4 / Kustomize Version: v5.4.2
```

## 3. Script bugs found during execution and the fixes (not committed)

**Symptom**: on the first real installation run of `tools/bootstrap-infra.sh`, helm / promtool reported
errors such as `archive did not contain linux-amd64/helm` after extraction, and the installation failed.

**Root cause**: the callers of `install_from_tarball` passed the **inner archive path** as `inner`, while also passing
`--strip-components=1`, so after extraction that path no longer exists and the existence check necessarily failed.

**Fix** (already in the working tree; verifiable via `git diff tools/bootstrap-infra.sh`; `bash -n` passes and the `--dry-run` output is unchanged):

- helm call site: `inner` changed from `"${HOST_OS}-${GOARCH}/helm"` to `"helm"`;
- promtool call site: `inner` changed from `"prometheus-${PROMETHEUS_VERSION}.${PLAT}/promtool"` to `"promtool"`;
- two comment lines added above the `install_from_tarball` definition: `inner` is the path **after strip-components is applied**, relative to the extraction root,
  not the full inner path of the archive.

**Status**: like all documentation changes of this round, this fix is **not committed**; it waits for the maintainer to decide how to split the commit.

## 4. Installation process (tool by tool, with deviations and provenance)

The uniform method follows plan §3: official artifacts are installed into `tools/bin/`, no root. **Installation order helm → kubectl → promtool → kind**;
the previous round was interrupted/aborted once each (see §10), and it was finally closed out with one complete re-run.

### 4.1 helm 3.16.4 — official tarball, the normal path

```
来源：https://get.helm.sh/helm-v3.16.4-linux-amd64.tar.gz（计划 §3.2 原始 URL）
tools/bin/helm version --short → v3.16.4+g7877b45
```

Conclusion: ✅ installed via the planned path, no deviation. `HELM_SHA256` was still empty at the time, so the script emitted the designed "unverified install" warning;
the official sha256 was back-filled into `tools/VERSIONS` during this round for mandatory verification in future.

### 4.2 kubectl 1.31.4 — official URL + parallel segmented download (deviation: transport method, not source)

```
偏差原因：GitHub/Fastly 出口被限速至约 20KB/s，脚本单流下载两次停滞（其中一次导致整轮中断）。
取径：同一官方 URL（https://dl.k8s.io/release/v1.31.4/bin/linux/amd64/kubectl）改用并行分段（HTTP Range）下载。
校验：官方 https://dl.k8s.io/release/v1.31.4/bin/linux/amd64/kubectl.sha256
      = 298e19e9c6c17199011404278f0ff8168a7eca4217edad9097af577023a5620f，与安装文件比对 → 一致（match OK）。
复验（本记录撰写时）：
      sha256sum tools/bin/kubectl
      → 298e19e9c6c17199011404278f0ff8168a7eca4217edad9097af577023a5620f  tools/bin/kubectl（逐字一致）
tools/bin/kubectl version --client=true → Client Version: v1.31.4
```

Conclusion: ✅ the source is the artifact from the official URL and the mandatory comparison against the official sha256 passes; **only the transport method deviates from the script's single-stream implementation**,
and that value has been locked into `KUBECTL_SHA256` in `tools/VERSIONS`.

### 4.3 promtool 2.55.1 — extracted from the official quay.io image (deviation: source carrier)

```
偏差原因：GitHub release tarball 出口当日约 1 小时完全无数据（0 字节），多波重试全部失败。
取径：官方镜像 quay.io/prometheus/prometheus:v2.55.1
      （digest quay.io/prometheus/prometheus@sha256:2659f4c2ebb718e7695cb9b25ffa7d6be64db013daba13e05c875451cf51b0d3）
      经 docker create + docker cp 提取 promtool 二进制。
tools/bin/promtool --version → promtool, version 2.55.1 (branch: HEAD, revision: 6d7569113f1ca814f1e149f74176656540043b8d)
```

Conclusion: ✅ the version matches the locked value 2.55.1 verbatim; **the provenance is the official image (digest as above), not the release tarball**.
The official sha256 of the tarball (`19700bdd42ec31ee162e4079ebda4cd0a44432df4daa637141bdbea4b1cd8927`, taken from the official
sha256sums.txt) has been locked into `tools/VERSIONS` with an explanatory note, for mandatory verification on future tarball installs.
This binary is the **same version** as the 2026-10-05 historical alert evidence, which satisfies the "only the same version is comparable" requirement of plan §3.2.

### 4.4 kind 0.24.0 — built locally from the official tag source (deviation: not a release binary)

```
偏差原因：GitHub release 二进制不可达（同 §4.3 的出口故障）。
取径：go install sigs.k8s.io/kind@v0.24.0（官方 tag 源码），
      GOPROXY=https://goproxy.cn,direct（模块完整性经 sumdb 校验，经代理不放行未校验模块）。
工具链：go1.22.10，其 tarball 来自 mirrors.aliyun.com/golang，
      sha256 = 736ce492a19d756a92719a6121226087ccd91b652ed5caec40ad6dbfb2252092（go1.22.10.linux-amd64.tar.gz 官方值）。
tools/bin/kind version → kind v0.24.0 go1.22.10 linux/amd64
```

Conclusion: ✅ it is a **source build** of the pinned v0.24.0, not a release binary; kind officially **does not publish** a sha256,
so `KIND_SHA256` in `tools/VERSIONS` stays empty with an explanatory note added.

### 4.5 kind node image

```
kindest/node:v1.31.0，1.49GB，自 docker hub 预拉；
digest sha256:25a3504b2b340954595fa7a6ed1575ef2edadf5abd83c0776a4308b64bf47c93（docker images --digests 实录）
```

## 5. Final bootstrap run and verification

After the interrupted intermediate round, one final complete re-run:

```
tools/bootstrap-infra.sh
→ 退出码 0；verify 段四行 OK（helm / kubectl / kind / promtool 全部命中锁定版本）；
  随后自动调用 tools/env-probe.sh，九项 ✅、❌（无）、⚠（无）（见 §2）。
```

`tools/bootstrap-infra.sh --dry-run` was also re-run after the fix: the four URLs print normally, exit 0, nothing is downloaded.

## 6. Delivery quality and cluster-level verification (plan §6.2–§6.4)

| Check | Command | Actual output (key lines) | Conclusion |
|---|---|---|---|
| chart-check | `export PATH="$PWD/tools/bin:$PATH"; make chart-check` | exit 0; last line `chart-check: OK`; `1 chart(s) linted, 0 chart(s) failed`; the two `[INFO] Fail:` lines belong to the expected fail-closed assertion | ✅ plan §6.2 achieved |
| alert-check | `make alert-check` | exit 0; `SUCCESS: 10 rules found` (N=10 > 5, covering as.call-path 5 + as.runtime 3 + as.platform 2) | ✅ plan §6.3 (core of P4) achieved, and with a local promtool 2.55.1 that is the **same version** as the 2026-10-05 evidence |
| kind cluster | `kind create cluster --name as-m5 --wait 120s` | exit 0 (node image see §4.5) | ✅ |
| context | `kubectl config get-contexts -o name \| grep -qx kind-as-m5 && echo "context OK"` | prints `context OK` | ✅ plan §6.4 achieved |

**Cluster-level product verification was not done**: `M5_STRICT=1 bash deploy/kind/m5-verify.sh` returns **exit=1** on the newly created `as-m5` cluster ——
the cluster has only an empty control plane, `No resources found in as-m5 namespace.` (the product AS pod is not deployed), and the jsonpath assertion goes out of range.
This is an **honest failure**, not pass evidence: it confirms plan §7 "having all the tools installed is not the same as cluster-level verification having passed". The cluster was not deleted; it is left for the separately authorized deployment verification.

## 7. Results of running the evidence collection script (deploy/kind/m5-record-artifacts.sh)

```
export PATH="$PWD/tools/bin:$PATH"
bash deploy/kind/m5-record-artifacts.sh
→ 脚本最终退出码 1（因含一项如实 FAIL，见下）；产物落 docs/acceptance/artifacts/m5/2026-10-11/
```

| Collected item | Exit code | Artifact |
|---|---|---|
| gate | 0 | `PASS-gate-2026-10-11.txt` (`1037 passed, 10 skipped, 206 deselected`, **including SKIPPED items**) and `PASS-gate-sample-2026-10-11.txt` |
| chart-check | 0 | `PASS-chart-check-2026-10-11.txt` / `PASS-chart-check-sample-2026-10-11.txt` |
| alert-check | 0 | `PASS-alert-check-2026-10-11.txt` (`SUCCESS: 10 rules found`) / `PASS-alert-check-sample-2026-10-11.txt` |
| m5-strict-context | 0 (context in place) | `FAILCLOSED-m5-strict-context-2026-10-11.txt` — by the design of the collection script it is **always** recorded as FAILCLOSED and is never used as pass evidence |
| m5-verify-strict | **1** | `FAIL-m5-verify-strict-2026-10-11.txt` / `FAIL-m5-verify-strict-sample-2026-10-11.txt` — **an honest failure**, the reason is in §6 |

Artifact triples (the index and how to read them are in [`../acceptance/artifacts/m5/README.md`](../acceptance/artifacts/m5/README.md)):

- `(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-gate-2026-10-11.txt, 2026-10-11)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-chart-check-2026-10-11.txt, 2026-10-11)`
- `(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-2026-10-11.txt, 2026-10-11)`
- `(failed, docs/acceptance/artifacts/m5/2026-10-11/FAIL-m5-verify-strict-2026-10-11.txt, 2026-10-11)`
- `FAILCLOSED-m5-strict-context-2026-10-11.txt` is not pass evidence and is not referenced with a triple.

## 8. Full self-check after the artifacts landed (plan §6.6)

```
uv run pytest tests/ -q   → 94 passed in 0.41s（exit 0）
uv run ruff check .       → All checks passed!（exit 0）
```

The evidence-discipline guard accepted all the new artifacts and documentation changes (the number of guard cases grows with the batches; 76 → 94 is a measured fact from different sessions,
just as the 62 / 68 / 76 in the §7.5 landing note of the register are not contradictory).

## 9. Version pinning written back (plan §7 item 5)

`tools/VERSIONS`: `HELM_SHA256` / `KUBECTL_SHA256` / `PROMETHEUS_SHA256` now hold the official values,
`KIND_SHA256` stays empty (not published officially); the kubectl value was compared verbatim against the actually installed file (§4.2);
the prometheus value is on the release-tarball basis with a note about the image provenance of the local binary; kind carries a note about the source-build basis.
**The version numbers were not changed at all.**

## 10. Deviation summary (against the original acquisition route of plan §3.2)

**Network degradation background (recorded as fact)**: on 2026-10-11 roughly 22:00–23:05+ (local time zone), the GitHub object egress dropped to 0 bytes
(all multi-wave parallel/serial retries failed); docker's daocloud image mirror returned 502 during part of that window;
dl.k8s.io single-stream was rate-limited to about 20KB/s (parallel segmentation worked). **The fallback acquisition route is used only when the official URL is unreachable**;
the provenance and verification of each fallback are as follows:

| Tool | Plan §3.2 route | Actual route | Nature of the deviation | Provenance verification |
|---|---|---|---|---|
| helm | official tarball | official tarball (unchanged) | none | version string `v3.16.4+g7877b45`; the official sha256 has been back-filled, pending verification in future |
| kubectl | official single-stream download | **the same official URL**, parallel segmented transport | transport method only | the official `.sha256` matches the installed file verbatim (§4.2, still consistent when re-verified while this record was written) |
| promtool | GitHub release tarball | extraction from the official quay.io image | source carrier | the image digest has been recorded (§4.3); the official tarball sha256 has been back-filled into `tools/VERSIONS` for mandatory verification in future |
| kind | official release binary | local build from the official tag source | build method | the version string contains `v0.24.0`; the go toolchain tarball sha256 is the official value; modules are verified via sumdb |

Other deviations on the execution side:

- The first bootstrap round was interrupted where the kubectl download stalled, and there was one further aborted intermediate round; the close-out is the final complete re-run (exit 0).
- The `m5-verify-strict` collection that comes with the collection script goes beyond the authorized list of plan §6.2–§6.4; it is pre-existing script behaviour when the "cluster is in place";
  its FAIL result was landed honestly and has been reported (§6 / §7), and no remedial renaming was done.

## 11. Out of scope / not done

- **Not a single byte of `deploy/` was touched** (chart / alerts / kind scripts are all outside the authorized scope).
- **No git write operation was performed**: no `commit` / `add` / `push` / `tag` / branch creation / remote change;
  the fix to `tools/bootstrap-infra.sh` and all documentation changes stay in the working tree, waiting for maintainer review and the commit split.
- **No REQ / milestone was signed off**; the existing closure of P4 (docker-based, 2026-10-11) was not reopened,
  and this time only adds a same-version local re-verification note (see the added correction in register §7.5, awaiting maintainer review).
- The `parl2` background loop during execution was an experimental aid used for troubleshooting during that session; it has been stopped and never entered any file in the repository.
- The kind cluster `as-m5` is **retained and not deleted** (cluster-level deployment verification awaits separate authorization); deletion is an irreversible action and must be confirmed first (plan §8.4).

---

**Landing date: 2026-10-11. Status: executed, awaiting maintainer review.**
(Corresponding plan: [`2026-10-11-local-infra-bootstrap-plan.md`](2026-10-11-local-infra-bootstrap-plan.md);
environment registry: §2 / §2.1 of [`../environments.md`](../environments.md); evidence index:
[`../acceptance/artifacts/m5/README.md`](../acceptance/artifacts/m5/README.md).)
