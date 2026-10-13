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

# Read-only environment probe (maintainer instruction, 2026-10-11).
#
# Why this exists
# ---------------
# The environment register (docs/environments.md) used to be filled in by hand,
# which left an un-fillable `infra-<hostname>` placeholder and, before that, the
# disease this repository retracted: prose that said 「本机无 helm」 and was read as
# 「项目不具备该能力」. A register that depends on a human remembering to type a
# hostname will always drift. This script removes the human from the loop: it
# *measures*, and the register is generated from the measurement.
#
# Contract
# --------
#   * Read-only. Installs nothing, writes nothing outside $TMPDIR, changes no
#     system state, needs no root, is safe to re-run any number of times.
#   * Exit code is 0 whenever the probe itself completed — a missing tool is a
#     normal result, not a script failure. Only a usage error exits non-zero (2).
#   * **No credentials, tokens, DSNs or internal addresses are ever printed**
#     (AGENT.md §11 / §13). Only tool paths, versions, hostname, OS and arch.
#
# The three states, which is the part that is easy to get wrong:
#   ✅ 具备          the tool resolves *and* its version command succeeded
#   ❌ 缺失          nothing found, neither tools/bin nor PATH
#   ⚠ 装了但不可用    the binary exists but is not usable (version command exits
#                    non-zero, or exits 0 printing nothing) — installed is not the
#                    same as working, and conflating the two hides broken installs
#
# Usage
# -----
#   tools/env-probe.sh                 human-readable table + the Markdown row
#   tools/env-probe.sh --markdown      only the paste-ready Markdown table
#   tools/env-probe.sh --json          machine-readable (no third-party deps)
#   tools/env-probe.sh --role infra    name becomes infra-<host-slug>
#   tools/env-probe.sh --name my-env   full override of the environment name
#
# Naming rule: <角色>-<hostname 小写去分隔符>, role defaults to `dev`.
#   `WIN-03IB7NIEPF0` -> `dev-win03ib7niepf0` — the row already in
#   docs/environments.md, so the default has to reproduce the register.
# shellcheck shell=bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

MODE="table"
NAME_OVERRIDE=""
ROLE="dev"

usage() {
  # Print the header comment block, but stop at the first non-comment line and
  # drop `# shellcheck shell=bash` — that directive is a machine pragma, not
  # part of the usage text a human reads.
  awk 'NR > 1 && /^#/ && !/^# shellcheck/ { sub(/^# ?/, ""); print; next } NR > 1 { exit }' "$0"
}

die_usage() {
  echo "env-probe: $*" >&2
  usage >&2
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --markdown) MODE="markdown" ;;
    --json) MODE="json" ;;
    --name)
      [[ $# -ge 2 ]] || die_usage "--name requires a value"
      NAME_OVERRIDE="$2"
      shift
      ;;
    --role)
      [[ $# -ge 2 ]] || die_usage "--role requires a value"
      ROLE="$2"
      shift
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *) die_usage "unknown argument: $1" ;;
  esac
  shift
done

# --- facts about the machine -------------------------------------------------

HOSTNAME_RAW="$(uname -n 2>/dev/null || hostname 2>/dev/null || echo unknown)"
ARCH="$(uname -m 2>/dev/null || echo unknown)"

OS="unknown"
if [[ -r /etc/os-release ]]; then
  # `set -e` + an assignment fed by a command substitution: if sourcing the file
  # fails, the assignment itself returns non-zero and the whole script would die
  # before printing anything. A probe that cannot read the OS name must still
  # report on the toolchain, so degrade to `unknown` instead of aborting.
  # shellcheck disable=SC1091
  OS="$(. /etc/os-release >/dev/null 2>&1 && printf '%s' "${PRETTY_NAME:-${NAME:-unknown}}" || echo unknown)"
elif [[ "$(uname -s 2>/dev/null || echo unknown)" == "Darwin" ]]; then
  OS="macOS $(sw_vers -productVersion 2>/dev/null || echo unknown)"
else
  OS="$(uname -s 2>/dev/null || echo unknown)"
fi

# Environment name: **role first**, then the lowercased hostname with separators
# removed. `WIN-03IB7NIEPF0` with the default role becomes `dev-win03ib7niepf0`,
# which is exactly the row already in docs/environments.md — the register is keyed
# on the name, so the default must reproduce it without `--name`.
# `--name` still overrides the whole name; `--role` still only picks the prefix.
# `tr -c` (complement) MUST NOT be used here. In GNU coreutils, `-c`/`-C` switches
# set2 from "the set to translate *to*" into "the characters to leave *alone*", and
# set2 is then not allowed to be empty — `tr -cs '[:alnum:]' ''` dies with
# `tr: when not truncating set1, string2 must be non-empty` and exit 1. That is the
# single defect that made this script fail on every invocation (measured
# 2026-10-11: it had never been run, and `bash -n` cannot see it, because it is a
# runtime argument error, not a syntax error). `-d` (delete) already means exactly
# what we want — throw away everything outside set1 — and needs no set2 at all.
# Do not "optimise" this back into `tr -c`.
slug() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | tr -cd '[:alnum:]'
}

ENV_SLUG="$(slug "${HOSTNAME_RAW}")"
if [[ -z "${ENV_SLUG}" ]]; then
  ENV_SLUG="unknown-host"
fi
ROLE_SLUG="$(slug "${ROLE}")"
if [[ -z "${ROLE_SLUG}" ]]; then
  ROLE_SLUG="dev"
fi
if [[ -n "${NAME_OVERRIDE}" ]]; then
  ENV_NAME="${NAME_OVERRIDE}"
else
  ENV_NAME="${ROLE_SLUG}-${ENV_SLUG}"
fi

# --- tool probing -----------------------------------------------------------

TOOLS=(docker uv python3.10 helm kubectl kind promtool make git)

ICON_OK="✅"
ICON_MISSING="❌"
ICON_BROKEN="⚠" # bare U+26A0: one code point, so the aligned table stays aligned

# Repo-local tools/bin wins over PATH: tools/bootstrap-infra.sh installs there so
# the binaries share the checkout's lifecycle instead of polluting the machine.
resolve_tool() {
  local tool="$1"
  if [[ -x "${ROOT}/tools/bin/${tool}" ]]; then
    printf '%s\n' "${ROOT}/tools/bin/${tool}"
    return 0
  fi
  command -v "${tool}" 2>/dev/null || return 1
}

# Each tool's own version flag. Kept explicit rather than guessed, because the
# wrong flag is one of the ways a working tool gets reported as broken.
version_args() {
  case "$1" in
    docker) printf '%s\n' --version ;;
    uv) printf '%s\n' --version ;;
    python3.10) printf '%s\n' --version ;;
    helm) printf '%s\n' version --short ;;
    kubectl) printf '%s\n' version --client=true -o yaml ;;
    kind) printf '%s\n' version ;;
    promtool) printf '%s\n' --version ;;
    make) printf '%s\n' --version ;;
    git) printf '%s\n' --version ;;
    *) : ;;
  esac
}

STATE=()
CELL_PATH=()
CELL_VERSION=()

# The path cell carries Markdown code ticks, so they are written as \` — an
# unescaped ` inside double quotes is STILL a command substitution in bash, so
# "`${path}`" used to run the tool with no arguments (docker printed its usage
# text, exited 2, and `set -e` killed the probe on its very first tool; measured
# 2026-10-11). `${var#\`}` in the JSON branch was already escaped — this was not.
probe_tool() {
  local tool="$1" path rc raw line first_line="" candidate
  local -a args=()

  if ! path="$(resolve_tool "${tool}")"; then
    STATE+=("MISSING")
    CELL_PATH+=("—")
    CELL_VERSION+=("未找到（tools/bin 与 PATH 均无）")
    return 0
  fi

  while IFS= read -r candidate; do
    [[ -n "${candidate}" ]] && args+=("${candidate}")
  done < <(version_args "${tool}")

  set +e
  if [[ ${#args[@]} -gt 0 ]]; then
    raw="$("${path}" "${args[@]}" 2>&1)"
  else
    raw="$("${path}" 2>&1)"
  fi
  rc=$?
  set -e

  while IFS= read -r line; do
    if [[ -n "${line}" ]]; then
      first_line="${line}"
      break
    fi
  done <<<"${raw}"

  if [[ "${rc}" -ne 0 ]]; then
    STATE+=("BROKEN")
    CELL_PATH+=("\`${path}\`")
    CELL_VERSION+=("版本命令退出码 ${rc}：装了但不可用")
    return 0
  fi
  if [[ -z "${first_line}" ]]; then
    STATE+=("BROKEN")
    CELL_PATH+=("\`${path}\`")
    CELL_VERSION+=("退出码 0 但无版本输出：装了但不可用")
    return 0
  fi
  STATE+=("OK")
  CELL_PATH+=("\`${path}\`")
  CELL_VERSION+=(
    "$(printf '%s' "${first_line}" | tr -s '[:space:]' ' ' | sed 's/^ //; s/ $//' | cut -c1-56)"
  )
}

for tool in "${TOOLS[@]}"; do
  probe_tool "${tool}"
done

icon_for() {
  case "$1" in
    OK) printf '%s' "${ICON_OK}" ;;
    MISSING) printf '%s' "${ICON_MISSING}" ;;
    BROKEN) printf '%s' "${ICON_BROKEN}" ;;
    *) printf '%s' "?" ;;
  esac
}

state_cell() {
  case "$1" in
    OK) printf '%s 具备' "${ICON_OK}" ;;
    MISSING) printf '%s 缺失' "${ICON_MISSING}" ;;
    BROKEN) printf '%s 装了但不可用' "${ICON_BROKEN}" ;;
    *) printf '%s' "?" ;;
  esac
}

tools_in_state() {
  local want="$1" i out=""
  for i in "${!TOOLS[@]}"; do
    if [[ "${STATE[$i]}" == "${want}" ]]; then
      out="${out}${out:+, }${TOOLS[$i]}"
    fi
  done
  printf '%s' "${out:-（无）}"
}

json_escape() {
  # JSON forbids raw control characters below 0x20, so \n \r \t are removed and
  # the two remaining C0 ones a version string could plausibly carry (\b \f) go
  # too. Backslash and double quote are escaped first, otherwise the escapes
  # introduced by the next sed pass would be double-escaped.
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr -d '\n\r\t\010\013'
}

# Markdown table cells are pipe-delimited. A tool version string containing `|`
# silently adds a column and turns the row into nonsense once it is pasted into
# docs/environments.md, and the register guard reads column offsets — so escape
# the pipe. Backticks are deliberately NOT escaped: the path cell already
# carries its own (correctly written, \`-escaped) code ticks, and escaping them
# twice turns `` `/usr/bin/docker` `` into a literal-backtick cell.
md_cell() {
  printf '%s' "$1" | tr '\n\r\t' '   ' | sed 's/|/\\|/g'
}

# --- output -----------------------------------------------------------------

if [[ "${MODE}" == "json" ]]; then
  printf '{\n'
  printf '  "environment_name": "%s",\n' "$(json_escape "${ENV_NAME}")"
  printf '  "hostname": "%s",\n' "$(json_escape "${HOSTNAME_RAW}")"
  printf '  "os": "%s",\n' "$(json_escape "${OS}")"
  printf '  "arch": "%s",\n' "$(json_escape "${ARCH}")"
  printf '  "tools": {\n'
  last=$(( ${#TOOLS[@]} - 1 ))
  for i in "${!TOOLS[@]}"; do
    sep=","
    if [[ "${i}" -eq "${last}" ]]; then
      sep=""
    fi
    bare_path="${CELL_PATH[$i]#\`}"
    bare_path="${bare_path%\`}"
    printf '    "%s": {"state": "%s", "path": "%s", "version": "%s"}%s\n' \
      "${TOOLS[$i]}" "${STATE[$i]}" \
      "$(json_escape "${bare_path}")" \
      "$(json_escape "${CELL_VERSION[$i]}")" "${sep}"
  done
  printf '  }\n'
  printf '}\n'
  exit 0
fi

if [[ "${MODE}" == "markdown" ]]; then
  printf '| 环境名 | hostname | OS | 架构 |'
  for tool in "${TOOLS[@]}"; do
    printf ' %s |' "${tool}"
  done
  printf '\n|'
  i=0
  while [[ "${i}" -le $(( 3 + ${#TOOLS[@]} )) ]]; do
    # `printf '---|'` fails with "printf: --: invalid option": bash's printf
    # parses a leading `-` in the FORMAT argument as an option, so a Markdown
    # rule can never be the format. Route it through %s instead.
    printf '%s' '---|'
    i=$(( i + 1 ))
  done
  printf '\n| `%s` | `%s` | %s | %s |' \
    "$(md_cell "${ENV_NAME}")" "$(md_cell "${HOSTNAME_RAW}")" \
    "$(md_cell "${OS}")" "$(md_cell "${ARCH}")"
  for i in "${!TOOLS[@]}"; do
    printf ' %s %s %s |' \
      "$(icon_for "${STATE[$i]}")" "$(md_cell "${CELL_PATH[$i]}")" \
      "$(md_cell "${CELL_VERSION[$i]}")"
  done
  printf '\n'
  exit 0
fi

# Human-readable table. The state column is sized for the widest label
# (1 icon + 1 space + 6 CJK characters), and every icon is exactly one code point
# so character-count padding lines the columns up in a UTF-8 locale.
width_state=8
width_tool=0
width_path=0
for i in "${!TOOLS[@]}"; do
  if [[ "${#TOOLS[$i]}" -gt "${width_tool}" ]]; then
    width_tool="${#TOOLS[$i]}"
  fi
  if [[ "${#CELL_PATH[$i]}" -gt "${width_path}" ]]; then
    width_path="${#CELL_PATH[$i]}"
  fi
done

echo "环境名：${ENV_NAME}   （规则 = <角色>-<hostname 小写去分隔符>，默认角色 dev；--role 换前缀，--name 整体覆盖）"
echo "hostname：${HOSTNAME_RAW}"
echo "OS：${OS}"
echo "架构：${ARCH}"
if [[ -z "${NAME_OVERRIDE}" ]]; then
  echo "提示：本行由规则生成。若登记表里该环境用的是别的历史命名，用 --name 完全覆盖后重新粘贴。"
fi
echo

rule() {
  # The trailing \n is load-bearing: `rule` is called as a bare command, so
  # without it the rule and the first data row share one physical line and the
  # whole table shifts by one row.
  printf '%s  %s  %s  %s\n' \
    "$(printf '%*s' "${width_state}" '' | tr ' ' '-')" \
    "$(printf '%*s' "${width_tool}" '' | tr ' ' '-')" \
    "$(printf '%*s' "${width_path}" '' | tr ' ' '-')" \
    "--------------------------------"
}

printf '%-*s  %-*s  %-*s  %s\n' "${width_state}" "状态" "${width_tool}" "工具" \
  "${width_path}" "路径" "版本 / 判定依据"
rule
for i in "${!TOOLS[@]}"; do
  printf '%-*s  %-*s  %-*s  %s\n' \
    "${width_state}" "$(state_cell "${STATE[$i]}")" \
    "${width_tool}" "${TOOLS[$i]}" \
    "${width_path}" "${CELL_PATH[$i]}" \
    "${CELL_VERSION[$i]}"
done

echo
echo "✅ 具备：$(tools_in_state OK)"
echo "❌ 缺失：$(tools_in_state MISSING)"
echo "⚠ 装了但不可用：$(tools_in_state BROKEN)"
echo
echo "粘贴进 docs/environments.md 的表格行（等价于 tools/env-probe.sh --markdown）："
MODE="markdown" "${BASH_SOURCE[0]}" --markdown
echo
echo "本脚本只输出工具路径、版本与机器标识；不含任何凭据、token、地址（AGENT.md §11 / §13）。"
