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

from dataclasses import dataclass, field
from typing import Optional

from .model import MemoryArray


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
        ok = self.array.cells[idx].write(payload, wear_cost=1.0)
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
        ok = self.array.cells[idx].write(payload, wear_cost=1.0)
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

    def __init__(self, array: MemoryArray, batch_size: int = 4):
        super().__init__(array)
        self.batch_size = batch_size
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
        ok = self.array.cells[idx].write(combined, wear_cost=1.0)
        self.result.internal_writes += 1
        if ok:
            return

        # cell died on this write: retire it, retry once on the next healthy cell
        healthy = self.array.healthy_indices()
        if not healthy:
            self._brick(hour, lost=len(batch))
            return
        idx = healthy[self._rr_pointer % len(healthy)]
        ok = self.array.cells[idx].write(combined, wear_cost=1.0)
        self.result.internal_writes += 1
        if not ok:
            self._brick(hour, lost=len(batch))

    def _brick(self, hour: float, lost: int) -> None:
        if self.result.bricked_at_hour is None:  # latch once, never overwrite
            self.result.bricked_at_hour = hour
        self.result.memories_lost += lost
