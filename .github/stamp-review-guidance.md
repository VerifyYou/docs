# Stamp review guidance

What a second reader checks before a pull request in this repository can merge on the review
gate's approval. The gate decides eligibility from `.github/stamp-policy.yml`; this file tells
the reader what to look at inside the diff it is handed. It never widens eligibility.

This is the public Mintlify docs site; the diffs that reach here are prose, a changelog entry
or an image.

## What to check

- Every factual claim passes the claim gates in `.claude/skills/david-docs-voice/`. A
  sentence that asserts compliance, storage behavior, accuracy or a product name that the
  gates do not allow is blocking, however small the diff.
- The person being verified is a "person": never guest, member or user. Reintroducing the
  retired framing, even in a quote from an older page, is a finding.
- The docs describe only the non-deprecated API surface, and the contract is app-service's
  generated `external.v3.openapi.json`. A new field, parameter, endpoint or default that
  the spec does not carry is blocking; the spec changes first, the docs second.
- v3 is the default version. A v3 page that links into `v2/` or `v1/` is a finding.
- A new or moved page is listed in `docs.json` navigation, and a moved or deleted page has a
  `redirects` entry. The policy makes `docs.json` needs-human, so a page move never reaches
  the reader alone; a new page with no nav entry is a finding.
- Changelog entries in `v3/changelog.mdx` follow `.claude/skills/changelog/`: say whether the
  reader has to change anything, group by date in `<Update>`, and cut the internal cause.
  An entry that explains our stack or names a defect's root cause is a finding.
- Server API and SDK pages keep the reference section order from `.claude/skills/dev-docs/`.
- Links resolve (`mint broken-links` is the check), images live under `images/`, and the PR
  title is a Conventional Commit.

## What is never eligible

The gate refuses these before the reader sees them, so a diff touching them here means the
policy file is wrong, not that the reader should try harder.

- `docs.json`, `.mintignore`, `vy-intro-gate.js`, `style.css`, `learn.css`: the site config
  and the code and styles shipped to every visitor.
- `v2/openapi.yaml`, `package.json`, `pnpm-lock.yaml`, `.claude/`, `CLAUDE.md`, CI, and this file.
- A pull request an agent opened. The fleet does not stamp itself.

## How to write a finding

- One finding per thread, on the line it is about. Prefix it: `blocking:` must change before
  merge; `suggestion:` worth considering; `nit:` the author can ignore; `question:` you need
  the answer before you can judge.
- Say what is wrong and what would make it right. Do not restate the diff.
- No register or wording comments; the voice skill owns those. You check claims, structure
  and links.
- If a finding is outside the change, say so and stop; it is not this PR's problem.

## Verdict

End the review with exactly one line:

- `verdict: no_blocking_findings` when nothing above is blocking.
- `verdict: blocking` when at least one finding is blocking; the threads say which.
- `verdict: needs-human` when the change touches something a person should read regardless
  of the paths: pricing, a security or privacy claim, a compliance statement, a customer-visible
  behavior the spec does not confirm, or anything you could not judge from the diff alone.
