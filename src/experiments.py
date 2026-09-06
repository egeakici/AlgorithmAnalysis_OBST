"""Reproducible timing experiments for the OBST algorithm."""

from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean
from time import perf_counter

from src.obst import compute_obst

DEFAULT_SIZES = [5, 10, 20, 50, 100]
DEFAULT_REPETITIONS = 5


def generate_dataset(n: int, seed: int) -> tuple[list[int], list[float]]:
    """Generate sorted unique keys and normalized probabilities deterministically."""

    if n <= 0:
        raise ValueError("Experiment size n must be positive.")

    rng = random.Random(seed)
    keys = sorted(rng.sample(range(1, n * 20 + 100), n))
    weights = [rng.random() + 0.01 for _ in range(n)]
    total_weight = sum(weights)
    probabilities = [weight / total_weight for weight in weights]
    return keys, probabilities


def time_single_run(keys: list[int], probabilities: list[float]) -> tuple[float, float]:
    """Time only the OBST construction and return elapsed seconds plus minimum cost."""

    start = perf_counter()
    result = compute_obst(keys, probabilities)
    elapsed = perf_counter() - start
    return elapsed, result.minimum_cost


def run_experiments(
    sizes: list[int] | None = None,
    repetitions: int = DEFAULT_REPETITIONS,
    base_seed: int = 2026,
) -> list[dict[str, str]]:
    """Run deterministic experiments and return CSV-ready rows."""

    selected_sizes = sizes or DEFAULT_SIZES
    rows: list[dict[str, str]] = []
    for n in selected_sizes:
        seed = base_seed + n
        keys, probabilities = generate_dataset(n, seed)
        timings: list[float] = []
        minimum_cost = 0.0
        for _ in range(repetitions):
            elapsed, minimum_cost = time_single_run(keys, probabilities)
            timings.append(elapsed)
        rows.append(
            {
                "n": str(n),
                "mean_execution_seconds": f"{mean(timings):.8f}",
                "minimum_expected_cost": f"{minimum_cost:.8f}",
                "seed": str(seed),
                "repetitions": str(repetitions),
                "remarks": "Deterministic generated keys and normalized probabilities",
            }
        )
    return rows


def write_experiment_results(
    output_path: str | Path = "experiments/results.csv",
    sizes: list[int] | None = None,
    repetitions: int = DEFAULT_REPETITIONS,
    base_seed: int = 2026,
) -> list[dict[str, str]]:
    """Run experiments and write results to a CSV file."""

    rows = run_experiments(sizes=sizes, repetitions=repetitions, base_seed=base_seed)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "n",
        "mean_execution_seconds",
        "minimum_expected_cost",
        "seed",
        "repetitions",
        "remarks",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return rows
