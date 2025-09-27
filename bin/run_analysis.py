#!/usr/bin/env python3
"""AutoCSV Profiler Suite - Analysis Orchestrator

Cross-platform CSV analysis tool with real-time monitoring.
"""

# Suppress common startup warnings only if not in debug mode
import os
import sys
import warnings
from pathlib import Path

if os.environ.get("DEBUG") != "1":
    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, module="pkg_resources"
    )
    warnings.filterwarnings("ignore", message=".*pkg_resources.*deprecated.*")
    warnings.filterwarnings("ignore", message=".*declare_namespace.*deprecated.*")

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Windows console encoding
if sys.platform == "win32":
    try:
        import codecs

        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        try:
            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
            sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")
        except Exception:
            pass

try:
    from autocsv_profiler.ui.interactive import CleanInteractiveMethods
    from autocsv_profiler.ui.interface import CleanCSVInterface
except ImportError as e:
    print(f"Error: Could not import clean interface: {e}")
    print("Please ensure the project is properly set up.")
    sys.exit(1)


def show_help():
    """Display help information"""
    help_text = """
AutoCSV Profiler Suite - Analysis Orchestrator

USAGE:
    python run_analysis.py [OPTIONS]

OPTIONS:
    --help, -h          Show this help message
    --debug             Enable debug mode with detailed error information

EXAMPLES:
    python run_analysis.py                    # Clean interface
    python run_analysis.py --debug            # Debug mode with detailed logs

ENVIRONMENTS:
    The launcher automatically manages three conda environments:
    - csv-profiler-main:      Core analysis and statistics
    - csv-profiler-profiling: YData Profiling and SweetViz
    - csv-profiler-dataprep:  DataPrep EDA analysis

For more information, visit: https://github.com/dhaneshbb/autocsv-profiler-suite
    """
    print(help_text)


def main():
    """Main entry point for the unified launcher"""

    import argparse

    parser = argparse.ArgumentParser(
        description="AutoCSV Profiler Suite - Clean Interface", add_help=False
    )
    parser.add_argument("csv_file", nargs="?", help="Path to the CSV file to analyze")
    parser.add_argument("--help", "-h", action="store_true", help="Show help message")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args, unknown = parser.parse_known_args()

    if args.help:
        show_help()
        return

    if args.debug:
        os.environ["DEBUG"] = "1"

    try:
        # Initialize clean interface (without layout conflicts)
        clean_interface = CleanCSVInterface()
        interactive_methods = CleanInteractiveMethods(clean_interface)

        if args.debug:
            print("[DEBUG] Debug mode enabled")
            print("[DEBUG] All engines will show debug messages in console")

        if args.csv_file:
            if not os.path.exists(args.csv_file):
                print(f"Error: CSV file not found: {args.csv_file}")
                sys.exit(1)

            print(f"Starting analysis of: {args.csv_file}")
            success = interactive_methods.run_analysis_direct(args.csv_file)
        else:
            success = interactive_methods.run_analysis()

        if not success:
            print("\nAnalysis failed or was cancelled")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n[INFO] Operation cancelled by user")
    except Exception as e:
        print(f"\n[FATAL ERROR] Launcher failed: {e}")

        # Debug information
        if args.debug or os.getenv("DEBUG"):
            import traceback

            traceback.print_exc()
        else:
            print("Run with --debug flag for detailed error information")

        sys.exit(1)


if __name__ == "__main__":
    main()
