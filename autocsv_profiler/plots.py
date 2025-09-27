import os
import pickle
import sys
import tempfile
from multiprocessing import Pool, cpu_count
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import pandas as pd

import matplotlib
import matplotlib.cm
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats
from tabulate import tabulate

from .core.utils import cat_high_cardinality


def execute_visualization_worker(args: tuple) -> tuple[bool, str, str]:
    """Worker function for parallel visualization execution.

    Args:
        args: Tuple containing (viz_info, data_temp_file, save_dir, target)

    Returns:
        Tuple containing (success, viz_name, error_message)
    """
    viz_info, data_temp_file, save_dir, target = args

    try:
        with open(data_temp_file, "rb") as f:
            data_copy = pickle.load(f)

        matplotlib.use("Agg")

        viz_info["function"](data_copy, save_dir)

        return True, str(viz_info["name"]), ""

    except Exception as e:
        return False, str(viz_info["name"]), str(e)


def plot_num_kde_subplot(
    data_copy: "pd.DataFrame",
    save_dir: str,
    layout_title: str = "KDE Plots of Numerical Variables",
) -> None:
    """Generate and save KDE plots for all numerical variables in a dataset in batches of 12 subplots."""
    plots_dir = os.path.join(save_dir, "kde_plots")
    os.makedirs(plots_dir, exist_ok=True)

    numerical_cols = data_copy.select_dtypes(include=[np.number]).columns.tolist()

    if not numerical_cols:
        return

    max_subplots_per_figure = 12

    for i in range(0, len(numerical_cols), max_subplots_per_figure):
        batch_cols = numerical_cols[i : i + max_subplots_per_figure]
        rows = (len(batch_cols) + 2) // 3
        cols = min(3, len(batch_cols))

        plt.figure(figsize=(cols * 7, rows * 5))

        for j, col in enumerate(batch_cols):
            plt.subplot(rows, cols, j + 1)
            sns.histplot(
                data_copy[col],
                bins=20,
                kde=True,
                color="skyblue",
                edgecolor="black",
                alpha=0.7,
            )

            stats = {
                "Mean": (data_copy[col].mean(), "darkred"),
                "Median": (data_copy[col].median(), "darkgreen"),
                "Mode": (
                    (
                        data_copy[col].mode()[0]
                        if not data_copy[col].mode().empty
                        else np.nan
                    ),
                    "darkblue",
                ),
                "Min": (data_copy[col].min(), "darkmagenta"),
                "25%": (data_copy[col].quantile(0.25), "darkorange"),
                "75%": (data_copy[col].quantile(0.75), "darkcyan"),
                "Max": (data_copy[col].max(), "darkviolet"),
            }

            for stat, (value, color) in stats.items():
                plt.axvline(
                    value,
                    color=color,
                    linestyle="--",
                    linewidth=2,
                    label=f"{stat}: {value:.2f}",
                )

            plt.title(f"Distribution and KDE of {col}", fontsize=14)
            plt.xlabel(col, fontsize=12)
            plt.ylabel("Density", fontsize=12)
            plt.legend(loc="upper right", fontsize=10, frameon=False)
            plt.grid(False)

        plt.suptitle(
            f"{layout_title} (Batch {i // max_subplots_per_figure + 1})",
            fontsize=16,
            fontweight="bold",
        )
        plt.tight_layout(pad=3.0, rect=(0, 0, 1, 0.95))

        plot_filename = os.path.join(
            plots_dir,
            f"kde_plots_batch_{i // max_subplots_per_figure + 1}.png",
        )
        plt.savefig(plot_filename, dpi=300)
        plt.close()


def plot_num_box_plots_all(
    data_copy: "pd.DataFrame",
    save_dir: str,
    layout_title: str = "Box Plots of Numerical Variables",
) -> None:
    """Generate and save box plots for all numerical variables in a dataset in batches of 12 subplots."""
    plots_dir = os.path.join(save_dir, "box_plots")
    os.makedirs(plots_dir, exist_ok=True)

    numerical_cols = data_copy.select_dtypes(include=[np.number]).columns.tolist()

    if not numerical_cols:
        return

    max_subplots_per_figure = 12

    for i in range(0, len(numerical_cols), max_subplots_per_figure):
        batch_cols = numerical_cols[i : i + max_subplots_per_figure]
        rows = (len(batch_cols) + 2) // 3
        cols = min(3, len(batch_cols))

        plt.figure(figsize=(cols * 7, rows * 5))

        for j, col in enumerate(batch_cols):
            plt.subplot(rows, cols, j + 1)
            sns.boxplot(x=data_copy[col], color="skyblue", fliersize=5, linewidth=2)

            stats = {
                "Mean": (data_copy[col].mean(), "darkred"),
                "Median": (data_copy[col].median(), "darkgreen"),
                "Min": (data_copy[col].min(), "darkblue"),
                "25%": (data_copy[col].quantile(0.25), "darkorange"),
                "75%": (data_copy[col].quantile(0.75), "darkcyan"),
                "Max": (data_copy[col].max(), "darkviolet"),
            }

            for stat, (value, color) in stats.items():
                plt.axvline(
                    value,
                    color=color,
                    linestyle="--",
                    linewidth=2,
                    label=f"{stat}: {value:.2f}",
                )

            plt.title(f"Box Plot of {col}", fontsize=14)
            plt.xlabel(col, fontsize=12)
            plt.legend(loc="upper right", fontsize=10, frameon=False)
            plt.grid(False)

        plt.suptitle(
            f"{layout_title} (Batch {i // max_subplots_per_figure + 1})",
            fontsize=16,
            fontweight="bold",
        )
        plt.tight_layout(pad=3.0, rect=(0, 0, 1, 0.95))

        plot_filename = os.path.join(
            plots_dir,
            f"box_plots_batch_{i // max_subplots_per_figure + 1}.png",
        )
        plt.savefig(plot_filename, dpi=300)
        plt.close()


def plot_num_qq_subplot(
    data_copy: "pd.DataFrame",
    save_dir: str,
    layout_title: str = "QQ Plots of Numerical Variables",
) -> None:
    """Generate and save QQ plots for all numerical variables in a dataset in batches of 12 subplots."""
    plots_dir = os.path.join(save_dir, "qq_plots")
    os.makedirs(plots_dir, exist_ok=True)

    numerical_cols = data_copy.select_dtypes(include=[np.number]).columns.tolist()

    if not numerical_cols:
        return

    max_subplots_per_figure = 12

    for i in range(0, len(numerical_cols), max_subplots_per_figure):
        batch_cols = numerical_cols[i : i + max_subplots_per_figure]
        rows = (len(batch_cols) + 2) // 3
        cols = min(3, len(batch_cols))

        plt.figure(figsize=(cols * 7, rows * 5))

        for j, col in enumerate(batch_cols):
            plt.subplot(rows, cols, j + 1)

            (osm, osr), (slope, intercept, r) = stats.probplot(
                data_copy[col], dist="norm", plot=None
            )
            plt.scatter(osm, osr, s=10, color="blue", alpha=0.6)
            plt.plot(osm, slope * osm + intercept, "r-", linewidth=2)

            plt.title(f"QQ Plot of {col}", fontsize=14)
            plt.xlabel("Theoretical Quantiles", fontsize=12)
            plt.ylabel(f"Quantiles of {col}", fontsize=12)
            plt.grid(False)

        plt.suptitle(
            f"{layout_title} (Batch {i // max_subplots_per_figure + 1})",
            fontsize=16,
            fontweight="bold",
        )
        plt.tight_layout(pad=3.0, rect=(0, 0, 1, 0.95))

        plot_filename = os.path.join(
            plots_dir, f"qq_plots_batch_{i // max_subplots_per_figure + 1}.png"
        )
        plt.savefig(plot_filename, dpi=300)
        plt.close()


def plot_categorical_summary(data: "pd.DataFrame", save_dir: str) -> None:
    """Generate and save a summary of categorical variables, including bar charts.

    High cardinality columns get individual plots, low cardinality get subplots.

    Args:
        data (pd.DataFrame): The input DataFrame.
        save_dir (str): The directory to save the plots to.
    """
    categorical_cols = data.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if not categorical_cols:
        return

    # Identify high cardinality columns
    high_cardinality_cols = cat_high_cardinality(data)

    # Create subplot arrangements for all columns (high and low cardinality)
    if categorical_cols:
        _plot_categorical_bar_charts_subplot(
            data, categorical_cols, high_cardinality_cols, save_dir
        )


def _plot_categorical_bar_charts_subplot(
    data: "pd.DataFrame",
    categorical_cols: list,
    high_cardinality_cols: list,
    save_dir: str,
    layout_title: str = "Bar Charts of Categorical Variables",
) -> None:
    """Generate and save bar charts for categorical variables in batches of 12 subplots.

    High cardinality columns are limited to top N categories.

    Args:
        data (pd.DataFrame): The input DataFrame.
        categorical_cols (list): List of all categorical column names to plot.
        high_cardinality_cols (list): List of high cardinality column names.
        save_dir (str): The directory to save the plots to.
        layout_title (str): Title for the subplot layout.
    """
    plots_dir = os.path.join(save_dir, "bar_charts")
    os.makedirs(plots_dir, exist_ok=True)

    if not categorical_cols:
        return

    max_subplots_per_figure = 12
    for i in range(0, len(categorical_cols), max_subplots_per_figure):
        batch_cols = categorical_cols[i : i + max_subplots_per_figure]

        # Calculate subplot layout (similar to pie charts)
        rows = (len(batch_cols) + 2) // 3
        cols = min(3, len(batch_cols))

        fig, axes = plt.subplots(rows, cols, figsize=(cols * 8, rows * 6))
        axes = axes.flatten()

        for j, col in enumerate(batch_cols):
            # Get value counts for the categorical variable
            counts = data[col].value_counts()

            # Apply different limits based on cardinality
            if col in high_cardinality_cols:
                # For high cardinality, limit to the high cardinality threshold
                from autocsv_profiler.config import settings

                threshold = settings.get("analysis.high_cardinality_threshold", 20)
                if len(counts) > threshold:
                    counts = counts.head(threshold)
                    title_suffix = f" (Top {threshold} of {data[col].nunique()})"
                else:
                    title_suffix = ""
            else:
                # For low cardinality, keep all categories (they're already low)
                title_suffix = ""

            # Create bar chart
            bars = axes[j].bar(
                range(len(counts)),
                counts.values,
                color=matplotlib.colormaps["tab20c"](np.linspace(0, 1, len(counts))),
            )

            # Customize the plot
            axes[j].set_title(
                f"Distribution of {col}{title_suffix}",
                fontsize=12,
                fontweight="bold",
            )
            axes[j].set_xlabel("Categories", fontsize=10)
            axes[j].set_ylabel("Count", fontsize=10)

            # Set category labels with rotation for better readability
            axes[j].set_xticks(range(len(counts)))
            axes[j].set_xticklabels(counts.index, rotation=45, ha="right", fontsize=9)

            # Add value labels on top of bars
            for bar, value in zip(bars, counts.values):
                axes[j].text(
                    bar.get_x() + bar.get_width() / 2.0,
                    bar.get_height() + 0.01 * max(counts.values),
                    f"{value}",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )

        # Remove empty subplots
        for k in range(len(batch_cols), len(axes)):
            fig.delaxes(axes[k])

        # Add main title and adjust layout
        fig.suptitle(
            f"{layout_title} (Batch {i // max_subplots_per_figure + 1})",
            fontsize=16,
            fontweight="bold",
        )
        plt.tight_layout(pad=3.0, rect=(0, 0, 1, 0.95))

        # Save the plot
        plot_filename = os.path.join(
            plots_dir,
            f"bar_charts_batch_{i // max_subplots_per_figure + 1}.png",
        )
        plt.savefig(plot_filename, dpi=300, bbox_inches="tight")
        plt.close()


def _analyze_and_plot_categorical_variable(
    data: "pd.DataFrame",
    attribute: str,
    save_dir: str,
    all_summaries: Optional[list] = None,
) -> None:
    """Analyzes and plots a single categorical variable.

    Args:
        data (pd.DataFrame): The input DataFrame.
        attribute (str): The categorical variable to analyze.
        save_dir (str): The directory to save the plots to.
        all_summaries (list, optional): A list to append the summary to. Defaults to [].
    """
    os.makedirs(save_dir, exist_ok=True)

    counts = data[attribute].value_counts().to_frame()
    counts.columns = ["Count"]
    percentages = (counts["Count"] / counts["Count"].sum() * 100).round(2)
    counts["Percentage"] = percentages

    final_table = counts.reset_index()
    final_table = final_table.rename(columns={"index": attribute.capitalize()})

    if all_summaries is not None:
        all_summaries.append(f"\n### {attribute.capitalize()} Summary ###\n")
        all_summaries.append(final_table.to_markdown(index=False, tablefmt="pipe"))

    plt.figure(figsize=(10, 6))
    sns.countplot(
        data=data, x=attribute, hue=attribute, palette="viridis", legend=False
    )
    plt.title(f"{attribute.capitalize()} Distribution")
    for p in plt.gca().patches:
        # Only process Rectangle patches (bars) which have these attributes
        if hasattr(p, "get_height") and hasattr(p, "get_x") and hasattr(p, "get_width"):
            height = p.get_height()
            if height > 0:
                plt.annotate(
                    f"{int(height)}",
                    (p.get_x() + p.get_width() / 2.0, height),
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    color="black",
                    xytext=(0, 5),
                    textcoords="offset points",
                )
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plot_path1 = os.path.join(
        save_dir, f"high_cardinality_{attribute}_distribution.png"
    )
    plt.savefig(plot_path1, dpi=300)
    plt.close()


def plot_cat_pie_charts_subplot(
    data_copy: "pd.DataFrame",
    save_dir: str,
    layout_title: str = "Pie Charts of Categorical Variables",
) -> None:
    """Generate and save pie charts for categorical variables.

    High cardinality columns get individual plots, low cardinality get subplots.
    """
    categorical_cols = data_copy.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    if not categorical_cols:
        return

    # Identify high cardinality columns
    high_cardinality_cols = cat_high_cardinality(data_copy)

    # Create subplot arrangements for all columns (high and low cardinality)
    if categorical_cols:
        _plot_pie_charts_subplot(
            data_copy,
            categorical_cols,
            high_cardinality_cols,
            save_dir,
            layout_title,
        )


def _plot_pie_charts_subplot(
    data_copy: "pd.DataFrame",
    categorical_cols: list,
    high_cardinality_cols: list,
    save_dir: str,
    layout_title: str = "Pie Charts of Categorical Variables",
) -> None:
    """Generate and save pie charts for categorical variables in batches of 12 subplots.

    High cardinality columns are limited to top N categories.
    """
    plots_dir = os.path.join(save_dir, "pie_charts")
    os.makedirs(plots_dir, exist_ok=True)

    if not categorical_cols:
        return

    max_subplots_per_figure = 12

    for i in range(0, len(categorical_cols), max_subplots_per_figure):
        batch_cols = categorical_cols[i : i + max_subplots_per_figure]
        rows = (len(batch_cols) + 2) // 3
        cols = min(3, len(batch_cols))

        fig, axes = plt.subplots(rows, cols, figsize=(cols * 7, rows * 5))
        axes = axes.flatten()

        for j, col in enumerate(batch_cols):
            series = data_copy[col].value_counts()

            # Apply different limits based on cardinality
            if col in high_cardinality_cols:
                # For high cardinality, limit to the high cardinality threshold
                from autocsv_profiler.config import settings

                threshold = settings.get("analysis.high_cardinality_threshold", 20)
                if len(series) > threshold:
                    series = series.head(threshold)
                    title_suffix = f" (Top {threshold} of {data_copy[col].nunique()})"
                else:
                    title_suffix = ""
            else:
                # For low cardinality, keep all categories (they're already low)
                title_suffix = ""

            sizes = series.values / series.sum() * 100
            colors = matplotlib.colormaps["tab20c"](np.linspace(0, 1, len(series)))
            wedges, _, autotexts = axes[j].pie(
                sizes, autopct="%1.1f%%", startangle=90, colors=colors
            )

            for text in autotexts:
                text.set_color("white")
                text.set_fontsize(12)

            axes[j].set_title(f"Distribution of {col}{title_suffix}", fontsize=14)
            legend_labels = [
                f"{label} ({size:.1f}%)" for label, size in zip(series.index, sizes)
            ]
            axes[j].legend(
                wedges,
                legend_labels,
                title=col,
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1),
            )

        for k in range(len(batch_cols), len(axes)):
            fig.delaxes(axes[k])

        fig.suptitle(
            f"{layout_title} (Batch {i // max_subplots_per_figure + 1})",
            fontsize=16,
            fontweight="bold",
        )
        plt.tight_layout(pad=3.0, rect=(0, 0, 1, 0.95))

        plot_filename = os.path.join(
            plots_dir,
            f"pie_charts_batch_{i // max_subplots_per_figure + 1}.png",
        )
        plt.savefig(plot_filename, dpi=300)
        plt.close()


def select_and_execute_visualizations(data_copy: "pd.DataFrame", save_dir: str) -> None:
    """Display visualization options in indexed format and execute selected ones."""
    visualizations = [
        {
            "name": "KDE Plots (All Numerical)",
            "function": plot_num_kde_subplot,
            "description": "Kernel density estimation plots in batches",
        },
        {
            "name": "Box Plots (All Numerical)",
            "function": plot_num_box_plots_all,
            "description": "Box plots for all numerical variables",
        },
        {
            "name": "QQ Plots (All Numerical)",
            "function": plot_num_qq_subplot,
            "description": "Quantile-Quantile plots in batches",
        },
        {
            "name": "Categorical Summary (Bar charts)",
            "function": plot_categorical_summary,
            "description": "Individual analysis for each categorical variable",
        },
        {
            "name": "Pie Charts (All Categorical)",
            "function": plot_cat_pie_charts_subplot,
            "description": "Pie charts for all categorical variables",
        },
    ]

    def display_visualizations_indexed(viz_list: list) -> None:
        """Display visualizations in a categorized format for easy selection."""
        print("\n" + "=" * 60)
        print("Visualization Selection - Choose analysis plots")
        print("=" * 60)

        table_data = []
        for i, viz in enumerate(viz_list):
            viz["index"] = i
            item_text = f"{viz['index']:2}: {viz['name']}\n    {viz['description']}"
            table_data.append([item_text])

        if table_data:
            print(
                tabulate(
                    table_data,
                    headers=["VISUALIZATIONS"],
                    tablefmt="pipe",
                    stralign="left",
                )
            )
        print(
            "Examples: 0,2,5 (specific) | 0-3 (range) | all (select all) | skip/enter (skip all)"
        )
        print("=" * 60 + "\n")

    display_visualizations_indexed(visualizations)

    selection = (
        input("  >>> Enter visualization indices, ranges, 'all', or skip/enter: ")
        .strip()
        .lower()
    )

    selected_visualizations = []

    if selection == "" or selection in ["skip", "none"]:
        print("Visualization generation skipped.")
        return
    elif selection == "all":
        selected_visualizations = visualizations
    else:
        try:
            indices: list[int] = []
            # Parse different input formats
            for part in selection.split(","):
                part = part.strip()
                if "-" in part and part.replace("-", "").replace(" ", "").isdigit():
                    # Handle range like "0-3"
                    start, end = map(int, part.split("-"))
                    indices.extend(range(start, end + 1))
                elif part.isdigit():
                    # Handle single number
                    indices.append(int(part))

            # Remove duplicates and filter valid indices
            indices = list(
                set([idx for idx in indices if 0 <= idx < len(visualizations)])
            )
            selected_visualizations = [visualizations[idx] for idx in sorted(indices)]

            if not selected_visualizations:
                print("No valid visualizations selected.")
                return

            # Display selected visualizations for confirmation
            print(f"\nSelected {len(selected_visualizations)} visualizations:")
            for idx in sorted(indices):
                print(f"  {idx}: {visualizations[idx]['name']}")
            print()

        except (ValueError, IndexError):
            print(
                "Invalid input format. Please use numbers, ranges, 'all', or skip/enter."
            )
            return

    if selected_visualizations:
        from tqdm import tqdm

        print("\nGenerating visualizations...")

        num_workers = max(1, min(4, int(cpu_count() * 0.75)))

        try:
            print(f"Using {num_workers} parallel workers for faster processing...")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as temp_file:
                pickle.dump(data_copy, temp_file)
                data_temp_file = temp_file.name

            # Prepare arguments for workers
            worker_args = [
                (viz, data_temp_file, save_dir, None) for viz in selected_visualizations
            ]

            with Pool(processes=num_workers) as pool:
                results = []
                with tqdm(
                    total=len(selected_visualizations),
                    desc="Processing Visualizations",
                    unit="plot",
                    leave=True,
                    position=0,
                    dynamic_ncols=True,
                    ascii=True,
                    miniters=1,
                    file=sys.stdout,
                ) as pbar:

                    for result in pool.imap_unordered(
                        execute_visualization_worker, worker_args, chunksize=1
                    ):
                        results.append(result)
                        success, viz_name, error = result
                        if success:
                            pbar.set_description(
                                f"Processing Visualizations - Completed {viz_name}"
                            )
                        else:
                            print(f"\nError generating {viz_name}: {error}")
                            pbar.set_description(
                                f"Processing Visualizations - Error in {viz_name}"
                            )
                        pbar.update(1)

        except Exception as mp_error:
            print(
                f"Multiprocessing failed ({mp_error}), falling back to sequential processing..."
            )
            results = []

            # Sequential processing with progress bar
            with tqdm(
                selected_visualizations,
                desc="Processing Visualizations",
                unit="plot",
                leave=True,
                ascii=True,
                file=sys.stdout,
            ) as pbar:

                for viz in pbar:
                    pbar.set_description(f"Processing {viz['name']}")
                    try:
                        viz["function"](data_copy, save_dir)
                        results.append((True, str(viz["name"]), ""))
                        pbar.set_description(f"Completed {viz['name']}")
                    except Exception as e:
                        results.append((False, str(viz["name"]), str(e)))
                        print(f"\nError generating {viz['name']}: {e}")
                        pbar.set_description(f"Error in {viz['name']}")

        # Clean up temporary file if it was created (only for multiprocessing)
        try:
            if "data_temp_file" in locals():
                os.unlink(data_temp_file)
        except Exception:
            pass
