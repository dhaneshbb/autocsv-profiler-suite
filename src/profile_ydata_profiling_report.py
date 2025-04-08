import sys
import subprocess
import os
import pandas as pd

def install_missing_packages():
    """Installs required packages if they are not already installed."""
    required_packages = [
        "ydata-profiling",
        "pandas>=1.4"
    ]

    for package in required_packages:
        package_name = package.split("==")[0] if "==" in package else package
        try:
            __import__(package_name.replace("-", "_"))  # Convert ydata-profiling to ydata_profiling for import check
        except ImportError:
            print(f"Installing missing package: {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    """Main function to generate the profiling report."""
    install_missing_packages()  # Ensure required packages are installed

    from ydata_profiling import ProfileReport  # Import after ensuring installation

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

        print(f"Profiling report saved to: {report_file}")

    except Exception as e:
        print(f"Error processing the file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
