# IE 306 — Homework 3: Drone Light Show Depot — Output Analysis

**Due Monday June 1, 2026, 23:59.** Teams of 3 (same teams as Assignment 2).

This repository contains everything you need to complete the assignment. You will use the **provided** SimPy model under `solution/` and run *output analysis* on it; you are not required to write any simulation code yourself.

## Quick start

1. Read `assignment_03.pdf` for the full problem description.
2. Open `assignment_03_starter.ipynb` in Jupyter.
3. Complete the five tasks (the notebook is pre-divided into Task 1 through Task 5).
4. Run the final cell — it writes `submission.json`.
5. Write a one-page `decision_memo.pdf` addressed to the operations manager.
6. Commit and push: the notebook, `submission.json`, and `decision_memo.pdf`.

## Files

All files live in the **same folder** (the repo root). The notebook imports the Python modules directly — no `solution/` subfolder, no path tricks needed.

- `assignment_03.pdf` — the assignment handout.
- `assignment_03_starter.ipynb` — the notebook template you complete.
- `config.py` — system parameters (read-only).
- `model.py` — SimPy depot model (read-only).
- `seeds.py` — CRN-aware random-number plumbing (read-only).
- `run.py` — small CLI helper to run one replication.

**Do not move, rename, or modify** `config.py`, `model.py`, or `seeds.py`. The autograder relies on these being unchanged.

## Running the model

Launch Jupyter from the repo root, open `assignment_03_starter.ipynb`, and the first cell will import:

```python
from config import FLEET_SIZE, MASTER_SEED, N_SWAP_A, N_SWAP_B, N_TEST, SIM_DUR, LONG_RUN_DUR
from model  import run_replication, swap_wait_series, air_count_series

state = run_replication(n_swap=5, n_test=1, master_seed=20260601,
                        rep_index=0, duration=30*3600)
t, w = swap_wait_series(state)   # arrays of (landing time, swap-queue wait)
```

The model also exposes `air_count_series(state)` for the in-air count time-series and `state.completions` for the full per-drone record `(t_landed, swap_wait, test_wait, sojourn)`.

## Grading

- 70 pts are automatic, based on the numeric fields in your `submission.json`.
- 30 pts are awarded by the instructor reading your notebook prose, decision memo, and V&V interpretation.

## Academic integrity

Discussion within your team is expected and encouraged. Discussion across teams, sharing code or `submission.json` files, or running the simulator on a non-canonical seed and reporting those numbers are violations of the course honor code.
