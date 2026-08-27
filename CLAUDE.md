# CLAUDE.md: VerifyYou docs

Public Mintlify docs site (docs.json + MDX under v1/ v2/ v3/). `mint dev` to
preview; `mint broken-links` and `mint validate` before pushing.

Three skills govern work here. Load them before editing, not after:

- **`.claude/skills/dev-docs/SKILL.md`**: read before touching `v3/dev/` or
  `docs.json`. The reader, the page architecture, what each Integrating page
  must teach, reference format, the deprecation workflow (spec first, docs
  second), where code samples come from, and the verify-before-you-write list.
- **`.claude/skills/david-docs-voice/SKILL.md`**: read before writing any
  prose a customer reads. Voice and claim gates. Repo override: the person
  being verified is a "person" (never guest, member, or user).
- **`.claude/skills/changelog/SKILL.md`**: read before adding or editing an
  entry in `v3/changelog.mdx`. The postmortem trap that makes fix entries leak
  internals, how much weight an item earns, date and time grouping in
  `<Update>`, and what to verify in the source before describing a fix.

`.claude/agents/technical-writer.md` is a reference for coverage checklists on
reference pages.

Quick facts: v3 is the default version (v2/v1 legacy behind the dropdown); the
publishable key is deprecated; docs document only the non-deprecated API
surface; the API contract is app-service's generated
`external.v3.openapi.json`; PR titles must be Conventional Commits.
