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

# `testbed/` — test instrumentation: the peer world (layer ⑥)

`testbed/` is the **peer world** the product under test faces: simulated network
elements, load generation, probes, contract fixtures, and a deployable
simulation platform. It is an R&D asset and **not a v1 deliverable** (ADR-0014);
testbed results must never be presented as operator IOT or live-network evidence.

## Division of labor vs root `tests/`

`testbed/` provides **environment and instrumentation**; root [`tests/`](../tests/)
holds **assertions and cross-cutting structural guards**. Test layering is
orthogonal to the directory axis: layers are selected by pytest markers
(`unit` / `contract` / `integration` / `e2e` / `performance`), so the directory
answers "where does the instrument live" and the marker answers "which gate runs
it". E2e assertion cases live in root [`tests/e2e/`](../tests/e2e/) since R2612;
nothing in this directory is an e2e assertion case anymore.

## Workspace membership rule

A subdirectory is a uv workspace member **only if it carries its own
`pyproject.toml`** (guard: [`tests/test_workspace_layout.py`](../tests/test_workspace_layout.py)).
Membership governs installability via uv — it is a separate mechanism from pytest
collection. Instrumentation directories without a `pyproject.toml` stay
non-members and are still collected by the root pytest `testpaths`
(`tests, src/platform, src/apps, src/services, testbed` — root `pyproject.toml`
`[tool.pytest.ini_options].testpaths`). `probe/` became member `as-probe`
in R2612 (previously a flat script directory with no `pyproject.toml`).

## Three layers (ADR-0014 evidence)

| Layer | Where | What it answers |
|---|---|---|
| ① Contracts / unit | `contracts/` + each package's `tests/` | the decision is correct, and every implementation is consistent |
| ② Simulated integration | `simulators/` | AS can work against something that behaves like the operator's peer |
| ③ Performance | `load/` | where exactly the capacity boundary lies |

Three rules, quoted verbatim by [`ADR-0014`](../docs/architecture/adr/0014-three-layer-testbed.md)
§Evidence — keep the wording stable so the ADR citation stays checkable:

- **Load testing must go through real sockets.** A harness that drives callbacks
  directly measures business logic, not capacity.
- v1 does not deliver the testbed as a deliverable. **It is an R&D asset;
  customer acceptance testing capability is left to v1.1.**
- SIPp may be used here. It is GPL, for **internal use only, never distributed
  with the product**.

## Two probes, on purpose (ruling Q7=B: keep both)

| Path | What it is |
|---|---|
| [`probe/`](probe/README.md) | **Python baseline probes** — workspace member `as-probe`, `src/as_probe` layout: `e1_baseline_probe`, `sequence_compare`, `tls_hot_rotation_probe` |
| [`simulators/resip-probe/`](simulators/resip-probe/README.md) | **Native probe harness** — reSIProcate C++ binding; the entry point of `make gate-native` and every `m2-native-*` target, all of which call its `scripts/m2-native.sh` |

Both are called probes; only the language and the role differ.

## Members

| Subdirectory | Workspace member | Holds |
|---|---|---|
| `simulators/` | `as-simulators` | Simulated peer NEs |
| `simulators/resip-probe/` | — (native harness) | reSIProcate C++ probe, vendored source, build scripts |
| `load/` | `as-load` | Real-socket load generator |
| `probe/` | `as-probe` | Python baseline probes (member since R2612) |
| `contracts/` | — | Declarative contract fixtures: `decision/`, `sip-baseline/` (pure data) |
| `sim-platform/` | — | Deployable simulation platform (see below) |

## Why `sim-platform/` is here and not in `deploy/`

`sim-platform/` simulates the **customer environment and the peer platform** —
it carries its own Helm chart, kind tooling, and product-bundle values. It is
part of the **world under test**, not a deliverable; its chart sitting parallel
to [`deploy/helm/`](../deploy/helm/) is deliberate (the product chart vs the
simulated target environment). It must never ship to a customer.
