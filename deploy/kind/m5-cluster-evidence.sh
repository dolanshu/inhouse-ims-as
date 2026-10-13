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

# M5-3a/b + 7.2d: kind cluster evidence bundle (plan.md §4.4).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DATE="$(date -u +%Y-%m-%d)"
ART="${ROOT}/artifacts/m5/${DATE}"
mkdir -p "${ART}"
LOG="${ART}/cluster-evidence.log"
exec > >(tee -a "${LOG}") 2>&1

echo "M5 cluster evidence ${DATE}"
cd "${ROOT}"

if [[ ! -f deploy/compose/certs/tls.crt ]]; then
  (cd deploy/compose && ./scripts/gen-certs.sh)
fi

./deploy/kind/m5-kind-up.sh
./deploy/kind/m5-images.sh
./deploy/kind/m5-helm-install.sh
./deploy/kind/m5-rollout-scale.sh   # includes m5-issu-scale-evidence.sh
./deploy/kind/m5-ingress-evidence.sh

echo "DONE log=${LOG}"
