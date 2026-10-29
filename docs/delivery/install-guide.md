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

# In-house IMS Application Server — installation and deployment guide

> **Deliverable**: the **installation guide** of the third delivery-form batch ([`../product-packaging-plan.md`](../product-packaging-plan.md) §1 **3.1 / 3.2**, same batch). Home directory [`docs/delivery/`](./README.md).
> **Boundary of this document (hard boundary)**: **it covers only the delivery checklist, image acquisition and mirroring, and the `helm install` command sequence. The single authority on Helm parameters, values semantics and rendering behaviour is [`../../deploy/helm/README.md`](../../deploy/helm/README.md)** — this document **does not copy** its parameter table and does not explain `--set` semantics item by item; it only answers "what is delivered, what do you fetch, and in what order do you type which commands" (review **G-P2-4** is exactly this boundary).
> **Production form**: **Helm-only** — Helm plus standard K8s resources is the only production form; no Operator, no second installer (ADR-0013; review G-P1-7).
> **Zero capacity figures**: the O1 capacity target is undecided (`AGENT.md` §2; [`../plan.md`](../plan.md) §5.1). This document gives **no** recommended values for CPS / concurrency / latency / resource specifications; `useCases[].resources` defaults to empty and this document does not fill it in.
> **Not validated on a real cluster**: M4b-7.2d / M8 7.2d real-cluster evidence is **still blocked** ([`../plan.md`](../plan.md) §5.4); **M8 RC artifacts ready ≠ exit sign-off complete**, and the exit sign-off remains pending. What this document gives are **executable actions**, not a "validated in production" conclusion. The **air-gapped scenario** (customer machine room with no external network) is covered by [`airgap-package.md`](./airgap-package.md).
>
> **Product name**: `In-house IMS Application Server`, **officially adopted as the product / documentation descriptor name** (G8-2; not a trademark / not a branding claim; 3GPP Third-Party AS role); the git repo name has been renamed by the maintainer report to `inhouse-ims-as` (G8-3; repo name and remote URL only). Naming boundary: chart name / image name / OTel service name remain `3rdparty-as`.
>
> **B6 review status**: this document has a review record from the B6 review — [`../reviews/product-packaging-review-checklist-2026-10-12.md`](../reviews/product-packaging-review-checklist-2026-10-12.md) §6 (first review 2026-10-12) and §7 (closed-loop re-review 2026-10-12); **the conclusion awaits maintainer confirmation** and until then must not be used as a basis for external delivery or acceptance (`AGENT.md` §3.3).

> **Note (added 2026-10-13)**: the statement "the O1 capacity target is undecided" in the paragraph above is factually stale (the internal engineering target value has landed; the externally committed value is still left unfilled). The handling (keep the original text + add this note) is in [`../next-release-v1.1-plan.md`](../next-release-v1.1-plan.md) §5-1, pending a maintainer decision on whether to sync it.

## 1. Applicability and prerequisites

**Delivered to**: the operator-side K8s administrator / delivery implementer responsible for deployment. After reading this document you should be able to: install a Helm release from the delivery package in order, and know what each step is verifying. **If anything is missing, do not start installing.**

| # | What is needed | Decision / remark |
|---|---|---|
| 1 | K8s cluster | The minimum minor version is derived and verified by [`preflight.sh`](./preflight.sh) (default 1.23, overridable with `--min-k8s`). **The chart itself has no `kubeVersion` declaration**, so Helm will not stop a too-old cluster for you (§10) |
| 2 | Helm 3.x (chart `apiVersion: v2`) + `kubectl` | The lower version bound is checked by `preflight.sh` |
| 3 | Product image obtainable | The customer's internal registry, or imported onto nodes with this directory's offline package. `registry.example.com` is a placeholder address and is **not pullable** |
| 4 | Redis (runtime state) and PostgreSQL (governance state) **decision** | Either external instances, or enable the chart's built-in `stateStores.enabled=true` (ADR-0026). **A built-in single replica is not HA**: the Redis HA topology values are decided (O5 / D3, G7: primary/replica + Sentinel, ADR-0008, Redis Cluster not chosen; the chart still renders a single replica and there is no evidence for measured failover behaviour; RPO / RTO figures are still undecided) |
| 5 | TLS Secret issued by the customer PKI | Keys `tls.crt` / `tls.key` / `ca.crt`. **The certificate is produced by the customer's PKI**, the chart only references `tls.secretName` (ADR-0016). [`../../deploy/kind/scripts/m5-gen-certs.sh`](../../deploy/kind/scripts/m5-gen-certs.sh) in this repository is only a kind self-signed precedent, **not a deliverable** |
| 6 | Target namespace + installer's account permissions | Example namespace `as-prod`; the chart **does not create** Roles/RoleBindings, permissions must be granted by the customer K8s administrator |

**Use [`preflight.sh`](./preflight.sh) (deliverable 3.1) for pre-checks, do not skip it** (`--dry-run` only checks local tooling and chart rendering and does not contact the cluster; `--skip-network` skips the dependent-service probes; the script **is not a capacity validation tool** — when `resources` is empty it only emits `WARN` and never guesses numbers):

```sh
docs/delivery/preflight.sh -n as-prod -f deploy/helm/values-onprem.example.yaml
```

| Exit code | Meaning | Handling |
|---|---|---|
| `0` | No `FAIL` (and no `WARN` under `--strict`) | You may proceed to installation (§4) |
| `1` | There is a `FAIL` | **Stop**; follow the remediation guidance printed on each line |
| `2` | Usage error (illegal argument) | Fix the arguments and retry |
| `3` | There is a `WARN` under `--strict` (no `FAIL`) | Continue only after confirming each one |

## 2. Delivery checklist

| Deliverable item | Form | Location / source | How it is verified |
|---|---|---|---|
| Helm chart package | `3rdparty-as-0.0.0-skeleton.tgz` (the actual current artifact name; `helm package` names it per the name/version in Chart.yaml, not synced with the root `VERSION` 0.2.0) | Produced by `bundle-images.sh` / `deploy/helm/` (install straight from the repository) | Included in `SHA256SUMS`; passes `make chart-check` rendering; version consistency is verified with [`../../scripts/sync-chart-version.sh`](../../scripts/sync-chart-version.sh) `--check` (read-only, exits 1 on drift); the first `--apply` is a maintainer decision |
| Production values file sample | Text | [`../../deploy/helm/values-onprem.example.yaml`](../../deploy/helm/values-onprem.example.yaml) | Every `REPLACE_WITH_*` placeholder in it must be replaced (§5) |
| Product image | Container image | `3rdparty-as` + **`3rdparty-as-config-service`** (required when the control plane is enabled); inventory template [`scripts/images.txt`](./scripts/images.txt) | tag / digest in `MANIFEST.txt`; no `ImagePullBackOff` on the Pods |
| TLS Secret | K8s Secret | **Issued by the customer PKI** (keys `tls.crt` / `tls.key` / `ca.crt`) | `kubectl -n <ns> get secret <tls-secret>` exists; key material **never enters the repository** |
| PostgreSQL credentials Secret | K8s Secret | Provided by the customer (`CONFIG_DB_USER`, `CONFIG_DB_PASSWORD`, `CONFIG_DB_OWNER_PASSWORD`, `POSTGRES_SUPERUSER_PASSWORD`, `REDIS_PASSWORD`) | **Required** when `stateStores.enabled=true` + `bootstrapDevCredentials=false` (§5 item 3) |
| config-service runtime Secret | K8s Secret | Provided by the customer (`AS_CONFIG_DSN` (the **`as_config_web` login**), `AS_AUDIT_RESOURCE_HMAC_KEY_B64`) | **Required** when `services.configService.enabled=true`; the `AS_CONFIG_DSN` login must be able to `SET ROLE` into the pre-provisioned `NOLOGIN` runtime role |
| Migration Job | K8s Job (one-off) | `stateStores.migrateJob.enabled=true` + `migrateJob.ownerSecretName` (key `AS_CONFIG_OWNER_DSN`) | `kubectl -n <ns> wait --for=condition=complete job/...` (§6.1) |
| Alert rules | YAML + Markdown | [`../../deploy/alerts/as-alerts.yaml`](../../deploy/alerts/as-alerts.yaml) (3 groups, 10 rules) + [`../../deploy/alerts/README.md`](../../deploy/alerts/README.md) | Judged by G9-a to be a delivery product; `promtool check rules` passed on 2026-10-11 ((verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-alert-check-2026-10-11.txt, 2026-10-11), `SUCCESS: 10 rules found`); **the scrape wiring is not closed (X1) and must be explained to the customer** — under a standard deployment the `as_*` series will not be collected by Prometheus |
| Documentation package | Markdown | This directory (`README.md` / this document / `airgap-package.md` / `preflight.sh`) + [`../operations/`](../operations/README.md) + [`../product/`](../product/one-pager.md) | — |

The chart **only references** customer credentials and **neither creates nor populates** them; the credentials Secret shipped with the chart is an **empty-string placeholder** (`AGENT.md` §13).

## 3. Image acquisition and mirroring

Two paths, pick one. **Path A** (the correct approach when the customer already has an internal registry) builds on the networked side and pushes into the customer registry:

```sh
docker build -t <customer-registry>/3rdparty-as:<VERSION> -f deploy/docker/Dockerfile .
docker build -t <customer-registry>/3rdparty-as-config-service:<VERSION> -f deploy/docker/config-service.Dockerfile .
```

After pushing, point §4's `--set image.repository` / `--set image.tag` at them and you are done. **Path B** (air-gapped, no external network; the complete flow for networked-side production and offline-side installation is in [`airgap-package.md`](./airgap-package.md) §3/§4):

```sh
docs/delivery/scripts/bundle-images.sh --images docs/delivery/scripts/images.txt --out ./airgap-out
docs/delivery/scripts/load-images.sh --bundle ./airgap-in --load --namespace as-prod
```

**Checksum discipline** — the packaging side and the receiving side **each run it once**, to distinguish "transfer corruption" from "packaging error" (the original text is in [`airgap-package.md`](./airgap-package.md) §3 step 5 / §4 step 1):

```sh
cd airgap-out && sha256sum -c SHA256SUMS   # networked side; hand the output to the customer together with the media
cd airgap-in  && sha256sum -c SHA256SUMS   # first step on the offline side; must abort on mismatch
```

Key points: `images/*.tar` and the chart tgz enter `SHA256SUMS` **together**; an offline environment cannot pull, so `image.tag` must match the tag actually imported **character for character** (otherwise you get nothing but `ImagePullBackOff`); prefer pinning by digest (`repository:tag@sha256:...`, precedent in the header comment of [`scripts/images.txt`](./scripts/images.txt)); one `docker save` tar carries only one platform, so across architectures package and verify separately.

## 4. Installation command sequence

**Parameter semantics are not explained here** — the meaning and rendering behaviour of `image.*`, `sip.*`, `tls.*`, `services.configService.*`, `stateStores.*` are in [`../../deploy/helm/README.md`](../../deploy/helm/README.md). The commands below are **copied verbatim** from [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) §"Install (on-prem)", with the **argument order unchanged**:

```sh
helm upgrade --install as deploy/helm \
  -f deploy/helm/values-onprem.example.yaml \
  --namespace as-prod --create-namespace \
  --set image.repository="<customer>/as-platform" \
  --set image.tag="<release>" \
  --set sip.peerAllowlist="<s-sbc-cidrs>" \
  --set tls.secretName="<tls-secret>" \
  --set services.configService.image.repository="<customer>/as-config-service" \
  --set services.configService.secretName="<runtime-secret>"
```

The namespace `--namespace as-prod --create-namespace` handles creation in one go; the chart renders **within that single namespace**; one Deployment per business use case (ADR-0002). The **air-gapped install method** only swaps the chart path for the tgz on the media (`./airgap-in/<chart>.tgz`) and the values file for the customer's values file, leaving every other parameter unchanged — the complete command is in [`airgap-package.md`](./airgap-package.md) §4 step 4, and is **not repeated here**. **kind / lab** (development credentials, emptyDir PG, **must not be used in customer production**): `M5_BUNDLED_STATE=1 bash deploy/kind/scripts/m5-helm-install.sh`.

## 5. The three mandatory pre-install items and fail-closed

If any one of the following three is missing, **the render stage fails** — this is the design intent (fail-closed), **not a bug**: better to fail to install than to go live with an empty certificate, or to let anyone who can reach the Service inject calls.

| # | Key | Trigger condition | The chart's verbatim error ([`../../deploy/helm/templates/validate-install.yaml`](../../deploy/helm/templates/validate-install.yaml)) |
|---|---|---|---|
| 1 | `tls.secretName` | `tls.enabled=true` (default) and empty | `tls.enabled=true requires tls.secretName (customer PKI Secret; ADR-0016)` |
| 2 | `sip.peerAllowlist` | empty (after trim) | `sip.peerAllowlist must be non-empty (ADR-0016 fail-closed)` |
| 3 | `postgres.secretName` | `stateStores.enabled=true` and `bootstrapDevCredentials=false` and empty | `stateStores.enabled with bootstrapDevCredentials=false requires postgres.secretName (Secret keys: POSTGRES_SUPERUSER_PASSWORD, CONFIG_DB_OWNER_PASSWORD, CONFIG_DB_PASSWORD)` |

**The equivalent fail messages are not in only one place**: [`../../deploy/helm/templates/deployment.yaml`](../../deploy/helm/templates/deployment.yaml) has two more **equivalent** fail messages (`tls.secretName` and `sip.peerAllowlist`, semantically consistent with `validate-install.yaml`) — the 2026-10-11 chart-check artifact proves a single lint output with 4 Fails ((verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-chart-check-2026-10-11.txt, 2026-10-11)). **`sip.allowEmptyAllowlistForTest` ([`../../deploy/helm/values.yaml`](../../deploy/helm/values.yaml), default `false`) must be `false` in production** — only the testbed may turn it on; enabling it in production means giving up fail-closed (the peer allowlist is no longer enforced).

The four placeholders `REPLACE_WITH_POSTGRES_SECRET` / `REPLACE_WITH_CONFIG_RUNTIME_SECRET` / `REPLACE_WITH_TLS_SECRET` / `REPLACE_WITH_S_SBC_CIDRS` in the values file **must all be replaced** — the chart does not raise an error just because a value is a placeholder string. **Verify the rendering locally first** (do not leave fail-closed to be discovered on the customer cluster): run `make chart-check` from the repository root (equivalent to `deploy/helm/scripts/chart-check.sh`, which asserts the default AS rendering, config-service enabled, the ingress template path and HPA fail-fast; this is gate ① the fast layer).

## 6. Post-installation steps

Do them in order, **do not skip steps**.

**6.1 Migration Job and waiting** — when `stateStores.migrateJob.enabled=true` and `services.configService.enabled=true`, copied verbatim from [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md):

```sh
helm upgrade --install as deploy/helm -f deploy/helm/values-onprem.example.yaml ...
kubectl -n <ns> delete job/as-3rdparty-as-config-migrate --ignore-not-found
kubectl -n <ns> wait --for=condition=complete job/as-3rdparty-as-config-migrate --timeout=300s
```

**Run once per schema version**. Production usage: pre-create the Secret `as-config-migrate-owner` (key `AS_CONFIG_OWNER_DSN`, the owner login); the Job with `bootstrapDevCredentials=true` inlining the owner DSN only applies to kind/dev. Manual migration (in a controlled environment or as an `as-config-service` image Job), copied verbatim:

```sh
export AS_CONFIG_OWNER_DSN="postgresql://as_config_owner:<password>@127.0.0.1:15432/as_config"
export AS_CONFIG_RUNTIME_ROLE=as_config_runtime
export AS_AUDIT_SCHEMA=console_audit
export AS_CONFIG_SCHEMA=as_config
uv run as-config-migrate
```

**6.2 PostgreSQL roles and DSN** — `as_config_owner` = the owner DSN for migration / bootstrap (`AS_CONFIG_OWNER_DSN`, used **only** for manual commands and the migration Job); **`as_config_web`** = the login for `AS_CONFIG_DSN` in the runtime Secret, which must be able to `SET ROLE` into `as_config_runtime` (**`NOLOGIN` least privilege**, pre-provisioned by the DBA). **The owner DSN never enters a Deployment** — it must not appear in Helm values, chart-managed Secrets, an external runtime Secret, or the web Pod (verbatim from [`../../deploy/helm/README.md`](../../deploy/helm/README.md)). Neither the chart nor the service **creates roles or grants privileges**; runtime startup performs **no** DDL / migration / grants. `configSchema` (default `as_config`) and `auditSchema` (default `console_audit`) must differ, and neither may be `public`.

**6.3 First administrator bootstrap** — copied verbatim from [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md):

```sh
kubectl -n <ns> exec -it deploy/as-3rdparty-as-config-service -- \
  as-config-bootstrap-admin   # reads env; interactive getpass
```

**You must migrate first, then bootstrap**; the exact entry point of the command is whatever the image entrypoint documentation / the `pyproject.toml` console script says.

**6.4 Connecting the S-SBC trunk and the peer allowlist** — SIP trunk: UDP `5060`, TCP `5060` (TCP listening requires `AS_SIP_ENABLE_TCP` to be on; off by default), TLS `5061` (mTLS, on by default). Put the S-SBC side address ranges in `sip.peerAllowlist`; empty means fail-closed (ADR-0016). The trunk is an **untrusted** boundary: the peer is validated against the allowlist, and TLS is terminated end-to-end with the S-SBC. See [`../product/ne-datasheet.md`](../product/ne-datasheet.md) §2 and [`../product/responsibility-matrix.md`](../product/responsibility-matrix.md) for the complete onboarding steps.

**6.5 iFC trigger verification** — the ISC trigger for iFC is configured on the **S-CSCF / HSS side**; **iFC is not on the AS side**, the AS side only implements the business decision after the ISC trigger (review G-P0-5 / G-P1-10). Verification requires cooperation from the S-CSCF / HSS side and is **cross-domain joint debugging**, not a one-sided installation action.

**6.6 Console and ingress-nginx** — the console and the API share the **same HTTPS origin** (`/` and `/internal/v1`, ClusterIP HTTP `8000`), with no separate console workload. Enable `services.configService.ingress` in production; the requirements are: `className` must be `nginx` (this template **only supports ingress-nginx**; anything other than `nginx` fails to render; other controllers need separately reviewed external configuration and this template **must not** stand in for them); `tlsSecretName` points at a customer-managed Secret; `proxyHeaders: true` plus an **explicit `trustedProxies` CIDR list** (`*`, `0.0.0.0/0`, `::/0` and other `/0` entries are rejected — **do not loosen proxy trust to make forwarded HTTPS "look secure"**). > ⚠️ **M4b-7.2d is still blocked**: the real-cluster controller configuration, the HTTP→HTTPS redirect behaviour, trusted-proxy behaviour and browser / network evidence have not been obtained and recorded; **a chart annotation is not redirect evidence** ([`../../deploy/helm/README.md`](../../deploy/helm/README.md) §"M4b-7.2d ingress-nginx deployment prerequisites (BLOCKED)").

## 7. Verification checklist

| Check item | Command / method | Expectation | Basis | Evidence level |
|---|---|---|---|---|
| chart render guard | `make chart-check` | Pass (lint + template assertions) | `Makefile` / `deploy/helm/scripts/chart-check.sh` | **Gate ① the fast layer, green** ((verified, docs/acceptance/artifacts/m5/2026-10-11/PASS-chart-check-2026-10-11.txt, 2026-10-11): `chart-check: OK`, `1 chart(s) linted, 0 chart(s) failed` (helm 3.16.4)) |
| Pods and readiness | `kubectl -n as-prod get pods -l app.kubernetes.io/part-of=3rdparty-as` | Each use-case Pod `Running`, READY true | NOTES.txt §2 | Verified on kind/dev; **not accepted in production** |
| Rollout completion | `kubectl -n <ns> rollout status deploy --selector app.kubernetes.io/part-of=3rdparty-as` | All rollouts complete, no Pods `Progressing` for a long time | NOTES.txt §3 (ADR-0009 draining) | Verified at the template layer; **not accepted in production** |
| Consistent version reporting | `kubectl -n <ns> exec deploy/<release>-<use-case> -- printenv CONFIG_VERSION` | Identical across replicas and equal to the version in effect on the control plane | NOTES.txt §2 (ADR-0006) | Verified on kind/dev; **not accepted in production** |
| Health endpoints | After `kubectl -n as-prod port-forward deploy/<release>-<use-case> 8080:8080`, access `/health/live` and `/health/ready` | live 200; ready 200 (**503 during draining is normal traffic removal**) | [`../operations/runbook-l1.md`](../operations/runbook-l1.md) §1 check 2 | Verified on kind/dev; **not accepted in production** |
| Metrics endpoint | Same port, `curl -s localhost:8080/metrics \| grep '^as_'` | Lists the session / decision related `as_*` series | `../operations/runbook-l1.md` §1 check 4 | **kind/dev only**; the chart has **no scrape annotation and no ServiceMonitor** → a standard deployment cannot be **collected** by Prometheus (§10) |
| State store reachability | Metric `as_state_store_available{use_case}` | `1` (**a missing series ≠ 0**: not emitted when `REDIS_URL` is empty) | The metric contract in `deploy/alerts/README.md` | Verified on kind/dev; **not accepted in production** |
| Built-in state stores | `make m5-kind-verify`; `kubectl -n as-m5 get pods -l app.kubernetes.io/part-of=3rdparty-as` | postgres-0 / redis / translation / anti-fraud / config-service ready | [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) §"Verify" | **kind only (`as-m5`)** |
| Console HTTPS | `curl -I -H 'Host: <ingress-host>' http://ingress-nginx-controller.ingress-nginx.svc/` | **301 / 308**; `empty reply` (curl 52) counts as **not passed** | `../operations/runbook-l1.md` §1 check 5 | **7.2d blocked, not accepted in production**; a port-forward 200 **cannot substitute** for this |
| Rollback command usable | `helm -n <ns> history as` → `helm -n <ns> rollback as <revision>` | The commands are executable and the revision exists | [`../../deploy/helm/templates/NOTES.txt`](../../deploy/helm/templates/NOTES.txt) §3 | Verified at the template layer; **rollback not drilled on a real cluster** |

> For the complete inspection checklist (including Redis / PostgreSQL / console login) see [`../operations/runbook-l1.md`](../operations/runbook-l1.md) §1. **Nothing above may be read as "validated in production"**: the current sign-off matrix status is pass 9 / fail 0 / blocked 12 / open 24 ([`../acceptance/report.md`](../acceptance/report.md) §0.5).

## 8. Upgrade and rollback

The **two kinds of "rollback" are not the same thing** (NOTES.txt §3 distinguishes them): **(a) configuration rollback** (ADR-0006) means rolling back the change record on the console / config-service side and re-distributing the old configuration version to instances in a canary fashion; that is the semantics of `ASConfigRollbackTriggered`, and **it must be confirmed by a human after the rollback**; **(b) image / manifest rollback** means rolling back the Helm release and letting the Deployment roll the Pods back itself, **going through draining on the way out** (ADR-0009). The commands are copied verbatim from [`../../deploy/helm/templates/NOTES.txt`](../../deploy/helm/templates/NOTES.txt) §3 (the original is the Go template `helm -n {{ include "as.namespace" . }} history {{ .Release.Name }}`; the text above is rendered with the release name `as` from §4 and the live namespace, with the **argument order unchanged character for character**):

```sh
helm -n <ns> history as
helm -n <ns> rollback as <revision>
kubectl -n <ns> rollout status deploy --selector app.kubernetes.io/part-of=3rdparty-as
```

| What changed | Upgrade path |
|---|---|
| **AS image / SIP knobs** | `helm upgrade`, touching only `image.*`, `sip.*`, `useCases` |
| **PostgreSQL image / PVC** | **Maintenance window**, following the customer Postgres upgrade process (`stateStores.migrateJob` is only a one-off schema migration, **not** a backup and **not** a PG upgrade channel) |
| **Redis** | **Maintenance window**, expecting a brief unavailability of runtime state |

Handling details are in [`../operations/rollback-playbook.md`](../operations/rollback-playbook.md) (traffic draining / rollback plus iFC-side coordination) and [`../operations/runbook-l1.md`](../operations/runbook-l1.md) §3.2; version support periods and EOL are in [`../product/version-lifecycle.md`](../product/version-lifecycle.md). Certificate rotation is a **configuration hot update** and does not restart the process (ADR-0016).

## 9. Boundaries against other documents

| Topic | Authoritative document | This document |
|---|---|---|
| Helm parameters, values semantics, render guards, fail-closed behaviour | [`../../deploy/helm/README.md`](../../deploy/helm/README.md) | **Does not copy the parameter table**, references only |
| Pre-deployment environment validation | [`preflight.sh`](./preflight.sh) | §1 gives the commands and exit codes |
| Production and use of the air-gapped installation package | [`airgap-package.md`](./airgap-package.md) | §3 gives only the two paths and the checksum commands |
| Migration / owner DSN / backup-restore details | [`../acceptance/m5-state-stores-runbook.md`](../acceptance/m5-state-stores-runbook.md) | §4 / §6.1–6.3 are **copied verbatim**, not expanded |
| Daily inspection, alarm handling, deep troubleshooting | [`../operations/runbook-l1.md`](../operations/runbook-l1.md) | §7 gives only the post-installation verification items |
| Positioning / capacity model / interface inventory / resource specifications, compliance (PDPO), lifecycle and EOL | [`../product/`](../product/one-pager.md) (`one-pager` / `ne-datasheet` / `security-privacy` / `version-lifecycle`) | Not repeated |

## 10. Known gaps and open items

| Item | Status | Blocking source |
|---|---|---|
| The chart has no `kubeVersion` declaration | Gap — Helm does not block a too-old cluster | [`../../deploy/helm/Chart.yaml`](../../deploy/helm/Chart.yaml) has no such field; `preflight.sh` derives a lower bound from the APIs the templates actually use as a fallback |
| The chart's `version` / `appVersion` are not synced with the root `VERSION` | Gap — still skeleton values (`0.0.0-skeleton` / `0.0.0`) | ADR-0018; run [`../../scripts/sync-chart-version.sh`](../../scripts/sync-chart-version.sh) `--check` before packaging (read-only, exits 1 on drift); the first `--apply` is left to the maintainer |
| `useCases[].resources` defaults to empty | **Deliberately left empty** — the chart renders no requests/limits, and **this document gives no recommended values** | Same root as O1; sizing is given by the NE datasheet after O1 is decided |
| Pods have no `prometheus.io/scrape` annotation and there is no ServiceMonitor | Gap — **every dashboard and alarm depending on `as_*` will not be collected in a standard deployment**; the OTLP exporter is currently `NoOp` | The scrape wiring is not closed (§7 metrics row) |
| 7.2d production ingress / trusted-proxy | **blocked** — production ingress, real HTTPS and browser evidence are missing | [`../plan.md`](../plan.md) §5.4; §6.6 |
| M8 exit sign-off | **Still pending** — RC artifacts ready ≠ closing the door | Maintainer exit sign-off is incomplete |
| E1 / E4 / E5 not accepted; 8 stable passes of `pytest -m e2e` | reSIProcate production-path behaviour, TLS hot rotation, externalised state and recovery are all unaccepted; the complete call + console end-to-end path has no automated evidence | O2 / O3; `pytest -m e2e` currently has 8 stable passes (fails rather than skips when the native is missing); REQ-F-1 = the automated subset is covered / the full text remains open |
| D1 Python 3.10 EOL; O5 / D3 Redis HA; PG HA / PITR | D1 **undecided**; O5 / D3 **values decided (G7)**; PG HA / PITR is **a customer-side responsibility** — the built-in Redis single replica is **not HA** (topology decided as primary/replica + Sentinel, ADR-0008, Redis Cluster not chosen; the chart still renders a single replica and there is no evidence for measured failover behaviour; RPO / RTO figures still undecided), `redis.sentinel.masters` / `.addresses` are deliberately left empty; the chart delivers a single-replica PG StatefulSet and **does not deliver a backup Job** | The D1 lifecycle endpoint; the customer SLA is undetermined (ADR-0008); the recovery drill awaits a real cluster ([`../operations/backup-restore.md`](../operations/backup-restore.md)) |

## 11. Traceability

| Item | Content |
|---|---|
| Corresponding deliverable | `delivery/install-guide.md` in the directory structure of [`../product-packaging-plan.md`](../product-packaging-plan.md) §2; delivery-form third batch **3.1 / 3.2**, same batch (same [`./README.md`](./README.md)). Engineering-fact constraints are in §0.3 of that plan |
| Boundary ruling | **G-P2-4** (overlap between `install-guide.md` and `deploy/helm/README.md`): this document only does the **delivery checklist + image mirroring + command sequence**; parameters and behaviour belong to `deploy/helm/README.md`, and the two documents cross-link without repeating. Review record [`../reviews/product-packaging-plan-review-2026-10-09.md`](../reviews/product-packaging-plan-review-2026-10-09.md) |
| Referenced ADRs | [ADR-0013](../architecture/adr/0013-helm-only-production.md) (Helm-only production form), [ADR-0016](../architecture/adr/0016-in-boundary-security.md) (in-boundary security: TLS + peer allowlist fail-closed), [ADR-0026](../architecture/adr/0026-in-cluster-state-stores-proposal.md) (in-cluster state stores); related: ADR-0002 (one process per use case), ADR-0006 (configuration governance / configuration rollback), ADR-0008 (redundancy), ADR-0009 (ISSU = draining) |
| What was deliberately not done | No capacity / resource specification / recovery-duration figures; nothing unaccepted written up as accepted; no citation of M6 dev-host measurements; no copying of the Helm parameter table; no second installation form |
