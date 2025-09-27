import os
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import researchpy as rp

from autocsv_profiler.core.logger import log_print
from autocsv_profiler.types import PathLike


def analyze_data(data: "pd.DataFrame") -> None:
    """Analyze numerical and categorical data using ResearchPy.

    Args:
        data: Pandas DataFrame to analyze
    """
    num_res: List["pd.DataFrame"] = []
    cat_res: List["pd.DataFrame"] = []
    num_cols = data.select_dtypes(
        include=[
            "int64",
            "float64",
            "int8",
            "int16",
            "int32",
            "float16",
            "float32",
        ]
    ).columns
    cat_cols = data.select_dtypes(include=["object", "category"]).columns
    for col in num_cols:
        stats = rp.summary_cont(data[col].dropna())
        stats["Variable"] = col
        num_res.append(stats)
    for col in cat_cols:
        stats = rp.summary_cat(data[col])
        stats["Variable"] = col
        cat_res.append(stats)
    if num_res:
        print("=== Numerical Analysis ===")
        print(pd.concat(num_res, ignore_index=True).to_markdown(tablefmt="pipe"))
    if cat_res:
        print("\n=== Categorical Analysis ===")
        print(pd.concat(cat_res, ignore_index=True).to_markdown(tablefmt="pipe"))


def researchpy_descriptive_stats(
    data_copy: "pd.DataFrame", save_dir: PathLike, delimiter: str = ","
) -> None:
    """
    Analyze numerical and categorical columns in a dataset using ResearchPy.

    Args:
        data_copy: Pandas DataFrame to analyze
        save_dir: Directory to save analysis results
        delimiter: CSV delimiter to use when saving results (default: ',')
    """
    os.makedirs(save_dir, exist_ok=True)

    # Get numerical columns
    numerical_columns = data_copy.select_dtypes(include=["float64", "int64"]).columns

    if len(numerical_columns) > 0:
        numerical_summaries = [
            rp.summary_cont(data_copy[col].dropna()).assign(Variable=col)
            for col in numerical_columns
        ]
        numerical_df = pd.concat(numerical_summaries, ignore_index=True)
    else:
        # Create empty dataframe with expected structure if no numerical columns
        numerical_df = pd.DataFrame(
            columns=[
                "Variable",
                "N",
                "Mean",
                "SD",
                "SE",
                "95% Conf.",
                "Interval",
            ]
        )
    numerical_output_path = os.path.join(save_dir, "numerical_stats.csv")
    numerical_df.to_csv(numerical_output_path, index=False, sep=delimiter)

    # Get categorical columns
    categorical_columns = data_copy.select_dtypes(
        include=["object", "category"]
    ).columns

    if len(categorical_columns) > 0:
        categorical_summaries = [
            rp.summary_cat(data_copy[col]).assign(Variable=col)
            for col in categorical_columns
        ]
        categorical_df = pd.concat(categorical_summaries, ignore_index=True)
    else:
        # Create empty dataframe with expected structure if no categorical columns
        categorical_df = pd.DataFrame(
            columns=["Variable", "Outcome", "Count", "Percent"]
        )
    categorical_output_path = os.path.join(save_dir, "categorical_stats.csv")
    categorical_df.to_csv(categorical_output_path, index=False, sep=delimiter)

    # Analysis completed - files saved


def TableOne_groupby_column(data_copy: "pd.DataFrame", save_dir: PathLike) -> None:
    """
    Analyze numerical and categorical columns in a dataset using TableOne.

    Args:
        data_copy: Pandas DataFrame to analyze
        save_dir: Directory to save analysis results
    """
    import os

    os.makedirs(save_dir, exist_ok=True)

    # Get columns in their actual dataset order
    all_columns: List[str] = data_copy.columns.tolist()
    categorical_columns: List[str] = data_copy.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    continuous_columns: List[str] = data_copy.select_dtypes(
        include=["number"]
    ).columns.tolist()

    def display_columns_indexed(
        all_cols: List[str],
        categorical_cols: List[str],
        continuous_cols: List[str],
    ) -> Dict[int, str]:
        """Display columns in a categorized side-by-side format for easy selection"""
        print("\n" + "=" * 60)
        print("TableOne Analysis - Select variables to group by")
        print("=" * 60)

        categorical_with_idx: List[tuple] = []
        continuous_with_idx: List[tuple] = []

        index_to_column_map: Dict[int, str] = {}

        for i, col in enumerate(all_cols):
            index_to_column_map[i] = col

            if col in categorical_cols:
                categorical_with_idx.append((i, col))
            elif col in continuous_cols:
                continuous_with_idx.append((i, col))

        col_width = 35

        headers = []
        if categorical_with_idx:
            headers.append("CATEGORICAL COLUMNS")
        if continuous_with_idx:
            headers.append("NUMERICAL COLUMNS")

        header_line = " | ".join([f"{header:<{col_width}}" for header in headers])
        print(header_line)
        print("-" * min(len(header_line), 60))

        max_items = max(
            len(categorical_with_idx) if categorical_with_idx else 0,
            len(continuous_with_idx) if continuous_with_idx else 0,
        )

        for i in range(max_items):
            row_items = []

            if categorical_with_idx and i < len(categorical_with_idx):
                idx, col_name = categorical_with_idx[i]
                row_items.append(f"{idx:2}: {col_name:<{col_width-4}}")
            elif categorical_with_idx:
                row_items.append(" " * col_width)

            if continuous_with_idx and i < len(continuous_with_idx):
                idx, col_name = continuous_with_idx[i]
                row_items.append(f"{idx:2}: {col_name:<{col_width-4}}")
            elif continuous_with_idx:
                row_items.append(" " * col_width)

            if row_items:
                print(" | ".join(row_items))
        print("Examples: 0,2,5 (specific columns) | skip/enter (skip analysis)")
        print("=" * 60)

        return index_to_column_map

    index_to_column_map = display_columns_indexed(
        all_columns, categorical_columns, continuous_columns
    )

    selection = (
        input("  >>> Enter column indices (comma-separated) or skip/enter: ")
        .strip()
        .lower()
    )

    groupby_columns = []

    if selection == "" or selection in ["skip", "none"]:
        print("TableOne analysis skipped.")
        return
    else:
        try:
            indices = [int(idx.strip()) for idx in selection.split(",") if idx.strip()]

            for idx in indices:
                if idx in index_to_column_map:
                    groupby_columns.append(index_to_column_map[idx])
                else:
                    print(f"Warning: Index {idx} is not valid. Skipping.")

            if not groupby_columns:
                print("No valid column indices selected. Skipping TableOne analysis.")
                return

        except (ValueError, IndexError):
            log_print(
                "ERROR: Invalid input. Please enter valid column indices. Exiting."
            )
            return

    print("-" * 80)

    try:
        from tableone import TableOne
    except ImportError:
        log_print(
            "ERROR: tableone library not installed. Please install it using: pip install tableone"
        )
        return

    for groupby_column in groupby_columns:
        log_print(f"INFO: Generating report for grouping by: {groupby_column}")

        try:
            table = TableOne(
                data_copy,
                columns=all_columns,
                categorical=categorical_columns,
                groupby=groupby_column,
                pval=True,
                isnull=True,
            )

            csv_output_path = os.path.join(
                save_dir, f"tableone_summary_{groupby_column}.csv"
            )
            table.to_csv(csv_output_path)
            log_print(
                f"SUCCESS: Summary table for grouping by '{groupby_column}' saved successfully"
            )

        except Exception as e:
            log_print(
                f"ERROR: Failed to generate TableOne for column '{groupby_column}': {str(e)}"
            )
            continue

    log_print("SUCCESS: Reports generation completed.")


def calculate_statistics(data: "pd.Series") -> dict:
    """
    Calculates various statistics for a numerical dataset.
    """
    stats = {
        "Count": data.count(),
        "Mean": data.mean(),
        "Std": data.std(),
        "Min": data.min(),
        "25%": data.quantile(0.25),
        "50%": data.median(),
        "75%": data.quantile(0.75),
        "Max": data.max(),
        "Mode": data.mode()[0] if not data.mode().empty else "N/A",
        "Range": data.max() - data.min(),
        "IQR": data.quantile(0.75) - data.quantile(0.25),
        "Variance": data.var(),
        "Skewness": data.skew(),
        "Kurtosis": data.kurt(),
    }
    return stats


def iqr_trimmed_mean(data: "pd.Series") -> float:
    """
    Calculates the trimmed mean using the IQR method.
    """
    q1, q3 = np.percentile(data.dropna(), [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    trimmed_data = data[(data >= lower_bound) & (data <= upper_bound)]
    return float(trimmed_data.mean())


def mad(data: "pd.Series") -> float:
    """
    Calculates the Median Absolute Deviation.
    """
    return float(np.median(np.abs(data - np.median(data))))


def num_var_analysis(
    data: "pd.DataFrame", attribute: str, target: Optional[str] = None
) -> "pd.DataFrame":
    """
    Analyzes a numerical variable and generates summary statistics.
    If a target is provided, computes grouped statistics as well.
    """
    var_summary = calculate_statistics(data[attribute])

    if target:
        grouped_summary = {
            group: calculate_statistics(group_data)
            for group, group_data in data.groupby(target)[attribute]
        }
        summary_table = pd.DataFrame(var_summary, index=["Overall"]).T
        for group, stats in grouped_summary.items():
            group_df = pd.DataFrame(stats, index=[f"{target}: {group}"]).T
            summary_table = summary_table.join(group_df)
    else:
        summary_table = pd.DataFrame(var_summary, index=["Overall"]).T

    summary_table.index.name = "Statistic"
    return summary_table
