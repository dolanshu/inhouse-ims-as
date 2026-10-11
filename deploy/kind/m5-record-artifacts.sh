#!/usr/bin/env bash
# Write redacted M5.1 verification transcripts into docs/acceptance/artifacts/m5/ (review G-1 / G-5).
#
# ---------------------------------------------------------------------------
# Exit-code discipline (2026-10-11)
# ---------------------------------------------------------------------------
# Every transcript used to be collected as
#
#     make <target> 2>&1 | strip_ansi > "${OUT}/<subject>.txt"
#
# A pipeline's status is the status of its *last* command, so the code that used
# to decide pass/fail was `strip_ansi`'s (always 0) — never `make`'s. A failing
# `make` therefore produced a file named like a pass, and the script went on to
# print "wrote under ...". Since 2026-10-11 the file name *is* the verdict
# (four-layer evidence mechanism, open-adjudication-register §7.4 layer 1), which
# makes that strictly worse than the old bug: it manufactures a `PASS-` file full
# of failure output.
#
# The rules this script now follows:
#
#   1. Capture the collected command's own exit code — `PIPESTATUS[0]`, never the
#      status of the ANSI filter.
#   2. exit 0 -> `PASS-<stem>-<date>.txt`; non-zero -> `FAIL-<stem>-<date>.txt`.
#      The real exit code is written into the file header *and* echoed here.
#   3. A failing command must NOT abort the script. Its transcript is the only
#      proof that it failed, so errexit is suspended *around the command only*
#      (`set +e` -> capture `PIPESTATUS[0]` -> `set -e`), failures are accumulated,
#      and the script exits non-zero at the very end naming every failed item.
#      A run that fails halfway still yields evidence instead of nothing at all.
#   4. `m5-strict-context` is *always* `FAILCLOSED-`, whatever the outcome: it
#      records the M5_STRICT=1 fail-closed path, which is never a pass.
# shellcheck shell=bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DATE="${M5_ARTIFACT_DATE:-$(date -u +%Y-%m-%d)}"
OUT="${ROOT}/docs/acceptance/artifacts/m5/${DATE}"
mkdir -p "${OUT}"

export NO_COLOR=1
export TERM=dumb

WORK="$(mktemp -d)"
trap 'rm -rf "${WORK}"' EXIT

# ---------------------------------------------------------------------------
# promtool resolution — one hard-coded path is not a lookup order
# ---------------------------------------------------------------------------
# Order: repo-local tools/bin (populated by tools/bootstrap-infra.sh, so the tool
# shares the checkout's lifecycle) -> PATH -> the legacy /tmp tarball, kept only
# as a last-resort fallback for older runbooks. When none of the three resolves,
# alert-check is NOT skipped silently: the run still happens, the transcript says
# promtool is unavailable, and the artifact is named FAIL-.
PROMTOOL_TRIED='tools/bin/promtool -> PATH -> /tmp/prometheus-2.55.1.linux-amd64/promtool'
PROMTOOL=""
for candidate in \
  "${ROOT}/tools/bin/promtool" \
  "$(command -v promtool 2>/dev/null || true)" \
  "/tmp/prometheus-2.55.1.linux-amd64/promtool"; do
  if [[ -n "${candidate}" && -x "${candidate}" ]]; then
    PROMTOOL="${candidate}"
    break
  fi
done
if [[ -n "${PROMTOOL}" ]]; then
  export PATH="$(cd "$(dirname "${PROMTOOL}")" && pwd):${PATH}"
  echo "==> promtool: ${PROMTOOL}"
else
  echo "==> promtool: NOT AVAILABLE (searched: ${PROMTOOL_TRIED})" >&2
fi

strip_ansi() {
  sed -E 's/\x1B\[[0-9;]*[[:alpha:]]//g'
}

# Accumulated failures; a non-empty value makes the script exit non-zero at the end.
FAILED_ITEMS=""
WRITTEN=""

note_failure() {
  FAILED_ITEMS="${FAILED_ITEMS}  - $1"$'\n'
}

note_written() {
  WRITTEN="${WRITTEN}  $1"$'\n'
}

# write_evidence <stem> <exit-code> <command-label> <body-file>
#
# Writes `<verdict>-<stem>-<date>.txt` with the verdict taken from the exit code.
# The header records what ran and what it returned, so the file is readable on its
# own without the index.
write_evidence() {
  local stem="$1" rc="$2" label="$3" body="$4"
  local verdict="PASS"
  if [[ "${rc}" -ne 0 ]]; then
    verdict="FAIL"
  fi
  {
    printf '# subject: %s\n' "${stem}"
    printf '# command: %s\n' "${label}"
    printf '# exit-code: %s\n' "${rc}"
    printf '# verdict: %s\n' "${verdict}"
    printf '# recorded-by: deploy/kind/m5-record-artifacts.sh on %s\n' "${DATE}"
    printf '# --- transcript begin ---\n'
    cat "${body}"
    printf '# --- transcript end ---\n'
  } >"${OUT}/${verdict}-${stem}-${DATE}.txt"
  note_written "${verdict}-${stem}-${DATE}.txt"
  printf '    %-10s %-26s exit=%s\n' "${verdict}" "${stem}" "${rc}"
}

# splice_note <evidence-file> <note-file>
#
# Insert a note between the header and the transcript of an already-written
# evidence file, keeping the recorded verdict and exit code.
splice_note() {
  local evidence_file="$1" note_file="$2"
  [[ -f "${evidence_file}" ]] || return 0
  # Both halves are staged before the redirection below, because `{ ... } > "$f"`
  # truncates $f *before* the commands inside it run — reading $f inside the block
  # would read an empty file and the header would be lost.
  sed -n '1,/^# --- transcript begin ---$/p' "${evidence_file}" >"${WORK}/head.tmp"
  sed '1,/^# --- transcript begin ---$/d' "${evidence_file}" >"${WORK}/body.tmp"
  {
    cat "${WORK}/head.tmp"
    cat "${note_file}"
    cat "${WORK}/body.tmp"
  } >"${evidence_file}"
}

# capture <stem> <label> <tail|copy> <command...>
#
# Runs the command with errexit suspended, then writes the full transcript and its
# sample. `tail` = last 5 lines (gate); `copy` = the whole run (chart / alert).
capture() {
  local stem="$1" label="$2" mode="$3"
  shift 3
  local body="${WORK}/${stem}.full"
  local sample="${WORK}/${stem}.sample"
  local rc=0

  # This is the only place in the script where a non-zero status is expected to
  # survive instead of aborting the run: the failing transcript is the evidence.
  set +e
  "$@" 2>&1 | strip_ansi >"${body}"
  rc="${PIPESTATUS[0]}"
  set -e

  if [[ "${mode}" == "tail" ]]; then
    tail -5 "${body}" >"${sample}"
  else
    cp "${body}" "${sample}"
  fi

  write_evidence "${stem}" "${rc}" "${label}" "${body}"
  write_evidence "${stem}-sample" "${rc}" "${label} (sample)" "${sample}"

  if [[ "${rc}" -ne 0 ]]; then
    note_failure "${label} (exit=${rc})"
  fi
}

cd "${ROOT}"

echo "==> gate"
capture gate "make gate" tail make gate

echo "==> chart-check"
capture chart-check "make chart-check" copy make chart-check

echo "==> alert-check"
if [[ -z "${PROMTOOL}" ]]; then
  printf 'NOTE: promtool is unavailable on this machine (searched: %s).\n' "${PROMTOOL_TRIED}" \
    >"${WORK}/alert-note"
  printf 'NOTE: "make alert-check" requires it; this artifact is the FAIL- record of that.\n' \
    >>"${WORK}/alert-note"
  printf '\n' >>"${WORK}/alert-note"
fi
capture alert-check "make alert-check" copy make alert-check
if [[ -z "${PROMTOOL}" ]]; then
  for stem in alert-check alert-check-sample; do
    splice_note "${OUT}/FAIL-${stem}-${DATE}.txt" "${WORK}/alert-note"
    splice_note "${OUT}/PASS-${stem}-${DATE}.txt" "${WORK}/alert-note"
  done
fi

# ---------------------------------------------------------------------------
# Strict-context transcript — always FAILCLOSED, never PASS
# ---------------------------------------------------------------------------
CLUSTER="${KIND_CLUSTER_NAME:-as-m5}"
STRICT_BODY="${WORK}/m5-strict-context.body"
{
  echo "M5_STRICT=1 cluster=kind-${CLUSTER}"
  echo "host has no guarantee of a live kind cluster; this transcript records the fail-closed path."
} >"${STRICT_BODY}"

set +e
bash -c "source '${ROOT}/deploy/kind/m5-lib.sh'; export M5_STRICT=1; export KIND_CLUSTER_NAME='${CLUSTER}'; m5_require_kind_context" \
  >>"${STRICT_BODY}" 2>&1
STRICT_RC=$?
set -e
echo "exit=${STRICT_RC}" >>"${STRICT_BODY}"

CLUSTER_PRESENT=0
if kubectl config get-contexts -o name 2>/dev/null | grep -qx "kind-${CLUSTER}"; then
  CLUSTER_PRESENT=1
fi

if [[ "${CLUSTER_PRESENT}" -eq 0 ]]; then
  echo "no live kind-${CLUSTER}; fail-closed transcript is FAILCLOSED-m5-strict-context-${DATE}.txt" \
    >>"${STRICT_BODY}"
  if [[ "${STRICT_RC}" -eq 0 ]]; then
    # M5_STRICT=1 with no cluster is documented to fail closed. exit 0 here means
    # the fail-closed guard regressed, which is a real defect, not a pass.
    note_failure "missing kind-${CLUSTER} did NOT fail under M5_STRICT=1 (exit=0): fail-closed guard regressed"
  fi
fi

{
  printf '# subject: m5-strict-context\n'
  printf '# command: M5_STRICT=1 m5_require_kind_context (cluster kind-%s)\n' "${CLUSTER}"
  printf '# exit-code: %s\n' "${STRICT_RC}"
  printf '# verdict: FAILCLOSED\n'
  printf '# note: records the fail-closed path itself; NOT pass evidence\n'
  printf '# recorded-by: deploy/kind/m5-record-artifacts.sh on %s\n' "${DATE}"
  printf '# --- transcript begin ---\n'
  cat "${STRICT_BODY}"
  printf '# --- transcript end ---\n'
} >"${OUT}/FAILCLOSED-m5-strict-context-${DATE}.txt"
note_written "FAILCLOSED-m5-strict-context-${DATE}.txt"
printf '    %-10s %-26s exit=%s\n' "FAILCLOSED" "m5-strict-context" "${STRICT_RC}"

# The strict transcript is FAILCLOSED by construction, so it never enters
# FAILED_ITEMS. Contradictions between the two observations below do.
if [[ "${CLUSTER_PRESENT}" -eq 1 ]]; then
  if [[ "${STRICT_RC}" -ne 0 ]]; then
    note_failure "kind-${CLUSTER} context exists but M5_STRICT=1 context check failed (exit=${STRICT_RC})"
  fi
  echo "==> live cluster: M5_STRICT=1 m5-verify (may take several minutes)"
  capture m5-verify-strict "M5_STRICT=1 bash deploy/kind/m5-verify.sh" copy \
    env M5_STRICT=1 bash "${ROOT}/deploy/kind/m5-verify.sh"
fi

# ---------------------------------------------------------------------------
# Summary — always say which artifacts exist and which runs failed
# ---------------------------------------------------------------------------
echo
echo "==> wrote under ${OUT}"
printf '%s' "${WRITTEN}" | sed '/^$/d'

if [[ -n "${FAILED_ITEMS}" ]]; then
  echo >&2
  printf 'm5-record-artifacts: FAILED — %s' "${FAILED_ITEMS}" >&2
  echo "m5-record-artifacts: those runs are on disk as FAIL-*.txt above; this run is NOT a pass." >&2
  exit 1
fi

echo "m5-record-artifacts: every collected command exited 0 (m5-strict-context stays FAILCLOSED by design)"
