# Dashboard screenshots

Nine. Four agreed first, two added when Per user drill in was written, and three wanted for
Existing users setup, not yet shot. James's 2026-08-28 walkthrough captures show the flow but
are of the live workspace with his real address, which rule 1 exists to keep off the site, so
the guide ships with switch-method only until the demo shots land. Check first that the demo
workspace offers the Existing users method, it is in beta.

Four, and only four. The reasoning is in the reply that commissioned them: this product changed
in four places between two scans two days apart, so a screenshot that goes stale fails silently
where a stale sentence gets caught by a reader.

## Rules

1. **Shoot the demo workspace, never the live one.** Live Activity carries real emails and phone
   numbers, and those become public the day this merges. The demo uses `scenario.vy.test`
   addresses, which are safe.
2. ~~Date every caption.~~ Dropped 2026-08-21, James: the dates read as clutter on the page. The
   trade-off is real, drift is now invisible to a reader, so the guard has to be process instead.
   Re-shoot all six whenever the dashboard changes shape, and treat these images the same way the
   link audit is treated: check them the morning of a merge, not weeks before.
3. **Nothing with a meaningful number in it.** Numbers date a shot fastest and none of ours mean
   anything to a reader.

## The four

Demo base URL:
`https://dev.platform.verifyyou.com/internal/preview/435be6dd-662c-43d0-a9d1-7a01ae5f3cd7/verifications/d85facc8-195b-4520-91cf-2a56e1c0d0cb`

| Save as | Where | Include | Goes on |
|---|---|---|---|
| `flags-list.png` | `/flags` | The family chips (All, Network, Geography, Accounts), the three bars, and the first four or five rows | Flags |
| `flags-detail.png` | `/flags`, then click any **VPN exit** row | The whole modal: the banner, What we saw, Where the connection surfaced, Final trust | Flags |
| `configuration-identity.png` | `/configuration` | The Identity panel expanded, showing the three access types | Configuration |
| `switch-method.png` | `/integration`, then **Switch method** | The dialog with all four methods visible | Integration |
| `person-trust-snapshot.png` | `/activity`, then open any row | The **right-hand panel only**: the score out of 100, the line under it that says the score is from the most recent scored pass, Attributes, and Activity | Per user drill in |
| `person-signals.png` | Same person, **Signals** tab | The five categories with their counts, and the High / Medium / Low filter | Per user drill in |
| `existing-users-add-people.png` | `/integration`, method on **Existing users** | The Add people panel: the explainer text, the paste box, Upload CSV, Add people | Existing users setup |
| `senders-panel.png` | `/activity`, then click the address in the header | The Senders panel: the address marked Verified, "Confirmed. Ready to send", and the TXT and CNAME rows | Existing users setup |
| `send-dialog.png` | `/activity`, select a row, then **Send** | The whole dialog: Recipients, From, the Message dropdown, the copy preview | Existing users setup |

Crop to the content area if you can. The internal preview banner at the top of the demo should not
be in shot.

Drop them in this folder and say the word.

## Added 2026-09-02

Five more, shot by James in the demo workspace, cropped to the content area here. Two carry his
green annotation arrows, kept on purpose: the caption says what the page needs, the arrow shows
it. All five carry demo numbers (224 verifications, 91% pass rate, 581 settled passes), which
bends rule 3; they are scenario data, but they will date the shots the same way real ones would,
so re-shoot on the same trigger as the rest.

| File | Where it was shot | Goes on |
|---|---|---|
| `new-verification.png` | Verifications list, New verification annotated | Creating a verification |
| `branding-tab.png` | A verification's Branding tab | Branding your check |
| `on-collision.png` | Configuration, the On collision panel in full | Configuration |
| `activity-filter-export.png` | A verification's Activity tab, Filter and Export annotated | Reading Activity |
| `insights-overview.png` | Insights, cropped above Top threat families | Reading Insights |

`insights-overview.png` is cropped above the lower panels deliberately: the demo (a DEV build)
titles the panel "Top threat families" while the docs and the 21 Aug prod scan say "Top threat
signals". Keeping the panel out keeps the shot from contradicting the page. If prod really did
rename it back, Reading Insights needs a text fix, not a wider crop.
