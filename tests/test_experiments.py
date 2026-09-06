import unittest

from src.experiments import generate_dataset
from src.obst import validate_input


class TestExperiments(unittest.TestCase):
    def test_generated_dataset_is_deterministic_for_same_seed(self) -> None:
        first_keys, first_probabilities = generate_dataset(10, seed=2036)
        second_keys, second_probabilities = generate_dataset(10, seed=2036)

        self.assertEqual(first_keys, second_keys)
        self.assertEqual(first_probabilities, second_probabilities)
        validate_input(first_keys, first_probabilities)


if __name__ == "__main__":
    unittest.main()
