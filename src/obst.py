"""Standard O(n^3) Dynamic Programming implementation of an OBST."""

from __future__ import annotations

import math
from time import perf_counter
from typing import Sequence

from src.models import OBSTResult, TreeNode

PROBABILITY_SUM_TOLERANCE = 1e-6


def validate_input(keys: Sequence[int | float], probabilities: Sequence[float]) -> None:
    """Validate keys and probabilities before constructing an OBST.

    Keys must be unique and strictly increasing. Probabilities must be finite,
    non-negative values whose sum is approximately one.
    """

    if len(keys) == 0:
        raise ValueError("Input must contain at least one key.")
    if len(keys) != len(probabilities):
        raise ValueError(
            f"Number of keys ({len(keys)}) does not match number of probabilities "
            f"({len(probabilities)})."
        )

    for index, key in enumerate(keys):
        if not isinstance(key, (int, float)) or isinstance(key, bool):
            raise ValueError(f"Key at position {index + 1} is not numeric.")
        if not math.isfinite(float(key)):
            raise ValueError(f"Key at position {index + 1} is not finite.")

    for index, probability in enumerate(probabilities):
        if not isinstance(probability, (int, float)) or isinstance(probability, bool):
            raise ValueError(f"Probability at position {index + 1} is not numeric.")
        if not math.isfinite(float(probability)):
            raise ValueError(f"Probability at position {index + 1} is not finite.")
        if probability < 0:
            raise ValueError(f"Probability at position {index + 1} is negative.")

    for index in range(1, len(keys)):
        if keys[index] == keys[index - 1]:
            raise ValueError(f"Duplicate key detected: {keys[index]!r}.")
        if keys[index] < keys[index - 1]:
            raise ValueError("Keys must be sorted in strictly increasing order.")

    probability_sum = sum(probabilities)
    if not math.isclose(
        probability_sum,
        1.0,
        rel_tol=PROBABILITY_SUM_TOLERANCE,
        abs_tol=PROBABILITY_SUM_TOLERANCE,
    ):
        raise ValueError(
            "Probabilities must sum to 1. "
            f"Current sum is {probability_sum:.12g}; tolerance is "
            f"{PROBABILITY_SUM_TOLERANCE:g}."
        )


def build_prefix_sums(probabilities: Sequence[float]) -> list[float]:
    """Return prefix sums where prefix[i + 1] stores sum(probabilities[:i + 1])."""

    prefix = [0.0]
    running_total = 0.0
    for probability in probabilities:
        running_total += probability
        prefix.append(running_total)
    return prefix


def interval_probability(prefix_sums: Sequence[float], i: int, j: int) -> float:
    """Return sum of probabilities from 0-based inclusive interval i..j."""

    if i > j:
        return 0.0
    return prefix_sums[j + 1] - prefix_sums[i]


def compute_obst(
    keys: Sequence[int | float],
    probabilities: Sequence[float],
) -> OBSTResult:
    """Compute an Optimal BST using the standard cubic Dynamic Programming method."""

    validate_input(keys, probabilities)
    keys_list = list(keys)
    probabilities_list = [float(probability) for probability in probabilities]
    n = len(keys_list)

    start = perf_counter()
    prefix_sums = build_prefix_sums(probabilities_list)
    cost_table: list[list[float | None]] = [[None for _ in range(n)] for _ in range(n)]
    root_table: list[list[int | None]] = [[None for _ in range(n)] for _ in range(n)]

    for i in range(n):
        cost_table[i][i] = probabilities_list[i]
        root_table[i][i] = i

    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            total_weight = interval_probability(prefix_sums, i, j)
            best_cost = math.inf
            best_root: int | None = None

            # Try every key in the interval as the root of this subproblem.
            for root_index in range(i, j + 1):
                left_cost = cost_table[i][root_index - 1] if root_index > i else 0.0
                right_cost = cost_table[root_index + 1][j] if root_index < j else 0.0
                candidate_cost = float(left_cost) + float(right_cost) + total_weight

                if candidate_cost < best_cost:
                    best_cost = candidate_cost
                    best_root = root_index

            cost_table[i][j] = best_cost
            root_table[i][j] = best_root

    tree = reconstruct_tree(keys_list, probabilities_list, root_table, 0, n - 1)
    elapsed_seconds = perf_counter() - start
    return OBSTResult(
        minimum_cost=float(cost_table[0][n - 1]),
        cost_table=cost_table,
        root_table=root_table,
        tree=tree,
        elapsed_seconds=elapsed_seconds,
    )


def reconstruct_tree(
    keys: Sequence[int | float],
    probabilities: Sequence[float],
    root_table: Sequence[Sequence[int | None]],
    i: int,
    j: int,
) -> TreeNode | None:
    """Reconstruct a real binary tree from the DP root table."""

    if i > j:
        return None

    root_index = root_table[i][j]
    if root_index is None:
        raise ValueError(f"Missing root table entry for interval [{i}, {j}].")

    node = TreeNode(
        key=keys[root_index],
        probability=float(probabilities[root_index]),
        original_index=root_index,
    )
    node.left = reconstruct_tree(keys, probabilities, root_table, i, root_index - 1)
    node.right = reconstruct_tree(keys, probabilities, root_table, root_index + 1, j)
    return node


def calculate_depths(tree: TreeNode | None) -> dict[int | float, int]:
    """Return a mapping from each key to its depth in the tree."""

    depths: dict[int | float, int] = {}

    def visit(node: TreeNode | None, depth: int) -> None:
        if node is None:
            return
        depths[node.key] = depth
        visit(node.left, depth + 1)
        visit(node.right, depth + 1)

    visit(tree, 0)
    return depths


def calculate_expected_cost(
    tree: TreeNode | None,
    probabilities_by_key: dict[int | float, float],
) -> float:
    """Calculate expected successful-search comparisons from a constructed tree."""

    depths = calculate_depths(tree)
    return sum(probabilities_by_key[key] * (depth + 1) for key, depth in depths.items())


def calculate_average_depth(tree: TreeNode | None) -> float:
    """Return the unweighted average depth of nodes in a tree."""

    depths = calculate_depths(tree)
    if not depths:
        return 0.0
    return sum(depths.values()) / len(depths)


def inorder_keys(tree: TreeNode | None) -> list[int | float]:
    """Return the keys visited by an inorder traversal."""

    if tree is None:
        return []
    return inorder_keys(tree.left) + [tree.key] + inorder_keys(tree.right)


def validate_bst_property(tree: TreeNode | None) -> bool:
    """Return True if the in-memory tree satisfies the BST ordering property."""

    keys = inorder_keys(tree)
    return all(keys[index] < keys[index + 1] for index in range(len(keys) - 1))
