# Contributing to project-81920

Thanks for reading this before opening a PR.

**If you're new to GitHub: nothing here is set in stone, and you can't
break this by trying.** Every episode outline, every parameter in the
simulator, every line in the season bible is a proposal, not a ruling —
including the ones that sound confident. If you're not sure how to open a
pull request, or you're worried about getting the git commands wrong, open
an Issue instead and just describe the idea in plain language; someone can
help turn it into a PR. Getting something "wrong" here just means someone
suggests a change — it doesn't cost anything and nobody's going to be
annoyed about it. The worst realistic outcome of a mistake is a comment
asking you to adjust something, same as everyone else who's contributed so
far, including the people who set the whole thing up.

Two guardrails matter more than style here:

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

The season spans roughly nine months — the same gap the anime itself uses
between Isla's death and Tsukasa meeting a new, unnamed partner. See
`story/SEASON-BIBLE.md`'s "Connecting to the anime's own ending" for why
that number specifically matters and isn't arbitrary. Individual episodes
don't need exact week numbers, but the season as a whole shouldn't drift
past that nine-month mark — a multi-year skip turns this into a different
continuity, which isn't the goal.
