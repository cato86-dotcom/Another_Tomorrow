"""
controllers.py -- three write strategies over the same MemoryArray.

(a) OriginalController    -- direct mapping, hard-coded lifetime lock.
                              This is the `systemctl suspend` of Alma
                              controllers: looks safe, quietly guarantees a
                              cliff edge. Mirrors the documented real-world
                              behaviour of SSD firmware that bricks itself to
                              read-only once predicted life hits 0%.

(b) NaiveUnlockController -- (a) with the artificial lock simply removed and
                              nothing else changed. This is `sudo chage -E -1
                              isla`, formalized. It should NOT score better
                              than "repaired" -- the simulator exists partly
                              to prove that.

(c) RepairedController    -- wear-leveling + over-provisioning + write
                              coalescing (lower write amplification). This is
                              the actual proposal in spec/ALMA-HYPOTHESIS.md.
                              No snapshot/restore path exists anywhere in
                              this controller -- there is structurally no way
                              for it to produce a second instance.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

from .model import Cell, MemoryArray, draw_wear_cost


@dataclass
class WriteResult:
    logical_writes: int = 0
    internal_writes: int = 0
    memories_lost: int = 0
    bricked_at_hour: Optional[float] = None  # None == still alive at run end


class BaseController:
    name = "base"

    def __init__(self, array: MemoryArray):
        self.array = array
        self.result = WriteResult()

    def write_memory(self, hour: float, payload: str) -> None:
        raise NotImplementedError

    def is_bricked(self) -> bool:
        return self.result.bricked_at_hour is not None


class OriginalController(BaseController):
    name = "original"
    HARD_LIMIT_HOURS = 81_920

    def write_memory(self, hour: float, payload: str) -> None:
        if self.is_bricked() or hour >= self.HARD_LIMIT_HOURS:
            if not self.is_bricked():
                self.result.bricked_at_hour = hour
            self.result.memories_lost += 1
            return

        idx = self.result.logical_writes % self.array.logical_size
        ok = self.array.cells[idx].write(payload, wear_cost=draw_wear_cost())
        self.result.logical_writes += 1
        self.result.internal_writes += 1
        if not ok:
            self.result.bricked_at_hour = hour
            self.result.memories_lost += 1


class NaiveUnlockController(BaseController):
    """
    Same 1:1 mapping as OriginalController, artificial lock removed.
    Expectation: cells still fail at their real, physically-grounded
    threshold, and once enough of them do, this is not a clean brick --
    it's slow, undetected loss. That distinction is the point.
    """

    name = "naive_unlock"
    BRICK_AT_FAILED_FRACTION = 0.5  # informal: "more than half of her, gone"

    def write_memory(self, hour: float, payload: str) -> None:
        idx = self.result.logical_writes % self.array.logical_size
        ok = self.array.cells[idx].write(payload, wear_cost=draw_wear_cost())
        self.result.logical_writes += 1
        self.result.internal_writes += 1
        if not ok:
            self.result.memories_lost += 1
            if (
                self.result.bricked_at_hour is None
                and self.array.failed_fraction() > self.BRICK_AT_FAILED_FRACTION
            ):
                self.result.bricked_at_hour = hour


class RepairedController(BaseController):
    name = "repaired"

    def __init__(self, array: MemoryArray, batch_size: int = 4, wear_spread: float = 0.25):
        super().__init__(array)
        self.batch_size = batch_size
        self.wear_spread = wear_spread
        self._pending: list[str] = []
        self._rr_pointer = 0

    def write_memory(self, hour: float, payload: str) -> None:
        if self.is_bricked():
            self.result.memories_lost += 1
            return

        self._pending.append(payload)
        self.result.logical_writes += 1
        if len(self._pending) < self.batch_size:
            return  # buffered: several memories become one physical write
        self._flush(hour)

    def _flush(self, hour: float) -> None:
        batch, self._pending = self._pending, []
        combined = "|".join(batch)  # this is the actual coalescing: N memories,
                                    # one physical write, instead of N writes

        healthy = self.array.healthy_indices()
        if not healthy:
            self._brick(hour, lost=len(batch))
            return

        idx = healthy[self._rr_pointer % len(healthy)]
        self._rr_pointer += 1
        ok = self.array.cells[idx].write(combined, wear_cost=draw_wear_cost(spread=self.wear_spread))
        self.result.internal_writes += 1
        if ok:
            return

        # cell died on this write: retire it, retry once on the next healthy cell
        healthy = self.array.healthy_indices()
        if not healthy:
            self._brick(hour, lost=len(batch))
            return
        idx = healthy[self._rr_pointer % len(healthy)]
        ok = self.array.cells[idx].write(combined, wear_cost=draw_wear_cost(spread=self.wear_spread))
        self.result.internal_writes += 1
        if not ok:
            self._brick(hour, lost=len(batch))

    def _brick(self, hour: float, lost: int) -> None:
        if self.result.bricked_at_hour is None:  # latch once, never overwrite
            self.result.bricked_at_hour = hour
        self.result.memories_lost += lost


class MaintainedController(RepairedController):
    """
    Extends RepairedController with periodic PROACTIVE maintenance: every
    `regen_interval` hours, any cell that has crossed `retire_at_fraction`
    of its own wear threshold gets retired and replaced with a fresh cell
    -- before it actually fails, not after.

    This exists because reactive regeneration (replace a cell only once
    it's already dead) has a structural floor on memory loss: whichever
    batch was mid-write when a cell crosses its threshold is lost no
    matter how fast maintenance runs afterward -- see
    experiments/tuned-v1/notes.md's human-lifespan follow-up for the
    numbers that showed this. Proactive retirement (closer to real
    S.M.A.R.T.-style predictive replacement) avoids that floor by
    replacing cells before they can fail mid-write at all.

    RepairedController alone also has a FIXED pool of cells -- no matter
    how well wear is leveled across it, the sum of everyone's thresholds
    is a hard ceiling. This also matches spec/ALMA-HYPOTHESIS.md's own
    framing of Alma maintenance as continuous, not a single patch --
    Moegi and Eru keep working on this, in-story, for exactly this reason.
    """

    name = "maintained"

    def __init__(
        self,
        array: MemoryArray,
        batch_size: int = 4,
        regen_interval: int = 100,
        retire_at_fraction: float = 0.8,
        wear_spread: float = 0.25,
    ):
        super().__init__(array, batch_size=batch_size, wear_spread=wear_spread)
        self.regen_interval = regen_interval
        self.retire_at_fraction = retire_at_fraction

    def write_memory(self, hour: float, payload: str) -> None:
        if hour > 0 and hour % self.regen_interval == 0:
            self._run_maintenance()
        super().write_memory(hour, payload)

    def _run_maintenance(self) -> None:
        at_risk = [
            i
            for i, c in enumerate(self.array.cells)
            if c.failed or c.wear >= self.retire_at_fraction * c.failure_threshold
        ]
        for i in at_risk:
            self.array.cells[i] = Cell()
        if self.array.healthy_indices():
            # revived: let the controller resume attempting writes instead
            # of staying permanently "bricked" from an earlier gap
            self.result.bricked_at_hour = None
