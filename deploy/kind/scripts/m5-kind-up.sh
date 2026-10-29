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

set -euo pipefail
CLUSTER_NAME="${KIND_CLUSTER_NAME:-as-m5}"
if ! command -v kind >/dev/null 2>&1; then
  echo "kind not installed" >&2
  exit 1
fi
if kind get clusters 2>/dev/null | grep -qx "${CLUSTER_NAME}"; then
  echo "kind cluster ${CLUSTER_NAME} already exists"
  exit 0
fi
kind create cluster --name "${CLUSTER_NAME}" --wait 120s
