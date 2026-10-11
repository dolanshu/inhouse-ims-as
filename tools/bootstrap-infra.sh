#!/usr/bin/env bash
# Install the infra toolchain into tools/bin/ — no root, no system state changed.
#
# Why tarballs into tools/bin/ and not apt
# ---------------------------------------
# * No root. This machine — and every other one this project may be worked on from
#   — must stay usable without sudo; a plan that needs sudo is a plan that stops.
# * Same lifecycle as the checkout. `git clean -xfd` removes the binaries along
#   with everything else; a distro package outlives the repo and never shows up
#   in `git status`.
# * One version per tool, pinned in tools/VERSIONS and visible in the repository.
#   Two machines with two promtool minor versions produce two different verdicts
#   on the same alert file, and afterwards neither is reproducible.
# apt is not *wrong* — it is simply the wrong default here: it needs root, it
# hands the machine a version nobody pinned, and it leaves the evidence trail
# pointing at a package the repository never mentions.
#
# Contract
# --------
#   * **No root, ever.** A step that would need root fails loudly. This script
#     never runs sudo and never asks you to run it.
#   * **Idempotent**: a tool already present at the pinned version is skipped, so
#     re-running after a partial failure is safe.
#   * `--dry-run` prints every URL and destination and downloads nothing.
#   * Writes only to tools/bin/ and $TMPDIR. Nothing else on the machine moves.
#   * Exits non-zero if any requested tool could not be installed or verified.
#
# Usage
# -----
#   tools/bootstrap-infra.sh              install everything missing
#   tools/bootstrap-infra.sh --dry-run    show the plan, download nothing
#   tools/bootstrap-infra.sh --only kind  install one tool (repeatable)
#   tools/bootstrap-infra.sh --force      reinstall even if already present
#
# shellcheck shell=bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSIONS_FILE="${ROOT}/tools/VERSIONS"
BIN_DIR="${TOOLS_BIN:-${ROOT}/tools/bin}"

DRY_RUN=0
FORCE=0
ONLY=()
FAILED=()

usage() {
  # Print the header comment block, but stop at the first non-comment line and
  # drop `# shellcheck shell=bash` — that directive is a machine pragma, not
  # part of the usage text a human reads.
  awk 'NR > 1 && /^#/ && !/^# shellcheck/ { sub(/^# ?/, ""); print; next } NR > 1 { exit }' "$0"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --force) FORCE=1 ;;
    --only)
      [[ $# -ge 2 ]] || {
        echo "bootstrap-infra: --only requires a tool name" >&2
        exit 2
      }
      ONLY+=("$2")
      shift
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      echo "bootstrap-infra: unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

[[ -r "${VERSIONS_FILE}" ]] || {
  echo "bootstrap-infra: missing ${VERSIONS_FILE}; versions are pinned there, not in this script" >&2
  exit 1
}

# shellcheck disable=SC1090
source <(grep -E '^[A-Z0-9_]+=' "${VERSIONS_FILE}")

for var in HELM_VERSION KUBECTL_VERSION KIND_VERSION PROMETHEUS_VERSION; do
  [[ -n "${!var:-}" ]] || {
    echo "bootstrap-infra: ${var} is not set in ${VERSIONS_FILE}" >&2
    exit 1
  }
done

HOST_OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
case "${HOST_OS}" in
  linux | darwin) ;;
  *)
    echo "bootstrap-infra: unsupported OS '${HOST_OS}'; download URLs are built for linux and" \
      "darwin only. Install the four tools by hand, then record the result in" \
      "docs/environments.md." >&2
    exit 1
    ;;
esac

HOST_ARCH="$(uname -m)"
case "${HOST_ARCH}" in
  x86_64 | amd64) GOARCH="amd64" ;;
  aarch64 | arm64) GOARCH="arm64" ;;
  *)
    echo "bootstrap-infra: unsupported CPU architecture '${HOST_ARCH}' (expected x86_64 or" \
      "aarch64)." >&2
    exit 1
    ;;
esac

# helm / kind / prometheus name their archives <os>-<arch>; kubectl uses <os>/<arch>.
PLAT="${HOST_OS}-${GOARCH}"
PLAT_SLASH="${HOST_OS}/${GOARCH}"

WANTED=(helm kubectl kind promtool)
if [[ ${#ONLY[@]} -gt 0 ]]; then
  WANTED=("${ONLY[@]}")
fi

# --- helpers ----------------------------------------------------------------

log() { printf '%s\n' "$*"; }
warn() { printf 'WARN: %s\n' "$*" >&2; }

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  FAILED+=("$*")
}

ensure_bin_dir() {
  if [[ -d "${BIN_DIR}" ]]; then
    if [[ ! -w "${BIN_DIR}" ]]; then
      echo "bootstrap-infra: ${BIN_DIR} exists but is not writable by $(id -un)." >&2
      echo "  Fix the ownership, or set TOOLS_BIN=<writable dir> and re-run." >&2
      echo "  This script will not sudo." >&2
      exit 1
    fi
    return 0
  fi
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    log "  would create ${BIN_DIR}"
    return 0
  fi
  if ! mkdir -p "${BIN_DIR}"; then
    echo "bootstrap-infra: cannot create ${BIN_DIR} as $(id -un)." >&2
    echo "  Fix the ownership, or set TOOLS_BIN=<writable dir> and re-run." >&2
    echo "  This script will not sudo." >&2
    exit 1
  fi
}

have_downloader() {
  command -v curl >/dev/null 2>&1 || command -v wget >/dev/null 2>&1
}

download() {
  local url="$1" dest="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL --retry 3 --connect-timeout 20 -o "${dest}" "${url}"
  else
    wget -q -O "${dest}" "${url}"
  fi
}

sha256_of() {
  # `sha256sum | awk` under `set -o pipefail` propagates the *reader's* failure
  # too, so an unreadable file aborted the whole script from inside a command
  # substitution. Print an empty result instead and let verify_checksum turn it
  # into a mismatch it can report.
  local file="$1" out=""
  if command -v sha256sum >/dev/null 2>&1; then
    out="$(sha256sum "${file}" 2>/dev/null | awk '{print $1}' || true)"
  else
    out="$(shasum -a 256 "${file}" 2>/dev/null | awk '{print $1}' || true)"
  fi
  printf '%s' "${out}"
}

verify_checksum() {
  local expected="${1:-}" file="$2" actual
  if [[ -z "${expected}" ]]; then
    warn "$(basename "${file}") has no pinned sha256 in tools/VERSIONS: installed unverified."
    warn "  Fetch the official checksum and fill it in to make this step reproducible."
    return 0
  fi
  actual="$(sha256_of "${file}")"
  if [[ "${actual}" != "${expected}" ]]; then
    echo "ERROR: checksum mismatch for $(basename "${file}")" >&2
    echo "  expected ${expected}" >&2
    echo "  actual   ${actual}" >&2
    return 1
  fi
  log "  checksum OK"
}

version_of() {
  local path="$1" raw="" line
  case "$(basename "${path}")" in
    helm) raw="$("${path}" version --short 2>&1 || true)" ;;
    kubectl) raw="$("${path}" version --client=true 2>&1 || true)" ;;
    kind) raw="$("${path}" version 2>&1 || true)" ;;
    promtool) raw="$("${path}" --version 2>&1 || true)" ;;
    *) raw="" ;;
  esac
  # First non-empty line — but deliberately NOT `... | head -1`. Under
  # `set -o pipefail` a producer that outruns its reader is killed by SIGPIPE
  # (exit 141; reproduced with `seq 1 200000 | head -1`), so the *pipeline*, not
  # the tool, would report failure and a correctly installed kubectl would be
  # declared "not at the pinned version" and reinstalled — breaking the
  # idempotency this script promises in its own header. `kubectl version` prints
  # two lines by design, so this path is not hypothetical.
  #
  # Always returns 0: a tool that cannot report a version is a *verdict* for the
  # caller to interpret, never a script error that should abort the run.
  while IFS= read -r line; do
    if [[ -n "${line}" ]]; then
      printf '%s\n' "${line}"
      return 0
    fi
  done <<<"${raw}"
  return 0
}

# installed_version <tool> <pinned> -> 0 when tools/bin/<tool> is already at <pinned>
installed_version() {
  local tool="$1" pinned="$2" path="${BIN_DIR}/${tool}" out=""
  [[ -x "${path}" ]] || return 1
  out="$(version_of "${path}")"
  [[ "${out}" == *"${pinned}"* ]]
}

url_for() {
  case "$1" in
    helm) printf '%s\n' "https://get.helm.sh/helm-v${HELM_VERSION}-${PLAT}.tar.gz" ;;
    kubectl) printf '%s\n' "https://dl.k8s.io/release/v${KUBECTL_VERSION}/bin/${PLAT_SLASH}/kubectl" ;;
    kind) printf '%s\n' "https://kind.sigs.k8s.io/dl/v${KIND_VERSION}/kind-${PLAT}" ;;
    promtool)
      printf '%s\n' \
        "https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VERSION}/prometheus-${PROMETHEUS_VERSION}.${PLAT}.tar.gz"
      ;;
    *)
      # Without this branch an unrecognised name makes the `case` fall off the end
      # and return 0 having printed *nothing* — a blank URL inside a log line,
      # i.e. a silently failed URL assembly. Fail loudly instead.
      echo "bootstrap-infra: no download recipe for '${1}'" >&2
      return 1
      ;;
  esac
}

pinned_for() {
  case "$1" in
    helm) printf '%s\n' "${HELM_VERSION}" ;;
    kubectl) printf '%s\n' "${KUBECTL_VERSION}" ;;
    kind) printf '%s\n' "${KIND_VERSION}" ;;
    promtool) printf '%s\n' "${PROMETHEUS_VERSION}" ;;
    *)
      echo "bootstrap-infra: no pinned version for '${1}'" >&2
      return 1
      ;;
  esac
}

checksum_for() {
  case "$1" in
    helm) printf '%s\n' "${HELM_SHA256:-}" ;;
    kubectl) printf '%s\n' "${KUBECTL_SHA256:-}" ;;
    kind) printf '%s\n' "${KIND_SHA256:-}" ;;
    promtool) printf '%s\n' "${PROMETHEUS_SHA256:-}" ;;
  esac
}

# --- plan -------------------------------------------------------------------

log "bootstrap-infra: target ${BIN_DIR}"
log "bootstrap-infra: platform ${PLAT}"
if ! have_downloader; then
  # A dry run downloads nothing, so it must not need a downloader. Exiting 1 here
  # (as this did) meant `--dry-run` printed not one line of the plan on a machine
  # without curl/wget — the one mode that is supposed to be safe everywhere.
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    warn "neither curl nor wget is on PATH; a real run would fail here."
    warn "  The dry run still prints the full plan, because it downloads nothing."
  else
    echo "bootstrap-infra: neither curl nor wget is available; cannot download anything." >&2
    exit 1
  fi
fi
if [[ "${DRY_RUN}" -eq 1 ]]; then
  log "bootstrap-infra: DRY RUN — nothing is downloaded or written"
fi
ensure_bin_dir

TODO=()
for tool in "${WANTED[@]}"; do
  case "${tool}" in
    helm | kubectl | kind | promtool) ;;
    *)
      echo "bootstrap-infra: unknown tool '${tool}' (helm|kubectl|kind|promtool)" >&2
      exit 2
      ;;
  esac
  # `|| exit 1` on both: url_for / pinned_for return non-zero when they have no
  # recipe for a name, and a bare `$(...)` inside a log argument swallows that
  # status — the run would carry on printing a blank version and a blank URL.
  pinned="$(pinned_for "${tool}")" || exit 1
  url="$(url_for "${tool}")" || exit 1
  log ""
  log "== ${tool} ${pinned}"
  log "   url:  ${url}"
  log "   dest: ${BIN_DIR}/${tool}"
  if [[ "${FORCE}" -eq 0 ]] && installed_version "${tool}" "${pinned}"; then
    log "   status: already at ${pinned} — skipped (use --force to reinstall)"
  else
    if [[ "${FORCE}" -eq 1 ]]; then
      log "   status: --force, will reinstall"
    else
      log "   status: will install"
    fi
    TODO+=("${tool}")
  fi
done

if [[ "${DRY_RUN}" -eq 1 ]]; then
  log ""
  log "bootstrap-infra: dry run complete; nothing was downloaded."
  log "bootstrap-infra: re-run without --dry-run to install."
  exit 0
fi

# --- install ----------------------------------------------------------------

install_from_tarball() {
  local tool="$1" url="$2" strip="$3" inner="$4" expected="${5:-}"
  local tmp extract
  tmp="$(mktemp -d)"
  if ! download "${url}" "${tmp}/archive.tar.gz"; then
    rm -rf "${tmp}"
    fail "${tool}: download failed (${url})"
    return 1
  fi
  if ! verify_checksum "${expected}" "${tmp}/archive.tar.gz"; then
    rm -rf "${tmp}"
    fail "${tool}: checksum verification failed; refusing to install an unverified archive"
    return 1
  fi
  extract="${tmp}/extract"
  mkdir -p "${extract}"
  if ! tar -xzf "${tmp}/archive.tar.gz" -C "${extract}" --strip-components="${strip}"; then
    rm -rf "${tmp}"
    fail "${tool}: archive did not extract"
    return 1
  fi
  if [[ ! -f "${extract}/${inner}" ]]; then
    rm -rf "${tmp}"
    fail "${tool}: archive did not contain ${inner}"
    return 1
  fi
  chmod +x "${extract}/${inner}"
  mv "${extract}/${inner}" "${BIN_DIR}/${tool}"
  rm -rf "${tmp}"
  log "  installed ${BIN_DIR}/${tool}"
}

install_single() {
  local tool="$1" url="$2"
  local tmp
  tmp="$(mktemp -d)"
  if ! download "${url}" "${tmp}/${tool}"; then
    rm -rf "${tmp}"
    fail "${tool}: download failed (${url})"
    return 1
  fi
  chmod +x "${tmp}/${tool}"
  mv "${tmp}/${tool}" "${BIN_DIR}/${tool}"
  rm -rf "${tmp}"
  log "  installed ${BIN_DIR}/${tool}"
}

for tool in "${TODO[@]+"${TODO[@]}"}"; do
  log ""
  log "==> installing ${tool}"
  case "${tool}" in
    helm)
      install_from_tarball helm "$(url_for helm)" 1 \
        "${HOST_OS}-${GOARCH}/helm" "$(checksum_for helm)" || true
      ;;
    kubectl) install_single kubectl "$(url_for kubectl)" || true ;;
    kind) install_single kind "$(url_for kind)" || true ;;
    promtool)
      install_from_tarball promtool "$(url_for promtool)" 1 \
        "prometheus-${PROMETHEUS_VERSION}.${PLAT}/promtool" "$(checksum_for promtool)" || true
      ;;
  esac
done

# --- verify -----------------------------------------------------------------

log ""
log "==> verifying"
for tool in "${WANTED[@]}"; do
  path="${BIN_DIR}/${tool}"
  if [[ ! -x "${path}" ]]; then
    fail "${tool}: still missing at ${path}"
    continue
  fi
  out="$(version_of "${path}" || true)"
  if [[ -z "${out}" ]]; then
    fail "${tool}: present at ${path} but running it produced no version output (装了但不可用)"
    continue
  fi
  pinned="$(pinned_for "${tool}")"
  if [[ "${out}" == *"${pinned}"* ]]; then
    log "  OK   ${tool} ${out}"
  else
    fail "${tool}: runs, but reports '${out}' instead of the pinned ${pinned}"
  fi
done

# --- hand over to the probe -------------------------------------------------

if [[ ${#FAILED[@]} -eq 0 ]]; then
  log ""
  log "==> handing over to tools/env-probe.sh"
  log "    export PATH=\"${BIN_DIR}:\${PATH}\"   # or rely on tools/bin being resolved directly"
  log "    环境名由 env-probe.sh 按默认规则 <角色>-<hostname 小写去分隔符> 生成（角色默认 dev）；"
  log "    要换前缀加 --role，要完全覆盖加 --name（见 docs/environments.md §3 第 4 条）。"
  "${ROOT}/tools/env-probe.sh" || warn "env-probe.sh exited non-zero; read its output"
else
  log ""
  printf 'bootstrap-infra: FAILED — %s\n' "${FAILED[@]}" >&2
  log "bootstrap-infra: the machine is NOT ready. Fix the items above and re-run; the script" >&2
  log "  is idempotent, so a partial install is a safe starting point." >&2
  exit 1
fi

log ""
log "bootstrap-infra: done. tools/bin/ holds no credentials and is not committed (see .gitignore)."
