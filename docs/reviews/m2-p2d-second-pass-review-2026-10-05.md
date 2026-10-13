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

# M2 P2d second-pass review (2026-10-05)

> **Subject:** REQ-S engineering tests for TLS certificate fingerprint peer policy  
> **Prior:** [`m2-p2d-tls-runtime-review-2026-10-05.md`](m2-p2d-tls-runtime-review-2026-10-05.md), [`m2-p2d-tls-runtime-adjudication-2026-10-05.md`](m2-p2d-tls-runtime-adjudication-2026-10-05.md)

## Deliverable

| Item | Artifact |
|------|----------|
| Fingerprint deny | `platform/tests/test_resip_runtime_tls_policy_integration.py::test_tls_fingerprint_policy_denies_when_token_not_in_allowlist` |
| Fingerprint allow | `same::test_tls_fingerprint_policy_allows_when_token_in_allowlist` (ingress pass → empty rules 404) |
| Cert material | `testbed/simulators/resip-probe/gen-cert.sh` in pytest `tmp_path`; client cert signed by server CA |

## Verification

```bash
make m2-platform-resip-build
uv run pytest platform/tests/test_resip_runtime_tls_policy_integration.py -m integration -q
make gate
```

## Fix (2026-10-05)

| Issue | Change |
|-------|--------|
| Allow-case returned **403** (no `certificate_id` on peer dict) | With `allowed_certificate_ids` non-empty, `ResipRuntimeListener` sets native `request_client_certificate` so TLS uses **Optional** client-cert request (peer may present cert without mandatory mTLS). |
| Fingerprint not captured during handshake | Native runtime hooks OpenSSL **`verify_callback`** (depth 0 leaf), not `cert_verify_callback` (no peer cert there). When `require_client_certificate` is false, callback still records SHA-256 fingerprint but returns success so untrusted presented certs do not abort TLS. |

## Assessment

| Finding | Disposition |
|---------|-------------|
| REQ-S acceptance / operator PKI | **Out of scope** — engineering pytest only |
| mTLS require-client-cert production path | **Open** — unchanged from P2d first pass |
| Duplicate deny test on general TLS file | **Fixed** — policy cases live on dedicated module |

## Recommendation

**Accept** as M2 **REQ-S engineering** tail. **Deny** M2 milestone exit and REQ-S-2/3 sign-off.

## Sign-off

- Second-pass review: 2026-10-05  
- Maintainer sign-off: **not requested**
