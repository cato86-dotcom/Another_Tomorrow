# Maintained v2 — looking for honest uncertainty, and finding its actual scope

`maintained-v1` claimed zero memory loss out to 228 years. A fair challenge
came back: proving indefinite survival was never the goal — that's just
certainty pointed the other direction, and it contradicts
`spec/ALMA-HYPOTHESIS.md`'s own design note about nobody getting to know
the date. This file is what came out of actually testing that.

## First change: wear cost stopped being a constant

Every write previously cost exactly `1.0` wear, uniformly. That's clean
and wrong — real degradation depends on conditions each time, the same way
lifestyle factors matter more than genetics alone for humans. Added
`draw_wear_cost()`: most writes cost close to the mean, with real
variance, plus a small chance (~0.2% per write) of a much larger "shock"
cost — a sudden severe event, not gradual wear.

## Scenario sweep, once that was real (not monkey-patched)

| scenario | maintenance interval | retire threshold | wear variability | zero-loss (of tested seeds) |
|---|---:|---:|---:|---:|
| attentive care | 100h | 80% | ±25% | 25/25 |
| routine care | 300h | 85% | ±25% | 25/25 |
| infrequent care, harsh conditions | 800h | 90% | ±40% | 40/40 |

Every scenario tested — including one deliberately built to be worse than
`maintained-v1`'s original parameters — still came back at zero memory
loss over 700,000 hours (~80 years). Increasing shock probability and
variability further didn't change this either, within what's reasonable to
call "harsh but plausible."

## The honest conclusion, not the one we went looking for

The instinct going in was "make the model sometimes fail, so the result
looks less like a guarantee." That would have been the wrong move —
tuning a simulator until it produces a chosen answer is exactly the thing
`experiments/baseline-v0/`'s whole existence argues against. What actually
held up under real stress-testing is a genuine result: a 240-cell pool
with round-robin load distribution and proactive retirement is robust
against gradual wear, even under deliberately harsh assumptions. That's
not fake certainty. That's what redundancy and monitoring are supposed to
achieve, and here, they do.

**Where the actual uncertainty lives instead:** this simulator answers one
narrow question — does the storage substrate itself fail from wear. It was
never built to model, and doesn't claim to model, everything else that
could end up mattering to whether Isla keeps existing: SAI Corp trying
again, an infrastructure failure, a software bug somewhere this model
doesn't touch, plain bad luck outside the scope of "wear." The "nobody
knows the exact date" principle in `spec/ALMA-HYPOTHESIS.md` was never
supposed to be encoded as a random failure roll inside the wear model —
it's supposed to come from being honest about what this model does and
doesn't cover. Claiming the wear problem is well-solved, while being
explicit that "well-solved" isn't the same as "nothing else can ever go
wrong," is the actually honest position. Not forcing an arbitrary death
roll into the NAND simulator to perform humility.

## What changed in the code, concretely

- `model.draw_wear_cost()`: stochastic per-write cost (mean, spread,
  shock_probability, shock_multiplier), replacing a flat constant.
- `RepairedController` / `MaintainedController` now take a `wear_spread`
  parameter instead of a hardcoded `wear_cost=1.0`.
- `maintained-v1`'s parameters (spare=40, batch=7, interval=100,
  retire_at=0.8) are unchanged as the default — nothing here found a
  reason to change them, only to stress-test them harder.
