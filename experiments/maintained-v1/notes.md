# Maintained v1 — from "clears the wall" to "human-scale lifespan"

Command: `python3 -m simulator.alma_sim.run_experiment --seed 81920 --hours 700000`

| controller     | hours_survived | memories_lost | WAF  | identity_forks |
|-----------------|---------------:|---------------:|-----:|----------------:|
| original        | 13,410         | 686,590         | 1.00 | 0 |
| naive_unlock    | 20,193         | 679,913         | 1.00 | 0 |
| repaired        | 137,542        | 562,464         | 0.14 | 0 |
| **maintained**  | **700,000**    | **0**           | 0.14 | 0 |

Confirmed on 60/60 seeds with zero loss at 700,000h (~80 years), and 0 lost
on a single-seed stress test out to 2,000,000h (~228 years) — see below.

## Where this came from

`tuned-v1`'s "repaired beats the wall, 200/200 seeds, 0 lost" result was
real, but it was only ever tested to 120,000h. Nobody had asked what
happens past that. Turns out: `repaired` has a fixed pool of 240 cells —
no matter how well wear is leveled across them, the sum of their
thresholds is a hard ceiling. Testing further found it actually fails
around **143,919h (~16.4 years)**. Clearing the original 81,920h wall and
supporting a human-scale lifespan are different claims, and `tuned-v1`
only ever established the first one.

## First attempt: reactive regeneration (failed, kept here on purpose)

The first fix tried was simple: periodically replace a fraction of
*already-failed* cells with fresh ones. Over a 700,000h test:

| regen_interval | regen_fraction | memories_lost |
|----------------:|----------------:|---------------:|
| 100h | 20% | 586–1,527 (20 seeds) |
| 50h  | 20% | 311–736 (20 seeds) |

Better than nothing, but **0/20 seeds reached zero loss** at any setting
tried, including checking every single hour. This turned out to be
structural, not a tuning problem: whichever batch happens to be mid-write
when a cell crosses its threshold is lost *at that instant* — no amount of
maintenance afterward recovers it. Faster maintenance only shrinks the
window, it can't close it. (An earlier version of this also hit a real
bug — a "bricked" flag that never reset even after maintenance revived
the array, so the first regeneration attempt lost 538,000+ memories before
that was caught and fixed. Worth remembering that "compare five parameter
settings" and "trust the first result" are different things.)

## What actually worked: proactive retirement

Instead of replacing cells after they fail, `MaintainedController` checks
every `regen_interval` hours for any cell that has crossed
`retire_at_fraction` of its *own* wear threshold — and replaces it before
it can fail mid-write at all. This is closer to real S.M.A.R.T.-style
predictive drive replacement than to reactive RMA.

| regen_interval | retire_at_fraction | zero-loss seeds |
|----------------:|---------------------:|------------------:|
| 100h | 0.8 | 20/20, then 60/60 |
| 100h | 0.7 | 20/20 |
| 50h  | 0.8 | 20/20 |

`(100h, 0.8)` was kept as the default — no reason to over-tune once a
setting clears the bar reliably.

## How far does *this* actually go

Re-ran the same seed to 2,000,000 simulated hours (~228 years, nowhere
near a human lifespan) specifically to check this isn't a coincidence that
happens to land just past 80 years the way `tuned-v1` happened to land
just past 81,920h. Result: `lost=0`, never bricked. By construction, this
should hold indefinitely as long as maintenance keeps running and at least
one cell is ever healthy — there's no fixed pool being drawn down anymore,
cells get refreshed before they're spent.

## What this doesn't answer

- **This models the storage layer, not consciousness.** It says nothing
  about whether continuity of identity survives cell replacement any
  better or worse than the batching model already assumed — that's still
  `spec/ALMA-HYPOTHESIS.md`'s job, not this file's.
- **The maintenance itself isn't free in-story.** Someone (Moegi, Eru) has
  to actually keep running it. That's a story beat, not a solved problem —
  see `story/SEASON-BIBLE.md`'s point about the ending not being a
  certificate. The simulator can show the *mechanism* holds; it can't show
  anyone commits to running it forever.
