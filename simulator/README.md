# simulator/

A small, dependency-free model of a *fictional* Alma memory substrate. Not a
tool for modifying real device firmware — see the disclaimer at the top of
`alma_sim/model.py`.

```
alma_sim/
├── model.py          Cell + MemoryArray: the substrate itself
├── controllers.py     three write strategies: original / naive_unlock / repaired
├── metrics.py          turns a run into the numbers spec/ALMA-HYPOTHESIS.md asks for
└── run_experiment.py   CLI entry point, writes experiments/<run>/results.csv
```

## Run it

```bash
python3 -m simulator.alma_sim.run_experiment --seed 81920 --hours 120000
```

## Extend it

Before opening a PR that changes a controller, read
`spec/ALMA-HYPOTHESIS.md`'s acceptance criteria, then run the baseline and
log the result under `experiments/`, per `CONTRIBUTING.md`. A change that
looks better in prose but isn't reflected in a logged run won't be merged.
