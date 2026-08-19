# Claim gates

What may and may not appear in published customer-facing copy. Check every factual sentence
against this before you publish.

**Why this file exists.** The failure mode here is not bad prose, it is confident prose that is
wrong. A previous pass of AI-written product copy in the dev docs shipped errors, and a separate
test of an AI email writer produced an invented product name ("HumanProof"), an unprompted
regulatory compliance claim, and a "no biometric storage" line, all in one afternoon. Two of
those three are the expensive kind.

**The uncomfortable part:** several of these banned claims come from things David says on calls
and things currently written on verifyyou.com. He is selling in a room, live, with a person who
can ask a follow-up. A doc has no follow-up. Take his framing, not his wording.

**Who answers what,** so a blocked sentence costs one message rather than a day:

| Question | Ask |
|---|---|
| Can we say this price, or this comparison figure | David |
| Is this shipped, and is it visible to a customer today | Zeek |
| What do we keep, and for how long | Zeek, and the privacy policy is the binding text |
| Can we say anything about a certification | Nobody yet. The answer is the security@ line below |
| Is this signal real, and on which page | Zeek, then re-check before the next customer list |

In-product copy has no separate review step. It lives inline in the components and ships with
the next deploy, so the check happens while you write it or it does not happen.

---

## The three hard gates

A draft with any one of these fails, no matter how well it reads.

### 1. The honest boundary

✅ We confirm there is a **real, unique, live human**, and whether we have seen them before.

❌ Never claim we verify a legal name, an identity, or who someone is.
❌ Never say VerifyYou does KYC, identity verification, or ID verification.

HumanCheck can sit **beside** or **on top of** KYC. It does not replace it and it is not a
lighter version of it. The positioning David uses, and the one to write toward, is the layer
between nothing and identity.

### 2. Data handling

This is the one with a dollar figure attached. Biometric privacy law (BIPA) prices a broken
deletion promise at up to $5,000 per willful violation, per person.

| ✅ Approved wording | ❌ Banned, and why |
|---|---|
| "VerifyYou does not store images." | "Images are never stored." Infrastructure may hold them; the subject of the sentence matters |
| "The scan becomes a face vector, a numerical representation of the face's geometry, and the image itself is discarded." | "Deleted within seconds." Unprovable, and minutes at best |
| "The face vector persists. We keep it on purpose, because that is what makes uniqueness work." | Any specific retention window not taken from the privacy policy |
| "Treated as sensitive biometric data." | "No biometric data is stored." A face vector is plausibly a biometric identifier |
| "The company receives a verdict and its own reference, never a face, an image, a name, or a document." | "Can't be turned back into your face." Non-invertibility is not contractually guaranteed |
| "For the exact categories, retention periods, and rights, the privacy policy is the binding source." | Restating retention in your own words anywhere |

The Face ID comparison is David's and it is fine as an **analogy for the reader's intuition**.
It is not fine as a technical guarantee. "Similar to how Face ID works" passes. "Non-reversible,
like Face ID" does not.

The load-bearing sentence, worth reusing: **uniqueness requires a persistent record.** If we did
not keep it, someone blocked could come straight back under a new email. So "we delete it" and
"we stop repeat offenders" cannot both be true, and the honest version is better copy anyway.

### 3. Compliance and certification

❌ **No SOC 2, ISO 27001, HIPAA, GDPR or CCPA claim. Do not use the words "certified" or
"compliant" about VerifyYou at all.** Not "compliant by design", not "built for GDPR", nothing.

This appears on verifyyou.com today and is being corrected. Do not propagate it. If a reader
needs this, the answer is: our current security documentation is available on request at
security@verifyyou.com, and we are happy to work through your vendor questionnaire.

---

## Do not publish without sign-off

**Pricing figures. Ask David.** No per-verification price, no discount multiple, no comparison
figure, not even one you heard on a call. Pricing is negotiated per account and varies with
volume, so any number in a doc is wrong for most readers. The published position is: tell us
your use case and we will give you a number.

**Retention and deletion specifics. Ask Zeek, and be careful.** See gate 2.

**How the matching works underneath. Never.** No cloud vendor name, no model name, no internal
terms like face IDs or vector databases. Describe what a customer experiences, not what runs
underneath.

**Unshipped features. Confirm with Zeek.** If it is not live in the product today it does not go
on the page, in any tense. Documenting something that does not exist is the fastest way to lose
a technical buyer, and it is the error mode AI-written docs fall into hardest.

**Self-serve signup. Do not imply it exists.** Workspaces are set up by the VerifyYou team.

**The word "sandbox".** Say test keys, or the simulator, whichever you actually mean.

---

## Capability boundaries to know

Things that are easy to write and are not true today. Re-verify with Zeek before stating any of
them, because several are mid-build and the answer moves.

- **No hardware-level device identifiers.** Known devices and new-device events exist in a
  loose sense. Never imply hardware fingerprinting.
- **Location is derived from IP**, not from device location. Do not make accuracy claims about
  it without Jack's sign-off.
- **Origin and referer** are captured but unreliable server to server, so they are not
  displayed. Do not list them as signals.
- **Two different taxonomies exist on two different pages.** The subject profile uses Capture,
  Person, Location, Device and Network. The Insights page uses threat bands (Low, Moderate,
  Elevated, High) and threat families (Network, Velocity, Automation, Liveness, Identity).
  Always name which page you are describing. Do not blend them.
- **The trust score is framed deductively:** everyone starts at 100 and signals collected during
  the flow deduct from it.
- **Cross-network recognition** is the platform story and is sold in the present tense. A
  technical reader who asks to *see* a partner count or a flagged-elsewhere signal will not find
  one in the dashboard yet. Write the capability, do not invent the UI for it.

## When you cannot ground something

Write `[PLACEHOLDER: <the exact question>]` and flag it in the PR. A placeholder costs one Slack
message. A wrong number costs a customer or a lawyer.
