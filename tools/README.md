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

# `tools/` — local toolchain & developer-machine bootstrap

`tools/` exists to **make the developer machine ready** to run this repository.
The boundary with [`scripts/`](../scripts/README.md): `scripts/` is repo logic
that goes into git and review; `tools/` is what a machine needs before that
logic can run.

## Contents

| Entry | What it does |
|---|---|
| `VERSIONS` | Single home of pinned infra tool versions (helm 3.16.4 / kubectl 1.31.4 / kind 0.24.0 / prometheus 2.55.1); upgrading = edit this file only, then re-run bootstrap (idempotent) |
| `bootstrap-infra.sh` | Installs the four pinned tools into `bin/` from tarballs — no root, no system state changed; optional sha256 enforcement |
| `env-probe.sh` | Read-only environment probe: fills the environment register from the actual machine instead of hand-typed prose |
| `bin/` | The install **target**, not repo content: `helm`, `kind`, `kubectl`, `promtool` — untracked by git |

`bin/` being untracked is the point: it keeps "content that enters git and
review" (`scripts/`, `VERSIONS`) separate from "local artifacts of this
checkout". `git clean -xfd` removes the binaries along with everything else;
re-running `bootstrap-infra.sh` restores them at the versions pinned in
`VERSIONS`.
