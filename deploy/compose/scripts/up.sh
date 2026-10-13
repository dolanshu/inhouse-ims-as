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

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

if [[ ! -f .env ]]; then
	echo "Missing ${ROOT}/.env — copy .env.example and set AS_AUDIT_RESOURCE_HMAC_KEY_B64." >&2
	exit 1
fi

if [[ ! -f certs/tls.crt ]]; then
	echo "Missing TLS certs — run: ./scripts/gen-certs.sh" >&2
	exit 1
fi

docker compose up -d --build postgres testbed-health config-service caddy
echo "HTTPS console/API: https://localhost:${HTTPS_PUBLISH_PORT:-8443}/ (trust self-signed cert in browser)"
