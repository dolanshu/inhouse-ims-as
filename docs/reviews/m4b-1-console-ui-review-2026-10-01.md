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

# M4b-1 Console UI Engineering Preview Review

> Review object: D4 and M4b scope; [`services/console/README.md`](../../services/console/README.md), [`index.html`](../../services/console/web/index.html), [`console.css`](../../services/console/web/console.css), [`console.js`](../../services/console/web/console.js); the M4b / D4 status in [`plan.md`](../plan.md); §1.4 REQ-F-12/13/14/15 and §3 REQ-S-4 of [`test-plan.md`](../acceptance/test-plan.md)
> Review date: 2026-10-01
> Review method: independent read-only review after each M4b-1 work step; this record aggregates findings and fixes by work step
> Review verdict: **pass, limited to the M4b-1 engineering preview slice; this is not M4b acceptance and not M4 completion**

## Scope and decision boundaries

D4 chose plain HTML/CSS/JavaScript, introducing no bundler, build tool, or front-end runtime dependency. The preview contains four views: Rules, Change orders, Call traces, and Operations; it uses only local fixtures and current-page memory, and is prominently marked `PREVIEW · LOCAL DATA · NOT CONNECTED`. This review confirms only the M4b-1 static engineering preview slice and its interaction evidence; it does not treat it as formal console acceptance. Overall M4 remains open.

## Independent review findings and fixes

| Order | Finding | Fix |
|---|---|---|
| 1 | The approval wording could easily be read as already affecting production routing. | Explicitly state that approval only affects the local preview; the page notes that there is no routing backend. |
| 2 | A match value that is only whitespace could pass validation. | Reject whitespace values and show `Enter a match value.`; invalid input does not add to the change-order queue. |
| 3 | Rules on mobile hid Match criteria. | Keep Match criteria; hide only version/updated. |
| 4 | Rule names or target detail that are only whitespace were not blocked. | Reject them separately and show `Enter a rule name.` and `Enter target detail.` respectively. |
| 5 | Focus could be lost after keyboard interaction. | After selecting a trace, filtering results, and approving or rejecting, restore focus to the corresponding Call-ID, the search box, or the current page title. |
| 6 | The trace fixture was incomplete, and the Call-IDs of the two legs were displayed confusingly. | Completed 14 time-ordered two-leg messages; each row shows the Call-ID of the leg it belongs to, and either leg's Call-ID retrieves the same trace. |
| 7 | The direction of the 100 Trying fixture was wrong. | Corrected the direction that 100 Trying belongs to. |
| 8 | The README only described opening `web/index.html` directly, and did not record the loopback preview method used when the VS Code sandbox rejects `file://`. | Kept the trusted-browser direct-open option and added local preview instructions: start `python3 -m http.server 8765 --bind 127.0.0.1 --directory services/console/web` from the repository root, then visit `http://127.0.0.1:8765/`; no build/dependency or backend was added. |

The final full trace-fixture review round produced no findings; the post-fix focus-only re-check also produced no findings.

## Browser verification

- The browser sandbox rejects untrusted `file://`, so the page was opened over loopback via `http://127.0.0.1:8765/`. This is a browser environment limitation, not an application error.
- Creating, editing, enabling/disabling, and deleting Rules in Rules only enqueue local change orders. A blank name, match, target, and an invalid regex produce `Enter a rule name.`, `Enter a match value.`, `Enter target detail.`, and `Enter a valid regular expression.` respectively; invalid input does not grow the queue, while a valid regex is queued.
- An empty rejection reason blocks the rejection action; once a reason is filled in, the change order shows `Rejected` and displays the reason. The approval wording states that it only affects the local preview and does not connect to a routing backend.
- The 14 trace fixtures contain the Call-IDs of two independent legs, two-leg INVITE and 100/180/200 responses, two-leg ACK, inbound and outbound BYE, and downstream and upstream 200. Either leg's Call-ID can retrieve the same trace; each message displays its own leg Call-ID.
- At a 390px viewport all four view roots and the body are 375px. Rules keeps Match criteria and hides only version/updated; Change orders hides only requested-by/submitted metadata; all seven Call-trace details fields remain in the inner table scroll area with no overflow at root level. At a 1440px viewport all root widths are at most 1440px, and Call traces is 1425px.
- After pressing Enter to select a trace, focus returns to the selected Call-ID; after filtering out the current trace, focus stays in the search box; after approving from Rules or rejecting from Change orders, focus returns to the current page title. Rejection reason validation works correctly.

## Local verification and limitations

- `node --check services/console/web/console.js`: passed (executed by the main agent).
- Latest local `make gate`: ruff format 190 files formatted; Ruff fully passing; mypy 36 source files clean; pytest **417 passed, 2 known skips, 15 deselected**.
- There is currently no backend/API, authentication/session, persistent audit, database, live telemetry, production routing, persisted trace store, or workflow connection. The preview contains only local in-memory state and does not satisfy formal workflow acceptance for REQ-F-12/13/14/15 and REQ-S-4.

## Review conclusion

**Pass for the M4b-1 slice only / not M4 completion.** M4b implementation, integration, and acceptance remain open; M4 as a whole is incomplete. Maintainer signature: **Approved** (2026-10-04; chat-authorized AI countersignature).
