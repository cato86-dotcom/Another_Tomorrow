# project-81920 — "Another Tomorrow"

*A fix, not a replacement.*

> Non-commercial fan project. Not affiliated with MAGES., 5pb., Aniplex, or
> Naotaka Hayashi. Transformative fan work set in the world of
> *Plastic Memories*.

```text
Issue #1: Isla should be able to make plans for next year.
Acceptance criteria: She gets to keep them.
```

## The premise

The game and anime both end Isla's story around a hard limit: 81,920 hours
of operation. What's actually confirmed, versus what we've invented to fill
the gap, is tracked explicitly in [`research/`](./research) — nothing in
`spec/` or `simulator/` is presented as canon.

The short version: on the visual novel's hibernation route, Tsukasa places
Isla in stasis and works with her creator to find a cure; she's later woken
up, but the game never explains the mechanism. That gap is this project.

## Goal

Fix the read/write limit in **original** Isla's Alma core, in place, while
she's hibernating — on the same physical and causal chain. No copy. No new
instance. No replacement. She gets to keep living, as herself, with Tsukasa
and the rest of Terminal Service.

Full technical hypothesis: [`spec/ALMA-HYPOTHESIS.md`](./spec/ALMA-HYPOTHESIS.md)

## Repo layout

```
project-81920/
├── research/     confirmed sources vs. our own invented analogues
├── spec/         the working technical hypothesis + acceptance criteria
├── simulator/    a small Python model that tests fix hypotheses honestly
├── experiments/  logged runs — including ones that didn't fully work
├── story/        season outline, character notes, episode drafts
└── CONTRIBUTING.md
```

## Running the simulator

No dependencies beyond the standard library.

```bash
python3 -m simulator.alma_sim.run_experiment --seed 81920
```

This compares three write controllers over the same synthetic 120,000-hour
memory stream:

| controller     | what it represents |
|-----------------|---------------------|
| `original`      | the canon hard limit — no wear-leveling, bricks on first cell failure |
| `naive_unlock`  | `sudo chage -E -1 isla`, formalized — just removing the deadline |
| `repaired`      | wear-leveling + over-provisioning + write coalescing, per the spec |

It prints a results table and writes `experiments/<run>/results.csv` so any
run is reproducible and citable, not just asserted.

**Current status:** `repaired` beats the other two by a wide margin but does
not yet reliably clear 81,920 simulated hours — see
[`experiments/baseline-v0/notes.md`](./experiments/baseline-v0/notes.md) for
the actual numbers and what's worth tuning next. This is tracked honestly on
purpose; a fix that only works in the README and not in the simulator isn't
a fix.

## Contributing

Fixing the simulator, tightening the source register, or drafting an episode
are all welcome — see [`CONTRIBUTING.md`](./CONTRIBUTING.md), including the
scope guard on Lsla's role in the story.

## License

MIT for code. CC-BY-NC-SA for story text and research prose. See `LICENSE`.
