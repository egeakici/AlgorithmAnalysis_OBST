import math
import unittest

from src.obst import (
    calculate_expected_cost,
    compute_obst,
    inorder_keys,
    validate_bst_property,
)


class TestOptimalBST(unittest.TestCase):
    def test_reference_example_cost(self) -> None:
        keys = [10, 20, 30, 40, 50]
        probabilities = [0.10, 0.20, 0.40, 0.20, 0.10]
        result = compute_obst(keys, probabilities)

        self.assertTrue(math.isclose(result.minimum_cost, 1.8, abs_tol=1e-9))
        self.assertEqual(result.tree.key, 30)

    def test_single_key(self) -> None:
        result = compute_obst([10], [1.0])

        self.assertTrue(math.isclose(result.minimum_cost, 1.0, abs_tol=1e-9))
        self.assertEqual(result.tree.key, 10)

    def test_two_key_example(self) -> None:
        result = compute_obst([10, 20], [0.25, 0.75])

        self.assertTrue(math.isclose(result.minimum_cost, 1.25, abs_tol=1e-9))
        self.assertEqual(result.tree.key, 20)

    def test_tree_reconstruction_contains_all_keys_once(self) -> None:
        keys = [10, 20, 30, 40, 50]
        result = compute_obst(keys, [0.10, 0.20, 0.40, 0.20, 0.10])

        self.assertEqual(sorted(inorder_keys(result.tree)), keys)
        self.assertEqual(len(inorder_keys(result.tree)), len(set(keys)))

    def test_bst_ordering_property_is_preserved(self) -> None:
        result = compute_obst([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])

        self.assertTrue(validate_bst_property(result.tree))

    def test_reconstructed_tree_cost_matches_dp_result(self) -> None:
        keys = [1, 2, 3, 4]
        probabilities = [0.1, 0.2, 0.3, 0.4]
        result = compute_obst(keys, probabilities)
        tree_cost = calculate_expected_cost(result.tree, dict(zip(keys, probabilities)))

        self.assertTrue(math.isclose(result.minimum_cost, tree_cost, abs_tol=1e-9))

    def test_root_table_contains_valid_indices(self) -> None:
        keys = [10, 20, 30, 40, 50]
        result = compute_obst(keys, [0.10, 0.20, 0.40, 0.20, 0.10])

        for i, row in enumerate(result.root_table):
            for j, root_index in enumerate(row):
                if i <= j:
                    self.assertIsNotNone(root_index)
                    self.assertGreaterEqual(root_index, i)
                    self.assertLessEqual(root_index, j)
                else:
                    self.assertIsNone(root_index)


if __name__ == "__main__":
    unittest.main()
