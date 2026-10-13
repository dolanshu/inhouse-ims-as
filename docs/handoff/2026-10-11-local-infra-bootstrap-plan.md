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

# Execution plan: local installation of infra (helm / kubectl / kind / promtool)

> **Landing date: 2026-10-11. Status: landed, awaiting maintainer review. This plan has not been executed.**
>
> **This document is a plan for the next session to execute, not an execution record.** It depends on no conversation context:
> just follow §2 onwards. After execution, write a separate execution record; do not back-fill execution results into "already done" in this document.

## 0. Why this is being done

The measured conclusion of 2026-10-11: this machine (`WIN-03IB7NIEPF0`) has `docker` / `uv` / `python3.10`,
and **does not have** `helm` / `kubectl` / `kind` / `promtool`. Therefore this machine **cannot** run
`make chart-check`, `make alert-check`, nor any kind cluster-level verification.

Yet the chart / alert evidence of 2026-10-05 was produced by **another machine** (the evidence records
`==> helm lint /home/shudong/project/3rdparty-as/deploy/helm`, the same user name and the same project path);
that machine has all four of the above tools, **but its identity is still unknown and cannot be back-filled**.

The consequence is not "a few missing tools" but two things:

1. **`deploy/alerts/` is part of the delivery product** (the decision line in §2 of [`../architecture/README.md`](../architecture/README.md)),
   and its two new rule groups, `as.runtime` / `as.platform`, **have still never been validated by any machine with promtool**
   (P4 in register §7.5). Delivery quality validation is left hanging, with nowhere for the responsibility to land.
2. "Does this project actually have infra capability" is repeatedly re-litigated. The root cause has been adjudicated as **the carrier of fact having no metadata**
   (register §7.4); this plan is one of the landing actions of that conclusion.

## 1. Goal and scope

### 1.1 Goal

Have `helm` / `kubectl` / `kind` / `promtool` **on this machine**, so that the following verifications can run locally:

| Goal | Current state | Basis for the verdict after it is achieved |
|---|---|---|
| `make chart-check` | cannot run locally | last line `chart-check: OK` |
| `make alert-check` | cannot run locally | last line `SUCCESS: N rules found` (N covers the two new groups) |
| kind cluster-level verification (`make m5-cluster-evidence` etc.) | cannot run locally | the cluster comes up and the script exits 0 |

### 1.2 Scope boundary (read this first, it saves a lot of rework)

- **kind / testbed is scaffolding and must not be used in customer production.** The decision line is in
  §2 of [`../architecture/README.md`](../architecture/README.md); the existing landing is in
  [`../delivery/install-guide.md`](../delivery/install-guide.md) `:19`, `:91`.
  The kind cluster installed by this plan is only for **our own** verification; the transcripts it produces are evidence class ②
  (a basis for external performance, **not** a customer acceptance item).
- This plan **changes no deliverable**: not a single byte of `deploy/helm/` or `deploy/alerts/` is touched.
  It only installs tools on **this machine**.
- This plan **does not solve** "who was the machine of 2026-10-05". That has been adjudicated as **not back-fillable** (see §8.5).

## 2. Step 0: prerequisite checks (run before installing anything)

> **Finish this section before installing anything.** Item 1 in it is the hard gate.

| # | What is checked | Command | Expected output | If not satisfied |
|---|---|---|---|---|
| 1 | **is the docker daemon really running** | `docker info` | prints the Server section (`Containers:` / `Server Version:` etc.), exit 0 | **this plan stops here** (see the hard gate below) |
| 2 | location of the docker client | `command -v docker` | `/usr/bin/docker` (known on this machine) | resolve docker itself first; unrelated to this plan |
| 3 | whether sudo is available | `sudo -n true 2>/dev/null && echo yes \|\| echo no` | either `yes` or `no` is fine | this plan **never needs root**; `no` does not block execution |
| 4 | current user | `id -un` | non-root is better | it also runs as root, but please execute as a normal user instead |
| 5 | CPU architecture | `uname -m` | `x86_64` or `aarch64` | other architectures need a manual install; `bootstrap-infra.sh` errors out explicitly |
| 6 | available disk | `df -h . \| tail -1` | at least 2 GB available | clean up and retry; kind pulling images consumes another 1–2 GB |
| 7 | whether it is WSL | `grep -qi microsoft /proc/version && echo WSL \|\| echo native` | `native` or `WSL` | WSL2 can use kind (needs systemd or starting dockerd manually); WSL1 **cannot**, stop |
| 8 | downloader | `command -v curl \|\| command -v wget` | at least one exists | if neither exists, stop and resolve that first |

### Hard gate (written into the original text, must not be bypassed)

> **If `docker info` does not work (daemon not started / not installed / no permission), kind cannot be installed at all, and this plan stops here.**
>
> This is not an "install it first and see" situation: creating a kind cluster depends precisely on the docker daemon. When the daemon does not work, an installed
> kind is just a binary that cannot run, which creates the illusion of "the tools are present" — exactly the kind of confusion this round is meant to eliminate.
>
> In that case there is **one** thing that is **allowed**: install helm / kubectl / promtool (they are independent of docker),
> write in the execution record that "kind was not installed because the docker daemon was unavailable", and **not** register this machine
> as having kind in any document.

## 3. Installation list

**Uniform method: unpack the official tarball / single file into `tools/bin/`, no root needed, same lifecycle as the repository.**

### 3.1 Why apt is not the first choice

| Reason | Explanation |
|---|---|
| root is required | no step of this project should depend on sudo; a root step becomes a "will anyone remember next time" hazard |
| the version is uncontrolled | apt gives whatever version the distribution packaged at the time, and nowhere in the repository is it recorded which version that was ⇒ the same alert rules are validated by two different promtools on two machines with different conclusions, which is not reproducible after the fact |
| lifecycle mismatch | distribution packages live outside the checkout, cannot be removed by `git clean -xfd`, and do not show up in `git status`; tools that live and die with the repository is the form this project wants |
| the supply chain is invisible | a tarball has an official sha256 that can be written into `tools/VERSIONS` for mandatory verification; the origin of an apt package is invisible to this document |

**apt is not wrong, it just should not be the default.** If the maintainer later adjudicates in favour of apt, the version-pinning strategy of §5 of this plan must be rewritten accordingly.

### 3.2 List

| Tool | Suggested version | Official source | Install location | Verification command | Expected |
|---|---|---|---|---|---|
| `helm` | `3.16.4` | `https://get.helm.sh/helm-v3.16.4-linux-amd64.tar.gz` | `tools/bin/helm` | `tools/bin/helm version --short` | `v3.16.4+…` |
| `kubectl` | `1.31.4` | `https://dl.k8s.io/release/v1.31.4/bin/linux/amd64/kubectl` | `tools/bin/kubectl` | `tools/bin/kubectl version --client=true` | `Client Version: v1.31.4` |
| `kind` | `0.24.0` | `https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64` | `tools/bin/kind` | `tools/bin/kind version` | `kind v0.24.0 … linux/amd64` |
| `promtool` | `2.55.1` (taken from the prometheus tarball) | `https://github.com/prometheus/prometheus/releases/download/v2.55.1/prometheus-2.55.1.linux-amd64.tar.gz` | `tools/bin/promtool` | `tools/bin/promtool --version` | `promtool, version 2.55.1` |

Basis for the version choices:

- **helm 3.16.4** — the chart is `apiVersion: v2` and needs Helm 3.x
  (item 2 of the prerequisites in [`../delivery/install-guide.md`](../delivery/install-guide.md)).
- **kubectl 1.31.4 + kind 0.24.0** — the two go together: the default node image of kind v0.24.0 is
  `kindest/node:v1.31.0`, the allowed version skew between kubectl and the cluster is ±1 minor, and picking the same minor is least effort.
  `deploy/kind/m5-kind-up.sh` does **not** pin the node image, so the kind version is the source of the node version.
- **promtool 2.55.1** — **deliberately unchanged**. The historical `/tmp` fallback path in `deploy/kind/m5-record-artifacts.sh`
  uses exactly 2.55.1; evidence validated by the same version of promtool is semantically comparable.

> Before executing, check the version numbers in the table above against the official release pages. The URLs in `tools/bootstrap-infra.sh` are assembled from
> `tools/VERSIONS` + `uname` and **do not check online whether a version exists**; a wrong version number shows up as a 404 on download.

### 3.3 kustomize is not installed (the judgement and the reason)

This repository has **no kustomize dependency**:

- chart rendering goes through `helm template` (`deploy/helm/scripts/chart-check.sh`, `make chart-check`);
- there is no `kustomization.yaml` under `deploy/`;
- the kind manifests are plain YAML (`deploy/kind/manifests/`).

Therefore **kustomize is not listed in this plan**. If it is introduced later: add one line to `tools/VERSIONS`,
and add one branch each to `url_for` / `pinned_for` / `checksum_for` in `tools/bootstrap-infra.sh`.

## 4. Script design

Two scripts have been landed in this round (**none of them was executed in this session**, see §6.0):

| Script | Responsibility | Invocation |
|---|---|---|
| [`../../tools/env-probe.sh`](../../tools/env-probe.sh) | **read-only** probing: hostname / OS / architecture + docker / uv / python3.10 / helm / kubectl / kind / promtool / make / git, distinguishing the three states "present / missing / **installed but unusable**" | `tools/env-probe.sh`, `--markdown`, `--json`, `--name`, `--role` |
| [`../../tools/bootstrap-infra.sh`](../../tools/bootstrap-infra.sh) | installs the four tools into `tools/bin/`: **no root, idempotent, supports `--dry-run`, automatically calls `env-probe.sh` after installing to verify** | `tools/bootstrap-infra.sh [--dry-run] [--only <tool>] [--force]` |

Auxiliary file: [`../../tools/VERSIONS`](../../tools/VERSIONS) (the single storage place for versions, see §5).
`tools/bin/` is already in `.gitignore`: **binaries are not committed**.

### 4.1 Design constraints (written in stone, changes need maintainer confirmation)

1. **No root.** Any path requiring root must **error explicitly**; a script must never quietly `sudo` internally.
   When the directory is not writable, report "fix the permissions or set `TOOLS_BIN=<writable directory>`" and exit.
2. **Idempotent.** Already at the locked version ⇒ skip; only `--force` reinstalls. After a mid-way failure, just re-run.
3. **Do not write outside the repository.** Only `tools/bin/` and `$TMPDIR` are written.
4. **A missing tool is not a failure.** `env-probe.sh` still exits 0 when any tool is missing — missing tools are the normal case.
5. **Do not print credentials.** Neither script prints environment variables, tokens or internal addresses (`AGENT.md` §11 / §13).

### 4.2 Execution order (the actual operation for the next session)

```bash
# 0) 前置核查（§2），尤其 docker info
docker info >/dev/null && echo "docker OK"

# 1) 只读探测，先看清现状（安全，可反复跑）
tools/env-probe.sh

# 2) 看安装计划，不下载任何东西
tools/bootstrap-infra.sh --dry-run

# 3) 真正安装（幂等；需要外网）
tools/bootstrap-infra.sh

# 4) 让 make 找得到 promtool / helm（当前 shell 生效）
export PATH="$PWD/tools/bin:$PATH"

# 5) 复验：三态应当全部变成「✅ 具备」
tools/env-probe.sh
```

## 5. Version-pinning strategy

### 5.1 One storage place

All versions live in [`../../tools/VERSIONS`](../../tools/VERSIONS), in the format `TOOL_VERSION=x.y.z`,
optionally with `TOOL_SHA256=` appended (if left empty, only a warning is printed and installation is not blocked). **Upgrading = changing only this one file**;
the scripts themselves do not hard-code version numbers.

### 5.2 Upgrade procedure

```bash
vim tools/VERSIONS                  # 改版本号，并顺手填上官方 sha256
tools/bootstrap-infra.sh --dry-run   # 确认 URL 变了
tools/bootstrap-infra.sh             # 幂等重跑，只更新变化的那几个
```

### 5.3 Relationship with the version numbers already hard-coded in the repository

| Location | What is hard-coded | How this plan handles it |
|---|---|---|
| `deploy/kind/m5-record-artifacts.sh` | `/tmp/prometheus-2.55.1.linux-amd64/promtool` as the **last fallback** | **kept** (the historical path is not deleted); the lookup order is changed to ① `tools/bin/promtool` → ② `PATH` → ③ the old `/tmp` path. When none of the three is present, `alert-check` writes a `FAIL-` artifact stating that promtool is unavailable, and does **not** skip silently |
| `Makefile:59` (`alert-check`) | bare `promtool` | **unchanged**. Satisfy it after installing with `export PATH="$PWD/tools/bin:$PATH"` |
| `deploy/kind/m5-kind-up.sh` | node image not pinned | **unchanged**. The node version follows the kind version (§3.2) |
| `deploy/kind/m5-ingress-evidence.sh:30` | the ingress-nginx manifest follows the `main` branch | unrelated to this plan; it belongs to another reproducibility problem, **not handled this time** |

**Constraint**: once `PROMETHEUS_VERSION` diverges from the 2.55.1 of the old `/tmp` path,
the comments in `tools/VERSIONS` must state "from X onwards the promtool version no longer shares a source with the historical evidence; the old evidence cannot be compared directly".

## 6. Verification steps (falsifiable)

> **Without evidence produced, the installation is not done.** Every item must give a checkable artifact path.

### 6.0 Known state before execution (must not be treated as verified)

This session **only wrote the scripts and executed none of them** (constrained globally: shell scripts are not executed apart from the `bash -n` syntax check).
Therefore the two commands below **have not been verified yet**, and the next session must run them first:

```bash
tools/env-probe.sh                  # 期望：docker/uv/python3.10 为 ✅，helm/kubectl/kind/promtool 为 ❌
tools/bootstrap-infra.sh --dry-run   # 期望：四条 url 打印出来，exit 0，不下载任何东西
```

If either errors out, **fix the script first, then install the tools**; do not work around it.

### 6.1 Tools in place

| Check | Command | Expected |
|---|---|---|
| all four present | `tools/env-probe.sh` | the helm / kubectl / kind / promtool lines are all `✅ 具备` |
| versions correct | `tools/env-probe.sh` | the version numbers match `tools/VERSIONS` verbatim |
| no "installed but unusable" | same | the "installed but unusable" column is (none) |

### 6.2 chart-check (delivery product quality evidence)

```bash
export PATH="$PWD/tools/bin:$PATH"
make chart-check
```

- Expected: exit 0, last line `chart-check: OK`, containing `1 chart(s) linted, 0 chart(s) failed`.
- `[INFO] Fail:` lines are an **expected assertion** (the fail-closed rendering guard) and do not indicate a failure.
- Artifacts: `docs/acceptance/artifacts/m5/<date>/PASS-chart-check-<date>.txt`
  and `PASS-chart-check-sample-<date>.txt`.
- **Naming is the script's responsibility**: running `bash deploy/kind/m5-record-artifacts.sh` directly routes automatically by exit code into
  `PASS-` / `FAIL-` and writes the real exit code; the price is that it first runs `make gate` (slow).
  When only the chart / alert evidence is wanted, the commands in this section and §6.3 can be run manually and landed under the file names above.

### 6.3 alert-check (**P4: the core goal of this round**)

```bash
make alert-check
```

- Expected: exit 0, last line `SUCCESS: N rules found`, and **N must be greater than 5** —
  `as.runtime` / `as.platform` were added on 2026-10-10, and the original 5 rules are unchanged.
  **`N == 5` means this validation did not reach the new groups, which is not enough to close out P4.**
- Artifacts: `PASS-alert-check-<date>.txt` / `PASS-alert-check-sample-<date>.txt`.
- The record must be written as a triple: `(verified, docs/acceptance/artifacts/m5/<date>/PASS-alert-check-<date>.txt, <date>)`.

### 6.4 kind cluster-level verification (**scaffolding, not a customer acceptance item**)

Prerequisite: `docker info` passes (item 1 of §2).

```bash
export PATH="$PWD/tools/bin:$PATH"
kind create cluster --name as-m5 --wait 120s
kubectl config get-contexts -o name | grep -qx kind-as-m5 && echo "context OK"
```

- Expected: prints `context OK`.
- **Pulling images requires external network access**; in an offline environment kind will inevitably fail, so do not retry repeatedly (see §8.2).
- If the artifacts land in `docs/acceptance/**` or in a handoff record, they are evidence class ②
  ([`../architecture/README.md`](../architecture/README.md) §3): **a basis for external performance, not a customer acceptance item**.

### 6.5 Mandatory naming convention for artifacts

All evidence under `docs/acceptance/artifacts/**` is landed as **the file name is the conclusion**, guarded by
[`../../tests/test_evidence_discipline.py`](../../tests/test_evidence_discipline.py):

| Prefix | Meaning | Is it pass evidence? |
|---|---|---|
| `PASS-` | the command exited 0 | yes |
| `FAIL-` | the command ran but exited non-zero | **no** |
| `FAILCLOSED-` | an explicit refusal rather than a guess | **no** |

Format `<conclusion>-<item-under-test>[-sample]-<YYYY-MM-DD>.txt`.
A failing run **must not** be written as `PASS-`; the guard rejects such a file name.

### 6.6 Full self-check

```bash
uv run pytest tests/ -q        # 证据纪律 + 工作区布局守卫
uv run ruff check .
```

Expected: all green. If `tests/` is red, it is most likely an artifact-naming violation (§6.5); **do not change the tests to accommodate the artifacts**.

## 7. Close-out write-back checklist

After the installation, the following locations **must** be updated in sync (missing one means the work is not done):

| # | Location | What to change |
|---|---|---|
| 1 | §2.1 of [`../environments.md`](../environments.md) | run `tools/env-probe.sh --markdown` and paste in the data rows of the per-tool matrix |
| 2 | §2 of [`../environments.md`](../environments.md) | remove the four now-complete items from the "missing tools" column; **keep the `WIN-03IB7NIEPF0` row as the truth** |
| 3 | §2.3 of [`../environments.md`](../environments.md) | tick off "P4 pending validation" and **note the name of the environment used for the validation** |
| 4 | register §7.5 and §0 of [`../plan.md`](../plan.md) | **update the P4 status**: state that `as.runtime` / `as.platform` has been validated by promtool 2.55.1, with the triple `(conclusion, evidence file, date)` |
| 5 | [`../../tools/VERSIONS`](../../tools/VERSIONS) | fill in the official sha256 of the four tools (if not filled in, it must be listed as a to-do in the execution record) |
| 6 | create a new execution record | `docs/handoff/<date>-local-infra-bootstrap-execution-record.md`, writing "command / actual output / conclusion" for each item |

> **Every review record is marked "awaiting maintainer review"; it must not be signed off on its own.**
> This plan **signs off** no REQ, no milestone, and no M5 / M8 closure condition.
> Having all the tools installed **is not the same as** "cluster-level verification has passed" — the latter needs its own evidence.

> The environment name is generated by the default rule **`<role>-<hostname lowercased, separators removed>`**, with the **default role `dev`**:
> `WIN-03IB7NIEPF0` → `dev-win03ib7niepf0`, consistent with the existing rows of the registry (maintainer adjudication of 2026-10-11: the role goes first).
> To change the prefix use `tools/env-probe.sh --role infra`; to override completely use `--name`.
> The **registry is authoritative** for the environment name: renaming means changing environments, which requires maintainer confirmation.

## 8. Risks and rollback

### 8.1 What to do when a step fails

| Failure point | Symptom | Handling |
|---|---|---|
| download failure | `download failed` | check external network / proxy; `bootstrap-infra.sh` can be re-run and already-installed tools are skipped automatically |
| checksum mismatch | `checksum mismatch` | **stop immediately**. Do not bypass with `--force`. Check the official release page; if it still mismatches, report it, and **do not** edit `tools/VERSIONS` to make it fit |
| `promtool` exists but cannot report its version | the probe shows "installed but unusable" | usually a wrong extraction level; `rm -f tools/bin/promtool` then reinstall with `--only promtool` |
| `make chart-check` still cannot find helm | PATH is not in effect | `export PATH="$PWD/tools/bin:$PATH"`. If a permanent effect is needed (writing shell config), **ask the maintainer first** — changing the user environment is outside this plan |
| kind cluster creation times out | `--wait 120s` times out | usually the image cannot be pulled (network). See §8.2. **Do not** retry repeatedly |

### 8.2 Network prerequisite for pulling docker images

`kind create cluster` needs to pull `kindest/node:v1.31.0` (about 1 GB) from the public network.
**Without external network access or under restrictions kind will inevitably fail**, and the failure message is usually a timeout, which is easily misread as "kind is broken".
When this happens: write in the execution record that "kind was not validated because the image was unreachable"; **do not** write "kind is unavailable".
helm / kubectl / promtool are independent of the image and remain usable.

### 8.3 Rolling back a single tool

```bash
rm -f tools/bin/kind && tools/bootstrap-infra.sh --only kind
```

Rollback = deleting one file + an idempotent reinstall: no root needed, no effect on other tools, no git change of any kind.
Full rollback: `rm -rf tools/bin` (that directory is in `.gitignore`, and deleting it produces no git change).

### 8.4 Which actions are irreversible

| Action | Reversibility |
|---|---|
| `rm -rf tools/bin` | **reversible** (just reinstall) |
| changing the version number in `tools/VERSIONS` | reversible, but **the evidence already produced loses comparability** — the evidence records the version at the time. Think it through before changing the version |
| `kind delete cluster --name as-m5` | **irreversible**: all runtime data in the cluster disappears. This plan does not delete the cluster; confirm first if it is to be deleted |
| the images pulled by `kind create cluster` | occupy disk (1–2 GB); deleting the cluster does not necessarily reclaim the images |
| modifying any file under `deploy/` | **outside this plan's authorization** (see §9) |

### 8.5 Items that cannot be rolled back / cannot be resolved

- **The identity of the machine of 2026-10-05**: adjudicated as **not back-fillable** (maintainer, 2026-10-11).
  Do not guess a hostname to fill it in "so the registry looks better" — that is exactly the recurrence of empty placeholder back-filling that this round forbids.
  The attribution of that batch of evidence stays "unregistered", see §2.2 of [`../environments.md`](../environments.md).

## 9. Stop line

**This plan authorizes none of the following. If execution finds that one of them must be crossed, stop and report to the maintainer:**

| Not authorized | Explanation |
|---|---|
| `git push` / `git tag` / creating a branch / changing remote | never done without the maintainer's explicit approval in **that conversation** |
| changing the root `VERSION` or `deploy/helm/Chart.yaml` | the version framing (G4/A6) is still awaiting adjudication |
| treating kind cluster evidence as a **customer acceptance item** | M5 "control plane cluster deployment proof" has been adjudicated as **a basis for external performance, not a customer acceptance item** (register §7.3) |
| signing off any REQ / milestone | always mark "awaiting maintainer review" |
| changing `deploy/alerts/` to make promtool pass | if an alert rule fails validation, that is a **defect to be fixed**, not a rule to be changed |
| using `sudo` to work around a permission problem | the script errors out explicitly; sudo that bypasses the script renders this plan's "no root" promise void |
| relaxing the guard tests to "make the gate green" | a red guard means the artifact or environment is non-compliant; fix the artifact/environment, do not change the guard |

**On encountering any of the following situations, stop immediately and write in the execution record "stopped + the reason + who must adjudicate":**
it is necessary to cross the stop line, root is needed, a deliverable has to be changed, or the plan is found not to match the actual state of the repository.

---

**This plan has executed no installation action**: this session did not run `tools/env-probe.sh`, did not run
`tools/bootstrap-infra.sh`, did not download any tarball, did not create any kind cluster, and did not execute any `make` target.
**Landing date: 2026-10-11. Status: landed, awaiting maintainer review.**
