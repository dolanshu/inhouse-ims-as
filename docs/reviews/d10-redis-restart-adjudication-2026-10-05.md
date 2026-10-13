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

# D10 Redis + process restart adjudication (2026-10-05)

| Item | Verdict |
|------|---------|
| Real Redis integration test (`test_d10_req_nf1_redis_integration.py`) | **Accept** (engineering) |
| Kill/restart subprocess harness (`test_d10_process_restart_integration.py`, `_d10_child.py`) | **Accept** (engineering) |
| REQ-NF-1 / full D10 acceptance | **Deny** |
| Maintainer sign-off | **Pending** |
