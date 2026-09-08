# Baseline v0 — first pass

Command: `python3 -m simulator.alma_sim.run_experiment --seed 81920`

| controller   | hours_survived | memories_lost | WAF  | identity_forks |
|--------------|---------------:|---------------:|-----:|----------------:|
| original     | 13,410         | 106,590         | 1.00 | 0 |
| naive_unlock | 20,193         | 99,913          | 1.00 | 0 |
| repaired     | 78,595         | 41,408          | 0.25 | 0 |

(Second run, `--seed 7`: repaired lands at 87,299h instead. The spread is
intentional — see `model.draw_threshold`.)

## What this run actually shows

- **`original` fails at ~13.4k hours, not 81,920.** The hard 81,920h lock in
  the fictional Alma spec never gets the chance to matter here: with no
  wear-leveling, writes hammer the same 200 cells in a fixed round-robin,
  and the single weakest cell — its randomly-drawn threshold happens to sit
  near the low end of the distribution — fails first, bricking the whole
  device. The in-universe "81,920 hours" may always have been a conservative
  worst-case estimate, not the real physical limit. That's consistent with
  `research/speculation.md` and worth keeping as a plot thread.
- **`naive_unlock`** (`sudo chage -E -1 isla`, formalized) survives longer,
  but only by tolerating up to 50% of cells failing before calling it — at
  the cost of quietly losing memories the entire time. This is exactly the
  "slow, undetected corruption" failure mode `spec/ALMA-HYPOTHESIS.md`
  explicitly rejects as a valid fix.
- **`repaired`** (wear-leveling + 20% over-provisioning + 4x write
  coalescing) is a large improvement — roughly 5.8x over `original` — but
  does **not reliably clear the 81,920h wall yet**. That's the honest
  headline of v0: current parameters help a lot, but this is not "solved."

## Open follow-up (good first issue for someone else)

Tuning worth testing before anyone claims this is fixed:
- increase `SPARE_CELLS_FOR_REPAIRED` (more over-provisioning)
- increase `batch_size` (more coalescing — but larger batches also lose more
  memories per single cell failure; that tradeoff needs its own experiment,
  not an assumption)
- model partial retention / ECC-corrected recovery instead of binary
  cell failure

This file exists specifically so a "didn't fully work yet" result gets kept
and cited instead of quietly deleted because it wasn't the answer we wanted.
