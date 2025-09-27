#!/usr/bin/env python3
"""AutoCSV Profiler Suite - Environment Setup Tool with Safe Parallel Processing"""

import concurrent.futures
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Dict, List

import yaml
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def run_cmd(cmd, capture_output=False, show_output=False):
    """Run command and return success"""
    try:
        if show_output:
            # Show real-time output without capturing
            result = subprocess.run(cmd, check=True)
            return True, "", ""
        elif capture_output:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return True, result.stdout, result.stderr
        else:
            subprocess.run(cmd, check=True, capture_output=True)
            return True, "", ""
    except subprocess.CalledProcessError as e:
        return False, "", str(e)


def run_cmd_with_output(cmd):
    """Run command and return detailed output"""
    return run_cmd(cmd, capture_output=True)


def run_cmd_with_live_output(cmd):
    """Run command and show live output"""
    return run_cmd(cmd, show_output=True)


def create_env(name: str, quiet: bool = False) -> Dict[str, any]:
    """Create conda environment - thread-safe version"""
    result = {"name": name, "success": False, "message": "", "start_time": time.time()}

    try:
        if env_exists(name):
            result["message"] = f"Environment '{name}' already exists"
            result["success"] = True
            return result

        # Generate environment files if they don't exist
        yaml_file = (
            Path(__file__).parent.parent
            / "config"
            / f"environment_{name.replace('csv-profiler-', '')}.yml"
        )
        if not yaml_file.exists():
            console.print(
                "[yellow]Environment file not found, generating from master config...[/yellow]"
            )
            generate_environment_files()

        if not yaml_file.exists():
            result["message"] = (
                f"Config file not found and could not be generated: {yaml_file}"
            )
            return result

        console.print(
            f"[blue][{threading.current_thread().name}][/blue] Creating environment [bold cyan]'{name}'[/bold cyan]..."
        )

        cmd = [
            "conda",
            "env",
            "create",
            "-f",
            str(yaml_file),
            "-y",
            "--no-default-packages",
        ]

        if quiet:
            cmd.append("--quiet")
            success, stdout, stderr = run_cmd_with_output(cmd)
        else:
            # Show live output for sequential processing
            success, stdout, stderr = run_cmd_with_live_output(cmd)

        if success:
            result["success"] = True
            result["message"] = f"Environment '{name}' created successfully"
            console.print(
                f"[blue][{threading.current_thread().name}][/blue] [green]SUCCESS:[/green] Environment [bold cyan]'{name}'[/bold cyan] created"
            )
        else:
            result["message"] = f"Failed to create environment '{name}': {stderr}"
            console.print(
                f"[blue][{threading.current_thread().name}][/blue] [red]ERROR:[/red] Failed to create [bold cyan]'{name}'[/bold cyan]: {stderr}"
            )

    except Exception as e:
        result["message"] = f"Exception creating '{name}': {str(e)}"
        console.print(
            f"[blue][{threading.current_thread().name}][/blue] [red]ERROR:[/red] Exception creating [bold cyan]'{name}'[/bold cyan]: {e}"
        )

    result["duration"] = time.time() - result["start_time"]
    return result


def remove_env(name: str, quiet: bool = False) -> Dict[str, any]:
    """Remove conda environment - thread-safe version"""
    result = {"name": name, "success": False, "message": "", "start_time": time.time()}

    try:
        if not env_exists(name):
            result["message"] = f"Environment '{name}' does not exist"
            result["success"] = True
            return result

        console.print(
            f"[blue][{threading.current_thread().name}][/blue] Removing environment [bold red]'{name}'[/bold red]..."
        )

        cmd = ["conda", "env", "remove", "-n", name, "-y"]
        if quiet:
            cmd.append("--quiet")
            success, stdout, stderr = run_cmd_with_output(cmd)
        else:
            # Show live output for sequential processing
            success, stdout, stderr = run_cmd_with_live_output(cmd)

        if success:
            result["success"] = True
            result["message"] = f"Environment '{name}' removed successfully"
            console.print(
                f"[blue][{threading.current_thread().name}][/blue] [green]SUCCESS:[/green] Environment [bold red]'{name}'[/bold red] removed"
            )
        else:
            result["message"] = f"Failed to remove environment '{name}': {stderr}"
            console.print(
                f"[blue][{threading.current_thread().name}][/blue] [red]ERROR:[/red] Failed to remove [bold red]'{name}'[/bold red]: {stderr}"
            )

    except Exception as e:
        result["message"] = f"Exception removing '{name}': {str(e)}"
        console.print(
            f"[blue][{threading.current_thread().name}][/blue] [red]ERROR:[/red] Exception removing [bold red]'{name}'[/bold red]: {e}"
        )

    result["duration"] = time.time() - result["start_time"]
    return result


def env_exists(name):
    """Check if environment exists"""
    try:
        result = subprocess.run(
            ["conda", "env", "list"], capture_output=True, text=True, check=True
        )
        return name in result.stdout
    except subprocess.CalledProcessError:
        return False


def generate_environment_files():
    """Generate individual environment YAML files from master config"""
    master_config_path = Path(__file__).parent.parent / "config" / "master_config.yml"
    config_dir = Path(__file__).parent.parent / "config"

    try:
        with open(master_config_path) as f:
            master_config = yaml.safe_load(f)

        environments = master_config.get("environments", {})
        generated_files = []

        for env_key, env_config in environments.items():
            # Create conda environment YAML structure
            conda_env = {
                "name": env_config["name"],
                "channels": ["conda-forge"],
                "dependencies": [],
            }

            # Add conda packages
            if "conda_packages" in env_config:
                conda_env["dependencies"].extend(env_config["conda_packages"])

            # Pip packages are no longer supported - using conda only

            # Add environment variables if they exist
            if "environment_variables" in env_config:
                conda_env["variables"] = env_config["environment_variables"]

            # Write environment file with preserved comments
            env_file_path = config_dir / f"environment_{env_key}.yml"
            with open(env_file_path, "w") as f:
                # Write header comment
                f.write(
                    f"# AutoCSV Profiler Suite - {env_config['name']} Environment\n"
                )
                f.write(f"# {env_config['description']}\n")
                f.write(f"# Python {env_config['python_version']}\n")
                f.write("#\n")
                f.write("# Generated from config/master_config.yml\n")
                f.write(
                    "# Do not edit manually - regenerate using setup_environments.py\n\n"
                )

                # Write YAML content
                yaml.dump(conda_env, f, default_flow_style=False, sort_keys=False)

            generated_files.append(env_file_path)
            console.print(f"[green]Generated:[/green] {env_file_path}")

        return generated_files

    except Exception as e:
        console.print(f"[red]ERROR:[/red] Failed to generate environment files: {e}")
        return []


def get_env_names():
    """Get environment names from master config"""
    config_path = Path(__file__).parent.parent / "config" / "master_config.yml"
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return [env["name"] for env in config["environments"].values()]
    except Exception as e:
        console.print(f"[red]ERROR:[/red] Failed to load config: {e}")
        return []


def process_environments_parallel(
    env_names: List[str], action: str, max_workers: int = 3, quiet: bool = True
) -> List[Dict[str, any]]:
    """Process environments in parallel with safe concurrency control"""
    results = []

    console.print(
        Panel(
            f"Processing [bold]{len(env_names)}[/bold] environments in parallel (max [bold]{max_workers}[/bold] workers)\n"
            f"Environments: [cyan]{', '.join(env_names)}[/cyan]",
            title="[bold blue]Parallel Processing[/bold blue]",
            border_style="blue",
        )
    )

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers, thread_name_prefix=f"{action}"
    ) as executor:
        # Submit all tasks
        future_to_env = {}
        for env_name in env_names:
            if action == "create":
                future = executor.submit(create_env, env_name, quiet)
            else:  # remove
                future = executor.submit(remove_env, env_name, quiet)
            future_to_env[future] = env_name

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_env):
            env_name = future_to_env[future]
            try:
                result = future.result()
                results.append(result)
                duration = result.get("duration", 0)
                console.print(
                    f"[green]Completed[/green] {action} for [cyan]'{env_name}'[/cyan] in [yellow]{duration:.1f}s[/yellow]"
                )
            except Exception as e:
                error_result = {
                    "name": env_name,
                    "success": False,
                    "message": f"Exception in parallel processing: {str(e)}",
                    "duration": 0,
                }
                results.append(error_result)
                console.print(
                    f"[red]ERROR:[/red] Exception processing [cyan]'{env_name}'[/cyan]: {e}"
                )

    return results


def process_environments_sequential(
    env_names: List[str], action: str, quiet: bool = False
) -> List[Dict[str, any]]:
    """Process environments sequentially for safer operation"""
    results = []

    console.print(
        Panel(
            f"Processing [bold]{len(env_names)}[/bold] environments sequentially\n"
            f"Environments: [cyan]{', '.join(env_names)}[/cyan]",
            title="[bold green]Sequential Processing[/bold green]",
            border_style="green",
        )
    )

    for env_name in env_names:
        console.print(
            f"[bold]Processing {action}[/bold] for [cyan]'{env_name}'[/cyan]..."
        )
        if action == "create":
            result = create_env(env_name, quiet)
        else:  # remove
            result = remove_env(env_name, quiet)
        results.append(result)
        duration = result.get("duration", 0)
        console.print(
            f"[green]Completed[/green] {action} for [cyan]'{env_name}'[/cyan] in [yellow]{duration:.1f}s[/yellow]"
        )

    return results


def print_summary(results: List[Dict[str, any]], action: str):
    """Print operation summary with rich formatting"""
    total = len(results)
    successful = sum(1 for r in results if r["success"])
    failed = total - successful
    total_time = sum(r.get("duration", 0) for r in results)

    # Create summary table
    table = Table(title=f"{action.upper()} SUMMARY", box=box.ROUNDED)
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")

    table.add_row("Total environments", str(total))
    table.add_row("Successful", f"[green]{successful}[/green]")
    table.add_row("Failed", f"[red]{failed}[/red]" if failed > 0 else "0")
    table.add_row("Total time", f"[yellow]{total_time:.1f}s[/yellow]")

    console.print(table)

    if failed > 0:
        console.print("\n[red]FAILED ENVIRONMENTS:[/red]")
        for result in results:
            if not result["success"]:
                console.print(
                    f"  [red]FAILED[/red] [cyan]{result['name']}[/cyan]: {result['message']}"
                )

    console.print("\n[green]SUCCESSFUL ENVIRONMENTS:[/green]")
    for result in results:
        if result["success"]:
            duration = result.get("duration", 0)
            console.print(
                f"  [green]SUCCESS[/green] [cyan]{result['name']}[/cyan]: {result['message']} [yellow]({duration:.1f}s)[/yellow]"
            )


def print_help():
    """Print help message"""
    print("AutoCSV Profiler Suite - Environment Setup Tool")
    print("Usage: python setup_environments.py <action> [options]")
    print("")
    print("Actions:")
    print("  generate              - Generate environment YAML files from master config")
    print("  create [env_name]     - Create environment(s)")
    print("  remove [env_name]     - Remove environment(s)")
    print("  recreate [env_name]   - Remove and create environment(s)")
    print("")
    print("Options:")
    print("  --help, -h            - Show this help message")
    print("  --parallel            - Use parallel processing (default: sequential)")
    print("  --workers N           - Max parallel workers (default: 3)")
    print("")
    print("Examples:")
    print("  python setup_environments.py --help")
    print("  python setup_environments.py create --parallel")
    print("  python setup_environments.py remove csv-profiler-main")
    print("  python setup_environments.py recreate --parallel --workers 2")
    print("")
    print("Environment Management:")
    print("  This tool manages isolated conda environments to resolve dependency")
    print("  conflicts between profiling engines. Each environment contains specific")
    print("  package versions optimized for different analysis capabilities.")


def main():
    """Main entry point with parallel processing support"""
    # Check for help flag first
    if len(sys.argv) == 1 or "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        sys.exit(0)

    # Parse arguments
    args = sys.argv[1:]
    action = args[0] if args else None

    if not action:
        print("ERROR: Action required")
        print("")
        print_help()
        sys.exit(1)

    # Check conda availability
    try:
        subprocess.run(["conda", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: Conda not found. Install Anaconda/Miniconda first.")
        sys.exit(1)

    parallel = "--parallel" in args

    # Get max workers
    max_workers = 3
    if "--workers" in args:
        try:
            worker_idx = args.index("--workers")
            max_workers = int(args[worker_idx + 1])
        except (IndexError, ValueError):
            print("ERROR: --workers requires a valid number")
            sys.exit(1)

    # Get environment name if specified
    env_name = None
    for arg in args[1:]:
        if not arg.startswith("--") and arg != str(max_workers):
            env_name = arg
            break

    # Handle generate action separately
    if action == "generate":
        print("Generating environment YAML files from master config...")
        generated_files = generate_environment_files()
        if generated_files:
            print(f"\nSuccessfully generated {len(generated_files)} environment files:")
            for file_path in generated_files:
                print(f"  - {file_path}")
        else:
            print("Failed to generate environment files.")
            sys.exit(1)
        sys.exit(0)

    if action not in ["create", "remove", "recreate"]:
        print("ERROR: Action must be 'generate', 'create', 'remove', or 'recreate'")
        sys.exit(1)

    # Determine environment names
    if env_name:
        env_names = [env_name]
    else:
        env_names = get_env_names()
        if not env_names:
            sys.exit(1)

    print(f"Environment Setup Tool - {action.upper()} mode")
    print(f"Processing mode: {'PARALLEL' if parallel else 'SEQUENTIAL'}")
    if parallel:
        print(f"Max workers: {max_workers}")
    print("")

    # Execute action
    start_time = time.time()

    if action == "recreate":
        # First remove, then create
        print("=== REMOVE PHASE ===")
        if parallel:
            remove_results = process_environments_parallel(
                env_names, "remove", max_workers, quiet=True
            )
        else:
            remove_results = process_environments_sequential(
                env_names, "remove", quiet=False
            )

        print_summary(remove_results, "remove")

        # Only create environments that were successfully removed or didn't exist
        envs_to_create = [r["name"] for r in remove_results if r["success"]]

        if envs_to_create:
            print("=== CREATE PHASE ===")
            if parallel:
                create_results = process_environments_parallel(
                    envs_to_create, "create", max_workers, quiet=True
                )
            else:
                create_results = process_environments_sequential(
                    envs_to_create, "create", quiet=False
                )

            print_summary(create_results, "create")
            results = remove_results + create_results
        else:
            results = remove_results
    else:
        # Single action
        if parallel:
            results = process_environments_parallel(
                env_names, action, max_workers, quiet=True
            )
        else:
            results = process_environments_sequential(env_names, action, quiet=False)

        print_summary(results, action)

    # Final summary
    total_time = time.time() - start_time
    successful = sum(1 for r in results if r["success"])
    total = len(env_names)

    print("=== FINAL SUMMARY ===")
    print(f"Operation: {action}")
    print(f"Total environments: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Total execution time: {total_time:.1f}s")

    sys.exit(0 if successful == total else 1)


if __name__ == "__main__":
    main()
