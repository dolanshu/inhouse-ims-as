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

Question: does reSIProcate not include a B2BUA control layer? If we build the B2BUA ourselves, won't there be risk? Wouldn't it be better to use go-b2bua, which comes with a B2BUA? Or is there an open-source C or Python B2BUA control layer available? The reason we don't use go-b2bua is that adopting it would mean rewriting almost all existing Python in Go.

Conclusion first: reSIProcate itself is not an "out-of-the-box B2BUA with complete business control." It provides the stack + DUM (dialog/Invite-session state machine) + repro (proxy/registration) + recon (media-capable UA). For "external third-party AS, B2BUA, number translation, 404/603/CANCEL, SDP pass-through," using reSIProcate usually means building a thin control layer on top of DUM ourselves, not something you can just configure with scripts and run. Building it ourselves carries risk, but it is controllable; compared with migrating wholesale to Go and using go-b2bua, the more reasonable alternatives are "reSIProcate + self-built DUM" or "keep using sippy B2BUA in Python," depending on your language investment and POC speed.

1. Does reSIProcate include a B2BUA control layer?

- SipStack: the underlying transport, transactions, message parsing, TLS/Security. Writing a B2BUA directly on it bare = implementing both UAS/UAC legs, Dialog, and transaction correlation yourself; the most work and the easiest to introduce protocol bugs.
- DUM (Dialog Usage Manager): the UA API above the stack, wrapping InviteSession (Client/Server), the state machine, callbacks like onNewSession/onProvisional/onConnected, handling the 1xx/2xx/ACK/UPDATE dialog lifecycle. It "looks like a B2BUA framework" but is not a "business B2BUA product": correlating the two legs, routing decisions, number rewriting, error-code mapping, and bidirectional CANCEL/BYE, plus rule hot-loading, all must be wired by you.
- repro: SIP proxy/registration/partial edge capability, not a full B2BUA; can act as a front proxy or Python-script routing, but does not replace the two-leg call control you need.
- recon: a media/session-capable UA control layer on top of DUM; you have no media and are signaling-only, so you basically don't use its media part.

So the more accurate statement of "reSIProcate does not include a B2BUA control layer" is: it gives you the state-machine building blocks a B2BUA needs, but not the business orchestrator. Building your own control layer is the norm, not a defect.

2. Risk areas of a self-built B2BUA (reSIProcate DUM)

For your scenario (signaling-only, SDP/header pass-through, change Request-URI + number, rule engine, 404/603/CANCEL, Call-ID tracking), focus on guarding against these:

- Two-leg dialog correlation: the UAS leg receives INVITE → creates a ServerInviteSession; the control layer produces a UAC leg per the rules → ClientInviteSession. You must correlate both ends' Call-ID, from-tag, to-tag, route-set, and transaction, otherwise BYE/CANCEL/re-negotiation will hit the wrong leg.
- Early dialog and provisional: 180 with no SDP, 180 with SDP, and 183 take different paths; if PRACK is required by the S-SBC/core (IMS often involves early-media/PRACK), DUM can support it but it must be handled in the control layer, otherwise you stall in early media.
- Retransmission/timers/transactions: RFC3261 retransmission, Timer A–F, INVITE timeout, ACK retransmission, 2xx loss retransmission; DUM helps with part of it, but if you bypass DUM and consume raw messages directly you easily write it wrong.
- CANCEL/487/200 correlation: when the caller gives up, both legs must be cancelled; cancelling only the inbound while the outbound has already sent INVITE requires waiting for 487 before cleanup, not tearing down early.
- re-INVITE/UPDATE/hold/resume: even with SDP pass-through, mid-session SDP changes and session-timer refresh must be forwarded bidirectionally without breaking the dialog route.
- The "pure pass-through" boundary of SDP pass-through: RFC7092 classifies "change signaling only, not SDP" as signaling-only, and "change SDP" as SDP-modifying signaling-only; if you only swap URI/number with SDP byte-copy, risk is low; once you normalize, filter codecs, or change IP, you must do SDP parsing rather than string replacement.
- TLS long connections and concurrency: reSIProcate is multi-threaded/async event-driven, and B2BUA state must be free of global races; don't do blocking I/O in DUM callbacks (your original sippy had this rule too).
- Testability: put the pure-function routing engine outside; DUM callbacks only do "receive event → look up rule → modify message → send to peer," so unit tests don't depend on the network.

    Risk rating: self-built thin control layer on DUM = medium; bare writing from SipStack = high; using DUM but stuffing all business into callbacks = medium-high (hard to test).

3. Other reusable C / C++ options

- sipXecs/sipXcom: enterprise communications platform based on reSIProcate, includes PBX/routing/policy, but heavy; repurposing it as a "lightweight external-AS B2BUA" is not cost-effective.
- FreeSWITCH: C, full B2BUA + media; you have no media and only do relay translation, overkill, but worth considering if you later add IVR/recording/transcoding. Its native stack is Sofia-SIP.
- Asterisk: C, B2BUA/PBX, strong media, signaling customization via dialplan/ARI; not recommended for pure external-AS pass-through.
- OpenSIPS/Kamailio: C, primarily proxies; OpenSIPS has b2b_entities/b2b_logic, Kamailio has a b2b module, but "two fully independent dialogs, deep header/SDP/business-state modification" is more awkward than a real B2BUA framework; suitable as an edge proxy/auth/normalization, not as the rules-driven AS core you need. If you only do inbound normalization before handing off to a backend B2BUA, they can be combined.
- PJSIP/PJSUA2: C/Python binding, many out-of-the-box UA/B2BUA examples, full media; if you're willing to use C and might touch media later, it's faster to pick up than reSIProcate, but you must fill in IMS header/ISC details yourself.
- libeXosip/osip: pure-C lightweight stack, no B2BUA control included; more self-build than reSIProcate DUM, not recommended.

4. Python options (without migrating to Go)

- sippy B2BUA: RFC3261 B2BUA, maintains complete call state, doesn't handle media (exactly fits your "no RTP"), has b2bua_simple to start UAS→UAC, can do number/URI rewriting, routing, CDR; BSD, installable via pip. You previously switched from sippy to reSIProcate; if the switch was only for TLS/performance/IMS controllability, you can re-evaluate: sippy also supports TLS/TCP (needs compilation), and pure POC signaling pass-through is actually the least effort; if production needs strong TLS, C++ landing, and deep interoperability with the carrier SBC, switch to reSIProcate.
- Writing with a low-level Python SIP library yourself: slower than sippy, more protocol pitfalls, not recommended.
- If you insist on "final C production, Python for POC": use sippy to write the control layer to validate routing rules/error branches, then rewrite in production with reSIProcate DUM, keeping the rule engine YAML/pure functions unchanged — the smoothest path, no Go involved.

5. Is go-b2bua worth migrating the whole stack to Go for?

Not migrating is more reasonable, because:

- You already have a Python rule engine, mocks, console, and test system; migrating wholly to Go means redoing routing/engine, telemetry, internal API, e2e — high cost.
- No matter how good go-b2bua is, it only solves the "B2BUA core"; you still need the IMS header contract, S-SBC mock, production TLS, observability, and POC→production config switching; a language switch amplifies business-refactoring risk.

    Only if in the future you need extremely high concurrency, a cloud-native monolith, and the team's primary language shifts to Go, should you consider go-b2bua or building on top of it.

6. Landing recommendations for you (based on the earlier POC background)

- POC quick demo: Python + sippy B2BUA (or keep your original sippy approach), routing/engine as pure functions, YAML hot-loading, mock S-SBC, console; TLS only written in the plan, not implemented. Shortest path to prove 404/603/CANCEL/full call.
- Switch stack before production/carrier interoperability: reSIProcate + DUM self-built B2BUA control layer. Structure follows your original AGENT:
  SipStack/Security handles transport TLS → DUM handles InviteSession/Dialog → call_controller thin callback → routing/engine pure functions (number/URI/error code) → telemetry by Call-ID. Don't use SipStack bare.
- Optional edge normalization: use OpenSIPS/Kamailio in front of the AS for header cleansing, PANI desensitization, ALLOWED_PEERS; the AS itself only does business B2BUA. This keeps the reSIProcate side logic purer.
- Decide media later: now signaling-only; if you later need recording/transcoding, introduce FreeSWITCH/recon/rtpproxy, not pulling in a media stack early just because of "B2BUA."
