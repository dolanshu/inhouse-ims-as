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

# M2 product TCP transport review (2026-10-05)

> **Subject:** Product `_resip_runtime` TCP listener (P2 remainder)  
> **Cross-ref:** [`m2-p2b-tcp-transport-review-2026-10-05.md`](m2-p2b-tcp-transport-review-2026-10-05.md) (testbed)

## Object

- `enable_tcp` on native `TransportConfig` + `ResipRuntimeListener(enable_tcp=True)`
- `platform/tests/test_resip_runtime_tcp_integration.py` — TCP INVITE → **404** (empty rules)
- `make m2-native-smoke-tcp-runtime`

## Conclusion

**Pass** for product TCP ingress engineering slice. REQ-S-2 TLS-only operator path unchanged.

## Verification

```sh
make m2-platform-resip-build
make m2-native-smoke-tcp-runtime
```

## Sign-off

- Engineering review recorded: 2026-10-05
- Maintainer sign-off: **pending**
