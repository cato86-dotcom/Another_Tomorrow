"""
metrics.py -- turns a controller's WriteResult into the numbers
spec/ALMA-HYPOTHESIS.md asks a valid fix to satisfy.
"""

from __future__ import annotations

from dataclasses import dataclass

from .controllers import BaseController


@dataclass
class Metrics:
    controller: str
    hours_survived: float
    memories_lost: int
    write_amplification_factor: float
    identity_forks: int  # always 0 by construction -- see run_experiment.py


def summarize(controller: BaseController, total_hours: float) -> Metrics:
    r = controller.result
    hours_survived = r.bricked_at_hour if r.bricked_at_hour is not None else total_hours
    waf = (r.internal_writes / r.logical_writes) if r.logical_writes else 1.0
    return Metrics(
        controller=controller.name,
        hours_survived=round(hours_survived, 1),
        memories_lost=r.memories_lost,
        write_amplification_factor=round(waf, 3),
        identity_forks=0,
    )
