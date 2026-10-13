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

# ADR-0011 — SIP stack: dual-stack parallel (sippy for production + go-b2bua pilot)

- **ID**: ADR-0011
- **Status**: **superseded-in-part by ADR-0019** (the "dual-stack parallel" framework remains valid; the "production stack = sippy" premise has been overturned)
- **Date**: 2026-09-27
- **Decides**: [`../system-architecture.md`](../system-architecture.md) §0 decision 8 — adopt the dual-stack parallel migration path: sippy continues as the production stack, go-b2bua as the pilot implementation.

---

## Context

The POC has verified the feasibility of `sippy==2.4.2` as a B2BUA; an official Go port `go-b2bua` also exists.
To reduce runtime risk and retain the cross-implementation parity framework, the maintainer confirmed sippy for production first, with go-b2bua as the pilot.

---

## Decision

1. The production stack continues to use `sippy==2.4.2`.
2. Start the `go-b2bua` image port in parallel, sharing the rules YAML with the Python implementation, and gradually canary it after passing cross-implementation contract-test parity.
3. The specific meaning of dual-stack parallel is re-interpreted by ADR-0019's selection result.

---

## Consequences

### Positive

- Risk contained: production behavior unchanged, the new stack validated gradually.
- Cross-implementation parity retained as the promotion gate (ADR-0012).

### Negative / accepted

- Risks such as sippy's upstream concentration and Python 3.10 EOL are not lifted by this decision; they are handled subsequently by ADR-0019.
- go-b2bua has no release; once selected it requires commit pin + vendoring.

---

## Alternatives considered

| Option | Why not |
|---|---|
| Switch everything to go-b2bua directly | Switching production before sufficient parity evidence carries too much risk |
| Continue with sippy alone | Does not address supply-chain and runtime lifecycle risks |

---

## Evidence

- [`../system-architecture.md`](../system-architecture.md) §10.1 / §10.2: the dual-stack migration state machine.
- `docs/SIP_stack_selection.md`: the candidate stack list and licensing red lines.

---

## Related

- [`../system-architecture.md`](../system-architecture.md) §0 decision 8, §10
- [`0019-sip-stack-selection.md`](0019-sip-stack-selection.md) (overturns the "production stack = sippy" premise)
- ADR-0012 (cross-implementation contract + parity, skeleton)
