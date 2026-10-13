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

# ADR-0001: Single monorepo + uv workspace

- **Status**: accepted
- **Date**: 2026-09-28
- **Decides**: §0 decision 3 — repository organization: single monorepo + uv workspace
- **Responds to REQ**: REQ-NF-12, REQ-G-2

---

## Context

The product's predecessor was two repositories: `3rtparty_AS_POC` and
`as_platform`. Their physical separation exposed three hard defects during the
POC phase:

1. **Every build job had to `git clone ../as_platform`.** Any cross-repo
   reference relied on the sibling repo happening to exist at the same relative
   path on the build machine, so the checkout had to happen twice every time.
   Build context, test parallelization, and cache hit rates all suffered for it.
2. **`deploy/Dockerfile.as` failed because the build context was outside the
   repo.** The Docker build context is confined to a single repo directory, so
   `COPY ../as_platform` is unavailable under a standard build environment. The
   build script had to manually merge the two repos into a temporary directory —
   an extra, fragile layer of glue.
3. **Version drift had already occurred.** The root `VERSION` file read `0.2.0`,
   while each component's own `pyproject.toml` said `0.1.0` — two numbers in two
   places, and no automated guard prevented the drift (see ADR-0018).

Every component of this product (the kernel `platform/`, the use cases
`apps/translation` / `apps/anti-fraud`, the control plane
`services/config-service` / `services/console`, and the test platform
`testbed/`) is implemented in Python. `uv`, a modern Python package manager,
natively supports the workspace concept: a top-level `pyproject.toml` declares
`[tool.uv.workspace]`, all members share the same toolchain configuration (lint,
format, type check), each member is published independently but constrained by a
unified structure guard.

The layering rule (`AGENT.md` §4) states clearly that the **kernel must never
import applications, services, or testbed**. But in a monorepo any import
resolves successfully — the repository boundary is no longer a line of defense,
so the defense must move into tests.

## Decision

Adopt **single repo + uv workspace** as the repository organization for this
product. All components belong to one workspace:

```
as-product/                       # single repo · uv workspace
├── platform/                     # kernel library (formerly as_platform, merged in)
├── apps/
│   ├── translation/              # number-translation AS (formerly as_app)
│   ├── anti-fraud/               # anti-fraud AS (formerly anti_fraud_as)
│   └── <future>/
├── services/
│   ├── config-service/           # rule version store + change order + distribution
│   └── console/                  # ops console
├── testbed/
├── deploy/
├── docs/architecture/adr/
└── AGENT.md
```

"Do not take a reverse dependency" is **guaranteed not by the repo boundary but
by tests**. `platform/tests/test_library_independence.py` uses an AST scan of
`APPLICATION_PACKAGES`; after moving into the monorepo it keeps running and
extends the guard scope to `services/`, `testbed/`. The structure itself is
guarded by `tests/test_workspace_layout.py`.

## Consequences

### Positive

- **Eliminates the three POC defects in one move**: sibling-repo checkout is no
  longer needed; the Docker build context is entirely within a single repo; the
  version-drift problem is solved by ADR-0018's root `VERSION` + `pyproject`
  interface-version governance.
- **Unified toolchain configuration for the workspace**: the top-level
  `pyproject.toml` declares `[tool.ruff]`, `[tool.mypy]`, and similar toolchain
  config centrally; each member only references it, so "same project, different
  lint rules per member" cannot happen.
- **Each component's version is independent but under unified guard**: the
  interface version in `pyproject.toml` is declared autonomously by each
  component; the root `VERSION` is the single source of product release, and the
  SemVer validity of the two is auto-checked by
  `tests/test_version_consistency.py`.
- **Simplified build / delivery**: no sibling-repo checkout is needed; `uv sync`
  pulls all dependencies in one go. Cache hit rate improves.

### Negative / accepted

- **Monorepo volume grows**: all components, testbed simulators, load-test
  harnesses, and contract use-case sets live in one repo. `AGENT.md` §4's
  layering rule and `test_library_independence.py`'s AST guard prevent mutual
  contamination.
- **"No reverse dependency" moves from a compile-time guard to a test guard**:
  under the multi-repo model, the kernel referencing application code would error
  at import time; under the monorepo any import resolves, so the guard degrades
  to pytest (gate tier ①). Accepted, because the AST-scan test blocks the PR at
  the first tier of `make gate`.

## Alternatives considered

| Option | Why not |
|---|---|
| Keep multiple repos as-is | Already proven to fail in the POC: every build must clone the sibling repo; the Docker build context cannot cross repos; version drift has no automated guard |
| JS-ecosystem Python substitutes like lerna / nx (pants / buck) | Adds toolchain complexity; uv workspace native support is sufficient for this repo's needs |

## Evidence

- `tests/test_workspace_layout.py` is implemented and passing; it checks the
  workspace member list, member path format, and presence of the top-level
  `pyproject.toml`.
- `platform/tests/test_library_independence.py` is implemented and passing; it
  uses AST scanning to verify the kernel does not reference `apps/`,
  `services/`, `testbed/`.
- `uv sync` resolves the workspace successfully in this repo, with correct
  inter-member dependency relationships.

## Related

- [`../system-architecture.md`](../system-architecture.md) §11.1 monorepo structure
- [`../../plan.md`](../../plan.md) §2.1 directory structure
- [`../../AGENT.md`](../../AGENT.md) §4 layering rules
- [ADR-0018](0018-release-versioning.md) unified product release version governance
