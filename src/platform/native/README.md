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

# Platform native bindings

Optional C++ extensions for the product SIP stack (reSIProcate per ADR-0019). They
are **not** part of the Hatch wheel; build them with CMake when
`AS_RESIP_HOME` / `AS_RESIP_BUILD` (or the repo `.cache/m2-resiprocate` trees from
`make m2-native-restore`) are available.

## `resip_runtime/` (M2 P2c)

Python module: `_resip_runtime` (imported by `as_platform.sip.resip_runtime`).

| Target | Command |
|--------|---------|
| Build extension | `make m2-platform-resip-build` |
| Integration tests | `uv run pytest src/platform/tests/test_resip_runtime_integration.py -m integration -q` |

Environment:

| Variable | Default |
|----------|---------|
| `AS_RESIP_HOME` | `$AS_RESIP_CACHE_ROOT/source` or `.cache/m2-resiprocate/source` |
| `AS_RESIP_BUILD` | `$AS_RESIP_CACHE_ROOT/build` or `.cache/m2-resiprocate/build` |
| `AS_RESIP_RUNTIME_BUILD` | `src/platform/native/resip_runtime/build` (directory containing `_resip_runtime*.so`) |

The extension links `libdum`, `libresip`, and `librutil` from the same minimal
reSIProcate build used by `testbed/simulators/resip-probe`.

## `resip_two_leg/` (M7 minimal slice)

Python module: `_resip_two_leg` (imported by `as_platform.sip.resip_two_leg`).

| Target | Command |
|--------|---------|
| Build extension | `make m7-platform-two-leg-build` |
| Integration tests | `uv run pytest src/platform/tests/test_resip_two_leg_integration.py -m integration -q` |

Environment:

| Variable | Default |
|----------|---------|
| `AS_RESIP_TWO_LEG_BUILD` | `src/platform/native/resip_two_leg/build` |

Inbound INVITE → outbound INVITE to a loopback peer; downstream **486** maps to inbound **486**. Derived from the D9 research module; not the production adapter or full B2BUA.
