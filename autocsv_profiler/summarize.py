from typing import List

import pandas as pd
from scipy import stats

from autocsv_profiler.config import settings
from autocsv_profiler.core.logger import get_logger

# Get module logger
logger = get_logger(__name__)


def num_summary(data: "pd.DataFrame") -> "pd.DataFrame":
    """
    Generate numerical summary statistics for DataFrame columns.

    Args:
        data: Pandas DataFrame to analyze

    Returns:
        DataFrame containing statistical summaries for numerical columns
    """
    num_cols = data.select_dtypes(include="number").columns
    if not num_cols.any():
        logger.info("No numerical columns found for summary")
        print("No numerical columns found.")
        return pd.DataFrame()

    # Get precision from configuration
    precision: int = settings.get("analysis.decimal_precision", 4)
    quantiles: List[float] = settings.get("analysis.quantiles", [0.25, 0.50, 0.75])

    return pd.DataFrame(
        {
            col: {
                "Count": data[col].count(),
                "Unique": data[col].nunique(),
                "Mean": round(data[col].mean(), precision),
                "Std": round(data[col].std(), precision),
                "Min": round(data[col].min(), precision),
                "25%": round(data[col].quantile(quantiles[0]), precision),
                "50%": round(data[col].median(), precision),
                "75%": round(data[col].quantile(quantiles[2]), precision),
                "Max": round(data[col].max(), precision),
                "Mode": (data[col].mode()[0] if not data[col].mode().empty else "N/A"),
                "Range": round(data[col].max() - data[col].min(), precision),
                "IQR": round(
                    data[col].quantile(quantiles[2]) - data[col].quantile(quantiles[0]),
                    precision,
                ),
                "Variance": round(data[col].var(), precision),
                "Skewness": round(data[col].skew(), precision),
                "Kurtosis": round(data[col].kurt(), precision),
                "Shapiro-Wilk Stat": round(stats.shapiro(data[col])[0], precision),
                "Shapiro-Wilk p-value": round(stats.shapiro(data[col])[1], precision),
            }
            for col in num_cols
        }
    ).T


def cat_summary(data: "pd.DataFrame") -> "pd.DataFrame":
    """
    Generate categorical summary statistics for DataFrame columns.

    Args:
        data: Pandas DataFrame to analyze

    Returns:
        DataFrame containing statistical summaries for categorical columns
    """
    cat_cols = data.select_dtypes(include=["object", "category"]).columns
    if not cat_cols.any():
        # Log to file only - no console output
        logger.info("No categorical columns found for summary")
        return pd.DataFrame()
    return pd.DataFrame(
        {
            col: {
                "Count": data[col].count(),
                "Unique": data[col].nunique(),
                "Top": (data[col].mode()[0] if not data[col].mode().empty else "N/A"),
                "Freq": (
                    data[col].value_counts().iloc[0]
                    if not data[col].value_counts().empty
                    else "N/A"
                ),
                "Top %": f"{(data[col].value_counts().iloc[0] / data[col].count()) * 100:.2f}%",
            }
            for col in cat_cols
        }
    ).T
