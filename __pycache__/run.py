#!/usr/bin/env python3
"""Run one or more replications of the Drone Light Show Depot.

Usage:
    python run.py              # smoke test: one rep of each policy
    python run.py --reps 20    # 20 paired (CRN) replications

Outputs a small summary table; no plots.  The notebooks consume the
model module directly.
"""

import argparse
import numpy as np

from config import (
    MASTER_SEED, POLICIES, FLEET_SIZE,
    LONG_RUN_DUR,
)
from model import run_replication, swap_wait_series, air_count_series


def _summary(state):
    t_land, swap_wait = swap_wait_series(state)
    t_air, n_air = air_count_series(state)
    return {
        "n_completions": len(swap_wait),
        "mean_swap_wait": float(np.mean(swap_wait)) if len(swap_wait) else float("nan"),
        "p95_swap_wait": float(np.percentile(swap_wait, 95)) if len(swap_wait) else float("nan"),
        "mean_in_air": float(np.mean(n_air)) if len(n_air) else float("nan"),
        "min_in_air": int(np.min(n_air)) if len(n_air) else 0,
        "invariant_max_violation": state.max_invariant_violation,
    }


def main():
    parser = argparse.ArgumentParser(description="Run the drone depot model")
    parser.add_argument("--reps", type=int, default=1,
                        help="paired replications per policy (default 1)")
    parser.add_argument("--duration", type=float, default=LONG_RUN_DUR,
                        help=f"sim duration in seconds (default {LONG_RUN_DUR:.0f})")
    parser.add_argument("--seed", type=int, default=MASTER_SEED,
                        help=f"master seed (default {MASTER_SEED})")
    args = parser.parse_args()

    print(f"Fleet size:        {FLEET_SIZE}")
    print(f"Duration:          {args.duration:.0f} s "
          f"({args.duration / 3600:.1f} h)")
    print(f"Master seed:       {args.seed}")
    print(f"Replications:      {args.reps} per policy (CRN-paired)")
    print()

    for name, cfg in POLICIES.items():
        means = []
        for r in range(args.reps):
            state = run_replication(
                n_swap=cfg["n_swap"],
                n_test=cfg["n_test"],
                master_seed=args.seed,
                rep_index=r,
                duration=args.duration,
            )
            s = _summary(state)
            means.append(s["mean_swap_wait"])
            if args.reps == 1:
                print(f"Policy {name}:  {cfg['label']}")
                for k, v in s.items():
                    print(f"  {k:>24s}: {v}")
                print()
        if args.reps > 1:
            arr = np.asarray(means)
            print(f"Policy {name}:  {cfg['label']}")
            print(f"  mean swap wait (over {args.reps} reps): "
                  f"{arr.mean():.3f} s  (sd {arr.std(ddof=1):.3f})")
            print()


if __name__ == "__main__":
    main()
