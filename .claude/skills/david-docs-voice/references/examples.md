# Examples

Before-and-after pairs by surface. Models imitate examples far better than they obey rules, so
this file moves a draft further than the rule list does. Match the moves, do not paste the
sentences.

Several "after" examples are strings that are live in the product or on the site today, marked
where that is the case. Those are the standard.

---

## 1. In-product: a checklist item

The dashboard's setup checklist is the best copy in the app and worth reading as a whole. What
makes it work is that each line answers "what is this step" in the reader's terms, not the
product's.

✅ **Live today, in `CustomerDashboard/GetStarted/SetupChecklist.tsx`**

> **Build a check**: Choose what you're verifying and how strict to be.
> **Share it or add it to your product**: A no-code link, or a few lines of code.
> **Verify your first real person**: The moment someone comes through and passes.

"The moment someone comes through and passes" is doing something a spec sheet cannot: it tells
you what success feels like. That is the register to aim for on a first-run surface.

❌ **The version to avoid**

> **Integration Setup**: Configure your verification parameters and implement the SDK.
> **Go Live**: Complete the onboarding process to begin verifying users.

Names the system's steps instead of the reader's, uses "users", and "Complete the onboarding
process" is a sentence about our funnel rather than their product.

---

## 2. In-product: What's New

✅ **Live today, and close**

> **HumanCheck now has an SDK**: Drop verification into your product faster, now on desktop as
> well as mobile.
> **A redesigned dashboard**: Every check has its own space for insights, activity,
> integration, and invites.

Both name the change and what the reader gets from it.

⚠️ **The one line in that file to fix**

> "We've rebuilt VerifyYou around your checks! Plus a few big additions this release."

The exclamation mark is announcement voice, and it is the exact tell that separates product
copy from marketing copy. It also sets a precedent every future entry has to match. Nothing
else about the sentence is wrong.

> Rewritten: "We've rebuilt VerifyYou around your checks, plus a few larger additions this
> release."

---

## 3. In-product: empty state

❌ **Before**

> No verifications yet! 🎉 Once your users start verifying, you'll see all their information
> here. Get started by integrating VerifyYou today!

✅ **After**

> No verifications yet. Each completed check appears here with its verdict and the signals
> behind it. Share your verification link or wire up the SDK to see the first one.

What will appear, then the one action that makes it appear. An empty state is the only screen
guaranteed to be seen by every new customer, so it is worth more care than its size suggests.

---

## 4. In-product: error message

❌ **Before**

> Oops! Something went wrong. Please try again later or contact support if the problem persists.

✅ **After**

> That token has already been confirmed. Each token can be exchanged once. Start a new check to
> verify this person again.

Cause, constraint, action. An error that does not name its cause is a support ticket you have
chosen to receive, and errors are also where a frustrated reader is least willing to forgive a
cheerful tone.

---

## 5. In-product: tooltip

❌ **Before**

> Trust Score: Our proprietary algorithm analyzes multiple data points to generate a
> comprehensive trust rating for each verification.

✅ **After**

> Everyone starts at 100. Signals collected during the check deduct from it.

Two sentences. If a tooltip wants a third, the label above it is doing too little work.

---

## 6. Docs: opening a concept page

❌ **Before**

> VerifyYou is a cutting-edge identity assurance platform that leverages advanced biometric
> technology to help businesses verify their users. In today's landscape, bots and fraudulent
> accounts are a growing challenge.

Leads with us, three banned words, no mechanism, "users" instead of guests, and "identity
assurance" claims something we deliberately do not do.

✅ **Live today, on `learn.verifyyou.com`**

> A check is a short, hosted flow. It can take over the page, open as a drawer over your app,
> or sit inline within it. The person does a quick face scan, and you get back a result your
> server can trust. The face never touches your systems.

Four sentences, lengths varied, mechanism first, and the last one answers the question the
reader was actually holding.

---

## 7. Docs: explaining something awkward

❌ **Before**

> VerifyYou is committed to privacy. Your data is secure with us and we only retain what is
> strictly necessary for the service to function.

Says nothing, and a technical reader reads "committed to privacy" as a signal that the detail
is worse than the summary.

✅ **Live today**

> The face vector persists. That is what makes uniqueness work: if we did not keep it, we could
> not tell a returning person from a brand new one, and someone you blocked could come straight
> back. We keep it on purpose.

The awkward fact, the reason, then ownership. Reach for this shape whenever a true fact looks
unhelpful.

---

## 8. Docs: the boundary against KYC

❌ **Before**

> HumanCheck delivers enterprise-grade identity verification without the friction of
> traditional KYC solutions.

Claims identity verification, which we do not do. "Enterprise-grade" means nothing. Frames KYC
as a competitor rather than a neighbour we sit beside.

✅ **After**

> We answer one question, is there a real, unique, live human on the other end, while holding as
> little about that person as possible. We do not need to know who someone is, so you carry far
> less personal data than a government-ID check would leave you holding, and none of the
> documents that come with it.

---

## 9. Reference: an endpoint

❌ **Before**

> The confirmation endpoint is a powerful tool that allows you to seamlessly retrieve the
> verification status of a user. Simply pass your token and you're good to go!

✅ **Live today**

> Your server exchanges the token at `GET /v3/confirmations/{token}` with your secret key, never
> from the browser, and gates access on the `verified` field it returns. That answer is the
> truth, not the hint on the URL.

The second sentence is not decoration. It names the mistake this endpoint invites, before the
reader makes it. That is the only kind of voice reference documentation wants.

---

## 10. Changelog entry

❌ **Before**

> ### Enhanced Dashboard Experience 🚀
>
> We're excited to announce a suite of powerful improvements! Users can now enjoy a more
> seamless and intuitive experience when reviewing verifications. This update represents a
> significant step forward in our mission.

✅ **After**

> ### Signal history on the subject profile
>
> The subject profile now keeps the last five changes to a person's signals, so you can see how
> someone's picture changed between their first check and their most recent one. Open any
> subject and the history sits under the current signals. This is most useful when a person
> passed once and looks different on return, which previously meant opening two sessions side
> by side and comparing them by hand.

What changed, what the reader sees and does, why it matters. No emoji in the heading, no
announcement voice, no mission statement.

Copy the shape, not the content. That entry is written from a standup note about signal history
being wired up, which is not the same as it being visible to a customer, so as written it would
trip the unshipped-feature gate. It is here because it is a useful illustration of how easily a
true-sounding release note gets ahead of the product.

---

## The two cadence tells

**Stacked short lines.** Five sentences in a row of near-identical length reads as generated
even when every sentence is true. Break the pattern deliberately.

**The closing summary.** After three examples, a model writes a sentence restating them.

❌ *"They aren't holding up a photo. They aren't using a printed page. They aren't wearing a
mask. All of these attacks are blocked."*

✅ *"They are not holding up a photo, not using a printed page, not wearing a mask. People try
all sorts of things."*
