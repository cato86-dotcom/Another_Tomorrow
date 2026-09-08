"""
run_experiment.py -- MVP baseline for project-81920.

Runs the three controllers over the same synthetic memory stream and writes
experiments/baseline-v0/results.csv, so anyone can reproduce or challenge the
numbers. Every cell's failure_threshold is drawn from a distribution (see
model.draw_threshold), so re-running with a different --seed gives a
genuinely different survival curve, not just cosmetic noise -- on purpose.

Usage:
    python3 -m simulator.alma_sim.run_experiment [--seed N] [--hours N]
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
SPARE_CELLS_FOR_REPAIRED = 40  # over-provisioning, repaired controller only


def build_controllers(seed: int):
    random.seed(seed)
    return [
        OriginalController(MemoryArray(LOGICAL_CELLS)),
        NaiveUnlockController(MemoryArray(LOGICAL_CELLS)),
        RepairedController(MemoryArray(LOGICAL_CELLS, SPARE_CELLS_FOR_REPAIRED)),
    ]


def run(seed: int = DEFAULT_SEED, total_hours: int = DEFAULT_TOTAL_HOURS) -> Path:
    controllers = build_controllers(seed)
    for hour in range(total_hours):
        for controller in controllers:
            for _ in range(WRITES_PER_HOUR):
                controller.write_memory(hour, payload=f"memory@{hour}")

    rows = [summarize(c, total_hours) for c in controllers]

    out_path = (
        Path(__file__).resolve().parents[2]
        / "experiments"
        / "baseline-v0"
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
    args = parser.parse_args()
    run(seed=args.seed, total_hours=args.hours)


if __name__ == "__main__":
    main()
