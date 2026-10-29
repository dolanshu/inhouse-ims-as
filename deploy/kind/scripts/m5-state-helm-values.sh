#!/usr/bin/env bash
# Inhouse-IMS-AS — Copyright 2026 Dolan Shu <dolan.d.shu@gmail.com>, Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

# ADR-0026 / M5 §4.6 (D12): bundled in-cluster PG+Redis for kind (dev credentials only).
set -euo pipefail
cat <<'EOF'
--set stateStores.enabled=true
--set stateStores.bootstrapDevCredentials=true
--set stateStores.networkPolicy.enabled=true
EOF
