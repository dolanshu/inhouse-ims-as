#!/usr/bin/env bash
# Keep deploy/helm/Chart.yaml's version/appVersion in step with the root VERSION file.
#
# Adjudication (maintainer, 2026-10-12): the answer to A6's "由谁改" is (a) —
# the synchronisation lives in the release flow / a script, not in someone's memory.
# The root VERSION file stays the single source (G4, adjudicated 2026-10-10); this
# script only ever writes *from* it *into* the chart.
#
# Safety: the default mode is --check, which never writes. Writing requires an
# explicit --apply. G4 also says "当前不修改 VERSION 与 Chart.yaml"; this script
# therefore only provides the capability — when the first real sync happens, and
# what value it lands on, is a maintainer decision.
#
# Usage:
#   scripts/sync-chart-version.sh            # --check (default): report drift, exit 1 if any
#   scripts/sync-chart-version.sh --check    # same
#   scripts/sync-chart-version.sh --apply    # write Chart.yaml from the root VERSION

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION_FILE="${REPO_ROOT}/VERSION"
CHART_FILE="${REPO_ROOT}/deploy/helm/Chart.yaml"

MODE="${1:---check}"

log() { echo "[sync-chart-version] $*"; }
die() { echo "[sync-chart-version] error: $*" >&2; exit 1; }

[[ -f "$VERSION_FILE" ]] || die "missing $VERSION_FILE"
[[ -f "$CHART_FILE" ]] || die "missing $CHART_FILE"

product_version="$(tr -d '[:space:]' <"$VERSION_FILE")"
[[ -n "$product_version" ]] || die "$VERSION_FILE is empty"

# Read the two fields without a YAML parser: both are top-level scalars in Chart.yaml.
chart_version="$(sed -n 's/^version:[[:space:]]*//p' "$CHART_FILE" | head -n1)"
chart_app_version="$(sed -n 's/^appVersion:[[:space:]]*//p' "$CHART_FILE" | head -n1)"
chart_app_version="${chart_app_version%\"}"
chart_app_version="${chart_app_version#\"}"

case "$MODE" in
  --check)
    drift=0
    if [[ "$chart_version" != "$product_version" ]]; then
      log "DRIFT version:     Chart.yaml='${chart_version}'  VERSION='${product_version}'"
      drift=1
    fi
    if [[ "$chart_app_version" != "$product_version" ]]; then
      log "DRIFT appVersion:  Chart.yaml='${chart_app_version}'  VERSION='${product_version}'"
      drift=1
    fi
    if ((drift)); then
      log "chart is out of step with the root VERSION; run with --apply to synchronise"
      exit 1
    fi
    log "OK: Chart.yaml version/appVersion both = '${product_version}'"
    ;;
  --apply)
    tmp="$(mktemp)"
    # Only rewrite the two top-level scalar lines; everything else is byte-preserved.
    awk -v v="$product_version" '
      /^version:[[:space:]]*/   { print "version: " v;         next }
      /^appVersion:[[:space:]]*/{ print "appVersion: \"" v "\""; next }
      { print }
    ' "$CHART_FILE" >"$tmp"
    mv "$tmp" "$CHART_FILE"
    log "applied: Chart.yaml version/appVersion -> '${product_version}'"
    ;;
  *)
    die "unknown mode '${MODE}' (use --check or --apply)"
    ;;
esac
