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

# M6 product runtime micro-measure review (2026-10-05)

> **Scope:** `testbed/load/scripts/m6-product-runtime-micro-measure.sh` (3s, cps 2, `resources.json`)  
> **Not:** O1 publication or M6 milestone exit

## Commands

```bash
make m2-platform-resip-build
bash testbed/load/scripts/m6-product-runtime-micro-measure.sh
```

## Result

Script unchanged in this slice; captures `summary.json` + `resources.json` (UAS RSS snapshot).

Pass (local 2026-10-05): `established_sessions=6`, evidence `/tmp/as-m6-product-runtime-micro-20261005-081951/`.

## Recommendation

**Accept** as optional engineering precursor. **Deny** O1 numbers and M6 milestone closure.
