"""
Functional tests for the main analyzer engine.

Tests the actual functionality of autocsv_profiler.engines.main.analyzer
without mocking the core functionality.
"""

import sys
import tempfile
from pathlib import Path

import pandas as pd
import pytest

# Add project root to path before importing project modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from autocsv_profiler.core.validation import (  # noqa: E402
    validate_csv_file,
)
from autocsv_profiler.ui.interactive import (  # noqa: E402
    detect_delimiter,
)


class TestAnalyzerEngineFunctional:
    """Functional tests for analyzer engine core functionality."""

    @pytest.fixture
    def temp_csv_file(self):
        """Create a temporary CSV file for testing."""
        temp_dir = Path(tempfile.mkdtemp(prefix="analyzer_test_"))
        csv_file = temp_dir / "test_data.csv"

        # Create test data
        data = {
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 40, 45],
            "salary": [50000.0, 60000.0, 70000.0, 80000.0, 90000.0],
            "department": ["Engineering", "Sales", "Marketing", "Engineering", "Sales"],
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False)

        yield csv_file

        # Cleanup
        if csv_file.exists():
            csv_file.unlink()
        if temp_dir.exists():
            temp_dir.rmdir()

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        temp_dir = Path(tempfile.mkdtemp(prefix="output_test_"))
        yield temp_dir

        # Cleanup
        import shutil

        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    def test_validate_csv_file_valid(self, temp_csv_file):
        """Test CSV validation with valid file."""
        # Should not raise any exception
        validate_csv_file(temp_csv_file)

    def test_validate_csv_file_nonexistent(self):
        """Test CSV validation with non-existent file."""
        with pytest.raises(FileNotFoundError):
            validate_csv_file(Path("nonexistent_file.csv"))

    def test_detect_delimiter_comma(self, temp_csv_file):
        """Test delimiter detection for comma-separated values."""
        delimiter = detect_delimiter(temp_csv_file)
        assert delimiter == ","

    def test_detect_delimiter_semicolon(self):
        """Test delimiter detection for semicolon-separated values."""
        temp_dir = Path(tempfile.mkdtemp(prefix="delimiter_test_"))
        csv_file = temp_dir / "semicolon_data.csv"

        # Create semicolon-separated data
        data = {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_file, sep=";", index=False)

        try:
            delimiter = detect_delimiter(csv_file)
            assert delimiter == ";"
        finally:
            # Cleanup
            if csv_file.exists():
                csv_file.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()

    def test_detect_delimiter_tab(self):
        """Test delimiter detection for tab-separated values."""
        temp_dir = Path(tempfile.mkdtemp(prefix="delimiter_test_"))
        csv_file = temp_dir / "tab_data.csv"

        # Create tab-separated data
        data = {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_file, sep="\t", index=False)

        try:
            delimiter = detect_delimiter(csv_file)
            assert delimiter == "\t"
        finally:
            # Cleanup
            if csv_file.exists():
                csv_file.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()

    def test_load_csv_data_basic(self, temp_csv_file):
        """Test basic CSV data loading."""
        delimiter = detect_delimiter(temp_csv_file)
        df = load_csv_data(temp_csv_file, delimiter)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert len(df.columns) == 5
        assert list(df.columns) == ["id", "name", "age", "salary", "department"]

        # Check data types
        assert df["id"].dtype in ["int64", "int32"]
        assert df["age"].dtype in ["int64", "int32"]
        assert df["salary"].dtype in ["float64", "float32"]
        assert df["name"].dtype == "object"
        assert df["department"].dtype == "object"

    def test_load_csv_data_with_missing_values(self):
        """Test CSV loading with missing values."""
        temp_dir = Path(tempfile.mkdtemp(prefix="missing_test_"))
        csv_file = temp_dir / "missing_data.csv"

        # Create data with missing values
        csv_content = """id,name,age,salary
1,Alice,25,50000
2,Bob,,60000
3,Charlie,35,
4,,40,80000
5,Eve,45,90000"""

        csv_file.write_text(csv_content)

        try:
            delimiter = detect_delimiter(csv_file)
            df = load_csv_data(csv_file, delimiter)

            assert isinstance(df, pd.DataFrame)
            assert len(df) == 5
            assert df["age"].isna().sum() == 1  # One missing age
            assert df["salary"].isna().sum() == 1  # One missing salary
            assert df["name"].isna().sum() == 1  # One missing name

        finally:
            # Cleanup
            if csv_file.exists():
                csv_file.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()

    def test_create_safe_output_dir_new(self, temp_output_dir):
        """Test creating new output directory."""
        output_dir = temp_output_dir / "new_analysis_output"
        result = create_safe_output_dir(output_dir)

        assert result == output_dir
        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_create_safe_output_dir_existing(self, temp_output_dir):
        """Test with existing output directory."""
        # Create directory first
        output_dir = temp_output_dir / "existing_output"
        output_dir.mkdir()

        result = create_safe_output_dir(output_dir)

        assert result == output_dir
        assert output_dir.exists()

    def test_create_safe_output_dir_with_files(self, temp_output_dir):
        """Test creating output directory when files exist."""
        output_dir = temp_output_dir / "analysis_output"
        output_dir.mkdir()

        # Create existing file
        (output_dir / "existing_file.txt").write_text("test content")

        result = create_safe_output_dir(output_dir)

        # Should create new directory with timestamp suffix
        assert result != output_dir
        assert str(result).startswith(str(output_dir))
        assert result.exists()

    def test_load_csv_data_encoding_detection(self):
        """Test CSV loading with different encodings."""
        temp_dir = Path(tempfile.mkdtemp(prefix="encoding_test_"))
        csv_file = temp_dir / "utf8_data.csv"

        # Create data with unicode characters
        data = {
            "id": [1, 2, 3],
            "name": ["André", "José", "François"],
            "city": ["São Paulo", "México", "Montréal"],
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False, encoding="utf-8")

        try:
            delimiter = detect_delimiter(csv_file)
            df_loaded = load_csv_data(csv_file, delimiter)

            assert isinstance(df_loaded, pd.DataFrame)
            assert len(df_loaded) == 3
            # Check unicode characters are preserved
            assert "André" in df_loaded["name"].values
            assert "São Paulo" in df_loaded["city"].values

        finally:
            # Cleanup
            if csv_file.exists():
                csv_file.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()

    def test_csv_with_quoted_fields(self):
        """Test CSV loading with quoted fields containing delimiters."""
        temp_dir = Path(tempfile.mkdtemp(prefix="quoted_test_"))
        csv_file = temp_dir / "quoted_data.csv"

        # Create CSV with quoted fields
        csv_content = '''id,description,price
1,"Product A, high quality",99.99
2,"Product B, ""premium""",149.99
3,"Product C
with newline",199.99'''

        csv_file.write_text(csv_content)

        try:
            delimiter = detect_delimiter(csv_file)
            df = load_csv_data(csv_file, delimiter)

            assert isinstance(df, pd.DataFrame)
            assert len(df) == 3
            assert "Product A, high quality" in df["description"].values
            assert 'Product B, "premium"' in df["description"].values

        finally:
            # Cleanup
            if csv_file.exists():
                csv_file.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()
