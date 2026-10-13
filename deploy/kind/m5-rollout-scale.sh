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

# M5-3a/b: rollout restart + ISSU/scale evidence (§217①②, H10).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
# shellcheck source=deploy/kind/m5-metrics-lib.sh
source "${ROOT}/deploy/kind/m5-metrics-lib.sh"
NS="${K8S_NAMESPACE:-as-m5}"
RELEASE="${HELM_RELEASE_NAME:-as}"

deploy="$(m5_use_case_deployment "${NS}" anti-fraud "${RELEASE}")"
echo "==> rollout restart ${deploy}"
kubectl -n "${NS}" rollout restart "deployment/${deploy}"
kubectl -n "${NS}" rollout status "deployment/${deploy}" --timeout=180s

bash "${ROOT}/deploy/kind/m5-issu-scale-evidence.sh"
echo "rollout-scale: OK"
