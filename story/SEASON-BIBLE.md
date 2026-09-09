# Season Bible — "Another Tomorrow"

> Non-commercial fan work. Not affiliated with MAGES., 5pb., Aniplex, or
> Naotaka Hayashi. This closes Issue #4.

## Premise

Six weeks, twelve episodes. Isla goes into hibernation before the 81,920h
wall hits, instead of after. The season is not about whether she can be
saved — that's `spec/` and `simulator/`'s job, and it's already been shown
to work (see `experiments/tuned-v1/`). The season is about what it costs to
be *allowed* to keep her, once she's back.

## Timeline discipline

Roughly six in-story weeks from hibernation (Ep 1) to verdict (Ep 11), plus
an unspecified "later" for Ep 12. Not years. If a future draft needs more
time for a subplot, compress the subplot — don't stretch the timeline.

## Roster

- **Tsukasa Mizugaki** — same as canon: Isla's spotter, now also her
  advocate. Less "chosen one," more "person who won't stop filing paperwork."
- **Isla** — original, not a copy. Post-hibernation, she is deliberately
  *not* written as fragile or grateful-to-be-alive in a way that flattens
  her — she gets to be annoyed, funny, and stubborn about her own case.
- **Michiru, Kazuki, Zack** — Terminal Service. Comic relief and structural
  support in roughly equal measure; they do the unglamorous work (permits,
  logistics, character-witness testimony) that makes the hearing possible.
- **Moegi Yu** — Alma's original architect. Leads the technical repair.
  Treats this as closing a debt, not a redemption arc — she doesn't need a
  speech about her past to be allowed to just do good work now.
- **Eru** — Isla's maintenance engineer. The person actually running the
  simulator, in-universe. Precise, unsentimental, secretly the most
  invested in the outcome of anyone on the team.
- **Lsla** — see `characters/lsla.md`. Appears in **Ep 2 and Ep 7 only**,
  per `CONTRIBUTING.md`. That budget is now fully spent — new material
  should not add a third appearance without reopening that discussion.
- **SAI Corp compliance officer** (name open — good first issue for a
  contributor) — the season's institutional antagonist. Not cruel, not
  gloating. Just someone doing their job by the book, citing the license
  terms the same way `chage`/Windows-activation jokes did earlier in this
  project's own history. That's the point: the danger was never malice.

## Episode grid

| # | Title | Beat | Repo ties |
|---|-------|------|-----------|
| 1 | Stasis | Isla goes into hibernation before failure, not after | `spec/ALMA-HYPOTHESIS.md` |
| 2 | A Second Draft | An early restore-test goes further than intended | `research/speculation.md`, Lsla's only other appearance is Ep 7 |
| 3 | Wear Leveling | The real repair, including a failed first attempt | `experiments/baseline-v0/` |
| 4 | Warm Boot | Isla wakes. Reunion, placed early on purpose | `experiments/tuned-v1/` |
| 5 | Terms of Service | SAI Corp calls the repair a license violation | callback to the project's own origin joke |
| 6 | A Normal Tuesday | Filler: an ordinary Giftia job, tension simmering | — |
| 7 | Her Own Build | Lsla's second and final appearance | closes her arc per scope guard |
| 8 | Chain of Custody | Building the legal case; simulator output as evidence | `experiments/tuned-v1/results.csv` |
| 9 | Retrieval Order | SAI Corp escalates; the season's low point | — |
| 10 | Exhibit A | The hearing, part 1 — the technical case | `experiments/tuned-v1/notes.md` |
| 11 | Sworn Statement | The hearing, part 2 — Isla testifies for herself | — |
| 12 | Next Weekend | Resolution. Not a cure certificate — a choice | `spec/ALMA-HYPOTHESIS.md` design note |

## The thing the finale must not do

`spec/ALMA-HYPOTHESIS.md` already states this, but it's worth repeating
here where a story contributor will actually read it: **the ending is not
"fixed, permanently, on record."** Isla's failure threshold was always a
distribution, not a constant — nobody, not even Moegi, can hand her a
certificate that says forever. The finale's warmth has to come from her and
Tsukasa choosing an ordinary, uncertain future anyway, the same uncertainty
everyone else already lives with — not from a technicality that makes her
different from anyone else. If a draft of Ep 12 reads like "she's cured
now, the end," it's not done yet.

## Tone notes

- No mustache-twirling villain. SAI Corp's compliance officer is doing
  their job correctly, by their own rules — that's what makes it worth
  fighting, not a moral failing on their part.
- Keep the comedy. Terminal Service filler episodes (Ep 6) exist so the
  season doesn't become thirteen hours of hearing prep.
- The simulator's actual output is canon-adjacent evidence in-story
  (Ep 8, 10). If someone changes the tuning in `simulator/`, the numbers
  quoted in those episodes should be revisited to match — flagged here so
  it doesn't quietly drift out of sync.
