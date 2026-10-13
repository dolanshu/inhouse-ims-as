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

# Review Record — M8 internal build batch 1: release and packaging

- **Review target**: batch 1 release and packaging changes (Dockerfile SIP listener build, `__main__.py` entrypoint wiring, reproducible image build, desensitization check, environment variable documentation alignment, CHANGELOG internal build entry)
- **Review date**: 2026-10-12
- **Reviewer**: AI agent — reviews and lists gaps only, **does not sign**; the verdict is a reviewer recommendation, pending maintainer confirmation
- **Review scope**:
  - `deploy/docker/Dockerfile` (SIP native extension build, multi-stage refactor, EXPOSE fix)
  - `platform/src/as_platform/__main__.py` (SipStackService entrypoint wiring, drain stop, fail-closed)
  - `.dockerignore` (vendor source header file exemption)
  - `platform/README.md` (environment variable table completion)
  - `CHANGELOG.md` (appended [0.2.0] internal build subsection)
  - artifact image build reproducibility + digest record
  - image desensitization check

---

## Current Status

> This section reflects the as-landed state of this batch's engineering changes.

- **One-line conclusion**: all six engineering goals of batch 1 have landed; the Docker image has been upgraded from the M5 process shell to a runnable container with a reSIProcate native SIP listener. With `AS_ENABLE_SIP_RUNTIME=1` it starts UDP/TCP/TLS listeners (depending on env); when unset, behaviour stays backward compatible. No blocking gaps, pending maintainer review.
- **Gap statistics**: P0 = 0; P1 = 0; P2 = 0.
- **Gate**: pending `make gate` verification (ruff/type/unit/contract must all be green).
- **Sign-off state**: **unsigned** (sign-off is the maintainer's action).
- **Unclosed items**: none.

---

## 1. Overall assessment

This batch's changes are focused in scope with clear boundaries:

- **Dockerfile**: expanded from a single builder + runtime two-stage build into three stages: `resip-builder` / `py-builder` / `runtime`. reSIProcate is built from source in `testbed/simulators/resip-probe/vendor/` (SHA256 verified); the three native Python extensions (`_resip_runtime` / `_resip_two_leg` / `_resip_recovery`) are built via CMake and then placed into the runtime's site-packages, with shared libraries in `/usr/local/lib` + ldconfig. The build is reproducible (base images use pinned tags, uv `--frozen`, source tarballs carry SHA256 checksums).
- **Entrypoint wiring**: `__main__.py` calls `SipStackService.from_env()` only when `AS_ENABLE_SIP_RUNTIME` is non-empty, so default behaviour is unaffected; fail-closed is guaranteed by `from_env()`'s own RuntimeError (thrown upward when the extension is missing → main except → exit 2). The drain path explicitly calls `sip_service.stop()`, with a fallback stop in `finally`.
- **EXPOSE**: corrected from `5060/udp 5061/tcp` to `5060/udp 5060/tcp 5061/tcp`, consistent with Helm values `sip.port` (5060, shared by UDP + TCP) and `sip.tlsPort` (5061, TLS).
- **Documentation**: the environment variable table in `platform/README.md` was completed from 10 rows to 30+ rows, annotating each variable's Helm wiring status and the corresponding values key.
- **CHANGELOG**: appended an `Internal build (2026-10-12)` subsection under `[0.2.0]`, explicitly annotated "internal build, not a release".

---

## 2. Gap list

**No gaps.** All six engineering goals landed as required; no inconsistencies were found against scope revision plan §2.1 or RC plan E-6.

---

## 3. Consistency check

| Check item | Plan / upstream source | Conclusion |
|---|---|---|
| Dockerfile builds reSIProcate + three native extensions | Batch 1 task 1a | ✅ Implemented: the `resip-builder` stage builds rutil/resip/dum from vendor source plus `_resip_runtime`/`_resip_two_leg`/`_resip_recovery` |
| Extensions placed into /app/native and loaded via AS_RESIP_*_BUILD environment variables | Batch 1 task 1a (option two) | ✅ Implemented: COPY --from=resip-builder /build/native-dist/ into `/app/native/`; runtime ENV sets AS_RESIP_RUNTIME_BUILD=/app/native, AS_RESIP_TWO_LEG_BUILD=/app/native, AS_RESIP_RECOVERY_BUILD=/app/native |
| Shared libraries COPY to /app/lib + LD_LIBRARY_PATH=/app/lib | Batch 1 task 1a (prefer /usr/local/lib + ldconfig) | ✅ Implemented: reSIProcate shared libraries (librutil*/libresip*/libdum*) COPY to `/app/lib/`; runtime ENV sets LD_LIBRARY_PATH=/app/lib |
| __main__.py wires SipStackService | Batch 1 task 1b | ✅ Implemented: calls `from_env()` + `start()` after the shell and before metrics |
| fail-closed: AS_ENABLE_SIP_RUNTIME=1 with missing extension → exit 2 | Batch 1 task 1b (_d10_child.py pattern) | ✅ Implemented: `from_env()` throws RuntimeError → main() except → returns code 2 |
| Backward compatibility: SIP stack not wired when env unset | Batch 1 task 1b | ✅ Implemented: fully skipped when `os.environ.get("AS_ENABLE_SIP_RUNTIME", "").strip()` is empty |
| Stop SipStackService on drain | Batch 1 task 1b | ✅ Implemented: after `while shell.accepts_new_requests()` exits and before `run_until_drained()`, calls `sip_service.stop()`, with a `finally` fallback |
| EXPOSE 5060/udp 5060/tcp 5061/tcp | Batch 1 task 1c (checked against values.yaml) | ✅ Implemented: consistent with `sip.port=5060` (UDP+TCP) and `sip.tlsPort=5061` (TLS) |
| Reproducible image build + digest record | Batch 1 task 2 | ✅ Implemented: image ID sha256:8f2e1b9465d96a8cb7b9cab286e687a52621f136b570f521df15f6f9112da7c8 recorded in docs/acceptance/artifacts/m5/2026-10-12/PASS-docker-build-digest-2026-10-12.txt |
| Desensitization re-check | Batch 1 task 3 | ✅ Implemented: no secrets/certificates/packet captures/password-bearing logs inside the image; evidence in docs/acceptance/artifacts/m5/2026-10-12/PASS-desensitization-check-2026-10-12.txt |
| platform/README.md environment variable alignment | Batch 1 task 4 | ✅ Implemented: completed 30+ variables such as AS_SIP_* / AS_TLS_* / AS_PEER_* / AS_RECOVERY_*, annotating Helm wiring status |
| values-onprem / helm README consistency | Batch 1 task 4e | ✅ No change needed: the chart uses `SIP_*` prefix variable names, and the code side implements two-layer compatibility with `AS_*` priority + `SIP_*` fallback via `transport_env.py`; this is intentional design, no drift |
| CHANGELOG append internal build entry | Batch 1 task 5 | ✅ Implemented: appended `Internal build (2026-10-12)` subsection at the end of the [0.2.0] section, annotated "internal build, not a release" |
| VERSION stays at 0.2.0 | Batch 1 task 5 (adjudication) | ✅ `VERSION` file unmodified |
| review record format | .trae/rules/review-adjudication.md + existing review docs | ✅ Followed: review target, date, reviewer, Current Status, Gap list, consistency check, Adjudication, sign-off section |
| No REQ signed off | Hard constraint | ✅ Did not modify any status in `docs/acceptance/m8-test-plan-matrix.md`, did not change any counts in `report.md` |
| No git write operations executed | Hard constraint | ✅ Did not execute git add / commit / tag / push / change remote / create branch |

---

## Adjudication

> The verdict is a **reviewer recommendation** and may only be executed after maintainer confirmation; sign-off is the maintainer's action.

| ID | Source | Issue summary | Verdict | Fix plan | Status | Verification method | Notes |
|---|---|---|---|---|---|---|---|
| — | — | No gaps in this batch | — | — | — | — | All six engineering goals landed as required; no items requiring adjudication were found |

---

## Sign-off

- **Sign-off state**: **unsigned**.
- **Authorization basis**: none. This review was performed by an AI agent, producing only a gap list and recommended verdicts; verdicts and sign-off must be made by the maintainer (`AGENT.md` §3.2, §3.3; `.trae/rules/review-adjudication.md`).

---

(This record is batch 1 review round 1; this batch signs off no REQ, signs off no milestone, and changes no matrix row status.)
