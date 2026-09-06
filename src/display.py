"""Text formatting helpers for command-line output."""

from __future__ import annotations

from typing import Sequence

from src.models import TreeNode
from src.obst import calculate_depths


def format_key(key: int | float) -> str:
    """Format numeric keys without unnecessary trailing .0."""

    if isinstance(key, float) and key.is_integer():
        return str(int(key))
    return str(key)


def format_probability(value: float) -> str:
    """Format probabilities and expected costs consistently."""

    return f"{value:.6f}".rstrip("0").rstrip(".") if value != 0 else "0"


def format_input(keys: Sequence[int | float], probabilities: Sequence[float]) -> str:
    """Return a readable input summary."""

    lines = ["Input Keys and Probabilities", "----------------------------"]
    for key, probability in zip(keys, probabilities):
        lines.append(f"{format_key(key):>8} : {probability:.6f}")
    return "\n".join(lines)


def format_cost_table(keys: Sequence[int | float], cost_table: Sequence[Sequence[float | None]]) -> str:
    """Return a formatted upper-triangular DP cost table."""

    labels = [format_key(key) for key in keys]
    width = max(10, max(len(label) for label in labels) + 2)
    header = " " * width + "".join(label.rjust(width) for label in labels)
    rows = ["DP Cost Table", "-------------", header]
    for i, label in enumerate(labels):
        cells = [label.rjust(width)]
        for j in range(len(labels)):
            value = cost_table[i][j]
            cells.append(("-" if value is None else f"{value:.4f}").rjust(width))
        rows.append("".join(cells))
    return "\n".join(rows)


def format_root_table(
    keys: Sequence[int | float],
    root_table: Sequence[Sequence[int | None]],
) -> str:
    """Return a formatted root table using actual key values."""

    labels = [format_key(key) for key in keys]
    width = max(10, max(len(label) for label in labels) + 2)
    header = " " * width + "".join(label.rjust(width) for label in labels)
    rows = ["Root Table", "----------", header]
    for i, label in enumerate(labels):
        cells = [label.rjust(width)]
        for j in range(len(labels)):
            root_index = root_table[i][j]
            value = "-" if root_index is None else format_key(keys[root_index])
            cells.append(value.rjust(width))
        rows.append("".join(cells))
    return "\n".join(rows)


def format_tree(tree: TreeNode | None) -> str:
    """Return an ASCII representation of a binary tree."""

    if tree is None:
        return "(empty)"

    lines = [format_key(tree.key)]

    def visit(node: TreeNode | None, prefix: str, branch_label: str, is_last: bool) -> None:
        if node is None:
            return
        connector = "`-- " if is_last else "|-- "
        lines.append(f"{prefix}{connector}{branch_label}: {format_key(node.key)}")
        child_prefix = prefix + ("    " if is_last else "|   ")
        children = [(node.left, "L"), (node.right, "R")]
        existing_children = [(child, label) for child, label in children if child is not None]
        for index, (child, label) in enumerate(existing_children):
            visit(child, child_prefix, label, index == len(existing_children) - 1)

    children = [(tree.left, "L"), (tree.right, "R")]
    existing_children = [(child, label) for child, label in children if child is not None]
    for index, (child, label) in enumerate(existing_children):
        visit(child, "", label, index == len(existing_children) - 1)
    return "\n".join(lines)


def format_depth_table(
    keys: Sequence[int | float],
    probabilities: Sequence[float],
    tree: TreeNode | None,
) -> str:
    """Return key, probability, depth, and comparison count table."""

    depths = calculate_depths(tree)
    lines = [
        "Key | Probability | Depth | Comparisons",
        "----|-------------|-------|------------",
    ]
    for key, probability in zip(keys, probabilities):
        depth = depths[key]
        lines.append(
            f"{format_key(key):>3} | {probability:>11.6f} | {depth:>5} | {depth + 1:>11}"
        )
    return "\n".join(lines)
