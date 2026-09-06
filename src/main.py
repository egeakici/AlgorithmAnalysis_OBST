"""Command-line interface for the Optimal Binary Search Tree project."""

from __future__ import annotations

import argparse
import math
import sys

from src.conventional_bst import build_conventional_bst, summarize_bst
from src.display import (
    format_cost_table,
    format_depth_table,
    format_input,
    format_root_table,
    format_tree,
)
from src.experiments import write_experiment_results
from src.input_parser import load_input
from src.obst import (
    calculate_average_depth,
    calculate_expected_cost,
    compute_obst,
    validate_bst_property,
)


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description="Build an Optimal Binary Search Tree using Dynamic Programming."
    )
    parser.add_argument("--input", help="Path to text or CSV input file.")
    parser.add_argument(
        "--format",
        choices=["auto", "text", "csv"],
        default="auto",
        help="Input format. Defaults to extension-based auto detection.",
    )
    parser.add_argument(
        "--show-tables",
        action="store_true",
        help="Print DP cost and root tables.",
    )
    parser.add_argument(
        "--compare-bst",
        action="store_true",
        help="Compare OBST with conventional insertion-order BST.",
    )
    parser.add_argument(
        "--run-experiments",
        action="store_true",
        help="Run deterministic timing experiments and write experiments/results.csv.",
    )
    return parser


def run_obst_cli(input_path: str, input_format: str, show_tables: bool, compare_bst: bool) -> None:
    """Load input, compute OBST, display results, and optionally compare with BST."""

    keys, probabilities = load_input(input_path, input_format)
    result = compute_obst(keys, probabilities)
    probabilities_by_key = dict(zip(keys, probabilities))
    reconstructed_cost = calculate_expected_cost(result.tree, probabilities_by_key)
    average_depth = calculate_average_depth(result.tree)
    is_valid_bst = validate_bst_property(result.tree)
    verification_ok = (
        math.isclose(result.minimum_cost, reconstructed_cost, rel_tol=1e-6, abs_tol=1e-6)
        and is_valid_bst
    )

    if not verification_ok:
        raise RuntimeError(
            "Verification failed: reconstructed tree cost or BST ordering does not match DP result."
        )

    print("Optimal Binary Search Tree Using Dynamic Programming")
    print("=" * 56)
    print()
    print(format_input(keys, probabilities))
    print()
    if show_tables:
        print(format_cost_table(keys, result.cost_table))
        print()
        print(format_root_table(keys, result.root_table))
        print()
    print("Optimal BST")
    print("-----------")
    print(format_tree(result.tree))
    print()
    print(format_depth_table(keys, probabilities, result.tree))
    print()
    print(f"Minimum expected search cost (DP): {result.minimum_cost:.6f}")
    print(f"Expected cost from reconstructed tree: {reconstructed_cost:.6f}")
    print(f"Unweighted average depth: {average_depth:.6f}")
    print(f"BST ordering property valid: {'yes' if is_valid_bst else 'no'}")
    print(f"Verification result: {'success' if verification_ok else 'failure'}")
    print(f"OBST construction time: {result.elapsed_seconds:.8f} seconds")

    if compare_bst:
        conventional_tree, construction_time = build_conventional_bst(keys, probabilities)
        summary = summarize_bst(conventional_tree, probabilities_by_key)
        print()
        print("Conventional BST Comparison")
        print("---------------------------")
        print("Construction method: insert keys in the supplied sorted order.")
        print()
        print(format_tree(conventional_tree))
        print()
        print(format_depth_table(keys, probabilities, conventional_tree))
        print()
        print(f"Expected search cost: {float(summary['expected_cost']):.6f}")
        print(f"Unweighted average depth: {float(summary['average_depth']):.6f}")
        print(f"Construction time: {construction_time:.8f} seconds")


def main(argv: list[str] | None = None) -> int:
    """Program entry point."""

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.run_experiments:
            rows = write_experiment_results()
            print("Experiments completed. Results written to experiments/results.csv.")
            for row in rows:
                print(
                    f"n={row['n']}, mean={row['mean_execution_seconds']}s, "
                    f"cost={row['minimum_expected_cost']}, seed={row['seed']}"
                )
            return 0

        if not args.input:
            parser.error("--input is required unless --run-experiments is used.")

        run_obst_cli(args.input, args.format, args.show_tables, args.compare_bst)
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
