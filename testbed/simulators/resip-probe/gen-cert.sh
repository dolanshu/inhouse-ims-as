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

# Generate self-signed TLS certificate for resip-probe E4 TLS scenario.
# Output: short-lived self-test-only cert.pem + key.pem in current directory
# (1 day validity).

set -euo pipefail

# Ensure newly created key/cert files are owner-readable only.
umask 077

for output in cert.pem key.pem; do
  if [[ -L "$output" ]]; then
    echo "[gen-cert] error: $output is a symlink; refusing to overwrite credentials" >&2
    exit 1
  fi
  if [[ -e "$output" ]]; then
    echo "[gen-cert] error: $output already exists; refusing to overwrite credentials" >&2
    exit 1
  fi
done

tmp_conf="$(mktemp ./resip-probe-openssl-XXXX.cnf)"
trap 'rm -f "$tmp_conf"' EXIT

cat > "$tmp_conf" <<'EOF'
[req]
distinguished_name = dn
x509_extensions = v3_ca
prompt = no

[dn]
CN = 127.0.0.1

[v3_ca]
subjectAltName = IP:127.0.0.1
basicConstraints = critical,CA:true
keyUsage = critical,digitalSignature,keyEncipherment,keyCertSign
extendedKeyUsage = serverAuth
EOF

openssl req -new -x509 -newkey rsa:2048 -nodes \
  -days 1 \
  -keyout key.pem \
  -out cert.pem \
  -config "$tmp_conf"

echo "[gen-cert] Generated cert.pem + key.pem (SAN IP=127.0.0.1, CA:TRUE, validity=1 day)"
