<!--
Inhouse-IMS-AS — Copyright 2026 Dolan Shu <dolan.d.shu@gmail.com>, Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-->

# `deploy/compose/` — M4b-8 dev HTTPS (same origin)

On a single Docker host (including WSL2), stand up **PostgreSQL 12.22**, the **config-service** runtime, and **Caddy** with a self-signed TLS reverse proxy, so the console static assets and the `/internal/v1` API share the same HTTPS origin. Used by [`docs/acceptance/m4b-8-runbook.md`](../../docs/acceptance/m4b-8-runbook.md) and `test-plan.md` §1.4 M4b-8; **not** a production deployment target (production is `deploy/helm/`).

## Prerequisites

- Docker Engine + Compose v2
- `openssl` (to generate the self-signed certificate)
- Optional: `uv` at the repo root (to run migrate directly against `localhost:55432` rather than via a compose profile)

## Quick start

```sh
cd deploy/compose
cp .env.example .env
# edit .env: set AS_AUDIT_RESOURCE_HMAC_KEY_B64 to a 32-byte base64 (openssl rand -base64 32)

./scripts/gen-certs.sh
docker compose up -d postgres
./scripts/migrate.sh
./scripts/bootstrap-admin.sh   # interactive: first administrator
./scripts/up.sh
./scripts/smoke-https.sh
```

Open `https://localhost:8443/` in a browser (accept the self-signed cert warning). Login requires the HTTPS scheme; Caddy forwards `X-Forwarded-Proto: https` to config-service, and `AS_CONFIG_TRUSTED_PROXIES` covers the compose network `10.89.0.0/24`.

## Services

| Service | Description |
|---|---|
| `postgres` | `postgres:12.22`, database `as_config`; init script creates `as_config_owner` / `as_config_web` + `as_config_runtime` (NOLOGIN) |
| `config-service` | image `deploy/docker/config-service.Dockerfile`; only runtime DSN + HMAC key |
| `caddy` | host `8443` → HTTPS → `config-service:8000` |
| `testbed-health` | optional; `http://10.89.0.30:8080/health` returns `{"healthy":true}`, for 7.5 fleet-probe integration |
| `migrate` / `bootstrap-admin` | one-shot tasks via `--profile setup` |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/gen-certs.sh` | writes `certs/tls.crt` / `tls.key` (localhost SAN) |
| `scripts/migrate.sh` | `as-config-migrate` (owner DSN) |
| `scripts/bootstrap-admin.sh` | `as-config-bootstrap-admin` (interactive) |
| `scripts/up.sh` | build and start runtime + reverse proxy + health stub |
| `scripts/smoke-https.sh` | `curl -k --noproxy '*'` to check `/` HTML and unauthenticated session 401 (avoids the host `HTTP(S)_PROXY` returning 504 for localhost) |
| `scripts/m4b-8-browser-evidence.sh` | Playwright screenshots + same-origin API evidence (needs `M4B8_E2E_PASSWORD`; auto-uses the Playwright Docker image when no local browser on Ubuntu 20.04) |

## Host integration tests (M5)

`pytest -m integration` defaults the DSN to `postgres:secret@127.0.0.1:55432`; the compose superuser password is in `.env.example` (default `postgres`). With the compose Postgres running:

```sh
# repo root
make test-integration-compose
# equivalent to AS_PG_TEST_DSN=postgresql://postgres:postgres@127.0.0.1:55432/as_config pytest -m integration
```

## Host migrate (optional)

The Postgres mapped port defaults to `55432`:

```sh
AS_CONFIG_OWNER_DSN="postgresql://as_config_owner:as_config_owner_dev@127.0.0.1:55432/as_config" \
  AS_CONFIG_RUNTIME_ROLE=as_config_runtime \
  uv run --directory services/config-service as-config-migrate
```

## Limitations

- Passwords and HMAC are **dev placeholders**; do not use in production.
- The 7.2d production ingress-nginx preflight is not implemented; M4b-8 browser evidence is in the runbook's **BLOCKED** item.
- Destroy data: `docker compose down -v`
