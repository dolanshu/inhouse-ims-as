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

# M2b Boundary Seam Review Record

> Review object: `platform/src/as_platform/sip/` (`__init__.py`, `transport.py`, `adapter.py`) and `platform/tests/test_transport_seam.py`, `test_sip_adapter_seam.py`
> Review date: 2026-09-28
> Reviewer: AI agent (actually ran the gate + cross-checked ADR-0016, ADR-0019, AGENT.md §13)
> Review verdict: **pass** — the boundary seam is landed, with no stack implementation; the 2 self-edits made to pass the gate are confirmed reasonable

## Gate evidence

| Item | Result |
|---|---|
| `uv run ruff format --check .` | 105 files already formatted |
| `uv run ruff check .` | All checks passed! |
| `uv run mypy` | Success: no issues found in 23 source files |
| `uv run pytest -m "unit or contract" -q` | 145 passed, 2 skipped |
| Structure guards | 3 additional parameterized cases appeared automatically as kernel source files grew, all passing |

## Review findings

| # | Finding | Adjudication |
|---|---|---|
| S1 | The peer allowlist `authorize_peer` is a pure function; when both policy sets are empty it returns `False` (fail-closed), consistent with the `gating` default-off | Accepted: fail-closed is the correct default for boundary safety (ADR-0016, AGENT.md §13) |
| S2 | The certificate dimension is independent of the address dimension; a hit on either one allows the request | Accepted: in mTLS scenarios the certificate is stronger identity evidence |
| S3 | TLS configuration hot rotation is implemented as an **immutable reload** (`reload` returns a new `TransportSeam`, and `config_version` increments), with a test asserting that "the old seam still adjudicates by the old policy" | Accepted: this is exactly the testable expression of "hot rotation without restarting the process and without losing in-flight calls" (AGENT.md §13) |
| S4 | `SipAdapter` only declares a Protocol (`parse` / `respond` / `forward`), with no implementation and no stack dependency | Accepted: legitimate scope for the first half of M2b; binding reSIProcate belongs to the second half and does not pollute the kernel (ADR-0019) |
| S5 | `decision_to_status_code`: `DECLINE → 603` (RFC 3261 §21.6.2), `NOT_FOUND → 404` (§21.4.5), `FORWARD/TRANSLATE → 0` (keep forwarding) | Accepted: the section numbers adopt the conclusions already corrected during PRD review, not the incorrect §21.6.5 / §21.4.4 |
| S6 | The `received_at` of `to_decision_request` is injected by the caller; the module does not read the clock | Accepted: keeps the `decide()` pure-function chain intact (AGENT.md §5) |
| S7 | Two self-edits made to pass the gate: the `reload` return annotation dropped its quotes (UP037, semantically equivalent), and `authorize_peer` changed to a direct boolean return (SIM103, keeping the `# See ADR-0016` comment) | Accepted: both are equivalent rewrites, and neither masks anything with `# type: ignore` or `# noqa` |
| S8 | The whole repository has no `# type: ignore` and no `# noqa` | Accepted |

## Gaps (non-blocking)

| # | Gap | Destination |
|---|---|---|
| S9 | `SipAdapter` has no implementation, and there are not yet integration use cases over real sockets | To be added after the second half of M2b (stack binding) |
| S10 | Real loading for certificate hot rotation (reading certificate files, handshake) is not implemented; this seam covers only policy and version semantics | Second half of M2b |
| S11 | The `integration` / `e2e` layers still have zero use cases, and layers ②③ remain non-blocking | The milestone that introduces the first use case in that layer must switch it to blocking (AGENT.md §9, plan.md §2.4) |

## Confirmation sign-off

| Item | Value |
|---|---|
| Review verdict | Pass |
| Gate | Fully green (145 passed / 2 skipped) |
| Reviewer | AI agent, 2026-09-28 |
| Maintainer signature | To be filled in |
