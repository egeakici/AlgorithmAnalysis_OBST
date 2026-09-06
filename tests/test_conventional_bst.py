import unittest

from src.conventional_bst import build_conventional_bst
from src.obst import inorder_keys, validate_bst_property


class TestConventionalBST(unittest.TestCase):
    def test_conventional_bst_contains_all_keys(self) -> None:
        keys = [10, 20, 30, 40, 50]
        probabilities = [0.10, 0.20, 0.40, 0.20, 0.10]
        tree, _ = build_conventional_bst(keys, probabilities)

        self.assertEqual(inorder_keys(tree), keys)

    def test_conventional_bst_ordering_property(self) -> None:
        tree, _ = build_conventional_bst([1, 2, 3], [0.2, 0.3, 0.5])

        self.assertTrue(validate_bst_property(tree))


if __name__ == "__main__":
    unittest.main()
