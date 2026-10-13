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

# M6 product runtime 60s measure review (2026-10-05)

> **Scope:** `testbed/load/scripts/m6-product-runtime-measure-60s.sh` (60s, cps 5, `summary.json` + `resources.json`)  
> **Not:** O1 publication, capacity target claims, or M6 milestone exit

## Commands

```bash
make m2-platform-resip-build
bash testbed/load/scripts/m6-product-runtime-measure-60s.sh
```

## Expected artifacts

| File | Content |
|------|---------|
| `summary.json` | `as_load` counts/latency for `stack=as-platform-resip-runtime` |
| `resources.json` | UAS RSS snapshot (`snapshots[]`) |

Output directory: `/tmp/as-m6-product-runtime-60s-<timestamp>/`.

## Limits

- Loopback UDP only; empty routing rules on `load_uas_runtime.py` accept-all harness path is **not** used here (fixture uses product listener accept path via load UAS — verify load_uas_runtime).
- Numbers are **engineering evidence** for harness stability under sustained load, not O1 answers.
- No maintainer sign-off on M6 or D8 REQ trace.

## Recommendation

**Accept** as optional M6 engineering measure. **Deny** O1 publication and M6 milestone closure.

## Sign-off

- Review recorded: 2026-10-05  
- Maintainer / M6 milestone sign-off: **not requested**
