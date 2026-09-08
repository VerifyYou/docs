# Changelog examples

Before-and-after pairs from a single real editing pass on `v3/changelog.mdx`, the
August 26, 2026 entries. Every "before" shipped to `main` in PR #38 and every
"after" is what replaced it in PR #39, so both halves are in git and neither is
invented.

Two of these took three passes. The intermediate drafts are included, because
the wrong middle version is more instructive than the finished one: it is what
a careful writer produces when they have fixed the obvious problem and not yet
found the real one.

---

## 1. The postmortem, in its purest form

❌ **Shipped**

> ## Embedded flows complete on Safari
>
> A person who opened your embedded flow in Safari, on an iPhone or a Mac, could
> tap Accept on the consent step and get nowhere. Safari keeps no cookies for a
> page shown inside another site, so every tap arrived as a brand new visit. The
> flow now carries the person's session for the life of the page whether or not
> the browser keeps the cookie. Nothing to change on your side, and nothing to
> upgrade: it works with the SDK version you already run.

Sentence two is a lesson in browser cookie policy. Sentence three describes the
mechanism we built to route around it. Together they tell a customer that our
embed hangs off a cookie and that we had not handled a well known browser
behavior. Neither sentence changes anything the reader does.

✅ **What landed**

> - Embedded flows now complete inside a native app webview.

One line, at the bottom of the list. See example 2 for why it also got narrower.

---

## 2. The scope error, and the draft that looked like a fix

This is the one worth studying. The first rewrite removed the mechanism
correctly and then made a worse mistake.

⚠️ **Intermediate draft, mechanism removed, scope broken**

> An embedded flow runs inside your page, often in a webview, where the browser
> is slow to keep the flow's session cookie or refuses to keep it at all. Two
> fixes came out of that:
>
> - The flow in Safari, on iPhone and on Mac, could stop at the consent step. It
>   completes.
> - A phone scanning the desktop QR code could be told the code was already used
>   on another device, when that other device was the same phone. It now resumes
>   where it left off.

Every sentence here is true of the bug that was fixed. It is still wrong,
because the webview case was **one customer hosting the flow in a native app**.
Written this way it reads as a property of embedded flows in general, so every
other reader now believes there is a cookie problem in the product they
integrated. A framing paragraph promotes a single case into a rule.

It is also 60 words of preamble on a release whose contents are three small
fixes.

✅ **What landed**

> ## Reliability fixes <span className="changelog-stamp">21:30 UTC</span>
>
> - An older phone scanning the desktop QR code could be told the code was
>   already used on another device. It now resumes where it left off. A different
>   phone opening a used code is still refused.
> - The consent step could do nothing at all for a person whose session had died.
>   It now refreshes and asks for one more tap.
> - Embedded flows now complete inside a native app webview.
>
> Nothing to upgrade. All three work with the SDK version you already run.

No framing paragraph. Ordered by who is affected, so the one customer case is
last. The "do I have to change anything" answer sits at the bottom covering all
three, rather than being repeated inside each item.

---

## 3. A claim that survived the trim and should not have

❌ **Shipped**

> ## The consent step recovers instead of stalling
>
> When a session has moved on since the page loaded, the consent step now
> refreshes itself and asks for one more tap, with a note saying why.

⚠️ **First rewrite, still wrong**

> The consent step could stall instead of telling the person what happened. It
> now refreshes and asks for one more tap, with a note saying why.

"With a note saying why" carried through the rewrite untouched, because it reads
like a detail rather than a claim. Opening the file settles it. The string is:

> `Your check was refreshed — tap again to continue.`

That says what happened and what to do next. It does not say why. The fix is one
word of scope, and it is only findable by reading the source.

✅ **What landed**

> - The consent step could do nothing at all for a person whose session had died.
>   It now refreshes and asks for one more tap.

Two notes on this one. "Could do nothing at all" is the honest symptom: the old
code called `setSubmitting(false)` and then threw from an async click handler,
which becomes an unhandled rejection, so the button unlocked and nothing
happened. And "whose session had died" is the scope the engineer confirmed, not
the scope inferred from the guard, which was narrower. When those two disagree,
say so in the PR rather than quietly picking one.

---

## 4. Feature entries leak too, just less

❌ **Shipped**

> - Nothing to upgrade: this is a platform change, and it works with the SDK
>   version you already run.
>
> Previously, a session minted without a redirect stopped on the verdict screen
> and the promise never resolved.

"This is a platform change" tells customers we change behavior underneath their
pinned SDK version without a release. It is meant to reassure and it does the
opposite. The "previously" sentence is a postmortem wearing a feature entry's
clothes, and "the verdict screen" is a screen name from our flow.

✅ **What landed**

> - A `redirect_url` you do pass still wins, and still comes back with
>   `?vyt=…&vyc=…` appended. If you were only passing one to keep an embed
>   working, you can drop it.
> - Nothing to upgrade. It works with the SDK version you already run.

The actionable half of the "previously" sentence, which is that you can now
delete a workaround, moves up into the bullet that already covers
`redirect_url`. The rest goes.

---

## 5. Grouping two releases on one day

❌ **Shipped**

```mdx
<Update label="August 26, 2026, 21:30 UTC" description="Reliability">
...
<Update label="August 26, 2026, 16:57 UTC" description="Embedded flow">
```

Two boxes for one day, and a label that cannot be grouped or scanned because the
clock time is buried in the middle of it.

✅ **What landed**

```mdx
<Update label="August 26, 2026" description="Embedded flow">

## Reliability fixes <span className="changelog-stamp">21:30 UTC</span>
...
## No redirect URL needed for embedded flows <span className="changelog-stamp">16:57 UTC</span>
```

The label is the group. The time is a stamp on the entry it belongs to. Days
with one release get no stamp at all, and a past entry that never recorded a
time does not get one invented for it.
