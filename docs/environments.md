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

# Environments Registry

> **This document is a long-term factual registry, not a session handoff.** It does not expire when a
> session ends, nor is it overwritten by the next working pass — the machines, tools, and produced
> evidence are long-term properties of the repository.
>
> **References to an environment in this document must use the "environment name" from the table; writing an anonymous "this machine" is no longer allowed.**
> Basis and approval record: [`handoff/2026-10-11-open-adjudication-register.md`](handoff/2026-10-11-open-adjudication-register.md) §7.4 layer 2.

## 0. Framing (maintainer position of 2026-10-11, read this first)

> **The project gets deployed on different computers. Environment differences are the norm — not a defect, and not evidence of a defect.**
> Work in this repository spans multiple machines and multiple sessions; if a conclusion only holds on one machine,
> then it must state on which machine it holds — that is precisely why this document exists.

Three hard rules follow:

1. **No document may depend on the capabilities of one particular machine.** When deciding "can the project do X", the only admissible basis is the assets and
   evidence in the repository, not one machine's `PATH`.
2. **"Machine X does not have X" must never be used to infer "the project has no X".** A single machine's tool inventory is **a fact about that machine**,
   not **a project capability**. The 2026-10-05 chart / alert evidence was produced by a machine that had the complete infra toolset but was never
   named; whereas the anonymous tool denial written down on 2026-10-10 was read as "the project has no promtool capability".
   **The cost of this confusion is an entire milestone being re-discussed over and over.**
3. **The environment information in this document is not maintained by hand**; it is **generated on the spot by probing** with
   [`../tools/env-probe.sh`](../tools/env-probe.sh) (see §3). The practice of entering hostnames by hand has been abolished: a hand-made table always drifts,
   and once it has drifted it gets read back in as fact. **There is no need to look up a hostname by hand** — the script probes it itself.

## 1. Why names are mandatory (background, not re-argued here)

The path recorded in the 2026-10-05 M5 evidence files (chart-check / alert-check) is
`==> helm lint /home/shudong/project/3rdparty-as/deploy/helm` — **the same user name, the same project path**;
whereas the workstation actually measured on 2026-10-11 has **no** helm / kubectl / kind / promtool.

⇒ The evidence was produced by **a different machine**, while the anonymous "this machine" in the documentation actually referred to **two different machines**.
This is the direct cause of the question "does the project have infra capability" being argued over and over again: **the carrier of the fact has no metadata**.
Giving environments names is adding metadata to the carrier of the fact.

## 2. Environment registry table

> This table registers **only machines that have actually been measured**. Anything that cannot be filled in gets **no placeholder row** — do not write
> "to be filled in" rows: an empty placeholder is read by the reader as "there is a machine, nobody filled it in", which is worse than not writing it. An unmeasured
> machine enters this table when it first runs [`../tools/env-probe.sh`](../tools/env-probe.sh).

| Environment name | hostname | Tools present | Tools missing | Evidence produced here | Notes |
|---|---|---|---|---|---|
| `dev-win03ib7niepf0` | `WIN-03IB7NIEPF0` | `docker` (`/usr/bin/docker` 29.2.1), `uv` (`/home/shudong/.local/bin/uv` 0.12.15), `python3.10` (`/usr/bin/python3.10` 3.10.12), `helm` (`tools/bin/helm` v3.16.4+g7877b45), `kubectl` (`tools/bin/kubectl` v1.31.4), `kind` (`tools/bin/kind` v0.24.0 go1.22.10), `promtool` (`tools/bin/promtool` 2.55.1), `make` (`/usr/bin/make` 4.3), `git` (`/usr/bin/git` 2.34.1) — the last four were installed into `tools/bin/` by `tools/bootstrap-infra.sh` on 2026-10-11 (not committed to the repo); after bootstrap, all nine items measured ✅ by `tools/env-probe.sh` | (none) — both ❌ missing and ⚠ installed-but-unusable are (none) (measured after the 2026-10-11 bootstrap; previously helm / kubectl / kind / promtool were "not found", see the historical data row in §2.1) | `docs/reviews/product-packaging-execution-record-2026-10-10.md:132` (`preflight.sh --dry-run` behaviour and exit code); the config-service PostgreSQL integration recorded in `docs/plan.md` §0 (2026-10-03, local PG 12.22); `docs/acceptance/artifacts/m5/2026-10-11/` (gate / chart-check / alert-check re-run locally on 2026-10-11, each PASS-, plus FAILCLOSED-m5-strict-context and the honest FAIL FAIL-m5-verify-strict; for collection and interpretation see [`acceptance/artifacts/m5/README.md`](acceptance/artifacts/m5/README.md)) | Current workstation / day-to-day development environment; OS `Ubuntu 22.04.5 LTS`, architecture `x86_64`. `uv` is at `/home/shudong/.local/bin/uv`. **Before the 2026-10-11 bootstrap** it was not possible to run `make chart-check` / `make alert-check` / any kind cluster-level verification (the historical conclusion is retained as an audit chain); **after the 2026-10-11 bootstrap** all three can run locally — chart-check / alert-check were re-run and passed the same day, the kind cluster `as-m5` has been created and the context `kind-as-m5` validates OK; **cluster-level product verification was not done** (m5-verify-strict honestly FAIL). For the tool-installation process and deviations see [`handoff/2026-10-11-local-infra-bootstrap-execution-record.md`](handoff/2026-10-11-local-infra-bootstrap-execution-record.md) |

> **This row was written from an actual 2026-10-11 measurement; afterwards regenerate it with `tools/env-probe.sh` — do not hand-edit this row.**
> This row is the truth value of this round's measurement and was not changed in this round. The execution plan for adding helm / kubectl / kind / promtool is
> [`handoff/2026-10-11-local-infra-bootstrap-plan.md`](handoff/2026-10-11-local-infra-bootstrap-plan.md).
>
> **2026-10-11 addition (re-post):** the "not changed in this round" note above records **the round in which it was first written to disk** — in that round the probe script
> **could not run** (the `tr` call errored), so this row and the §2.1 data row were **written by hand**. After the script was fixed it was actually run locally with
> `bash tools/env-probe.sh --markdown` (exit code 0), and this row has been re-posted from **that real output**.
> The instruction above — "afterwards regenerate with `tools/env-probe.sh`, do not hand-edit this row" — is **unchanged and still in effect**:
> next time the tool inventory changes, re-run the script and paste the whole block; do not hand-edit.

> **2026-10-11 addition (re-posted after the infra bootstrap; the text above is retained as-is, neither deleted nor altered; pending maintainer review):**
> [`handoff/2026-10-11-local-infra-bootstrap-plan.md`](handoff/2026-10-11-local-infra-bootstrap-plan.md) has been executed,
> and the four columns of this row — "tools present / tools missing / evidence produced here / notes" — have been **re-posted in full** from the fresh `tools/env-probe.sh` output after the bootstrap:
> helm / kubectl / kind / promtool changed from "not found" to ✅ present (path `tools/bin/`, not committed to the repo), and the tools-missing column is (none).
> The historical records under "evidence produced here" and "notes" are **retained undeleted, additions only**. The kubectl version v1.31.4 comes from running
> `tools/bin/kubectl version --client=true` directly (`Client Version: v1.31.4`) and from the verification section of `tools/bootstrap-infra.sh`;
> the env-probe basis column shows `clientVersion:` because that is the display form of taking the first line of its `version --client=true -o yaml` (see the note in §2.1),
> not a missing version. Execution record: [`handoff/2026-10-11-local-infra-bootstrap-execution-record.md`](handoff/2026-10-11-local-infra-bootstrap-execution-record.md).

### 2.1 Per-tool measurement matrix (generated by `tools/env-probe.sh --markdown`)

The columns of this table correspond **one-to-one, column by column**, with the `--markdown` output of [`../tools/env-probe.sh`](../tools/env-probe.sh); pasting the whole block works.
The "environment name" column is generated as **`<role>-<hostname lowercased, separators removed>`**, with **default role `dev`** (rule in item 4 of §3).
**No data row is written to disk in this round**: the script is newly created in this round, and this session only writes the script without executing it; the data row must be generated on the spot by the executor and
**must not be hand-filled**.

**2026-10-11 addendum (the preceding paragraph records the state "as of the round in which it was first written to disk"):** after the script was fixed it was actually run locally with
`bash tools/env-probe.sh --markdown` (exit code 0), and the data row below = that real output pasted **as a whole block**, not hand-filled.
Anything the script did not output is left unfilled: in this round all four missing-tool columns were judged "not found" by the script; **not a single cell needed "not probed"**.

| Environment name | hostname | OS | Architecture | docker | uv | python3.10 | helm | kubectl | kind | promtool | make | git |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `dev-win03ib7niepf0` | `WIN-03IB7NIEPF0` | Ubuntu 22.04.5 LTS | x86_64 | ✅ `/usr/bin/docker` Docker version 29.2.1, build a5c7197 | ✅ `/home/shudong/.local/bin/uv` uv 0.12.15 (x86_64-unknown-linux-gnu) | ✅ `/usr/bin/python3.10` Python 3.10.12 | ❌ — not found (neither in tools/bin nor in PATH) | ❌ — not found (neither in tools/bin nor in PATH) | ❌ — not found (neither in tools/bin nor in PATH) | ❌ — not found (neither in tools/bin nor in PATH) | ✅ `/usr/bin/make` GNU Make 4.3 | ✅ `/usr/bin/git` git version 2.34.1 |

**2026-10-11 addendum (after the infra bootstrap; the row above is retained as the pre-bootstrap truth value, neither deleted nor altered; pending maintainer review):**
[`handoff/2026-10-11-local-infra-bootstrap-plan.md`](handoff/2026-10-11-local-infra-bootstrap-plan.md) has been executed,
and the four infra tools were installed into `tools/bin/` (not committed to the repo). The data row below = the post-bootstrap fresh
`bash tools/env-probe.sh --markdown` (exit code 0) output pasted **as a whole block** (header row + separator row + data row), not hand-filled:

| Environment name | hostname | OS | Architecture | docker | uv | python3.10 | helm | kubectl | kind | promtool | make | git |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `dev-win03ib7niepf0` | `WIN-03IB7NIEPF0` | Ubuntu 22.04.5 LTS | x86_64 | ✅ `/usr/bin/docker` Docker version 29.2.1, build a5c7197 | ✅ `/home/shudong/.local/bin/uv` uv 0.12.15 (x86_64-unknown-linux-gnu) | ✅ `/usr/bin/python3.10` Python 3.10.12 | ✅ `/home/shudong/project/3rdparty-as/tools/bin/helm` v3.16.4+g7877b45 | ✅ `/home/shudong/project/3rdparty-as/tools/bin/kubectl` clientVersion: | ✅ `/home/shudong/project/3rdparty-as/tools/bin/kind` kind v0.24.0 go1.22.10 linux/amd64 | ✅ `/home/shudong/project/3rdparty-as/tools/bin/promtool` promtool, version 2.55.1 (branch: HEAD, revision: 6d7569 | ✅ `/usr/bin/make` GNU Make 4.3 | ✅ `/usr/bin/git` git version 2.34.1 |

> **kubectl cell note (`clientVersion:` is the script's raw output, not hand-filled):** env-probe's probe command for kubectl is
> `version --client=true -o yaml`, and the basis column displays the YAML first line `clientVersion:` verbatim; the pinned version
> v1.31.4 is triple-confirmed by running `tools/bin/kubectl version --client=true` directly (`Client Version: v1.31.4`),
> by the verification section of `tools/bootstrap-infra.sh` (exit 0), and by a byte-for-byte match against the official sha256 of the installed file.
> The tail of this round's plain output: ❌ missing: (none); ⚠ installed but unusable: (none).

**How to read the three states (the script distinguishes them as follows; do not conflate them):**

| Marker | Meaning | Criterion |
|---|---|---|
| ✅ Present | The tool resolves **and** its version command succeeds | Has a path + has a version number |
| ❌ Missing | No executable file can be resolved | Absent from both `tools/bin/` and `PATH` |
| ⚠ Installed but unusable | The binary exists but cannot run | The version command exits non-zero, or exits 0 with no output |

> **"Installed but unusable" is a newly identified confusion point in this round**: installed ≠ usable. Counting it as "present" means supporting a
> "verified" conclusion with a binary that cannot even run — the same root cause as "the filename is the conclusion": in both cases the carrier is made to lie.

### 2.2 Evidence not yet attributed (must not be defaulted to any environment)

| Evidence file | Status |
|---|---|
| `docs/acceptance/artifacts/m5/2026-10-05/PASS-gate-2026-10-05.txt` / `PASS-gate-sample-2026-10-05.txt` | Producing environment **not registered**. They were committed in the same batch, but this document only holds path evidence for the chart / alert pair (`helm lint` absolute path); the gate pair has no comparable clue, so no inference is drawn |
| `docs/acceptance/artifacts/m5/2026-10-05/FAILCLOSED-m5-strict-context-2026-10-05.txt` | Producing environment **not registered**; the content is a fail-closed record (`exit=1`), **not passing evidence** |

### 2.3 Items awaiting verification (register the executing environment in this document first)

- **P4's promtool verification**: the two alert-rule groups `as.runtime` / `as.platform` added on 2026-10-10 have still not been verified by any
  registered environment (this requires running `promtool check rules`, **not run in this round**). The executing environment should be registered in this document before execution.

> **2026-10-11 closing-round correction (the original P4 entry above is retained, neither deleted nor altered):** P4 has been verified by the registered environment
> **`dev-win03ib7niepf0`** (host `WIN-03IB7NIEPF0`) **using a containerized (docker) approach** —
> promtool inside the container image `prom/prometheus:v2.45.0` ran `check rules` against `deploy/alerts/as-alerts.yaml`,
> outputting `SUCCESS: 10 rules found` (as.call-path 5 + as.runtime 3 + as.platform 2, 3 groups in total),
> and the main agent independently re-ran the same command on the same host the same day with exit=0.
> Triple: **(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-full-2026-10-11.txt, 2026-10-11)**.
> **Relation to the tool matrix (the two do not contradict each other):** that environment's `PATH` **still contains no local promtool binary**,
> so the promtool cell in the §2 / §2.1 tool matrix **stays at the env-probe measured "❌ — not found"** (the matrix rows are
> generated by `tools/env-probe.sh` and **must not be hand-edited**); the containerized promtool verification does not change the PATH fact — lacking a local binary
> and "being able to run the in-container promtool via docker" both hold at the same time.
> **The remaining pending items are unaffected:** the other objectives of the local tool installation plan
> [`handoff/2026-10-11-local-infra-bootstrap-plan.md`](handoff/2026-10-11-local-infra-bootstrap-plan.md)
> (local helm / kubectl / kind in place, chart-check re-run locally, kind cluster evidence) are **unaffected by P4's closure and
> remain pending execution / pending authorization**.

> **2026-10-11 addition (infra bootstrap round; the P4 docker-closure note above is retained, neither deleted nor altered; pending maintainer review):**
> local promtool **2.55.1** is now in place (`tools/bin/promtool`, **the same version** as the 2026-10-05 historical alert evidence;
> the binary's provenance is extraction from the official image `quay.io/prometheus/prometheus@sha256:2659f4c2ebb718e7695cb9b25ffa7d6be64db013daba13e05c875451cf51b0d3`,
> see the execution record), and `make alert-check` has been re-run locally (environment `dev-win03ib7niepf0`):
> `promtool check rules` → **`SUCCESS: 10 rules found`** (as.call-path 5 + as.runtime 3 + as.platform 2, 3 groups in total).
> Triple: **(verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-2026-10-11.txt, 2026-10-11)**.
> This note **upgrades** the evidence basis for P4 (docker-containerized prometheus v2.45.0 → local promtool 2.55.1, the same version as the historical evidence),
> and **does not change** P4's closure decision itself; the status stays "closed", and this addition is pending maintainer review.
> Execution record: [`handoff/2026-10-11-local-infra-bootstrap-execution-record.md`](handoff/2026-10-11-local-infra-bootstrap-execution-record.md).

## 3. How to add / update a row (no need to look up a hostname by hand)

1. On the target machine, enter the repository root and run:

   ```bash
   tools/env-probe.sh              # human-readable table: the three states at a glance
   tools/env-probe.sh --markdown   # paste straight into the table row in §2.1
   ```

   Both commands are **read-only**: they install nothing, change no system state, require no root, and can be run repeatedly.
   The exit code is still 0 when tools are missing — **missing tools are the norm, not a script failure**.

2. Paste the `--markdown` output **as a whole block** (header row + separator row + data row) into §2.1.
   This table already has a header row and a separator row; keep the column order unchanged when pasting.

3. Update the corresponding row of the §2 registry table in sync. A first-time environment is handled as "**append a row**"; existing rows are not altered.

4. **Naming rule: `<role>-<hostname lowercased, separators removed>`, default role `dev`.**
   `WIN-03IB7NIEPF0` → `dev-win03ib7niepf0`, consistent with the existing row in §2 — maintainer ruling of 2026-10-11:
   **the role goes first as a prefix**. To change the role use `--role` (`tools/env-probe.sh --role infra` → `infra-win03ib7niepf0`);
   to override the environment name entirely use `--name` (`tools/env-probe.sh --name my-env`).
   **The registry is keyed by name, not by generation rule** — renaming equals substituting a different environment and requires maintainer confirmation.

5. **Write missing items truthfully.** If helm is missing, write that helm is missing; "installed but the version command errors" must be recorded as
   ⚠ installed but unusable, never as present. **Never** infer "the project lacks the capability" from one machine missing a tool.

## 4. Citation convention: the status-claim triple

**Whenever writing "verified / unverified", always write it as the triple `(conclusion, evidence file, date)`; a bare sentence is not allowed.**

| | Example | Explanation |
|---|---|---|
| ✅ Positive | `(verified, docs/acceptance/artifacts/m5/2026-10-05/PASS-chart-check-2026-10-05.txt, 2026-10-05)` | Conclusion, evidence file, and date are all present; the reader can open it and check |
| ❌ Counter-example | "chart-check passed" | **Forbidden** — it does not state on which machine it ran, so the reader cannot judge whether the conclusion reproduces in the current environment; this is precisely the root cause of the repeated rework before 2026-10-11 |

Supplementary conventions:

- **Three things that are easily misread** (`FAILCLOSED-` files are not passing evidence; chart-check's `[INFO] Fail:` is an expected assertion;
  `PASS-gate-*.txt` contains SKIPPED items) see
  [`acceptance/artifacts/m5/README.md`](acceptance/artifacts/m5/README.md).
- **`Fail` / `ERROR` wording inside this directory is normal semantics; never judge a file failed on that basis — always go by the file-name prefix.**
- **Project** capabilities beyond machine capability are not adjudicated by this document; for the delivery boundary see
  [`handoff/2026-10-11-open-adjudication-register.md`](handoff/2026-10-11-open-adjudication-register.md) §7.1.

## 5. Security boundary

**This document contains no credentials, tokens, or addresses** (`AGENT.md` §11 / §13): no passwords, certificate private keys, tokens, DSNs,
cookies, and no real IPs / domain names / registry addresses. Tool paths are recorded only to the extent needed to explain capability;
the output of `tools/env-probe.sh` is bound by the same constraint — it prints only tool paths, versions, and machine identifiers, and
**prints no environment variables**. Evidence files are bound by the same constraint; see the last line of `acceptance/artifacts/m5/README.md`.

## 6. Maintenance conventions

- **Environment information is script-generated, not hand-filled** (§0 item 3). The hand-maintained registry has been abolished.
- Adding an environment = **appending a row**; existing rows are not altered, and **a hostname must never be an empty string nor a leftover placeholder**.
  This table has no "to be filled in" rows: if a hostname cannot be written, that means the machine has not been probed yet.
- Tool additions and removals must carry a **measurement date**; "probably present" does not constitute a registry entry.
- Guard: [`../tests/test_evidence_discipline.py`](../tests/test_evidence_discipline.py) enforces that `tools/env-probe.sh` exists and is executable, that no empty-hostname placeholder reappears in this document, and that this document links to that script.
- This table, the evidence grading in [`architecture/README.md`](architecture/README.md), and
  §7.4 of [`handoff/2026-10-11-open-adjudication-register.md`](handoff/2026-10-11-open-adjudication-register.md)
  together constitute the layer-2 mechanism, guarded by the regression test `tests/test_evidence_discipline.py`.

**Written to disk: 2026-10-11. Status: written to disk, pending maintainer review.**
(2026-10-11 change: removed the unfillable infra placeholder row; environment information is now generated by on-the-spot probing with `tools/env-probe.sh`;
added the §0 framing section, the §2.1 per-tool matrix, and the §3 update procedure. The `dev-win03ib7niepf0` row is the measured truth value and was not changed.
Same day: the default naming rule of `tools/env-probe.sh` changed from "role as suffix" to "**role as prefix, default role `dev`**",
consistent with the existing rows; the semantics of `--role` / `--name` are unchanged. Basis: maintainer ruling of 2026-10-11.)
**2026-10-11 third change (re-posted from the real output):** the sentence above stating "the `dev-win03ib7niepf0` row is the measured truth value and was not changed" records
**the round in which it was first written to disk** — in that round the probe script could not run and that row was hand-written. After the script was fixed it was actually run locally with
`bash tools/env-probe.sh --markdown` (exit code 0), and the §2 registry row and the §2.1 matrix data row have been re-posted from that real output
(adding the measured values for the two new columns `make` / `git`, plus OS and architecture; `helm` / `kubectl` / `kind` / `promtool` all confirmed as "not found").
All version numbers come from the script output; not a single cell was hand-filled. §2.1's original "no data row written to disk in this round" statement is retained undeleted as the audit chain requires,
with the subsequent addendum stating the current state. §0 framing, §3 naming rule, §4 triple, §5 security boundary, and §6 maintenance conventions are unchanged.
