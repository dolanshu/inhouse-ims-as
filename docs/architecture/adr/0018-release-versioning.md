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

# ADR-0018: Unified product release version + independent component interface versions

- **Status**: accepted
- **Date**: 2026-09-28
- **Decides**: §11.3 — one product release version, independent component interface versions; eliminate VERSION drift
- **Responds to REQ**: REQ-NF-11

---

## Context

VERSION drift already occurred in the POC phase: the root `VERSION` file declared `0.2.0`, but each component's own `pyproject.toml` said `0.1.0` — two numbers in two places, with no automated guard preventing the drift. `AGENT.md` §8 explicitly lists this as one of the three defects the monorepo must eliminate.

This product is delivered as **one system per customer**. What we deliver to the carrier is a complete system version, not a combination of independent component versions. The carrier receives a Docker image set + Helm chart; the version number should be a single release number, not one version number per component for ops to align.

The monorepo + uv workspace (ADR-0001) provides the technical foundation for unified version governance: all components live in one repo, so version-consistency can be centrally validated in a single local gate, without cross-repo scripts.

`AGENT.md` §8 already has a clear rule draft:
- `./VERSION` is the **single source** of the product release version;
- `<member>/pyproject.toml` carries that component's own interface version;
- **no member may have a `VERSION` file**;
- `tests/test_version_consistency.py` guards that VERSION is SemVer and that the latest CHANGELOG heading equals it.

## Decision

The root `./VERSION` file is the **single source** of the product release version. The product is delivered under one release version number; each release bumps the root VERSION and synchronously updates the latest CHANGELOG heading.

Each component (`platform/`, `apps/*`, `services/*`) may declare an **independent interface version** (semantic SemVer) in its own `pyproject.toml`, for upstream consumers to reference. The component interface version and the product release version are independent: interface `0.3.1` can appear inside product release `1.2.0`.

**No component may have an independent `VERSION` file.** The root VERSION is the only release-version source; components keep only the interface version in `pyproject.toml`. The validity and consistency of these two versions are auto-guarded by `tests/test_version_consistency.py`.

The complete version-governance constraints are defined by `AGENT.md` §8; this ADR hardens the binary structure of root VERSION + pyproject interface version, and their guard mechanism.

## Consequences

### Positive

- **Eliminates VERSION drift.** The root VERSION is the only source of the release; automated tests guard its SemVer validity against CHANGELOG and each component's `pyproject.toml`. The POC situation where VERSION and pyproject each reported their own number will not recur.
- **Clear, traceable delivery version number.** Carrier ops receives a release number (e.g., `as-product@1.0.0`) that can be traced directly to the Git tag, CHANGELOG entry, and Helm chart version, without aligning component versions themselves.
- **Independent component interface version declaration.** An API change across a component boundary (e.g., `platform`'s interface to `apps` bumping from `0.1.0` to `0.2.0`) has a semantic marker, so consumers can explicitly pin or handle compatibility.

### Negative / accepted

- **Slightly more complex version governance.** Maintaining both the root VERSION and each component's pyproject interface version. But `tests/test_version_consistency.py` reduces the manual maintenance burden to zero — `make gate` auto-runs SemVer validity checks and CHANGELOG heading alignment on every run, blocking the PR on violation.
- **Need to distinguish the two concepts "release version" and "interface version".** The product release number describes the delivery version of the whole system; the component interface version describes the API semantic change that component exposes externally. Docs and communication must make this semantic distinction clear.

## Alternatives considered

| Option | Why not |
|---|---|
| Independent VERSION file per component | Worse drift. Each component has both a VERSION file + a pyproject.toml version, turning one number into two numbers' worth of drift. The carrier receives a combination of version numbers — untraceable, unalignable |
| Rely only on pyproject.toml version | `pyproject.toml`'s version is the Python package publication version, not the product release concept. The two semantics differ: the release version describes a delivery snapshot of the whole system, the pyproject version describes a single component's interface semantics. Forcing the release into pyproject muddles version semantics |

## Evidence

- `tests/test_version_consistency.py` is implemented and passing, checking the root VERSION and each component's pyproject.toml version for SemVer validity, and the alignment of the CHANGELOG latest heading with the root VERSION.
- `AGENT.md` §8 clearly defines the VERSION file's single-source role, and the hard constraint "no member may have a VERSION file."
- ADR-0011's established sippy version pin (commit pin + vendoring) is consistent with this version-governance philosophy: external dependencies go through commit pin + automated guards, internal components go through the root VERSION + pyproject interface-version binary structure.

## Related

- [`../system-architecture.md`](../system-architecture.md) §11.3 development mode — version governance section
- [`../../AGENT.md`](../../AGENT.md) §8 version and dependencies
- [`../../AGENT.md`](../../AGENT.md) §11 Git rules (commit-message convention with feat/fix prefixes, auto-generated CHANGELOG)
- [ADR-0011](0011-sip-stack-dual-path.md) and ADR-0019 external-dependency pin philosophy
