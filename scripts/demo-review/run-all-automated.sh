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

# Run all demo stories that do not require manual browser / kind (best-effort).
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/demo-review/lib.sh
source "${DIR}/lib.sh"

STRICT=0
REQUIRE_REDIS=0
REQUIRE_KIND=0
REQUIRE_NATIVE=0
for arg in "$@"; do
  case "${arg}" in
    --strict) STRICT=1 ;;
    --require-redis) REQUIRE_REDIS=1 ;;
    --require-kind) REQUIRE_KIND=1 ;;
    --require-native) REQUIRE_NATIVE=1 ;;
    -h | --help)
      echo "Usage: $0 [--strict] [--require-redis] [--require-kind] [--require-native]"
      exit 0
      ;;
  esac
done

demo_log "repo: ${REPO_ROOT}"
PASS=0
SKIP=0
FAIL=0
SKIP_NAMES=()
ART="$(demo_artifact_dir run-all)"
SUMMARY="${ART}/summary.txt"

run_story() {
  local name="$1"
  shift
  if bash "${DIR}/${name}" "$@"; then
    demo_log "${name}: PASS"
    PASS=$((PASS + 1))
  else
    demo_log "${name}: FAIL"
    FAIL=$((FAIL + 1))
  fi
}

skip_story() {
  local name="$1"
  local reason="$2"
  demo_log "SKIP ${name} (${reason})"
  SKIP=$((SKIP + 1))
  SKIP_NAMES+=("${name}:${reason}")
}

run_story story-b.sh
run_story story-a.sh --skip-pg
run_story story-e.sh

export AS_REDIS_URL="${AS_REDIS_URL:-redis://127.0.0.1:6379/0}"
if demo_redis_reachable 2>/dev/null; then
  run_story story-d.sh
else
  if [[ "${REQUIRE_REDIS}" -eq 1 ]] || [[ "${STRICT}" -eq 1 ]]; then
    demo_die "Redis required but unreachable at ${AS_REDIS_URL}"
  fi
  skip_story "story-d.sh" "no Redis at ${AS_REDIS_URL}"
fi

if [[ "${REQUIRE_KIND}" -eq 1 ]] && ! demo_m71_present; then
  demo_die "kind context required (kind-as-m71)"
fi
run_story story-c.sh

{
  echo "PASS=${PASS}"
  echo "SKIP=${SKIP}"
  echo "FAIL=${FAIL}"
  for item in "${SKIP_NAMES[@]:-}"; do
    echo "SKIPPED=${item}"
  done
} | tee "${SUMMARY}"

if [[ "${FAIL}" -ne 0 ]]; then
  demo_die "run-all-automated: FAIL=${FAIL} (see ${SUMMARY})"
fi
if [[ "${STRICT}" -eq 1 && "${SKIP}" -ne 0 ]]; then
  demo_die "run-all-automated: strict mode but SKIP=${SKIP}"
fi
demo_log "run-all-automated: PASS=${PASS} SKIP=${SKIP} FAIL=${FAIL} (see ${SUMMARY})"
