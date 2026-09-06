# Algorithm Explanation

## 1. Binary Search Tree

A Binary Search Tree (BST) stores keys so that every key in a node's left
subtree is smaller than the node's key, and every key in the right subtree is
larger. This ordering makes search follow one path from the root to the target.

## 2. Why Arrangement Affects Search Cost

Keys near the root are found with fewer comparisons. If a frequently searched
key is placed deep in the tree, it contributes a large amount to expected cost.

## 3. Why Probabilities Change Optimality

A balanced BST minimizes height reasonably well, but it does not consider how
often each key is searched. An Optimal BST minimizes probability-weighted search
cost, so a more frequent key may be placed closer to the root even when the
tree is not perfectly balanced.

## 4. Balanced BST vs Optimal BST

A balanced BST is usually designed to keep subtree heights close. An OBST is
designed to minimize expected comparisons based on probabilities. These goals
can produce different trees.

## 5. DP State

In mathematical 1-based notation:

```text
C[i,j] = minimum expected search cost for keys k_i through k_j
```

In Python, the same state is stored as `cost[i - 1][j - 1]` because lists are
0-based.

## 6. Base Cases

```text
C[i,i] = p_i
C[i,i-1] = 0
```

A single key costs its probability times one comparison. An empty subtree has no
cost.

## 7. Recurrence

```text
C[i,j] = sum(p_s for s=i..j) + min over r=i..j (C[i,r-1] + C[r+1,j])
```

Every possible root `r` is tried for the interval.

## 8. Meaning of the Summation Term

When a root is placed above two subtrees, every key inside those subtrees becomes
one level deeper. Since one extra level means one extra comparison, the
additional expected cost is the sum of all probabilities in the interval.

## 9. Optimal Substructure

If a key `r` is the root of an optimal tree for interval `[i,j]`, then the left
subtree must be optimal for `[i,r-1]` and the right subtree must be optimal for
`[r+1,j]`. Otherwise, replacing a non-optimal subtree would improve the whole
tree.

## 10. Overlapping Subproblems

Many larger intervals reuse smaller intervals such as `[i,j-1]`, `[i+1,j]`, and
other subranges. Dynamic Programming stores these results instead of recomputing
them.

## 11. Bottom-Up Filling Order

The table is filled by increasing interval length. Length `1` intervals are
base cases. Length `2` intervals depend only on length `1` and empty intervals,
and so on until the full interval is computed.

## 12. Prefix Sums

The implementation builds:

```text
prefix[0] = 0
prefix[i+1] = prefix[i] + probabilities[i]
```

For 0-based inclusive indices:

```text
weight(i,j) = prefix[j+1] - prefix[i]
```

This makes interval probability calculation `O(1)`.

## 13. Root Table

The `root[i][j]` table stores which index was selected as the optimal root for
interval `[i,j]`. The displayed table shows key values for readability.

## 14. Tree Reconstruction

Starting from `root[0][n-1]`, the algorithm recursively constructs the root,
then the left subtree from the left interval, and the right subtree from the
right interval. Empty intervals return `None`.

## 15. Expected-Cost Verification

After reconstruction, the program traverses the tree, computes each key's depth,
uses `comparisons = depth + 1`, and checks that:

```text
sum(p_i * comparisons_i) approximately equals cost[0][n-1]
```

## 16. Pseudocode

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

## 17. Time Complexity

There are `O(n^2)` intervals `[i,j]`. For each interval, the algorithm tries up
to `O(n)` roots. Therefore:

```text
O(n^2) * O(n) = O(n^3)
```

## 18. Space Complexity

The cost and root tables each use `O(n^2)` space. Prefix sums use `O(n)`, and
the reconstructed tree uses `O(n)`, so the total asymptotic space complexity is
`O(n^2)`.

## Project Evaluation Questions

**What does C[i,j] represent?** It is the minimum expected search cost for keys
from `k_i` through `k_j`.

**Why is Dynamic Programming appropriate here?** The problem has optimal
substructure and overlapping subproblems.

**What are the overlapping subproblems?** The same key intervals are needed
when evaluating many larger intervals.

**What is the optimal-substructure property?** Once a root is chosen, its left
and right subtrees must also be optimal for their intervals.

**Why do we add the sum of probabilities?** All keys in the chosen subtrees move
one level deeper, adding one comparison weighted by their probabilities.

**Why do we need a root table?** The cost table gives the value, while the root
table records choices needed to rebuild the actual tree.

**Why is the time complexity O(n^3)?** `O(n^2)` intervals times up to `O(n)`
candidate roots.

**Why is the space complexity O(n^2)?** The algorithm stores two `n x n` tables.

**What is the difference between depth and comparison count?** The root depth is
`0`, but finding it still needs one comparison, so comparisons equal
`depth + 1`.

**Why is an OBST not necessarily balanced?** It optimizes probability-weighted
cost, not height.

**How do you verify the final expected cost?** Traverse the constructed tree,
compute `sum(probability * (depth + 1))`, and compare it with the DP result.

**Why are prefix sums useful?** They make interval probability sums constant
time.

**What would happen with a naive recursive solution?** It would recompute many
subintervals repeatedly and become inefficient.

**What does the conventional BST comparison show?** It shows how insertion
order, especially sorted order, can create an inefficient unbalanced tree.
