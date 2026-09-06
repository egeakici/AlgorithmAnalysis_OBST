# Experiments

Run:

```bash
python -m src.main --run-experiments
```

The experiment runner evaluates `n = 5, 10, 20, 50, 100`. For each `n`, it:

1. Generates sorted unique keys using a deterministic seed.
2. Generates positive random weights.
3. Normalizes the weights into probabilities that sum to `1`.
4. Runs the OBST construction several times.
5. Writes the mean construction time and minimum expected cost to
   `experiments/results.csv`.

Input generation and terminal output are not included in the timed algorithm
section.
