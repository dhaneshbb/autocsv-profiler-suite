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

def install_missing_packages():
    """Installs required packages if they are not already installed."""
    required_packages = [
        "dataprep",
        "pandas"
    ]

    for package in required_packages:
        package_name = package.split("==")[0] if "==" in package else package
        try:
            __import__(package_name.replace("-", "_"))  # Convert dataprep to dataprep for import check
        except ImportError:
            print(f"Installing missing package: {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    """Main function to generate the dataprep EDA report."""
    install_missing_packages()  # Ensure required packages are installed

    from dataprep.eda import create_report  # Import after ensuring installation

    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_csv_file> <delimiter>")
        sys.exit(1)

    csv_path = sys.argv[1]
    delimiter = sys.argv[2]

    try:
        # Load the CSV file
        df = pd.read_csv(csv_path, delimiter=delimiter)

        # Create and save the report
        report = create_report(df)
        report_file = os.path.join(os.path.dirname(csv_path), "dataprep_report.html")
        report.save(report_file)

        log_success(f"Dataprep report saved to: {report_file}")

    except Exception as e:
        print(f"Error processing the file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
