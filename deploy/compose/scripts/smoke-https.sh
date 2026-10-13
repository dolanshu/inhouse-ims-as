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

# Minimal same-origin HTTPS smoke (no browser). Requires stack up and certs generated.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

if [[ -f .env ]]; then
	# shellcheck disable=SC1091
	set -a && source .env && set +a
fi

BASE="${AS_COMPOSE_HTTPS_URL:-https://localhost:8443}"

# Corporate HTTP(S)_PROXY often breaks CONNECT to localhost; bypass for compose smoke.
CURL_LOCAL=(curl -fsS -k --noproxy '*')
CURL_LOCAL_STATUS=(curl -sS -k --noproxy '*')

echo "GET ${BASE}/"
html="$("${CURL_LOCAL[@]}" "${BASE}/")"
if ! grep -qi '<html' <<<"${html}"; then
	echo "Expected HTML console shell at /" >&2
	exit 1
fi

echo "GET ${BASE}/internal/v1/auth/session (unauthenticated)"
status="$("${CURL_LOCAL_STATUS[@]}" -o /dev/null -w '%{http_code}' "${BASE}/internal/v1/auth/session")"
if [[ "${status}" != "401" ]]; then
	echo "Expected 401 without session cookie, got ${status}" >&2
	exit 1
fi

echo "smoke-https: OK"
