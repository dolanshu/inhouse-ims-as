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

# `scripts/` — repository workflow automation

Everything here is **part of the repository's logic**: automation invoked
directly by the Makefile, the gate, or the release flow. It is tracked in git
and reviewed like source code. The boundary with [`tools/`](../tools/README.md):
`scripts/` makes the **repo** work; `tools/` makes the **machine** ready.

## Contents

| Entry | What it does |
|---|---|
| `check_adr_annotations.py` | REQ-G-3 ADR-annotation scan: non-obvious code must point to its ADR. Run by `make gate-strict`, deliberately outside `make gate` (ADR-0015) |
| `sync-chart-version.sh` | Writes `deploy/helm/Chart.yaml` **from** the root `VERSION` (single source). Default `--check` reports drift without writing; `--apply` writes |
| `d10-req-nf1-harness.sh` | REQ-NF-1 engineering harness (evidence run; not the maintainer D10 sign-off) |
| `lib/repo-toolchain.sh` | Shared shell library for repo scripts |
| `demo-review/` | Pre-M8 demo & review orchestration: story-a…e, bundle publishing, reset between demos (see [`demo-review/README.md`](demo-review/README.md)) |

Rule of thumb: a script that gates, syncs, guards, or produces review evidence
belongs here and gets reviewed. A binary that merely needs to exist on the
developer machine belongs in `tools/bin/` and is not tracked.
