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
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CLUSTER_NAME="${KIND_CLUSTER_NAME:-as-m5}"
PLATFORM_TAG="${AS_PLATFORM_IMAGE:-as-platform:m5}"
CONFIG_TAG="${AS_CONFIG_IMAGE:-as-config-service:m5}"

cd "${ROOT}"
docker build -t "${PLATFORM_TAG}" -f deploy/docker/Dockerfile .
docker build -t "${CONFIG_TAG}" -f deploy/docker/config-service.Dockerfile .
kind load docker-image "${PLATFORM_TAG}" --name "${CLUSTER_NAME}"
kind load docker-image "${CONFIG_TAG}" --name "${CLUSTER_NAME}"
echo "loaded ${PLATFORM_TAG} and ${CONFIG_TAG} into kind ${CLUSTER_NAME}"
