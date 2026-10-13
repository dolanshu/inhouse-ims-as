# REQ-NF-1 live on-site evidence (restriction: no collection before Close)

> **Status**: restriction (2026-10-07). No customer K8s live kill/restart/BYE evidence collection before Close. This directory stays empty.
> Requirement: `docs/acceptance/test-plan.md` §2 REQ-NF-1; `docs/plan.md` §5.2 D10;
> recording: `docs/acceptance/m8-environment-evidence.md` D-2.
> Engineering harness (non-live acceptance) see `platform/tests/test_d10_product_recovery_integration.py`,
> `platform/tests/test_d10_req_nf1_harness_integration.py`, etc. M7 D10 slices.

## Files to submit when collecting evidence (redacted)

1. `README.md` (this file updated to the collection record): cluster info (version, node count), image tag, Helm values version,
   kill/restart timeline, executor, referenced runbook version.
2. `kill-restart.transcript.md`: `kubectl delete pod / rollout restart` command transcript (object names masked).
3. `dialog-recovery.redacted.md`: dialog state comparison before and after restart (redacted log excerpts, Call-ID masked or truncated).
4. `bye-verdict.txt`: BYE cross-check verdict (text verdict that both-leg hang-up behavior meets expectations + redacted excerpt).

## Prohibited from submission

**Do not submit private keys, certificate plaintext, or real captures** (`*.key` / `*.pem` real content / `*.pcap` / `*.pcapng` /
logs containing passwords or real numbers / full plaintext Call-IDs). Violating files will be blocked by `.gitignore` or must be directly rejected from the repo during review.
