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

## Why this exists

The anime gives Isla a fixed, countable death — she knows the exact hour it
happens. Real terminal illness rarely works that way; even a diagnosis
usually leaves a range, not a date. In a strange way, a known date is
worse than either terminal illness or ordinary mortality: there's no
uncertainty left to actually live inside. A fix that just deleted the
number would still leave her flattened to a countdown, only a longer one.
That's why `spec/ALMA-HYPOTHESIS.md`'s repair deliberately produces an
*uncertain* lifespan (see its design note on distributed failure
thresholds), not a certified-forever one. Nobody, including Isla, gets to
know the date again. That's not a weaker ending — it's the ordinary one
everyone else already lives with, and the show never let her have it.

The Giftia's decline before that cutoff — memories going first, personality
following — reads as more than a plot mechanism to anyone who has watched a
person's mind go before their body does. This project doesn't try to be
subtle about that. "Zero memories lost" in `spec/ALMA-HYPOTHESIS.md` isn't
a technical flourish; it's the actual bar that matters, and the whole
`experiments/` habit of logging failures instead of hiding them exists
because pretending a fix works when it doesn't is its own kind of harm.

The official material never fully closed this door, either. The visual
novel has its own separate hibernation route where Isla is found again
with no mechanism given. The anime's own epilogue introduces Tsukasa's
"new Giftia partner" nine months later — and never shows her face. See
`research/confirmed/anime-ending.md` for the sourcing. That's not nothing.
That's a door left ajar. This project walks through it.

And the last thing worth saying plainly: people don't stop fighting for
someone just because the fight is hard, as long as there's still something
left to fight *for*. Isla's canon ending accepts her death because canon
gives Tsukasa no alternative. This project exists because the source
material — deliberately or not — gave fans one anyway.

## Repo layout

```
project-81920/
├── research/     confirmed sources vs. our own invented analogues
├── spec/         the working technical hypothesis + acceptance criteria
├── simulator/    a small Python model that tests fix hypotheses honestly
├── experiments/  logged runs — including ones that didn't fully work
├── story/        season outline, character notes, episode drafts, art/
├── COMMUNITY.md  where Plastic Memories fans actually gather, if you want
│                 to point someone here
└── CONTRIBUTING.md
```

## Running the simulator

No dependencies beyond the standard library.

```bash
python3 -m simulator.alma_sim.run_experiment --seed 81920
```

This compares four write controllers over the same synthetic memory stream:

| controller     | what it represents |
|-----------------|---------------------|
| `original`      | the canon hard limit — no wear-leveling, bricks on first cell failure |
| `naive_unlock`  | `sudo chage -E -1 isla`, formalized — just removing the deadline |
| `repaired`      | wear-leveling + over-provisioning + write coalescing — clears the canon wall, but has its own hidden ceiling |
| `maintained`    | `repaired` plus proactive cell retirement — the current best answer |

It prints a results table and writes `experiments/<run>/results.csv` so any
run is reproducible and citable, not just asserted.

**Current status:** `maintained` clears a human-scale lifespan (~80 years /
700,000 simulated hours) with zero memories lost, confirmed on 60/60 tested
seeds, plus a single-seed stress test to ~228 years with the same result —
see [`experiments/maintained-v1/notes.md`](./experiments/maintained-v1/notes.md).
That file also documents the honest dead end along the way: `repaired`
alone (the earlier `tuned-v1` result) turned out to have its own hidden
ceiling around 16.4 years once actually tested past the original 81,920h
wall, and a first attempt at fixing that reactively — replacing cells only
after they'd already failed — never reached zero loss on any tested seed.
The earlier, superseded results are kept at
[`experiments/baseline-v0/notes.md`](./experiments/baseline-v0/notes.md) and
[`experiments/tuned-v1/notes.md`](./experiments/tuned-v1/notes.md) as
"before" records — nothing gets deleted just because it wasn't the final
answer.

## Contributing

New to GitHub, or not sure you'll do it "right"? `CONTRIBUTING.md` opens
with a section just for that — short version: nothing here is final, and
you can't break this by trying. Fixing the simulator, tightening the
source register, or drafting an episode are all welcome — see
[`CONTRIBUTING.md`](./CONTRIBUTING.md), including the scope guard on Lsla's
role in the story.

## Supporting real research and care

This project is fiction. Lewy body dementia and other conditions that take
memory and identity before they take anything else are not. If anything
above resonated, consider supporting an organization that funds research
into it and supports the families actually living with it:

- [Lewy Body Dementia Association](https://lbda.org/donate) (US, 501(c)(3))
- [Lewy Body Society](https://www.lewybody.org/join-in/donate/) (UK,
  registered charity 1114579 / SC047044)

No pressure beyond this paragraph — just leaving the door open, the same
way this whole project started.

## License

MIT for code. CC-BY-NC-SA for story text and research prose. See `LICENSE`.
