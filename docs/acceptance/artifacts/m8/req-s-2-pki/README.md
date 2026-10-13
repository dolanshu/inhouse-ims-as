# REQ-S-2 on-site evidence (restriction: no collection before Close)

> **Status**: restriction (2026-10-07). No real operator S-SBC / operator PKI evidence collection before Close. This directory stays empty.
> Requirement: `docs/acceptance/test-plan.md` §3 REQ-S-2; recording: `docs/acceptance/m8-environment-evidence.md` D-1.

## Files to submit when collecting evidence (redacted)

1. `README.md` (this file updated to the collection record): collection date, environment (operator PKI lab name masked), executor, tested version tag, runbook version.
2. `tls-handshake.transcript.md`: AS→S-SBC TLS handshake command transcript (target address/port masked), verdict is handshake success.
3. `plaintext-rejected.transcript.md`: command transcript of plaintext 5060 connection being rejected (failure excerpt).
4. `pki-chain.txt`: `openssl verify -CAfile <masked path>` verdict excerpt + `openssl x509 -noout -subject -issuer -dates`
   metadata output (serial/fingerprint masked or truncated, no certificate plaintext pasted).

## Prohibited from submission

**Do not submit private keys, certificate plaintext, or real captures** (`*.key` / `*.pem` real content / `*.pcap` / `*.pcapng` /
logs containing passwords or real numbers). Violating files will be blocked by `.gitignore` or must be directly rejected from the repo during review.
