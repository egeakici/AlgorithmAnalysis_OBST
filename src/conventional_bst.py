"""Conventional insertion-order Binary Search Tree baseline."""

from __future__ import annotations

from time import perf_counter
from typing import Sequence

from src.models import TreeNode
from src.obst import calculate_average_depth, calculate_depths, calculate_expected_cost


def insert(root: TreeNode | None, key: int | float, probability: float, index: int) -> TreeNode:
    """Insert one key using ordinary BST insertion rules."""

    if root is None:
        return TreeNode(key=key, probability=float(probability), original_index=index)

    current = root
    while True:
        if key < current.key:
            if current.left is None:
                current.left = TreeNode(key=key, probability=float(probability), original_index=index)
                return root
            current = current.left
        elif key > current.key:
            if current.right is None:
                current.right = TreeNode(key=key, probability=float(probability), original_index=index)
                return root
            current = current.right
        else:
            raise ValueError(f"Duplicate key cannot be inserted into BST: {key!r}.")


def build_conventional_bst(
    keys: Sequence[int | float],
    probabilities: Sequence[float],
) -> tuple[TreeNode | None, float]:
    """Build a conventional BST by inserting keys in the supplied order."""

    start = perf_counter()
    root: TreeNode | None = None
    for index, (key, probability) in enumerate(zip(keys, probabilities)):
        root = insert(root, key, float(probability), index)
    return root, perf_counter() - start


def summarize_bst(
    tree: TreeNode | None,
    probabilities_by_key: dict[int | float, float],
) -> dict[str, float | dict[int | float, int]]:
    """Return depth and cost metrics for a BST."""

    depths = calculate_depths(tree)
    return {
        "depths": depths,
        "expected_cost": calculate_expected_cost(tree, probabilities_by_key),
        "average_depth": calculate_average_depth(tree),
    }
