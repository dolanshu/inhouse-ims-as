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

# Security policy

## Reporting

Report suspected vulnerabilities privately to the maintainer (<dolan.d.shu@gmail.com>). Do not report security issues in a public issue. Please include what you observed, how to reproduce it, and the version number in `./VERSION`.

## Scope

In scope: the AS processes under `apps/` and `platform/`, the control plane under `services/`, the deployment assets under `deploy/`, and the attack surface facing the trunk.

Explicitly out of scope by design:

- **Lawful interception** — not implemented and not planned (ADR-0016).
- **Media handling** — this system does signaling only (ADR-0004).
- **Billing and CDR** — not implemented (ADR-0017).

## Expectations of the system

- The SIP trunk is treated as **untrusted**: peers must be validated against an allowlist, and TLS must terminate end-to-end with the S-SBC. Anyone who can impersonate the S-SBC can inject calls, so peer authenticity is not optional.
- Certificate rotation is a configuration hot-update — no restart, and no in-flight calls dropped.
- Every console operation must be authenticated and audited.
- Payload logging is toggleable and off by default in logs.

## Things never committed

Keys, certificates, tokens, real network addresses, and real traffic captures. The repository holds only `.env.example` placeholders.
