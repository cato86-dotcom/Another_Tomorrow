# Tuned v1 — closes the gap left by baseline-v0

Command: `python3 -m simulator.alma_sim.run_experiment --seed 81920`

| controller   | hours_survived | memories_lost | WAF  | identity_forks |
|--------------|---------------:|---------------:|-----:|----------------:|
| original     | 13,410         | 106,590         | 1.00 | 0 |
| naive_unlock | 20,193         | 99,913          | 1.00 | 0 |
| repaired     | 120,000        | 0               | 0.14 | 0 |

`original` and `naive_unlock` are unchanged from `experiments/baseline-v0/`
on purpose — this run only tunes the `repaired` controller's parameters.
`repaired` now survives the full 120,000-hour test window with zero
memories lost, on this seed and (see below) reliably in general.

## What changed, and why these numbers and not others

`baseline-v0` used `spare=40, batch=4` (batch was an unlabeled class
default, not a named tuning knob yet). That configuration only cleared the
81,920h wall on 35 of 50 tested seeds — a coin flip with better odds, not a
fix. Two knobs were available: more over-provisioning (`spare`), or more
write coalescing (`batch`). A sweep across `spare in {40,60,80,100}` and
`batch in {4,5,6,7,8}`, 20–50 seeds each, showed `batch` mattered far more
than `spare` — increasing `spare` alone only pushed survival up gradually,
while crossing `batch=7` at the *same* modest `spare=40` (20%
over-provisioning) flipped the result from "usually fails" to "always
survives the full test window with zero loss."

A finer sweep (`batch=4..8`, `spare=40`, 50 seeds) found the actual
threshold:

| batch | clears 81,920h wall | max memories lost across seeds |
|------:|---------------------:|--------------------------------:|
| 4     | 35/50                | 45,104 |
| 5     | 50/50                | 26,380 |
| 6     | 50/50                | 7,656 |
| 7     | 50/50                | **0** |
| 8     | 50/50                | 0 |

Note the distinction: `batch=5` and `batch=6` both clear the 81,920h wall on
every tested seed, but they still eventually lose memories afterward — that
fails `spec/ALMA-HYPOTHESIS.md`'s separate "zero memories lost" criterion
even though it satisfies "survives past 81,920h." **`batch=7`** is the
smallest value that satisfies both, so that's what's now baked into
`run_experiment.py`'s defaults, confirmed clean on a 200-seed re-run
(200/200 cleared the wall, 0/200 lost any memories).

`batch=8` and above also pass, with more margin, but `7` was kept
deliberately close to the threshold rather than rounding up to a safer-
looking number — the point of this project is a defensible fix, not the
most padded one.

## Known limitation (log it, don't hide it)

Coalescing means memories sit in a buffer until `batch_size` of them have
accumulated. With `batch=7` and a 120,000-hour run, `120,000 mod 7 = 6` — up
to 6 of the most recent memories can be sitting unflushed in the buffer,
unwritten to any cell, at the exact moment the simulation loop ends. The
current `memories_lost` metric does not count these, because they were
never attempted as a write that failed — they're just not committed yet.
This is the simulator's version of the write-buffering-without-fsync problem
raised earlier in the project's own history. It doesn't affect whether the
81,920h wall is cleared, but it means "zero memories lost" in this table is
accurate for *committed* memories only, not for whatever was mid-buffer at
the instant the test harness stopped. A real implementation would need an
explicit flush-on-shutdown path; the simulator doesn't model shutdown yet.

## Historical baseline

`experiments/baseline-v0/` is left untouched as the "before" record. Compare
the two directly rather than editing baseline-v0's results after the fact.
