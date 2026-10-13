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

# 3rdparty-as — the local gate.
#
# `make gate` is layer ① — lint, type, then unit/contract tests, in that order.
# Nothing is committed unless it is green here first (AGENT.md §Git rules).

.PHONY: help sync fmt lint type test test-unit test-integration test-integration-compose test-e2e test-perf chart-check alert-check gate gate-strict gate-native \
	m2-native-restore m2-native-build m2-native-smoke m2-native-smoke-tcp m2-native-smoke-tls-runtime m2-native-smoke-tcp-runtime m2-native m2-platform-resip-build m7-platform-two-leg-build m7-platform-recovery-build m71-sim

# Matches deploy/compose/.env.example POSTGRES_SUPERUSER_PASSWORD on published port 55432.
COMPOSE_PG_DSN ?= postgresql://postgres:postgres@127.0.0.1:55432/as_config

# Non-login shells often omit ~/.local/bin; resolve uv the way docs expect `uv sync`.
UV := $(shell command -v uv 2>/dev/null)
ifeq ($(UV),)
  ifneq ($(wildcard $(HOME)/.local/bin/uv),)
    UV := $(HOME)/.local/bin/uv
  else ifneq ($(wildcard $(HOME)/.cargo/bin/uv),)
    UV := $(HOME)/.cargo/bin/uv
  else
    UV := uv
  endif
endif
export UV

help: ## list the targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk -F':.*?## ' '{printf "  %-18s %s\n", $$1, $$2}'

sync: ## create or refresh the locked environment for the whole workspace
	$(UV) sync

fmt: ## apply ruff format
	$(UV) run ruff format .

lint: ## ruff format --check + ruff check
	$(UV) run ruff format --check .
	$(UV) run ruff check .

type: ## mypy, strict, src only
	$(UV) run mypy

# 2026-10-11 追加（本 target 行为一个字未改，只补注记）：e2e Wave 1 已于同日落地在
# testbed/e2e/test_sip_first_edition.py，`uv run pytest -m e2e -q` 现收集到 5 条且稳定通过
# —— 上方注释里「e2e 用例尚未落地」的事实前提已变，按保史约定原文保留、此处说明。
# e2e 层是否**重新纳入** `make test` 属门禁配置变更，与 A4-4（kind e2e 进 PR required 的 E2E
# policy）同为维护者裁决事项，而该裁决明确「不构成任何配置变更授权」；故此处保持 S1 第一批的
# 原样，e2e 仍由 `make test-e2e` 显式运行。执行记录见
# docs/handoff/2026-10-11-w0-native-and-e2e-execution-record.md §7.3。
test: ## every layer below ④ (e2e 用例尚未落地，落地方案见 docs/acceptance/2026-10-09-e2e-test-plan.md)
	$(UV) run pytest -m "unit or contract" -q
	$(UV) run pytest -m integration -q

test-unit: ## ① unit + contract
	$(UV) run pytest -m "unit or contract" -q

test-integration: ## ② integration against simulated peers
	$(UV) run pytest -m integration -q

test-integration-compose: ## ② integration using deploy/compose Postgres (AS_PG_TEST_DSN)
	AS_PG_TEST_DSN="$(COMPOSE_PG_DSN)" $(UV) run pytest -m integration -q

chart-check: ## helm lint + template guards (M5-0c; requires helm 3.x)
	deploy/helm/scripts/chart-check.sh

alert-check: ## promtool check rules on deploy/alerts/as-alerts.yaml
	@command -v promtool >/dev/null 2>&1 || { echo "promtool not found; install prometheus or set PATH" >&2; exit 1; }
	promtool check rules deploy/alerts/as-alerts.yaml

m5-cluster-evidence: ## kind cluster M5 rollout/ingress evidence (needs docker+kind)
	bash deploy/kind/m5-cluster-evidence.sh

m5-kind-verify: ## gate + chart-check + kind smoke (existing as-m5)
	bash deploy/kind/m5-verify.sh

m5-issu-scale-evidence: ## §217①② + H10 on existing kind-as-m5 (needs cluster)
	bash deploy/kind/m5-issu-scale-evidence.sh

m5-7.2d-evidence: ## 7.2d ingress L7 + browser HTTPS (needs M5_7_2D_E2E_PASSWORD)
	bash deploy/kind/m5-7.2d-evidence.sh

test-e2e: ## ③ end-to-end call flows
	$(UV) run pytest -m e2e -q

test-perf: ## ④ capacity baseline (never part of the commit gate)
	$(UV) run pytest -m performance -q

m2-native-restore: ## M2 P0: extract bundled reSIProcate vendor source to repo cache
	bash testbed/simulators/resip-probe/scripts/m2-native.sh restore

m2-native-build: ## M2 P0: cmake-build reSIProcate + resip_probe under .cache/m2-resiprocate
	bash testbed/simulators/resip-probe/scripts/m2-native.sh build-resip
	bash testbed/simulators/resip-probe/scripts/m2-native.sh build-probe

m2-native-smoke: ## M2 P0: run resip_probe S1 UDP smoke from native cache build
	bash testbed/simulators/resip-probe/scripts/m2-native.sh smoke

m2-native-smoke-tcp: ## M2 P2b: run resip_probe S1 TCP smoke from native cache build
	bash testbed/simulators/resip-probe/scripts/m2-native.sh smoke-tcp

m2-native-smoke-tls-runtime: ## M2 P2d: platform TLS resip_runtime integration smoke (pytest)
	bash testbed/simulators/resip-probe/scripts/m2-native.sh smoke-tls-runtime

m2-native-smoke-tcp-runtime: ## M2 P2: product TCP resip_runtime integration smoke (pytest)
	bash testbed/simulators/resip-probe/scripts/m2-native.sh smoke-tcp-runtime

m2-native: m2-native-restore m2-native-build m2-native-smoke ## M2 P0: restore, build, and smoke native probe

m2-platform-resip-build: ## M2 P2c: cmake-build platform _resip_runtime extension
	bash testbed/simulators/resip-probe/scripts/m2-native.sh build-platform-resip

m7-platform-two-leg-build: ## M7 slice: cmake-build platform _resip_two_leg extension
	bash testbed/simulators/resip-probe/scripts/m2-native.sh build-platform-two-leg

m7-platform-recovery-build: ## M7 slice: cmake-build platform _resip_recovery extension
	bash testbed/simulators/resip-probe/scripts/m2-native.sh build-platform-recovery

m71-sim: ## M7.1 local SIP path, load scenarios, and chart policy text
	$(UV) run pytest platform/tests/test_udp_retransmission_contract.py testbed/load/tests/test_scenarios.py testbed/load/tests/test_no_retransmit.py testbed/load/tests/test_harness.py testbed/simulators/tests -q

demo-story-a: ## pre-M8 demo story A (translation + control plane); see scripts/demo-review/README.md
	bash scripts/demo-review/story-a.sh

demo-story-b: ## pre-M8 demo story B (block 603 + anti-fraud decision)
	bash scripts/demo-review/story-b.sh

demo-story-c: ## pre-M8 demo story C (Helm / ops / alerts)
	bash scripts/demo-review/story-c.sh

demo-story-d: ## pre-M8 demo story D (checkpoint / Redis harness)
	bash scripts/demo-review/story-d.sh

demo-story-e: ## pre-M8 demo story E (capacity smoke + O1 report head)
	bash scripts/demo-review/story-e.sh

demo-review-all: ## run automated demo stories (best-effort; needs Redis for D)
	bash scripts/demo-review/run-all-automated.sh

gate: lint type test-unit ## the pre-commit gate: lint, type, then layer ① (unit + contract)

gate-native: m2-platform-resip-build ## layer ① with _resip_runtime required (builds the extension first)
	AS_REQUIRE_NATIVE_EXTENSIONS=1 $(MAKE) gate

gate-strict: gate ## gate plus the REQ-G-3 ADR annotation scan (ADR-0015)
	$(UV) run python scripts/check_adr_annotations.py
