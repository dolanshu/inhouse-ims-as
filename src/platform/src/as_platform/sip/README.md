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

# Product SIP adapter (`as_platform.sip`)

## Runtime listener

`ResipRuntimeListener` binds reSIProcate DUM on a background thread and calls Python
``decide()`` for inbound INVITEs (unless ``accept_all_invites`` harness mode is on).
``accept_all_invites`` is testbed-only: it answers 100/180/200 with a minimal SDP
after ingress, and is not the production routing path.

Native module: ``src/platform/native/resip_runtime`` → ``_resip_runtime``.

## D9 adapter boundary (engineering complete)

| Direction | Behavior |
|-----------|----------|
| Inbound INVITE | ``on_invite(peer_dict, sip_summary)`` → SIP status **or** ``{"status": 0, "route_target": "<uri>"}`` for FORWARD |
| FORWARD UAC | Native creates outbound INVITE (distinct Call-ID), relays SDP offer bytes, maps downstream **486** → inbound **486** |
| Early CANCEL (UAS) | ``early_cancel_harness`` + ``accept_all_invites``: hold after 180; DUM answers CANCEL/487 |
| B2BUA CANCEL | Inbound ``RemoteCancel`` ends outbound ``DialogSetId`` via ``DialogUsageManager::end`` |
| Dialog established | Optional Python ``on_dialog_established(fields)`` for checkpoint commit |

Isolated two-leg spike remains in ``_resip_two_leg`` for regression; production path uses
``_resip_runtime`` FORWARD (``AS_SIP_TWO_LEG=1`` not required).

## Environment (process shell)

| Variable | Effect |
|----------|--------|
| ``AS_ENABLE_SIP_RUNTIME=1`` | Start ``SipStackService`` from ``as_platform.__main__`` |
| ``AS_SIP_ACCEPT_ALL_INVITES=1`` | Harness accept-all UAS (D10 / smoke) |
| ``AS_RULESET_JSON`` | Inline JSON rule list or ``{"rules": [...]}`` |
| ``AS_CONFIG_BUNDLE_PATH`` | Path to ConfigBundle-shaped JSON (rules subset) |

See ``src/apps/translation/README.md`` for translation entrypoint.
