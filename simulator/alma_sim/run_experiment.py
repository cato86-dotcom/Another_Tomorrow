"""
run_experiment.py -- experiment runner for project-81920.

Runs the three controllers over the same synthetic memory stream and writes
experiments/<run_name>/results.csv, so anyone can reproduce or challenge the
numbers. Every cell's failure_threshold is drawn from a distribution (see
model.draw_threshold), so re-running with a different --seed gives a
genuinely different survival curve, not just cosmetic noise -- on purpose.

Default parameters currently reflect experiments/tuned-v1/ (spare=40,
batch=7), not the original experiments/baseline-v0/ (spare=40, batch=4).
Pass --run-name when trying new parameters so you don't overwrite either
historical record.

Usage:
    python3 -m simulator.alma_sim.run_experiment [--seed N] [--hours N] [--run-name NAME]
"""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

from .controllers import NaiveUnlockController, OriginalController, RepairedController
from .metrics import summarize
from .model import MemoryArray

DEFAULT_SEED = 81_920
DEFAULT_TOTAL_HOURS = 120_000  # run well past the original 81,920h wall
WRITES_PER_HOUR = 1
LOGICAL_CELLS = 200

# Tuned in experiments/tuned-v1/ via a 200-seed sweep: this is the smallest
# (spare, batch) pair that cleared the 81,920h wall with zero memory loss on
# every seed tested, not just the first one we tried. See that notes.md for
# the sweep that ruled out smaller values (batch=4..6 all still lose memories
# on some seeds -- "clears the wall" and "loses zero memories" are different
# claims, and only batch>=7 satisfied both here).
SPARE_CELLS_FOR_REPAIRED = 40  # 20% over-provisioning
BATCH_SIZE_FOR_REPAIRED = 7    # write coalescing factor

DEFAULT_RUN_NAME = "tuned-v1"  # historical runs (e.g. baseline-v0) are frozen;
                                # pass --run-name to avoid overwriting one


def build_controllers(seed: int):
    random.seed(seed)
    return [
        OriginalController(MemoryArray(LOGICAL_CELLS)),
        NaiveUnlockController(MemoryArray(LOGICAL_CELLS)),
        RepairedController(
            MemoryArray(LOGICAL_CELLS, SPARE_CELLS_FOR_REPAIRED),
            batch_size=BATCH_SIZE_FOR_REPAIRED,
        ),
    ]


def run(
    seed: int = DEFAULT_SEED,
    total_hours: int = DEFAULT_TOTAL_HOURS,
    run_name: str = DEFAULT_RUN_NAME,
) -> Path:
    controllers = build_controllers(seed)
    for hour in range(total_hours):
        for controller in controllers:
            for _ in range(WRITES_PER_HOUR):
                controller.write_memory(hour, payload=f"memory@{hour}")

    rows = [summarize(c, total_hours) for c in controllers]

    out_path = (
        Path(__file__).resolve().parents[2]
        / "experiments"
        / run_name
        / "results.csv"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].__dict__.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)

    print(f"seed={seed}  total_hours={total_hours}\n")
    for row in rows:
        print(
            f"{row.controller:14s} | survived {row.hours_survived:>9.1f}h "
            f"| lost {row.memories_lost:>4d} | WAF {row.write_amplification_factor:>5.2f} "
            f"| forks {row.identity_forks}"
        )
    print(f"\nwritten to {out_path}")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--hours", type=int, default=DEFAULT_TOTAL_HOURS)
    parser.add_argument("--run-name", type=str, default=DEFAULT_RUN_NAME)
    args = parser.parse_args()
    run(seed=args.seed, total_hours=args.hours, run_name=args.run_name)


if __name__ == "__main__":
    main()
