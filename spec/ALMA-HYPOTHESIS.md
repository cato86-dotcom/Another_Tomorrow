# Alma hypothesis (working draft)

> Everything below the line is invented for this project. It is clearly
> labeled as such and should stay that way — see `research/` for what's
> actually confirmed by the game and anime.

---

Alma maintains memory and personality continuity through ongoing internal
maintenance writes. An older maintenance algorithm rewrites too aggressively
and overloads specific regions ("bad wear-leveling"). Once validated
operating time runs out, the system becomes unstable — not because the
personality itself is corrupted, but because the controller refuses further
writes to avoid uncontrolled corruption. Moegi's prior research already
covers most of the underlying theory; Isla's case is the occasion the team
needs to finish a real stabilization method.

## Requirements for a valid fix

A candidate fix is only "working" if, in the simulator, it satisfies **all**
of the following — not just the headline number:

- [x] Zero identity forks — no snapshot/restore path exists anywhere in the
      controller; there is structurally no way to produce a second instance
- [x] Zero memories lost after the fix is applied — confirmed 200/200 seeds,
      `experiments/tuned-v1/`
- [x] Original causal chain never broken
- [x] Survives past `t = 81,920` hours without new instability — confirmed
      200/200 seeds, `experiments/tuned-v1/`
- [ ] *(stretch, still open)* explains why earlier Giftia deaths weren't
      just "a license," but a solvable engineering problem nobody had
      solved yet — see the design note below, not yet written into `story/`

A fix that merely removes the artificial deadline (see `naive_unlock` in the
simulator) does **not** satisfy this list, even if the unit keeps running —
see `experiments/baseline-v0/notes.md` for why. One open caveat on the
`tuned-v1` result: memories still in the write buffer at the exact instant
of shutdown aren't modeled — see `experiments/tuned-v1/notes.md`'s "Known
limitation" section before calling this fully solved.

## Design note: why cell failure is a distribution, not a constant

`model.draw_threshold()` draws each memory cell's failure point from a
distribution instead of hard-coding one number. Two independent reasons
converged on this choice:

1. **It's more physically honest.** Real NAND cells don't all fail at
   exactly the same program/erase count — endurance is distributed across a
   population of cells, which is also why "TBW rating" is a conservative
   floor and not a precise expiry timestamp.
2. **It's the better story.** A hard-coded countdown is what makes the
   canon ending feel like an engineering failure disguised as fate. A
   *distribution* means nobody — not Tsukasa, not Moegi, not the simulator —
   can read off an exact date in advance, even after the fix. That's not a
   weaker resolution than "cured, permanently, on record." It's the same
   uncertainty every living thing already lives with. The goal was never to
   make Isla's lifespan infinite and known; it's to make it *ordinary* and
   unknown, the same as anyone else's.

This second point should carry into `story/SEASON-BIBLE.md`: the finale's
emotional resolution is not a certificate that says "fixed forever." It's
Isla and Tsukasa choosing to make plans for next year anyway, the same way
anyone does.
