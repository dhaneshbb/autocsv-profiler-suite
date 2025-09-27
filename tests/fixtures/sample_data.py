"""
Sample data generators for testing AutoCSV Profiler Suite.

Provides functions to generate various types of test data for CSV analysis testing.
"""

import random
import string
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict

import numpy as np
import pandas as pd


def generate_clean_sample_data(num_rows: int = 100) -> pd.DataFrame:
    """Generate clean sample data with no quality issues."""
    np.random.seed(42)  # For reproducible tests
    random.seed(42)

    data = {
        "id": range(1, num_rows + 1),
        "name": [f"Person_{i}" for i in range(1, num_rows + 1)],
        "age": np.random.randint(18, 80, num_rows),
        "salary": np.random.normal(50000, 15000, num_rows).round(2),
        "department": np.random.choice(
            ["IT", "HR", "Finance", "Marketing", "Operations"], num_rows
        ),
        "is_active": np.random.choice([True, False], num_rows, p=[0.8, 0.2]),
        "join_date": [
            (datetime.now() - timedelta(days=np.random.randint(30, 1825))).strftime(
                "%Y-%m-%d"
            )
            for _ in range(num_rows)
        ],
    }

    return pd.DataFrame(data)


def generate_dirty_sample_data(num_rows: int = 100) -> pd.DataFrame:
    """Generate sample data with various quality issues."""
    np.random.seed(42)
    random.seed(42)

    # Start with clean data
    df = generate_clean_sample_data(num_rows)

    # Introduce missing values
    missing_indices = np.random.choice(
        df.index, size=int(num_rows * 0.1), replace=False
    )
    df.loc[missing_indices, "name"] = np.nan

    missing_indices = np.random.choice(
        df.index, size=int(num_rows * 0.05), replace=False
    )
    df.loc[missing_indices, "age"] = np.nan

    missing_indices = np.random.choice(
        df.index, size=int(num_rows * 0.08), replace=False
    )
    df.loc[missing_indices, "salary"] = np.nan

    # Introduce invalid ages
    invalid_age_indices = np.random.choice(df.index, size=3, replace=False)
    df.loc[invalid_age_indices[0], "age"] = -5
    df.loc[invalid_age_indices[1], "age"] = 150
    df.loc[invalid_age_indices[2], "age"] = 0

    # Introduce invalid salaries
    invalid_salary_indices = np.random.choice(df.index, size=2, replace=False)
    df.loc[invalid_salary_indices[0], "salary"] = -10000
    df.loc[invalid_salary_indices[1], "salary"] = 10000000  # Unrealistically high

    # Introduce empty strings
    empty_string_indices = np.random.choice(df.index, size=5, replace=False)
    df.loc[empty_string_indices, "name"] = ""

    # Introduce invalid dates
    invalid_date_indices = np.random.choice(df.index, size=3, replace=False)
    df.loc[invalid_date_indices, "join_date"] = ["2021-13-45", "invalid-date", ""]

    return df


def generate_large_sample_data(num_rows: int = 10000) -> pd.DataFrame:
    """Generate large sample data for performance testing."""
    np.random.seed(42)
    random.seed(42)

    data = {
        "id": range(1, num_rows + 1),
        "category_a": np.random.choice([f"Cat_A_{i}" for i in range(50)], num_rows),
        "category_b": np.random.choice([f"Cat_B_{i}" for i in range(20)], num_rows),
        "numerical_1": np.random.normal(100, 25, num_rows),
        "numerical_2": np.random.exponential(2, num_rows),
        "numerical_3": np.random.uniform(0, 1000, num_rows),
        "text_field": [
            "".join(
                random.choices(string.ascii_letters + " ", k=random.randint(10, 100))
            )
            for _ in range(num_rows)
        ],
        "boolean_field": np.random.choice([True, False], num_rows),
        "timestamp": [
            (datetime.now() - timedelta(seconds=np.random.randint(0, 31536000)))
            for _ in range(num_rows)
        ],
    }

    return pd.DataFrame(data)


def generate_high_cardinality_data(num_rows: int = 1000) -> pd.DataFrame:
    """Generate data with high cardinality columns for testing."""
    np.random.seed(42)
    random.seed(42)

    data = {
        "id": list(range(1, num_rows + 1)),
        "unique_id": [
            f"UUID_{random.randint(10000000, 99999999):08x}" for _ in range(num_rows)
        ],
        "email": [f"user{i}@example{i % 5}.com" for i in range(1, num_rows + 1)],
        "phone": [
            f"+1{random.randint(1000000000, 9999999999)}" for _ in range(num_rows)
        ],
        "category": np.random.choice(
            ["A", "B", "C"], num_rows
        ).tolist(),  # Low cardinality for comparison
        "value": np.random.normal(0, 1, num_rows).tolist(),
    }

    return pd.DataFrame(data)


def generate_special_characters_data(num_rows: int = 50) -> pd.DataFrame:
    """Generate data with special characters, unicode, and encoding issues."""

    name_list = [
        "José María",
        "François Müller",
        "Ñoño García",
        "王小明",
        "Mohammed عبد الله",
        "Olga Москва",
        "Κωνσταντίνος",
        "Søren Østergård",
        "Piñata Niño",
        "田中太郎",
    ]

    desc_list = [
        "Text with \"quotes\" and 'apostrophes'",
        "Data, with, commas, everywhere",
        "Semicolons; are; common; in; Europe",
        "Tabs\tare\tdifficult\tto\thandle",
        "Line\nbreaks\ncan\nbreak\nCSVs",
        "Pipes | are | sometimes | delimiters",
        "Special chars: !@#$%^&*()",
        "HTML tags: <div>content</div>",
        'JSON: {"key": "value", "number": 123}',
        "URLs: https://example.com/path?param=value",
    ]

    data = {
        "id": list(range(1, num_rows + 1)),
        "name_unicode": [name_list[i % len(name_list)] for i in range(num_rows)],
        "description_special": [desc_list[i % len(desc_list)] for i in range(num_rows)],
    }

    return pd.DataFrame(data)


def generate_mixed_types_data(num_rows: int = 100) -> pd.DataFrame:
    """Generate data with mixed/inconsistent types in columns."""
    np.random.seed(42)
    random.seed(42)

    mixed_numbers = ["123", 456, "78.9", 101.1, "not_a_number"]
    mixed_dates = [
        "2023-01-15",
        "2023/02/20",
        "15-Mar-2023",
        "20230425",
        "invalid_date",
    ]
    mixed_bools = [True, False, "true", "false", 1, 0, "yes", "no"]

    data = {
        "id": list(range(1, num_rows + 1)),
        "mixed_numbers": [
            mixed_numbers[i % len(mixed_numbers)] for i in range(num_rows)
        ],
        "mixed_dates": [mixed_dates[i % len(mixed_dates)] for i in range(num_rows)],
        "mixed_booleans": [mixed_bools[i % len(mixed_bools)] for i in range(num_rows)],
    }

    return pd.DataFrame(data)


def create_sample_csv_files(output_dir: Path) -> Dict[str, Path]:
    """Create various sample CSV files for testing."""
    output_dir.mkdir(parents=True, exist_ok=True)

    files_created = {}

    # Clean data
    clean_df = generate_clean_sample_data(100)
    clean_file = output_dir / "clean_sample.csv"
    clean_df.to_csv(clean_file, index=False)
    files_created["clean"] = clean_file

    # Dirty data
    dirty_df = generate_dirty_sample_data(100)
    dirty_file = output_dir / "dirty_sample.csv"
    dirty_df.to_csv(dirty_file, index=False)
    files_created["dirty"] = dirty_file

    # Large data
    large_df = generate_large_sample_data(5000)  # Smaller for faster tests
    large_file = output_dir / "large_sample.csv"
    large_df.to_csv(large_file, index=False)
    files_created["large"] = large_file

    # High cardinality
    high_card_df = generate_high_cardinality_data(500)
    high_card_file = output_dir / "high_cardinality_sample.csv"
    high_card_df.to_csv(high_card_file, index=False)
    files_created["high_cardinality"] = high_card_file

    # Special characters
    special_df = generate_special_characters_data(50)
    special_file = output_dir / "special_characters_sample.csv"
    special_df.to_csv(special_file, index=False, encoding="utf-8")
    files_created["special_characters"] = special_file

    # Mixed types
    mixed_df = generate_mixed_types_data(100)
    mixed_file = output_dir / "mixed_types_sample.csv"
    mixed_df.to_csv(mixed_file, index=False)
    files_created["mixed_types"] = mixed_file

    # Different delimiters
    delimiters = [";", "\t", "|", ":"]
    for delimiter in delimiters:
        delimiter_name = {";": "semicolon", "\t": "tab", "|": "pipe", ":": "colon"}[
            delimiter
        ]
        delimiter_file = output_dir / f"delimiter_{delimiter_name}_sample.csv"
        clean_df.to_csv(delimiter_file, index=False, sep=delimiter)
        files_created[f"delimiter_{delimiter_name}"] = delimiter_file

    # Empty file
    empty_file = output_dir / "empty_sample.csv"
    empty_file.touch()
    files_created["empty"] = empty_file

    # Single column
    single_col_df = pd.DataFrame({"single_column": range(1, 21)})
    single_col_file = output_dir / "single_column_sample.csv"
    single_col_df.to_csv(single_col_file, index=False)
    files_created["single_column"] = single_col_file

    # Headers only
    headers_only_file = output_dir / "headers_only_sample.csv"
    with open(headers_only_file, "w") as f:
        f.write("col1,col2,col3\n")
    files_created["headers_only"] = headers_only_file

    return files_created


def get_expected_analysis_results() -> Dict[str, Any]:
    """Get expected results for sample data analysis."""
    return {
        "clean_sample": {
            "expected_columns": 7,
            "expected_rows": 100,
            "expected_missing_percentage": 0.0,
            "expected_numeric_columns": ["id", "age", "salary"],
            "expected_categorical_columns": ["name", "department", "join_date"],
            "expected_boolean_columns": ["is_active"],
        },
        "dirty_sample": {
            "expected_columns": 7,
            "expected_rows": 100,
            "expected_missing_percentage": 23.0,  # Approximate
            "expected_issues": [
                "missing_values",
                "invalid_ages",
                "invalid_salaries",
                "empty_strings",
                "invalid_dates",
            ],
        },
        "large_sample": {
            "expected_columns": 9,
            "expected_rows": 5000,
            "expected_high_cardinality_columns": ["id", "text_field", "timestamp"],
            "performance_expectations": {
                "max_memory_mb": 50,
                "max_processing_time_seconds": 30,
            },
        },
    }
