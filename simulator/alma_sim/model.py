"""
model.py -- a fictional model of Alma's memory substrate.

This is NOT a tool for modifying real SSD/NAND firmware. It's a small,
inspectable simulation of a *fictional* system, built for the project-81920
fan project, loosely inspired by real NAND endurance concepts: wear
leveling, over-provisioning, write amplification, and probabilistic cell
failure.

Vocabulary:
    cell      -- one addressable unit of Isla's long-term memory substrate
    wear      -- cumulative internal write/rewrite stress on a cell
    threshold -- the wear level at which a cell can no longer hold data
    spare     -- an over-provisioned cell, invisible to the logical address
                 space, used only for wear-leveling and replacement
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional


def draw_threshold(mean: float = 100.0, spread: float = 0.12) -> float:
    """
    Draw a per-cell failure threshold from a distribution instead of a single
    fixed constant.

    Real NAND cells don't all die at exactly the same program/erase count --
    endurance is distributed across a population of cells. Modeling that
    (instead of one hard number) is more physically honest, and it also
    happens to fit the story better than a countdown clock does: nobody --
    not Tsukasa, not the simulator -- can read off an exact expiry date in
    advance. `spread` is the coefficient of variation. The draw is clipped so
    no single cell is absurdly fragile or absurdly durable.
    """
    raw = random.gauss(mean, mean * spread)
    return max(mean * 0.6, min(mean * 1.6, raw))


def draw_wear_cost(
    mean: float = 1.0,
    spread: float = 0.25,
    shock_probability: float = 0.002,
    shock_multiplier: float = 8.0,
) -> float:
    """
    How much a single write actually costs a cell isn't fixed, and it isn't
    just mild day-to-day noise either. Most writes cost close to `mean`
    (ordinary variation -- ordinary lifestyle factors). But roughly
    `shock_probability` of the time, a write draws from a much higher
    range instead: a sudden severe event, not gradual wear. This is the
    honest reason no maintenance margin can promise zero risk -- a finite
    safety buffer against *gradual* wear doesn't protect against a single
    event large enough to skip past it entirely. See
    experiments/maintained-v2/notes.md: this is what actually introduces
    real variance into outcomes, not just clipped day-to-day noise, which
    turned out to be too well-behaved to ever break through any reasonable
    maintenance margin.
    """
    if random.random() < shock_probability:
        return random.uniform(mean * 3, mean * shock_multiplier)
    raw = random.gauss(mean, mean * spread)
    return max(mean * 0.3, min(mean * 2.5, raw))


@dataclass
class Cell:
    """One unit of memory substrate."""

    wear: float = 0.0
    failure_threshold: float = field(default_factory=draw_threshold)
    failed: bool = False
    data: Optional[str] = None  # a "memory" payload, or None if empty/lost

    def write(self, payload: str, wear_cost: float) -> bool:
        """Attempt to write. Returns True if the write succeeded."""
        if self.failed:
            return False
        self.wear += wear_cost
        if self.wear >= self.failure_threshold:
            self.failed = True
            # A cell that dies mid-write takes whatever was there with it.
            self.data = None
            return False
        self.data = payload
        return True


@dataclass
class MemoryArray:
    """
    The addressable memory space: `logical_size` cells the outside world can
    write to, plus `spare_size` over-provisioned cells hidden from that
    count and used only by controllers that know how to use them.
    """

    logical_size: int
    spare_size: int = 0
    cells: list[Cell] = field(init=False)

    def __post_init__(self) -> None:
        self.cells = [Cell() for _ in range(self.logical_size + self.spare_size)]

    def healthy_indices(self) -> list[int]:
        return [i for i, c in enumerate(self.cells) if not c.failed]

    def failed_fraction(self) -> float:
        return sum(c.failed for c in self.cells) / len(self.cells)
