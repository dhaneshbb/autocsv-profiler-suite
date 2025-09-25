#!/usr/bin/env python3
"""
autocsv-profiler-suite - YData Profiling Report Generator
Licensed under the MIT License. See LICENSE file for details.
"""

import sys
import subprocess
import os
import pandas as pd

# Color and console utilities
class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Additional colors
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

def colored_print(message, color=Colors.WHITE, bold=False):
    """Print colored message"""
    style = Colors.BOLD if bold else ""
    print(f"{style}{color}{message}{Colors.ENDC}")

def log_success(message):
    """Print success message in green"""
    colored_print(f"SUCCESS: {message}", Colors.OKGREEN)


def main():
    """Main function to generate the profiling report."""
    from ydata_profiling import ProfileReport

    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_csv_file> <delimiter>")
        sys.exit(1)

    csv_path = sys.argv[1]
    delimiter = sys.argv[2]

    try:
        # Load the CSV file
        df = pd.read_csv(csv_path, delimiter=delimiter)

        # Generate a profiling report
        profile = ProfileReport(df, title="Profiling Report", explorative=True)

        # Save the report as an HTML file in the same directory as the CSV file
        report_file = os.path.join(os.path.dirname(csv_path), "profiling_report.html")
        profile.to_file(report_file)

        log_success(f"Profiling report saved to: {report_file}")

    except Exception as e:
        print(f"Error processing the file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
