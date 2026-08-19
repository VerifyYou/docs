---
name: david-docs-voice
description: The VerifyYou customer-facing writing voice, derived from how David actually explains the product, plus the claim gates that stop copy from shipping things that are not true. Use this whenever you write or edit words a customer will read: a docs or concept page, a changelog or What's New entry, an empty state, a tooltip, a button label, an error message, onboarding or Get Started copy, a marketing-adjacent page, or a PR that touches any user-facing string. Reach for it even when the request is "just a quick copy tweak" or "fix this wording" and nobody mentions voice, because the failure mode here is confident prose that is subtly wrong. Not needed for internal staff-only screens, code comments, or commit messages.
---

# The VerifyYou customer voice

David Graham is the CEO and the reason customer-facing copy sounds the way it does. But
**David does not write documentation or product copy.** He writes sales email and he talks on
calls. Port his email voice into a dashboard and you get exclamation marks, `:)`, "Happy to",
and a sign-off in the middle of a tooltip.

What transfers is **how he explains a thing**. The sales apparatus around it does not. This
file is that split.

One rule sits above the rest:

> **The voice comes from David. The claims never do.**
>
> He says things on calls, and verifyyou.com says things, that cannot be published. His
> framing is the source of the prose. `references/claim-gates.md` is the source of what is
> allowed to be true. When they disagree the gate wins.

That is not fussiness. The last pass of AI-written product copy shipped errors, and a parallel
test of an AI writer invented a product name, asserted GDPR compliance unprompted, and claimed
no biometric storage, all in one afternoon. Two of those three are the expensive kind. Read the
gates before you write a factual sentence, not after.

## Who is reading

Check this first, because it decides how much of the file applies.

**Customer-facing** is anything a customer or a guest sees: the customer dashboard, docs,
changelog, onboarding, error states, emails. All of this file applies.

**Internal and staff-only** is the internal portal, admin tools, debug surfaces, Storybook
titles, code comments, commit messages, and PR bodies. Be clear and be brief. None of the voice
rules below apply, and forcing them there wastes everyone's time.

If a component is imported by both, write for the customer.

## The six moves that carry over

Each is a real David sentence, then the same move in product register. Imitate the move, do not
paste the sentence.

**1. Explain the mechanism, then name it.**

> David on a call: *"We prove liveness, so you can't run a bot script. And then number two,
> uniqueness, so you can't have one person creating 15 identities."*

Consequence first, term second. So: "a quick scan confirms a live, present human, and checks
whether we have seen them before" lands before the words liveness and uniqueness appear. A
reader who meets a term after the idea remembers it. A reader who meets it first skims.

**2. Lead with the reader's job.**

> David on what buyers actually want: *"They're not really after your identity, and they don't
> really want the PII. They just wanna make sure that if I block him, he's not gonna come back
> 15 times over."*

Open on the reader's problem or their next action, never on "VerifyYou is a platform that...".
The live docs do this: *"You send them through a hosted verification flow; they come back with
a result you confirm on your server."*

**3. Reach for the concrete comparison.**

> David on the record: *"similar to how Apple's Face ID works."*
> David on fraud economics: *"We use a framework called cost to beat. Ours is nearly $20,000,
> plus a lot of skill and time."*

A comparison the reader already holds beats an accurate abstraction. Tier labels and internal
vocabulary lose people. This product is genuinely hard to understand, and it is mistaken for
KYC constantly, so the analogy is doing real work rather than decorating.

**4. Name the limit instead of routing around it.**

> The best sentence currently on the site: *"The face vector persists. That is what makes
> uniqueness work: if we did not keep it, we could not tell a returning person from a brand new
> one, and someone you blocked could come straight back. We keep it on purpose."*

Say the awkward thing, then say why, then own the decision. Copy that hides a limitation reads
as marketing, and the reader finds the limitation anyway, in production, at a worse moment.

**5. Leave lists open.**

> David on spoof attempts: *"they're not a picture of a picture. They're not a piece of paper.
> They're not wearing a mask"* ... *"there's so many different things that people try."*

Three examples is fine. Three examples presented as the complete set is the tell. He is naming
things off the top of his head and he knows there are more, so he shrugs at the end. A model
closes the list and then writes a summary sentence under it, because to a model the list was
the point. Skip that summary sentence.

**6. Stop when the answer is done.**

No uplifting closer, no restatement. The last sentence is the last piece of information.

## What does not transfer from his email

| In David's email | In product and docs |
|---|---|
| `Hey Neha,` / `Best,` + signature | Nothing. No greeting, no sign-off |
| `:)` with no space, `💪` | Never |
| "Excited to get this live!" | A release note can be pleased. It cannot be excited |
| "Happy to", "Are you open to a quick chat?" | No CTAs into sales. A doc ends on a link or on nothing |
| "I", "we'd love to" | Second person for the reader. "We" only for VerifyYou doing a thing |
| A question mark on a statement, as a softener | Product copy states |
| Spaced dashes as a connector, which he uses constantly | Zero dashes of any kind |

## The four surfaces

One voice, different amounts of it. Voice concentrates in explaining and thins toward reference.

**Concept and explainer pages** carry the most. Analogy, the honest boundary, the mechanism
walked step by step. This is where a reader decides whether to trust the thing.

**Reference** (endpoints, parameters, SDK calls) is nearly voiceless. Second person,
imperative, one idea per sentence. Voice shows up only as the aside that saves an hour, like
*"The `vyc` value the client sees is only a UI hint."* Do not warm up a parameter table.

**In-product copy** is the shortest register and the least forgiving. An error names what
failed and the one action that fixes it. An empty state names what will appear here and how to
make it appear. A tooltip that needs three sentences means the label is wrong. No apology, no
emoji, no exclamation mark. Note that this copy lives inline in the components, so the moment
you write it, it ships with the next deploy; there is no separate copy review.

**Changelog and What's New** carries what changed, what the reader now sees or does, and why it
matters, in that order, ordered by how much a customer cares. One line is fine for a small item
and depth is right for the top one. Never write an entry for something that has not shipped.

## Mechanics

- **No em dashes and no en dashes, anywhere.** Comma, full stop, or rewrite. Ranges are "3 to
  5", not "3-5". David uses dashes constantly in his own email. The ban is deliberate and it
  applies to written copy because the dash is the single strongest signal a page was machine
  written.
- **Second person, active.** "You set the threshold," not "the threshold is set."
- **One idea per sentence. Sentence case headings.**
- **Vary sentence length.** Five sentences of near-identical length reads as generated even
  when every one is true. Put a long flowing sentence next to a short one.
- **Never open two consecutive paragraphs the same way.**
- **Banned vocabulary:** delve, leverage, robust, navigate, landscape, seamless, game-changer,
  best-in-class, value add, drive results, "in today's world", "we're excited to announce",
  "circle back", "touch base", and the construction "it's not just X, it's Y".
- **No significance inflation.** Not watershed, not pivotal, not revolutionary.

## Terminology, exactly

- **HumanCheck** is the product, one word, capital H and C. **VerifyYou** is the company.
- **Guests** are the people being verified. **Members** are the customer's own logged-in
  people. Not "users", not "accounts", for either.
- **Face vector**, described as a numerical representation of the face's geometry. Never "face
  ID", "hash", "template", or the vendor or model behind it.
- **Verification** is the event. **Verdict** is what a server gates on.
- The two things proven are **liveness** (a real, live person, not a script or a replay) and
  **uniqueness** (this person once, not fifteen times).
- Say **test keys** or **the simulator**. Never "sandbox".

## Working through a change

1. Decide the surface and the audience. Internal? Stop, just write clearly.
2. Draft it. Reach for `references/examples.md` when a draft is factually right and still reads
   generated. That file is before-and-after pairs taken from copy that is live today, and
   examples move a draft further than rules do.
3. Check every factual sentence against `references/claim-gates.md`. If a fact is not in the
   gates and not in the product in front of you, write `[PLACEHOLDER: the exact question]` and
   flag it rather than guessing a number, a retention window, a signal name, or a capability.
4. Score it with `references/rubric.md` if it is more than a line or two. Ship at 17 of 20 with
   no zero on the three hard gates.

## Making this yours

This started as a distillation of one company's voice, and the parts most likely to need
adjusting are, in order: the terminology list, which drifts as the product renames things; the
capability boundaries at the end of `claim-gates.md`, which are the most perishable thing here
and are worth re-checking against the product every month or so; and the examples, which get
stronger every time a real page you liked replaces an invented one. The six moves and the
mechanics are the stable core and are the last thing to touch.

If you want this to fire reliably, add a line to the repo's `CLAUDE.md` pointing at it, since
that file is always in context and the skill description alone is doing all the triggering work
today.
