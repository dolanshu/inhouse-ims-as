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

# M8 native 一致性 runbook（一句话）

签收跑前必须先构建与被测证据对应的 native 扩展：`make m2-platform-resip-build`，行使 two-leg / recovery 证据时另加 `make m7-platform-two-leg-build` / `make m7-platform-recovery-build`；随后运行计划 §7 命令：`AS_REQUIRE_NATIVE_EXTENSIONS=1 uv run pytest platform/tests/test_e1_contract_resip_runtime_full.py -m contract -q` 与 `AS_REQUIRE_NATIVE_EXTENSIONS=1 uv run pytest platform/tests/test_m7_forward_two_leg_integration.py platform/tests/test_req_f4_sdp_identity_integration.py -m integration -q`（缺扩展即 fail 而非 skip）。
