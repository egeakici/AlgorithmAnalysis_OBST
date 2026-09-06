import unittest
from pathlib import Path

from src.input_parser import parse_csv_input, parse_text_input
from src.obst import validate_input


FIXTURE_DIR = Path(__file__).parent / "fixtures"


class TestInputValidation(unittest.TestCase):
    def test_probabilities_not_sum_to_one(self) -> None:
        with self.assertRaisesRegex(ValueError, "sum to 1"):
            validate_input([10, 20], [0.2, 0.2])

    def test_negative_probability(self) -> None:
        with self.assertRaisesRegex(ValueError, "negative"):
            validate_input([10, 20], [1.1, -0.1])

    def test_duplicate_key(self) -> None:
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate_input([10, 10], [0.5, 0.5])

    def test_unsorted_keys(self) -> None:
        with self.assertRaisesRegex(ValueError, "sorted"):
            validate_input([20, 10], [0.5, 0.5])

    def test_empty_input(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least one"):
            validate_input([], [])

    def test_text_parser_mismatched_count(self) -> None:
        with self.assertRaisesRegex(ValueError, "Expected 3"):
            parse_text_input(FIXTURE_DIR / "bad_mismatched_count.txt")

    def test_text_parser_malformed_number(self) -> None:
        with self.assertRaisesRegex(ValueError, "probability is not numeric"):
            parse_text_input(FIXTURE_DIR / "bad_malformed_number.txt")

    def test_csv_parser(self) -> None:
        keys, probabilities = parse_csv_input(FIXTURE_DIR / "sample.csv")

        self.assertEqual(keys, [10, 20])
        self.assertEqual(probabilities, [0.4, 0.6])


if __name__ == "__main__":
    unittest.main()
