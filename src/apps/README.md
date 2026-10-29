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

# `apps/` — signaling-plane business use cases (layer ①)

`apps/` holds the **IMS business use cases** this Application Server exists to
host. In the IMS sense an "Application Server" carries subscriber services; here
that means one directory per use case.

**Not the web meaning of "app".** In a web monorepo `apps/` means "independently
deployable applications". Here an app has no process entry point of its own. Per
[ADR-0002](../docs/architecture/adr/0002-per-usecase-process-state-redis.md):
one use case = one process = one K8s Deployment, and the process shell is
provided by the kernel (`src/platform/src/as_platform/__main__.py`) — the app is
loaded as a business module, and its decisions enter the engine through the
`decide()` pure-function seam (no socket, no clock, no global state). The target
form is one Deployment / one fault domain / one canary unit / one independent
scale unit per use case; the current Helm chart still renders a single AS
Deployment, so this remains the ADR-0002 target shape, not today's topology.

**Stateless.** Session, rate-window, and reputation state live in Redis through
the `StateStore` seam; a pod can be killed at any time. One app must never
import another app.

## Dependency direction (gate-locked)

```
apps/ ──uses──▶ platform/     (platform never imports apps)
```

In a monorepo any import resolves, so the direction is asserted by
[`src/platform/tests/test_library_independence.py`](../platform/tests/test_library_independence.py)
and [`tests/test_layer_boundaries.py`](../tests/test_layer_boundaries.py).

## Not `services/`

The two directory names are deliberately distinct in kind:

| Directory | Plane | Meaning |
|---|---|---|
| `apps/` | Signaling | IMS business use cases, one process per use case (ADR-0002) |
| `services/` | Control | Long-running control-plane processes: `console/`, `config-service/` |

## Members

Both are uv workspace members with the standard `src/` + `tests/` layout:

| Directory | Package | Use case |
|---|---|---|
| [`translation/`](translation/README.md) | `as-translation` | Number translation & routing (two-leg B2BUA) |
| [`anti-fraud/`](anti-fraud/README.md) | `as-anti-fraud` | Caller screening — single leg, `608 Rejected` (RFC 8688) |
