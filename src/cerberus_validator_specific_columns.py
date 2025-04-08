import os
import sys
import subprocess
import pandas as pd
from cerberus import Validator
from tqdm import tqdm

def install_missing_packages():
    """Installs missing required packages if not already installed."""
    required_packages = ["pandas", "tqdm", "cerberus"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing missing package: {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def validate_csv_column(data_copy, column_name, save_dir):
    """
    Validates a single column in the given DataFrame against a schema defined interactively.
    Saves results in a separate folder within save_dir.
    """
    # Ensure save directory exists
    validation_dir = os.path.join(save_dir, "validation_results")
    os.makedirs(validation_dir, exist_ok=True)

    # Ensure the column exists
    if column_name not in data_copy.columns:
        print(f"Error: Column '{column_name}' not found in the dataset.")
        return

    # Define schema interactively
    print(f"Defining schema for column: {column_name}")
    schema = {}

    schema['type'] = input("Enter the data type ('string', 'integer', 'float', 'boolean', 'list', 'dict'): ").strip()
    if schema['type'] in ['integer', 'float']:
        min_value = input("Enter the minimum value (leave blank if none): ").strip()
        if min_value:
            schema['min'] = float(min_value) if schema['type'] == 'float' else int(min_value)

        max_value = input("Enter the maximum value (leave blank if none): ").strip()
        if max_value:
            schema['max'] = float(max_value) if schema['type'] == 'float' else int(max_value)

    if schema['type'] == 'string':
        allowed = input("Enter allowed values separated by commas (leave blank if any value is allowed): ").strip()
        if allowed:
            schema['allowed'] = [val.strip() for val in allowed.split(",")]

    is_required = input("Is this field required? ('yes' or 'no'): ").strip().lower()
    schema['required'] = is_required == 'yes'

    if schema['type'] == 'string':
        regex = input("Enter a regex pattern to match (leave blank if none): ").strip()
        if regex:
            schema['regex'] = regex

    # Validator instance
    v = Validator({column_name: schema})

    # Validate rows
    valid_rows = []
    invalid_rows = []
    print("\nValidating rows...")
    for i, value in enumerate(tqdm(data_copy[column_name], desc=f"Validating {column_name}")):
        try:
            if schema['type'] == 'integer':
                value = int(value)
            elif schema['type'] == 'float':
                value = float(value)
        except ValueError:
            invalid_rows.append((i + 1, data_copy[column_name].iloc[i], {'type': f'not a valid {schema["type"]}'}))
            continue

        if v.validate({column_name: value}):
            valid_rows.append(value)
        else:
            invalid_rows.append((i + 1, data_copy[column_name].iloc[i], v.errors))

    # Save results
    results_path = os.path.join(validation_dir, f"{column_name}_validation_results.csv")
    with open(results_path, 'w', encoding='utf-8') as f:
        f.write(f"Validation Report for column: {column_name}\n")
        f.write(f"Total rows: {len(data_copy)}\n")
        f.write(f"Valid rows: {len(valid_rows)}\n")
        f.write(f"Invalid rows: {len(invalid_rows)}\n\n")

        if invalid_rows:
            f.write("Invalid Rows:\n")
            for row_num, value, errors in invalid_rows:
                f.write(f"Row {row_num}: Value '{value}' failed validation. Errors: {errors}\n")

    print(f"Validation results saved to: {results_path}")

def main():
    """Main function to execute CSV validation."""
    install_missing_packages()  # Ensure required packages are installed

    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_csv_file> <delimiter>")
        sys.exit(1)

    # Load CSV file
    csv_path = sys.argv[1]
    delimiter = sys.argv[2]

    try:
        df = pd.read_csv(csv_path, delimiter=delimiter)
        data_copy = df.copy()

        # Ask for the column to validate
        column_name = input("Enter the column name to validate: ").strip()
        save_dir = os.path.dirname(csv_path)  # Save results in the same directory as CSV
        validate_csv_column(data_copy, column_name, save_dir)

    except Exception as e:
        print(f"Error reading the file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
