# M8 environment evidence directory (redaction convention)

> Basis: `docs/handoff/2026-10-06-m8-release-candidate-plan.md` §4 Phase D;
> recording carrier: `docs/acceptance/m8-environment-evidence.md`.

## Directory structure

```text
docs/acceptance/artifacts/m8/
  README.md                # this file (convention description)
  <date>/                  # evidence-collection date directory, e.g. 2026-10-06 (created when maintainer collects on-site)
    req-s-2-pki/           # REQ-S-2: operator PKI / S-SBC TLS
    req-s-3-rotation/      # REQ-S-3: lossless certificate rotation
    req-nf-1-live/         # REQ-NF-1: customer K8s live kill/restart/BYE
```

The placeholder subdirectories (`req-s-2-pki/`, `req-s-3-rotation/`, `req-nf-1-live/`, same level as this README)
each contain a `README.md`, currently all in the state **awaiting maintainer on-site evidence collection**, with no fabricated evidence.

## `.gitignore` note (checked this time, no modification needed)

- This repo's `.gitignore` includes `artifacts/` but also an exception `!docs/acceptance/artifacts/`,
  so `docs/acceptance/artifacts/m8/` **can be tracked** (verified with `git check-ignore`: no ignore hit).
- Secret extensions (`*.log` / `*.pcap` / `*.pcapng`, etc.) are still ignored, which is **expected behavior**:
  M8 requires "reviewable redacted evidence"; real captures and secrets should not be committed anyway.
- Conclusion: this time **no modification** to `.gitignore`; if tightening is needed in the future (e.g. adding `*.key` global ignore),
  it must be evaluated separately to avoid accidentally harming placeholder files like `deploy/**/certs/.gitkeep`.

## Redaction red line (reiterated)

- **Must not commit**: private keys (`*.key`), certificate plaintext (`*.pem` / `*.crt` real content),
  real captures (`*.pcap` / `*.pcapng`), logs containing passwords / tokens / real numbers.
- Allowed to commit: command transcripts (sensitive fields masked), `openssl x509 -noout -subject -issuer -dates`
  metadata output (serial/fingerprint masked or truncated), version numbers and image tags.
