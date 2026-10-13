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

# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows SemVer, and `./VERSION` is the single source of the product release version (ADR-0018).

## [0.2.0] - Unreleased

### Added

- M8 release-candidate execution plan: [`docs/handoff/2026-10-06-m8-release-candidate-plan.md`](docs/handoff/2026-10-06-m8-release-candidate-plan.md) (phases A→E; `plan.md` §0/§4 entry updated).
- First Helm chart version sync (A6, maintainer to set timing and value on 2026-10-12): `deploy/helm/Chart.yaml`'s `version` / `appVersion` are fixed to the root `VERSION` (`0.2.0`), and `kubeVersion: ">=1.23.0-0"` declared (derived from the chart's actual APIs; the most constraining are `autoscaling/v2` and Job TTL). Sync is driven by `scripts/sync-chart-version.sh` (default `--check` is read-only and exits 1; explicit `--apply` writes); `make chart-check` re-runs `chart-check: OK`.
- Product SIP runtime: `AS_SIP_BIND_ADDRESS` / `AS_SIP_ADVERTISED_ADDRESS` and `AS_TLS_*` / `AS_PEER_*` environment-variable seams (`transport_env.py`).
- `platform/tests/native_extensions.py`: when `AS_REQUIRE_NATIVE_EXTENSIONS=1`, contract tests fail if the native extension is absent.
- Demo: story C M5 reconciliation talking points, story B adds S4/487 steps, `run-all-automated` PASS/SKIP/FAIL summary.
- Blocking native gate targets (`m2-platform-resip-build` / `m2-native-smoke` / `m7-*` integration, fail when `_resip_runtime` is missing) + `chart-check` / `gate-strict` enter gate layer ① (F9).
- `resip_runtime_log_contract` (`RESIP_RUNTIME_*` field contract) + 13 contract tests + NF-13 mapping (F8).
- Helm H-1…H-4 fail-closed (secret key completion / stateStores production combination fails / empty `tls.secretName` fails / empty `peerAllowlist` fails) + chart-check onprem matrix; kind script fail-closed (K-1/K-2).
- HLD/LLD M5 delta + ADR-0008 SPoF gap amendment + ADR-0013 amendment note.
- M8 sign-off matrix (`m8-test-plan-matrix.md`) + environment evidence (`m8-environment-evidence.md`) + exit review (`m8-exit-review-2026-10-06.md`); M8 RC does not claim all-green, sign-off pending maintainer.

### Changed

- REQ-F-10: downstream 408/480/486/503/504 pass-through to upstream (`CallController` + native runtime).
- After the FORWARD two-leg is established, the native side returns the real UAC checkpoint fields; BYE recovery uses the checkpoint Contact/route_set.
- `as_load` supports `--min-success-rate` / `--max-unresolved` exit-code strategy.
- M5 closure meaning downgraded to engineering closure (not REQ acceptance); M5 REQ-level fails, 10 items deferred (see `m5-req-acceptance-review-2026-10-06.md`; proposed new plan §5 lines M5D-1…M5D-6 to be set by the maintainer).
- The performance gate layer has been blocking since the first M6 use case; the e2e layer still does not block (0 tests).
- `m2-platform-resip` fails integration cases when `_resip_runtime` is missing (not skip).

### Internal build (2026-10-12)

> **This is an internal build, not a release.** The version stays `0.2.0` (the `VERSION` file unchanged); the image tag suffix is `-internal-<date>`.

- **Docker image carries SIP listener**: `deploy/docker/Dockerfile` adds a multi-stage build (`resip-builder` / `py-builder` / `runtime`); the builder stage builds the reSIProcate shared library (rutil/resip/dum) from `testbed/simulators/resip-probe/vendor/` source plus three native Python extensions (`_resip_runtime`, `_resip_two_leg`, `_resip_recovery`); the runtime stage places the reSIProcate shared library at `/app/lib` (`LD_LIBRARY_PATH=/app/lib`) and the native extensions at `/app/native` (`AS_RESIP_RUNTIME_BUILD` / `AS_RESIP_TWO_LEG_BUILD` / `AS_RESIP_RECOVERY_BUILD=/app/native`).
- **Release image enables SIP listener by default**: the runtime stage sets `AS_ENABLE_SIP_RUNTIME=1`, so the container starts the native listener on boot (UDP/TCP/TLS depending on `AS_SIP_*` / `AS_TLS_*`); when no port is set, UDP binds 5060.
- **Process entry wires in the SIP stack**: `platform/src/as_platform/__main__.py`'s `main()` calls `SipStackService.from_env()` + `start()` inside the try block after the shell is created; on drain it calls `sip_service.stop()`, with a finally fallback to stop; fail-closed: when `AS_ENABLE_SIP_RUNTIME=1` but the native extension is missing, `from_env` raises RuntimeError → the except returns exit code 2 (not a crash); when the env var is unset, behavior matches the old version.
- **EXPOSE correction**: changed from `5060/udp 5061/tcp` to `5060/udp 5060/tcp 5061/tcp` (TCP and UDP share 5060, TLS uses 5061, consistent with Helm `values.yaml`'s `sip.port` / `sip.tlsPort`).
- **Image reproducible build + digest record**: base image pinned tag, uv `--frozen`, source tarball with SHA256 verification; after build, the image ID is recorded to `docs/acceptance/artifacts/m5/2026-10-12/PASS-docker-build-digest-2026-10-12.txt`.
- **Desensitization re-check passed**: no `.pem` / `.key` / `.pcap` / `.pcapng` sensitive files in the image, no password-bearing logs.
- **Image tag format**: `as-platform:0.2.0-internal-<date>` (date format `YYYYMMDD`).
- **Chart not synced**: the Helm chart stays at `0.2.0` and does not change with the internal build.
- **Positioning of this build**: function complete + simulator evidence + reproducible build; it signs off no REQ, does not constitute M8 milestone closure, and is not published externally.

## [0.1.0] - Unreleased

### Added

- Repository skeleton: uv workspace, seven members, in `platform/`, `apps/`, `services/`, `testbed/`.
- Structure guards: dependency direction (`platform/tests/`), workspace layout, version consistency (`tests/`).
- Four-layer test gate: fast → integration → e2e → performance.
- `AGENT.md` — the product's collaboration rules of engagement.
- ADR registry: maps the 19 confirmed decisions to ADR numbers, plus an ADR template.
- `docs/plan.md` — milestone plan and open-item registry.
- `docs/migration/triage.md` — POC and library code inventory, initial classification, and the triage rules for gated adoption.
- `docs/architecture/system-architecture.md` — the confirmed design baseline.
- Feature capability-gating decision: layered toggles (deployment-level master switch + runtime fine-grained override, ADR-0020), and defines the new-feature implementation flow (`AGENT.md` §3.4).
- M1 behavior baseline: under `testbed/contracts/sip-baseline/`, S1 basic call (14 messages), S2 no-match 404 (4 messages), S3 policy-reject 603 (4 messages), S4 caller-cancel CANCEL (12 messages) — four message samples; S5–S8 ruled as derived baseline, S10/S11 moved to M2 probe, see `docs/plan.md` §4.1.
- SIP stack selection validation: reSIProcate E1 probe and build scripts (ADR-0019).
- Requirement → ADR bidirectional references: each ADR header adds a "responds to REQ" field.
- Requirement standard `docs/requirements/prd.md` v0.2: added REQ-S-* security requirement class, REQ-F-12 (rule CRUD), REQ-F-14 (approval workflow), and corrected RFC 3261 section numbers.
- M1 acceptance report `docs/acceptance/report.md` and exit review record `docs/reviews/m1-exit-review.md`.
- M2a core (`platform/`): `decide()` decision pure function and rule matching (longest prefix, block first), `StateStore` seam and `InMemoryStateStore` / `RedisStateStore` dual implementations, feature-gating seam (layered, default off, fail-closed), bounded-queue telemetry (export does not block the call path), process shell and draining, internal API contract model.
- Dependency: runtime state store wired to `redis>=5.0` (ADR-0002 / ADR-0007).
- Design and review: `docs/architecture/hld.md`, `lld.md`; `docs/reviews/m2-design-review.md`, `m2a-kernel-review.md`.
- M2b boundary seam (`platform/src/as_platform/sip/`): peer allowlist and TLS config hot-rotation (immutable reload, no restart, no dropped calls), SIP adaptor seam (Protocol only, no stack implementation), decision-to-SIP-status-code mapping (603 / 404).
- M3 decision module: `apps/translation` (number translation, with baseline fact `+8613800138000` → `013800138000` assertion) and `apps/anti-fraud` (rate-window over-limit judgment, `RATE_LIMIT`), both built on the core `decide()`, pure functions, TDD.
- M3 contract case set: `testbed/contracts/decision/` (14 declarative cases), replayed by both `apps/translation` and `apps/anti-fraud` (marker `contract`).
- First `integration`-layer case: `platform/tests/test_telemetry_export_integration.py` (real-socket verification that telemetry export does not block the call path); layer ② switched to blocking.
- M4 config-governance core (`services/config-service`): change-order state machine (approval trail, illegal transitions rejected), immutable config version store, batched canary distribution with auto-rollback.
- Toggles go through the change pipeline: `ConfigBundle` adds `ToggleDTO` (with a mandatory removal condition), in the same config version as rules; both on/off states covered by tests.
- M4 console auth and audit (`services/console`): role / permission matrix, submitter cannot approve their own change, both allow and deny are trailed, audit records immutable.
- M4b control-plane engineering slice (2026-10-02/03): persistent auth / audit integration, console real-time read / session, reuse of the ChangeOrder submit / approve / reject workflow, same-origin ASGI static assets / runtime factory / CLI, and optional Helm config-service wiring; engineering slice only, not REQ/M4b acceptance. Real deployment HTTPS / ingress / proxy, lossless rule compilation, real-time trace, cluster notification / health, Helm render and image build remain unverified or TODO.
- New owner-only PostgreSQL setup command `as-config-migrate`: initializes the dedicated `as_config` and audit schema via the store schema API, granting the pre-provisioned runtime role only its required config table/column permissions. The database role is pre-created by the DBA; the owner DSN is for manual operations only and never enters the web Pod. Runtime startup still performs no DDL. Fake-connection-focused tests pass; no Helm render/deployment or M4b/M4/REQ acceptance is claimed.
- Open item D7 adjudication (ADR-0021): runtime-override granularity is number range + stable-hash percentage, judgment idempotent; `gating/overrides.py` and its tests.
- M5 deployment artifacts: Helm templates (one Deployment / Service, ConfigMap / Secret, HPA, PDB, SA, NOTES per use case) and alert rule set (`deploy/alerts/`, 8 rules, only ratio / relative-quantity / state-quantity thresholds).
- Capacity-number discipline: HPA threshold and replica bounds left empty and guarded by `required`; the entire `deploy/` directory contains no absolute CPS or concurrency values (O1 pending M6 measurement).
- PostgreSQL-version `VersionStore` (`services/config-service`): immutable append (no UPDATE / DELETE), table-name allowlist, lazy `psycopg` import; 9 real PostgreSQL 16 container integration cases (`pytest -m integration` totals 12 passed).
- Core metric seam (`platform/src/as_platform/telemetry/metrics.py`): `MetricsRegistry` / `CallMetrics`, per-instance `as_active_calls` and `as_sip_responses_total` / `as_rule_hits_total` / `as_telemetry_dropped_total`, same names as the metric contract in `deploy/alerts/`; no thresholds or defaults.
- M5 container image: `deploy/docker/Dockerfile` (multi-stage uv build, non-root, `python -m as_platform` entry) and process entry point `platform/src/as_platform/__main__.py`; in-image SIGTERM drain measured exit code 0.
- `testbed/probe/`: SIP stack selection probes (E1 baseline diff, E4 TLS hot-rotation) and sequence comparator; fails loudly with exit code 2 when the binding is missing.

### Notes

- No product code yet: the skeleton deliberately contains no business logic, so the structure can be reviewed before code is migrated in.
- Gate layers ② ③ ④ do not block before the milestone that first introduces that class of test. See `docs/plan.md` §2.4.
- M1 is a documentation and baseline milestone, **with no product code delivered**, so `VERSION` stays `0.1.0`, not bumped (ADR-0018).
- M2a has product code delivered, but the product is not yet released, so `VERSION` stays `0.1.0`, with all increments going into the Unreleased section; the version number is set at first release per ADR-0018.
