# Design and Implementation of an Optimal Binary Search Tree Using Dynamic Programming

## 1. Introduction

This project implements an Optimal Binary Search Tree (OBST) using Dynamic
Programming. The purpose is to construct a Binary Search Tree that minimizes the
expected number of comparisons for successful search when each key has a known
search probability.

## 2. Problem Definition

Given sorted keys `K = {k1, k2, ..., kn}` and successful-search probabilities
`p1, p2, ..., pn`, construct a BST with minimum expected successful-search cost.
The root depth is defined as `0`, so a key at depth `d` requires `d + 1`
comparisons.

## 3. Dynamic Programming Formulation

Let `C[i,j]` be the minimum expected search cost for keys `k_i` through `k_j` in
1-based mathematical notation.

Base cases:

```text
C[i,i] = p_i
C[i,i-1] = 0
```

Recurrence:

```text
C[i,j] = sum(p_s for s=i..j) + min over r=i..j (C[i,r-1] + C[r+1,j])
```

The implementation stores the same state with 0-based Python lists:
mathematical `C[i,j]` corresponds to `cost[i-1][j-1]`.

The probability summation term appears because all keys in the left and right
subtrees move one level deeper when a root is placed above them.

## 4. Algorithm / Pseudocode

```text
OBST(keys, p):
    n = number of keys

    create cost[n][n]
    create root[n][n]
    build prefix sums

    for i = 0 to n-1:
        cost[i][i] = p[i]
        root[i][i] = i

    for length = 2 to n:
        for i = 0 to n-length:
            j = i + length - 1
            cost[i][j] = infinity
            total_weight = weight(i,j)

            for r = i to j:
                left_cost = cost[i][r-1] if r > i else 0
                right_cost = cost[r+1][j] if r < j else 0
                candidate = left_cost + right_cost + total_weight

                if candidate < cost[i][j]:
                    cost[i][j] = candidate
                    root[i][j] = r

    tree = reconstruct(root, 0, n-1)
    return cost[0][n-1], cost, root, tree
```

## 5. Implementation

The implementation is divided into small modules:

| File | Purpose |
|---|---|
| `src/obst.py` | DP algorithm, validation, reconstruction, tree metrics |
| `src/models.py` | `TreeNode` and `OBSTResult` dataclasses |
| `src/conventional_bst.py` | Standard insertion-order BST baseline |
| `src/input_parser.py` | Text and CSV input parsers |
| `src/display.py` | Tables and ASCII tree formatting |
| `src/experiments.py` | Deterministic timing experiments |
| `src/main.py` | Command-line interface |

Prefix sums are used with:

```text
prefix[0] = 0
prefix[i+1] = prefix[i] + p[i]
weight(i,j) = prefix[j+1] - prefix[i]
```

This avoids repeatedly summing probabilities inside the innermost DP loops.

## 6. Experimental Results

Experiments are generated and timed by the program. The final values in this
section must match `experiments/results.csv`.

| n | Mean execution seconds | Minimum expected cost | Seed | Repetitions |
|---|---:|---:|---:|---:|
| 5 | 0.00002722 | 1.79467990 | 2031 | 5 |
| 10 | 0.00005962 | 2.56711511 | 2036 | 5 |
| 20 | 0.00028114 | 3.03411892 | 2046 | 5 |
| 50 | 0.00266794 | 4.38649218 | 2076 | 5 |
| 100 | 0.01913680 | 5.31942274 | 2126 | 5 |

Actual timings may not perfectly follow a cubic ratio because of interpreter
overhead, operating system scheduling, CPU caching, timer noise, and small
sample sizes. The overall growth trend is still expected to reflect `O(n^3)`.

## 7. Comparison with a Conventional BST

The conventional BST baseline inserts the same keys in the supplied order. Since
the assignment inputs are sorted, direct insertion creates a highly unbalanced
tree. The comparison uses the same probabilities as the OBST and reports tree
structure, depths, expected successful-search cost, average depth, and
construction time.

For the sample input, the OBST expected cost is `1.800000`. The conventional BST
constructed by sorted-order insertion has expected search cost `3.000000` and
unweighted average depth `2.000000`. The OBST has unweighted average depth
`1.200000`.

| Tree | Expected successful-search cost | Unweighted average depth |
|---|---:|---:|
| Optimal BST | 1.800000 | 1.200000 |
| Conventional sorted-insertion BST | 3.000000 | 2.000000 |

## 8. Complexity Analysis

Time complexity is `O(n^3)`. There are `O(n^2)` intervals `[i,j]`, and each
interval tries up to `O(n)` roots.

Space complexity is `O(n^2)` because the algorithm stores `cost[n][n]` and
`root[n][n]`. Prefix sums use `O(n)` additional space, and the reconstructed
tree uses `O(n)` node space.

## 9. Discussion

The OBST may not be height-balanced because it optimizes probability-weighted
comparisons rather than height. A frequent key can be placed near the root even
when this makes the tree shape less balanced. The conventional BST comparison
illustrates how a simple insertion-order BST can perform poorly on sorted
input.

The project handles only successful-search probabilities. A complete textbook
OBST variant can also include unsuccessful-search probabilities, but that is
outside this assignment's stated problem.

## 10. Conclusion

The project demonstrates how Dynamic Programming solves the OBST problem by
combining optimal substructure, overlapping subproblems, a root-choice table,
and bottom-up computation. The reconstructed tree is verified independently by
recomputing expected cost from actual node depths.

## 11. References

- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein,
  *Introduction to Algorithms*, Dynamic Programming chapter.
- Donald E. Knuth, *The Art of Computer Programming*, Volume 3: Sorting and
  Searching.

Note: `report/report.pdf` was not generated in this environment because Pandoc
was not installed. The Markdown report is complete and can be converted with the
command listed in `README.md`.
