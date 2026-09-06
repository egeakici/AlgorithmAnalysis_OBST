# Optimal Binary Search Tree Using Dynamic Programming

This repository is a university-level **Design and Analysis of Algorithms**
course project. It is intentionally written as an academic, explanation-first
implementation rather than only as a short coding exercise.

The project demonstrates how to construct an **Optimal Binary Search Tree
(OBST)** using the standard `O(n^3)` Dynamic Programming algorithm. It includes
the algorithm implementation, input validation, command-line usage, automated
tests, sample inputs and outputs, experimental timing results, and a written
report.

## Academic Purpose

The main goal of this project is to make the OBST algorithm understandable and
defensible during a course evaluation. A Computer Engineering student should be
able to explain:

- what problem an Optimal BST solves
- why search probabilities affect the best tree shape
- how the Dynamic Programming state is defined
- how the recurrence is derived
- why prefix sums are used
- how the root table reconstructs the final tree
- why the time complexity is `O(n^3)`
- why the space complexity is `O(n^2)`
- how the result compares with a conventional BST

## Project Description

Given sorted unique keys and successful-search probabilities, the program builds
a Binary Search Tree that minimizes the expected number of comparisons required
to find a key.

For example, if key `30` is searched more often than the other keys, the optimal
tree may place it closer to the root even if that does not simply mean building
a perfectly balanced tree.

The implementation does **not** hard-code the sample result. All costs, tables,
roots, depths, and tree structures are computed from the input.

## Problem Definition

Given:

```text
K = {k1, k2, ..., kn}
p = {p1, p2, ..., pn}
```

where the keys are sorted and the probabilities are non-negative values that sum
to approximately `1`, construct a Binary Search Tree that minimizes:

```text
sum(p_i * comparisons_i)
```

The root has depth `0`, so:

```text
comparisons = depth + 1
```

## Dynamic Programming Formulation

Let `C[i,j]` be the minimum expected successful-search cost for keys `k_i`
through `k_j` in mathematical 1-based notation.

Base cases:

```text
C[i,i] = p_i
C[i,i-1] = 0
```

Recurrence:

```text
C[i,j] =
    sum(p_s for s = i..j)
    + min over r = i..j (C[i,r-1] + C[r+1,j])
```

The summation term is added because when a root is placed above the left and
right subtrees, every key in those subtrees becomes one level deeper and
therefore costs one additional comparison.

The Python implementation uses 0-based indexing:

```text
mathematical C[i,j]  ->  Python cost[i-1][j-1]
```

Prefix sums are used so interval probabilities are computed in `O(1)`:

```text
prefix[0] = 0
prefix[i+1] = prefix[i] + probabilities[i]
weight(i,j) = prefix[j+1] - prefix[i]
```

## What the Program Produces

For a given input file, the CLI can show:

- input keys and probabilities
- Dynamic Programming cost table
- root table
- reconstructed Optimal BST
- depth of every key
- comparison count of every key
- expected cost recomputed from the tree
- verification result
- conventional BST comparison
- construction time

The verification step is important: the program rebuilds the tree from the root
table, traverses it, recalculates expected cost, and checks that this value
matches the DP minimum.

## Project Structure

```text
.
|-- README.md
|-- requirements.txt
|-- src/
|   |-- __init__.py
|   |-- models.py
|   |-- obst.py
|   |-- conventional_bst.py
|   |-- input_parser.py
|   |-- display.py
|   |-- experiments.py
|   `-- main.py
|-- tests/
|   |-- __init__.py
|   |-- test_obst.py
|   |-- test_input_validation.py
|   |-- test_conventional_bst.py
|   `-- fixtures/
|-- data/
|   |-- sample_input.txt
|   |-- sample_input.csv
|   `-- README.md
|-- docs/
|   |-- algorithm.md
|   `-- sample_output.txt
|-- experiments/
|   |-- README.md
|   `-- results.csv
|-- outputs/
|   `-- .gitkeep
`-- report/
    |-- report.md
    `-- figures/
```

## Requirements

Python 3.10+ is recommended.

The project uses only the Python standard library. No third-party package is
required.

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/egeakici/AlgorithmAnalysis_OBST.git
cd AlgorithmAnalysis_OBST
```

Check Python:

```bash
python --version
```

No dependency installation is needed. `requirements.txt` is included only to
state that the project has no external dependencies.

## Input Format

### Text Input

The first line is `n`. Each following line contains one key and one probability:

```text
5
10 0.10
20 0.20
30 0.40
40 0.20
50 0.10
```

### CSV Input

CSV files must contain `key` and `probability` columns:

```csv
key,probability
10,0.10
20,0.20
30,0.40
40,0.20
50,0.10
```

Input validation checks:

- `n > 0`
- no missing values
- numeric keys and probabilities
- unique keys
- strictly increasing sorted keys
- no negative probabilities
- probabilities sum to `1` within tolerance `1e-6`

## How to Run

Run the main sample with DP tables and conventional BST comparison:

```bash
python -m src.main --input data/sample_input.txt --compare-bst --show-tables
```

Run the CSV version:

```bash
python -m src.main --input data/sample_input.csv --format csv --compare-bst --show-tables
```

Run without printing large DP tables:

```bash
python -m src.main --input data/sample_input.txt --compare-bst
```

Run deterministic experiments:

```bash
python -m src.main --run-experiments
```

## Example Result

For the sample input:

```text
Keys:          10  20  30  40  50
Probabilities: .10 .20 .40 .20 .10
```

The program computes:

```text
Minimum expected search cost (DP): 1.800000
Expected cost from reconstructed tree: 1.800000
Verification result: success
```

The reconstructed Optimal BST is:

```text
30
|-- L: 20
|   `-- L: 10
`-- R: 40
    `-- R: 50
```

Representative actual output is stored in:

```text
docs/sample_output.txt
```

## Conventional BST Comparison

The project also constructs a conventional BST by inserting the same keys in the
supplied order.

Because the sample keys are sorted, ordinary insertion creates an unbalanced
tree:

```text
10
`-- R: 20
    `-- R: 30
        `-- R: 40
            `-- R: 50
```

For the sample data:

```text
Optimal BST expected cost:      1.800000
Conventional BST expected cost: 3.000000
```

This comparison shows why tree shape matters and why probabilities should be
considered when searches are not equally likely.

## Running Tests

Run all automated tests:

```bash
python -m unittest discover -s tests
```

The tests cover:

- the required five-key reference example
- single-key and two-key cases
- tree reconstruction
- BST ordering property
- DP cost versus reconstructed tree cost
- invalid probabilities
- duplicate and unsorted keys
- malformed input files
- conventional BST construction
- deterministic experiment data generation

## Running Experiments

Experiments are run for:

```text
n = 5, 10, 20, 50, 100
```

For each size, the experiment runner:

1. generates sorted unique keys
2. generates positive random weights
3. normalizes weights into probabilities
4. uses deterministic seeds
5. times only the OBST construction
6. writes results to `experiments/results.csv`

View the generated results:

```bash
type experiments\results.csv
```

On macOS/Linux:

```bash
cat experiments/results.csv
```

## Generated Outputs

- `docs/sample_output.txt`: actual captured output from the sample command
- `experiments/results.csv`: actual timing experiment results
- `report/report.md`: academic report source
- `report/report.pdf`: PDF version of the academic report
- `docs/algorithm.md`: detailed algorithm explanation and oral evaluation notes

## Report

The report is available at:

```text
report/report.md
report/report.pdf
```

It includes the problem definition, DP formulation, pseudocode, implementation
details, experimental results, conventional BST comparison, complexity analysis,
discussion, conclusion, and references.

If the Markdown report is edited later and Pandoc is installed, it can be
converted again with:

```bash
pandoc report/report.md -o report/report.pdf
```

The repository also includes a standard-library PDF generator:

```bash
python scripts/generate_report_pdf.py
```

The included PDF is generated from the report source for final submission.

## Complexity

Time Complexity: `O(n^3)`

Reason:

```text
O(n^2) intervals * O(n) candidate roots = O(n^3)
```

Space Complexity: `O(n^2)`

Reason:

```text
cost[n][n] + root[n][n] = O(n^2)
```

Prefix sums require `O(n)` additional space and the reconstructed tree requires
`O(n)` node space, so they do not change the total asymptotic space complexity.

## Notes for Evaluation

Important points to explain during a project presentation:

- `cost_table[i][j]` stores the best cost for a subarray of keys.
- `root_table[i][j]` stores the root choice used to reconstruct the tree.
- root depth is `0`, but root search cost is `1` comparison.
- expected search cost and average depth are different metrics.
- the implementation uses the standard cubic DP algorithm, not Knuth
  optimization.
- the conventional BST baseline uses the same probabilities as the OBST.
- experimental timings may vary because of interpreter overhead, operating
  system scheduling, CPU caching, and timer noise.

## License

This repository is intended for academic coursework and learning.
