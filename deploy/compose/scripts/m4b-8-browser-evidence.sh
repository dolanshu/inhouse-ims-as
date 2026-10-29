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
REPO="$(cd "${ROOT}/../.." && pwd)"
cd "${ROOT}"

if [[ -f .env ]]; then
	# shellcheck disable=SC1091
	set -a && source .env && set +a
fi

: "${M4B8_E2E_PASSWORD:?Set M4B8_E2E_PASSWORD in the environment (12+ chars, dev-only)}"

export AS_CONFIG_OWNER_DSN="${AS_CONFIG_OWNER_DSN:-postgresql://as_config_owner:${AS_CONFIG_OWNER_PASSWORD:-as_config_owner_dev}@127.0.0.1:${POSTGRES_PUBLISH_PORT:-55432}/as_config}"
export AS_CONFIG_SCHEMA="${AS_CONFIG_SCHEMA:-as_config}"

echo "Seeding e2e console users (owner DSN)…"
uv run --directory "${REPO}/src/services/config-service" python "${ROOT}/scripts/m4b-8-seed-users.py"

export AS_COMPOSE_HTTPS_URL="${AS_COMPOSE_HTTPS_URL:-https://localhost:8443}"
export M4B8_ARTIFACT_DATE="${M4B8_ARTIFACT_DATE:-2026-10-03}"

run_browser_evidence() {
	NO_PROXY='*' node "${ROOT}/scripts/m4b-8-browser-evidence.mjs"
}

echo "Capturing browser evidence…"
if [[ ! -d node_modules/playwright ]]; then
	echo "Installing Playwright npm package (deploy/compose)…"
	npm install --no-fund --no-audit
fi

if npx playwright install chromium 2>/dev/null; then
	run_browser_evidence
else
	echo "Host Playwright browsers unavailable; using Docker (playwright jammy image, host network)…"
	docker run --rm \
		--user "$(id -u):$(id -g)" \
		--network host \
		-v "${REPO}:/work" \
		-w /work/deploy/compose \
		-e "M4B8_E2E_PASSWORD=${M4B8_E2E_PASSWORD}" \
		-e "AS_COMPOSE_HTTPS_URL=${AS_COMPOSE_HTTPS_URL}" \
		-e "M4B8_ARTIFACT_DATE=${M4B8_ARTIFACT_DATE}" \
		-e "AS_TESTBED_HEALTH_URL=${AS_TESTBED_HEALTH_URL:-http://10.89.0.30:8080/health}" \
		-e NO_PROXY='*' \
		mcr.microsoft.com/playwright:v1.49.1-jammy \
		bash -lc 'npm install --no-fund --no-audit && node scripts/m4b-8-browser-evidence.mjs'
fi

"${ROOT}/scripts/smoke-https.sh"
echo "m4b-8-browser-evidence: OK"
