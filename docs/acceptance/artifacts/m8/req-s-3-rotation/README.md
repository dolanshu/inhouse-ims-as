# REQ-S-3 on-site evidence (restriction: no collection before Close)

> **Status**: restriction (2026-10-07). No real peer-side operator certificate rotation evidence collection before Close. This directory stays empty.
> Requirement: `docs/acceptance/test-plan.md` §3 REQ-S-3; recording: `docs/acceptance/m8-environment-evidence.md` D-1.

## Files to submit when collecting evidence (redacted)

1. `README.md` (this file updated to the collection record): rotation window start/end time, environment, executor, tested version tag, old/new certificate metadata comparison.
2. `rotation-window.txt`: proof of old/new certificate coexistence (`openssl x509 -noout -subject -issuer -dates` metadata output, masked).
3. `calls-unaffected.log.redacted.md`: observation record that existing calls during rotation were unaffected (redacted log excerpt, Call-ID masked or truncated).
4. `new-connections.txt`: verification excerpt that new TLS connections during rotation used the new certificate (command transcript, masked).

## Prohibited from submission

**Do not submit private keys, certificate plaintext, or real captures** (`*.key` / `*.pem` real content / `*.pcap` / `*.pcapng` /
logs containing passwords or real numbers). Violating files will be blocked by `.gitignore` or must be directly rejected from the repo during review.
