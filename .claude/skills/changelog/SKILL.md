---
name: changelog
description: How to write a VerifyYou changelog entry, especially for bug fixes and reliability releases. Use whenever adding or editing an entry in v3/changelog.mdx, writing release notes, or turning a batch of merged PRs into something a customer reads. Covers the postmortem trap that makes fix entries leak internals, how much weight an item earns, the date and time grouping in the Update component, and what to verify in the source before describing a fix. Load it before writing the entry, not after.
---

# Writing a VerifyYou changelog entry

For voice, load `.claude/skills/david-docs-voice/SKILL.md`; its claim gates decide
what may be stated as fact. This file is what the voice skill's one changelog
paragraph does not cover: what to do when the thing that shipped is a bug fix.

The entries live in `v3/changelog.mdx`. Feature entries are the easy case and
mostly write themselves from the API surface. Fix entries are where this goes
wrong, every time, in the same way.

## The reader and what they want

A developer who has already integrated. They are scanning for one of three
things, in this order:

1. **Do I have to change anything?** Answer it in the entry, always. Usually
   "nothing to upgrade, it works with the SDK version you already run."
2. **Was that weird thing I saw last week this?** They fielded a support ticket
   or watched a person fail a check. They want to match their symptom to your
   line and close the loop.
3. **Did a behavior I depend on change?**

Nobody is reading to learn how our system works. That is the whole reason fix
entries go wrong.

## The postmortem trap

The natural shape for a fix, and the one a model reaches for unprompted, is:

> symptom, then internal cause, then fix

Cut the middle. The cause is the part that describes our stack, and it is the
part the reader cannot act on. Keeping it does three kinds of damage at once:
it teaches customers our internals, it advertises that we shipped the defect,
and it pads an entry that should be one line.

The claim gate this sits under is "describe what a customer experiences, not
what runs underneath" (`david-docs-voice/references/claim-gates.md`).

❌ **Shipped, then rewritten**

> A small share of phones that scanned the QR code on the desktop flow were told
> the code had already been used on another device. The page was claiming the
> code twice from the same phone. It claims once now, and a second scan from the
> same phone resumes where it left off.

"The page was claiming the code twice" is a race condition narrated to
customers. It is also the only sentence in there they cannot use.

✅ **What landed**

> An older phone scanning the desktop QR code could be told the code was already
> used on another device. It now resumes where it left off. A different phone
> opening a used code is still refused.

Symptom, current behavior, and one guard clause. See `references/examples.md`
for the rest of the pairs, including the two that took several passes.

Root cause analysis is not homeless, it just lives somewhere else: an incident
note, a status page, the PR body. Not the developer changelog.

## Weight matches blast radius

Order items by how many people are affected, and give each one only as much room
as that earns. Three small fixes are three bullets under one heading, not three
`##` sections. A `##` section per fix puts a two-line bug on the same visual
footing as a feature, which is how a "quick fixes" release ends up reading like
a bad quarter.

One line is a complete entry. Depth is for the item at the top.

## Scope a fix honestly

**A fix for one customer is not a statement about every reader.** This is the
easiest way to write something technically true and substantively misleading.
If a bug only ever reproduced in one customer's native app webview, the entry
gets one line at the bottom. It does not get a framing paragraph explaining
what "embedded flows" do, because that reads as a property of the product and
sends everyone else chasing a problem they do not have.

Before writing a cause or a condition into an entry, ask who it actually
applied to. "Older phones", "a person whose session had died", and "inside a
native app webview" are honest scopes. "Browsers", "embedded flows", and "some
users" are usually a one-case bug wearing a general costume.

## Verify the fix before describing it

Same failure mode as the rest of the docs: confident prose that is wrong. Read
the actual diff, not the PR title, not the commit message.

- **app-fe fixes**: find the handler or the hook. What the person sees is the
  claim you are making, so read to the render, not just to the network call.
- **Check the trigger's real scope.** A recovery path guarded by two specific
  error codes is not "when something goes wrong". If your sentence is broader
  than the guard, either narrow the sentence or flag that the fix may not cover
  what people actually hit.
- **Read the string.** If you write "with a note saying why", open the file and
  confirm the note says why. It usually says what happened and what to do next,
  which is a different claim.

Cannot ground it? `[PLACEHOLDER: the exact question]` and flag it, per the voice
skill.

## Keep the guard clauses

Trim words, not claims. A clause that stops a reader from concluding something
false about security or data earns its space even in a one-line entry.

> A different phone opening a used code is still refused.

Nine words, and without them the bullet reads like QR codes became reusable
across devices. When cutting for length, cut mechanism first, then adjectives,
then background. Guard clauses go last.

## Mechanics

**One `<Update>` per release day**, labelled with the date:

```mdx
<Update label="August 26, 2026" description="Embedded flow">
```

**Two releases in one day** do not get two boxes. Put both under the one dated
label and give each entry its time beside the heading:

```mdx
## Reliability fixes <span className="changelog-stamp">21:30 UTC</span>
```

`.changelog-stamp` is defined in `style.css` at the repo root. It uses
`currentColor` with opacity rather than a palette token, so it stays muted in
both themes and survives a Mintlify rename. The stamp is only for days carrying
more than one release; a single-release day needs no time, and never invent one
for a past entry that did not record it.

Note that the time rides in a span inside the heading, so it appears in
Mintlify's right-hand "On this page" list too. That is the accepted cost of
keeping it beside the heading.

**Newest first**, and entries are append-at-top. Do not renumber or restructure
older entries while adding a new one.

## Before you open the PR

- `npx mint validate` and `npx mint broken-links` pass.
- No em or en dashes. No "guest", "member", "user", or "sandbox". The person
  being verified is a **person**.
- Every fix entry answers "do I have to change anything?"
- No sentence explains why the bug happened.
- Nothing describes a scope wider than the one you verified.
- PR title is Conventional Commits.
