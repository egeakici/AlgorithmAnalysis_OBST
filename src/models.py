"""Data models shared by the OBST and comparison implementations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    """A node in a binary search tree."""

    key: int | float
    probability: float
    original_index: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


@dataclass
class OBSTResult:
    """Complete result produced by the Dynamic Programming OBST algorithm."""

    minimum_cost: float
    cost_table: list[list[float | None]]
    root_table: list[list[int | None]]
    tree: TreeNode | None
    elapsed_seconds: float
