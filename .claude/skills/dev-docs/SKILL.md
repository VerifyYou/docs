---
name: dev-docs
description: How to write and maintain the VerifyYou v3 Dev docs. Use whenever adding, editing, restructuring, or reviewing anything under v3/dev/ or docs.json. Covers the reader, the page architecture, what each Integrating page must teach, reference-page format, the deprecation workflow, where code samples come from, and the verification steps that stop confident-but-wrong docs from shipping.
---

# VerifyYou Dev docs

Read this whole file before touching `v3/dev/` or `docs.json`. For prose voice,
also load `.claude/skills/david-docs-voice/SKILL.md`; its claim gates decide
what may be stated as fact. This file governs structure, content, and process.

## The reader

Developers and AI coding agents. They know what they want; we are guiding them
and handing them tools, not persuading them. To the point, no warm-up, no
recap sentences. If a page can lose a paragraph and still integrate someone,
lose the paragraph. Verbose is acceptable only in the spec pages.

Terminology override on top of the voice skill: the person being verified is a
**person**. Never "guest", never "user", never "member". The members/guests
framing is retired; do not reintroduce it even when quoting older pages.

## The product story the docs tell

VerifyYou reports whether a person is a real, live, unique human. It never
decides what the customer's app does. Every page reinforces the same contract:

1. **We report `true` or `false`.** The customer's platform makes the pass or
   fail call, server side.
2. **The token is proof, not a verdict.** `vyt` exists so results cannot be
   forged, replayed, or borrowed from someone else. `vyc` is a UI hint.
3. **The FE SDK is for showing and processing the check.** It is not a routing
   solution. Routing lives in the customer's code, next to the gated action.

## Architecture

One **Dev** tab. v3 is the default version; v2 and v1 sit behind the version
dropdown as legacy and are never linked from v3 pages. Navbar links out to the
live OpenAPI spec (`https://trust.verifyyou.com/openapi.json`).

Groups, in order:

1. **Integrating**: the guided path, three pages (below).
2. **Server API**: one page per endpoint.
3. **Browser SDK**: one page per export, `vycheck()` first.

Navigation rules learned the hard way:

- Mintlify's right-hand "On this page" TOC cannot move into the left sidebar.
  An anchor that deserves navigation becomes its own page.
- A group containing one page repeats its name in the sidebar. Avoid one-page
  groups.
- Endpoint page titles are bare paths (`/v3/initialize`), no HTTP verb. The
  verb opens the body as inline code: `` `POST` Secret key. ... ``
- SDK page titles are the export names (`vycheck()`, `VyResult`).
- Deleted or moved pages get a `redirects` entry in `docs.json`. Old URLs keep
  working forever.

## The Integrating pages: what each one must teach

These three pages are the product's integration doctrine. Edits must preserve
these points; they are the reason the pages exist.

**Start a session**
- Sessions are minted server side with the secret key. The publishable key is
  deprecated; the browser only ever sees a `session_id`.
- The developer passes a claim or identifier that ties the check to whatever
  they use for their account: `external_id` for an existing record, `email` or
  `phone` to bind a new signup so the person cannot swap identities.
- Anonymous flows still initialize server side, for two reasons spelled out on
  the page: nobody can flood the account from a browser, and the developer
  gates *when* a check runs off their own signals that a request is low
  quality. A scan is spent deliberately.

**Placing your check**
- The SDK's job is getting the person to and through the check. `vycheck()`
  and `vyget()` are gating calls: `vycheck()` is the code gate that produces a
  token to pass to the backend, placed on the action only humans should do.
- Redirect is the primary tab, then drawer, then inline.
- The token rides in the same request as the action it gates.

**Handling results**
- Comes immediately after a token is obtained. The token lives 30 minutes and
  is exchanged on the backend for the real result.
- Recommend tying the token's submission to the server-side action that needs
  humanness (a form submit and its handler), so proof and action never exist
  apart.
- Reiterate: we report, the platform decides; the FE SDK is not routing.
- Fail closed; test partition never unlocks live actions; strip `vyt`/`vyc`
  after handoff; idempotency over lock unless "one pass per human, ever".

## Reference page format

Server API pages: method + one-line contract, then `## Body` (or
`## Path parameter`), `## Response`, `## Errors`, `## Example`. One-line
`ParamField`/`ResponseField` entries. Error tables are status / `detail` /
when.

Browser SDK pages: `## Signature`, `## Options`, `## Returns`, `## Errors`,
`## Example`. Shared options are documented once on `vycheck()`; `init()`
points at them.

**Document only the non-deprecated surface.** Deprecated fields, params, and
endpoints get exactly one footer line naming them plus a link to the OpenAPI
spec. Nothing else: no ParamField, no table row, no nav entry. The documented
confirmation surface is `verified`, `status`, `reasons`, `declined`.

## Deprecation workflow

Docs never declare a deprecation the spec does not carry. Source first:

1. In app-service, add `deprecated=True` (+ a `**Deprecated.**` description
   prefix) on the Pydantic field or route decorator.
2. Regenerate: `uv run python scripts/export_openapi.py`.
3. Confirm the append-only baseline still passes:
   `uv run pytest tests/unit/test_external_baseline.py` (deprecation is
   additive and allowed; removal is not).
4. Then edit the docs: drop the field/page, add the footer line, fix nav and
   redirects.

## Where code samples come from

The canonical snippets live in connect-fe:
`src/pages/dashboard/verifications/integration/CodeIntegration.tsx` (and
`integrationPrompt.ts`). Docs code blocks mirror them, comments included, so a
developer sees the same code in the dashboard and the docs. When either side
changes, sync the other, and correct drift against the live API rather than
copying it (that page has shipped `"flagged"` and `["collision"]`; the live
enum is `approved | denied` and reasons like `collision_company`).

## Verify before you write

The failure mode is confident prose that is wrong. Before stating any
behavior:

- **API fields and errors**: find them in `app-service/external.v3.openapi.json`
  or the route source `app-service/src/app/routes/external/v3/`. Known
  verified errors beyond the tables: `link_not_active`, `method_not_runnable`,
  `invalid_verification_config`.
- **SDK behavior**: read `browser-sdk/src/` (client.ts, connect.ts, errors.ts,
  protocol.ts). Known trap: a failed initialize throws a plain `Error`
  (connect.ts), while `VerifyYouError` is constructed only in http.ts
  `fetchWithTimeout`; check callers before documenting which error type a path
  produces.
- **Unresolved**: trust-score framing (claim gates say deductive from 100; the
  wire says 0 to 100, higher = riskier). Do not write score prose until
  reconciled.

Cannot ground a fact? `[PLACEHOLDER: exact question]` and flag it, per the
voice skill.

## Ship checklist

- `mint broken-links` and `mint validate` pass.
- No dashes in prose. No "guest"/"member"/"user". No "sandbox".
- New/moved/deleted pages have redirects.
- PR title is Conventional Commits (enforced; commit messages are warn-only).
