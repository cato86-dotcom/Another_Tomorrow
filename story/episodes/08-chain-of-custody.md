# Episode 8 — "Chain of Custody"

**Logline:** Saving Isla was the technical problem. Proving it, on the
record, to people who don't want to believe it, is a different one.

**Timeframe:** Following directly from Ep 7.

**Focus:** Moegi, Eru, Michiru, Tsukasa.

## Beats

- The team shifts from "did it work" to "can we prove it worked, to
  someone who'd rather we hadn't." Moegi and Eru compile a formal record:
  every test run, every failure, every parameter change — including the
  ones that didn't work, submitted alongside the ones that did.
- A pointed exchange: Michiru asks why they're including the *failed*
  attempts in the filing at all — wouldn't a clean record look stronger?
  Moegi's answer is the episode's thesis: a result nobody can independently
  re-derive isn't evidence, it's a claim. The failures are what make the
  success credible.
- The simulator's actual output becomes a literal prop on screen — Eru
  presenting a results table (numbers matching `experiments/tuned-v1/`)
  as Exhibit material, in-universe, for the first time.
- Michiru handles the unglamorous legal-adjacent labor: statements from
  Terminal Service coworkers, character-witness affidavits, the
  paperwork nobody wants to do but which the case depends on.
- A quiet scene between Tsukasa and Isla about what testifying will
  actually mean for her — not talked out of it, but making sure she knows
  it's a choice, echoing Ep 7's point.
- Ends with the filing complete and a hearing date confirmed — and SAI
  Corp's retrieval order, still "under review" since Ep 5, suddenly moving
  again.

## Ties to repo

Directly stages `experiments/tuned-v1/results.csv` and its accompanying
notes.md as in-story evidence. If those numbers change in a future PR, this
episode's dialogue should be checked for drift.

## Tone

Methodical, a little dry, with the stakes creeping in around the edges of
otherwise procedural scenes.
