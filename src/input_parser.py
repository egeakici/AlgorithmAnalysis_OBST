"""Input parsing utilities for text and CSV OBST datasets."""

from __future__ import annotations

import csv
from pathlib import Path


def parse_key(raw_value: str, line_number: int) -> int | float:
    """Parse a numeric key, preserving integer-looking keys as int values."""

    try:
        value = float(raw_value)
    except ValueError as exc:
        raise ValueError(f"Line {line_number}: key is not numeric: {raw_value!r}.") from exc
    if value.is_integer():
        return int(value)
    return value


def parse_probability(raw_value: str, line_number: int) -> float:
    """Parse a probability value."""

    try:
        return float(raw_value)
    except ValueError as exc:
        raise ValueError(
            f"Line {line_number}: probability is not numeric: {raw_value!r}."
        ) from exc


def parse_text_input(path: str | Path) -> tuple[list[int | float], list[float]]:
    """Parse the simple text format documented in README.md."""

    lines = Path(path).read_text(encoding="utf-8").splitlines()
    non_empty_lines = [(index + 1, line.strip()) for index, line in enumerate(lines) if line.strip()]
    if not non_empty_lines:
        raise ValueError("Input file is empty.")

    first_line_number, first_line = non_empty_lines[0]
    try:
        expected_count = int(first_line)
    except ValueError as exc:
        raise ValueError(f"Line {first_line_number}: first line must be an integer n.") from exc

    if expected_count <= 0:
        raise ValueError("n must be greater than 0.")

    data_lines = non_empty_lines[1:]
    if len(data_lines) != expected_count:
        raise ValueError(
            f"Expected {expected_count} key/probability rows, found {len(data_lines)}."
        )

    keys: list[int | float] = []
    probabilities: list[float] = []
    for line_number, line in data_lines:
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(
                f"Line {line_number}: expected exactly two values: key probability."
            )
        keys.append(parse_key(parts[0], line_number))
        probabilities.append(parse_probability(parts[1], line_number))

    return keys, probabilities


def parse_csv_input(path: str | Path) -> tuple[list[int | float], list[float]]:
    """Parse CSV input with key and probability columns.

    Header names are matched case-insensitively after trimming whitespace, so
    both ``key,probability`` and ``Key,Probability`` are accepted.
    """

    keys: list[int | float] = []
    probabilities: list[float] = []
    with Path(path).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or missing a header.")
        required_columns = {"key", "probability"}
        normalized_to_original = {
            field.strip().lower(): field for field in reader.fieldnames if field is not None
        }
        if required_columns - set(normalized_to_original):
            raise ValueError("CSV header must contain 'key' and 'probability' columns.")
        key_column = normalized_to_original["key"]
        probability_column = normalized_to_original["probability"]

        for row_number, row in enumerate(reader, start=2):
            key_value = row.get(key_column)
            probability_value = row.get(probability_column)
            if key_value is None or probability_value is None:
                raise ValueError(f"Row {row_number}: missing key or probability.")
            keys.append(parse_key(key_value.strip(), row_number))
            probabilities.append(parse_probability(probability_value.strip(), row_number))

    if not keys:
        raise ValueError("CSV input must contain at least one data row.")
    return keys, probabilities


def load_input(path: str | Path, input_format: str = "auto") -> tuple[list[int | float], list[float]]:
    """Load an input file using text, CSV, or extension-based auto detection."""

    path = Path(path)
    selected_format = input_format.lower()
    if selected_format == "auto":
        selected_format = "csv" if path.suffix.lower() == ".csv" else "text"

    if selected_format == "text":
        return parse_text_input(path)
    if selected_format == "csv":
        return parse_csv_input(path)
    raise ValueError("Format must be one of: auto, text, csv.")
