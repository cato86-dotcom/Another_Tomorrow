# Contributing to project-81920

Thanks for reading this before opening a PR. Two guardrails matter more than
style here:

## 1. Label your sources

Every claim goes in one of three buckets, and the bucket must be visible at
a glance:

- **Confirmed** — traceable to the game, anime, or an official source. Cite
  it in `research/confirmed/`.
- **Analogue** — a real-world engineering fact (SSD/NAND behavior, etc.)
  used as inspiration. Cite it in `research/analogues/`.
- **Invented** — made up for this project. Goes in `spec/` or
  `research/speculation.md`, explicitly marked as invention.

Do not blend these. A PR that states an invented mechanism as if it were
confirmed canon will be asked to re-label, not merged as-is.

## 2. Lsla — scope guard

Lsla exists to make one narrative point: a restore is not a rescue, it's a
new person who inherits someone else's memories. Once that point is made,
she steps back.

- She is not the villain and not a disposable copy to be deleted.
- She is her own person, with Isla's memories up to the snapshot point —
  and she's written as one.
- **Hard limit: no more than 2 episodes total across the season**, and she
  never competes with Isla for Tsukasa. That's a different show.

PRs that expand her role past this will be redirected, not rejected outright
— there's likely a good idea in there, it just belongs in a spin-off, not
here.

## 3. Simulator changes

If you change `simulator/alma_sim/`, re-run the baseline and update or add a
file under `experiments/` with the actual numbers, including if your change
makes things worse. A failed experiment that's logged is more useful to the
next contributor than a passing one that isn't reproducible.

```bash
python3 -m simulator.alma_sim.run_experiment --seed 81920
```

## 4. Timeline discipline (story contributions)

Keep the in-story time gap short — weeks, not years. A multi-year skip turns
this into a different continuity, which isn't the goal.
