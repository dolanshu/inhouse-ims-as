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

# Generate self-signed TLS material for local M4b-8 HTTPS (localhost + 127.0.0.1).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CERT_DIR="${ROOT}/certs"
mkdir -p "${CERT_DIR}"

openssl req -x509 -newkey rsa:2048 -sha256 -days 825 -nodes \
	-keyout "${CERT_DIR}/tls.key" \
	-out "${CERT_DIR}/tls.crt" \
	-subj "/CN=localhost" \
	-addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

chmod 0644 "${CERT_DIR}/tls.crt"
chmod 0600 "${CERT_DIR}/tls.key"
echo "Wrote ${CERT_DIR}/tls.crt and tls.key"
