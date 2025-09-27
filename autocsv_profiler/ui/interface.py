"""
Clean CSV Profiler Interface

A simple, effective interface that avoids Rich Live display conflicts
while maintaining clean appearance and functionality.
"""

import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import psutil
import yaml
from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Table


@dataclass
class SystemInfo:
    """System information for status display."""

    app_name: str = "AutoCSV Profiler Suite"
    version: str = "2.0.0"
    python_version: str = ""
    memory_usage: float = 0.0
    cpu_usage: float = 0.0
    active_environment: str = "main"

    def __post_init__(self) -> None:
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


class CleanCSVInterface:
    """
    Clean CSV Profiler Interface

    Simple, effective interface without complex layout conflicts.
    Uses Rich components individually without Live display system.
    """

    def __init__(self, config_path: Optional[Path] = None):
        # Initialize console
        self.console = Console(force_terminal=True, legacy_windows=True)

        # Project setup
        self.project_root = Path(__file__).parent.parent.parent
        self.config_path = (
            config_path or self.project_root / "config" / "master_config.yml"
        )
        self.config = self._load_config()

        # System information (initialized but not populated until needed)
        self.system_info = SystemInfo()

        # UI state
        self.current_step = "initializing"
        self.current_csv_path: Optional[Path] = None
        self.current_delimiter: Optional[str] = None
        self.selected_engines: List[Dict] = []

        # Progress tracking
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console,
            transient=False,
        )

        # Color theme
        self.theme = {
            "primary": "cyan",
            "secondary": "blue",
            "success": "green",
            "warning": "yellow",
            "error": "red",
            "info": "blue",
            "accent": "magenta",
            "muted": "dim white",
        }

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                return config if isinstance(config, dict) else {}
        except Exception as e:
            self.console.print(f"[red]Warning: Could not load config: {e}[/red]")
            return {}

    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            process = psutil.Process(os.getpid())
            memory_bytes = process.memory_info().rss
            return float(memory_bytes / (1024 * 1024))  # Convert to MB
        except Exception:
            return 0.0

    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        try:
            # Use interval=None for immediate reading to avoid delays
            return float(psutil.cpu_percent(interval=None))
        except Exception:
            return 0.0

    def show_welcome(self) -> None:
        """Display welcome message and system information."""

        # Update system info just before display (avoid initialization delays)
        self.system_info.memory_usage = self._get_memory_usage()
        self.system_info.cpu_usage = self._get_cpu_usage()

        version_str = self.config.get("project", {}).get(
            "version", self.system_info.version
        )

        # Simple, clean header that works across all terminals
        app_title = "AutoCSV Profiler Suite"
        version_line = f"Version {version_str}"

        # Create clean header content without complex formatting
        welcome_text = f"[bold {self.theme['primary']}]{app_title}[/bold {self.theme['primary']}]\n"
        welcome_text += (
            f"[{self.theme['accent']}]{version_line}[/{self.theme['accent']}]\n"
        )
        welcome_text += (
            f"\n[{self.theme['muted']}]Multi-Environment CSV Data Analysis "
            f"Orchestrator[/{self.theme['muted']}]"
        )

        welcome_panel = Panel(
            Align.center(welcome_text),
            title="[bold]Welcome[/bold]",
            border_style=self.theme["primary"],
            padding=(1, 2),
            box=box.ROUNDED,
        )
        self.console.print(welcome_panel)
        self.console.print()

    def show_step_header(
        self, step_number: int, step_name: str, description: str
    ) -> None:
        """Display step header."""
        step_panel = Panel(
            f"{description}",
            title=f"[{self.theme['primary']}]Step {step_number}: {step_name}[/{self.theme['primary']}]",
            border_style=self.theme["primary"],
        )
        self.console.print(step_panel)
        self.console.print()

    def show_step_content(self, step_number: int, step_name: str, content: str) -> None:
        """Display step content with Rule header."""
        from rich.rule import Rule

        self.console.print(
            Rule(
                f"[{self.theme['primary']}]Step {step_number}: {step_name}[/{self.theme['primary']}]",
                style=self.theme["primary"],
            )
        )
        self.console.print(content)
        self.console.print()

    def start_step_panel(
        self, step_number: int, step_name: str, description: str
    ) -> None:
        """Start a step panel that will collect content."""
        self.current_step_number = step_number
        self.current_step_name = step_name
        self.current_step_description = description
        self.step_content_lines = [f"{description}\n"]

    def add_step_content(self, content: str) -> None:
        """Add content to the current step panel."""
        if hasattr(self, "step_content_lines"):
            self.step_content_lines.append(content)

    def finish_step_panel(self) -> None:
        """Display the completed step panel with all content."""
        if hasattr(self, "step_content_lines"):
            content = "\n".join(self.step_content_lines)
            step_panel = Panel(
                content,
                title=(
                    f"[{self.theme['primary']}]Step {self.current_step_number}: "
                    f"{self.current_step_name}[/{self.theme['primary']}]"
                ),
                border_style=self.theme["primary"],
            )
            self.console.print(step_panel)
            self.console.print()
            # Clear the content
            del self.step_content_lines

    def show_status_line(self) -> None:
        """Show current status line."""
        # Update system info
        self.system_info.memory_usage = self._get_memory_usage()

        file_name = self.current_csv_path.name if self.current_csv_path else "None"
        engine_count = len(self.selected_engines)
        delimiter_display = (
            repr(self.current_delimiter) if self.current_delimiter else "Not set"
        )

        status_text = (
            f"[{self.theme['info']}]Status:[/{self.theme['info']}] "
            f"[{self.theme['accent']}]{self.current_step.replace('_', ' ').title()}[/{self.theme['accent']}] | "
            f"[{self.theme['success']}]File: {file_name}[/{self.theme['success']}] | "
            f"[{self.theme['warning']}]Delimiter: {delimiter_display}[/{self.theme['warning']}] | "
            f"[{self.theme['secondary']}]Engines: {engine_count}[/{self.theme['secondary']}] | "
            f"[{self.theme['muted']}]Memory: {self.system_info.memory_usage:.1f}MB[/{self.theme['muted']}]"
        )

        status_panel = Panel(status_text, border_style="dim blue", box=box.SIMPLE)
        self.console.print(status_panel)
        self.console.print()

    def show_completion_summary(self, output_dir: Path, results: List[Dict]) -> None:
        """Display analysis completion summary with styled formatting."""
        successful_engines = [r for r in results if r["success"]]
        failed_engines = [r for r in results if not r["success"]]

        # Results summary with consistent styling
        summary_table = Table(
            title="[bold]Analysis Results[/bold]",
            show_header=True,
            header_style=f"bold {self.theme['primary']}",
            box=box.ROUNDED,
            border_style=self.theme["primary"],
        )
        summary_table.add_column("Engine", style=self.theme["secondary"], width=30)
        summary_table.add_column("Status", style="bold", width=12, justify="center")
        summary_table.add_column("Details", style=self.theme["muted"])

        for result in results:
            if result["success"]:
                status_symbol = "[green]+ SUCCESS[/green]"
                details = "Analysis completed successfully"
            else:
                status_symbol = "[red]X FAILED[/red]"
                error_msg = result.get("error", "Unknown error")
                details = error_msg[:60] + "..." if len(error_msg) > 60 else error_msg

            # Clean up engine name for display
            engine_name = result["engine"].replace("engines/", "").replace(".py", "")
            summary_table.add_row(engine_name, status_symbol, details)

        self.console.print(summary_table)
        self.console.print()

        # Create success indicator
        if len(successful_engines) == len(results):
            status_indicator = "[SUCCESS]"
            status_text = "All engines completed successfully!"
            status_color = self.theme["success"]
        elif successful_engines:
            status_indicator = "[PARTIAL]"
            status_text = (
                f"{len(successful_engines)} of {len(results)} engines completed"
            )
            status_color = self.theme["warning"]
        else:
            status_indicator = "[FAILED]"
            status_text = "All engines failed"
            status_color = self.theme["error"]

        # Truncate output directory path for display
        display_path = (
            self._truncate_file_path(str(output_dir))
            if len(str(output_dir)) > 60
            else str(output_dir)
        )

        # Final summary panel with clean formatting
        summary_text = f"""[bold {status_color}]{status_indicator} {status_text}[/bold {status_color}]

[{self.theme['info']}]Results saved to:[/{self.theme['info']}]
[bold]{display_path}[/bold]

[{self.theme['success']}]Successful:[/{self.theme['success']}] {len(successful_engines)} engines"""

        if failed_engines:
            summary_text += f"""
[{self.theme['error']}]Failed:[/{self.theme['error']}] {len(failed_engines)} engines"""

        final_panel = Panel(
            Align.center(summary_text),
            title="[bold]Analysis Complete[/bold]",
            border_style=status_color,
            box=box.ROUNDED,
            padding=(1, 2),
        )

        self.console.print(final_panel)

    def log(self, level: str, message: str, show_timestamp: bool = False) -> None:
        """Log a message with consistent formatting and optional timestamp."""
        level_symbols = {
            "INFO": "*",
            "SUCCESS": "+",
            "WARNING": "!",
            "ERROR": "X",
            "DEBUG": "-",
        }

        level_colors = {
            "INFO": self.theme["info"],
            "SUCCESS": self.theme["success"],
            "WARNING": self.theme["warning"],
            "ERROR": self.theme["error"],
            "DEBUG": self.theme["muted"],
        }

        symbol = level_symbols.get(level, "*")
        color = level_colors.get(level, "white")

        # Truncate very long file paths for readability
        if len(message) > 80 and ("\\" in message or "/" in message):
            message = self._truncate_file_path(message)

        if show_timestamp:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_text = f"[dim]{timestamp}[/dim] [{color}]{symbol}[/{color}] {message}"
        else:
            log_text = f"[{color}]{symbol}[/{color}] {message}"

        self.console.print(log_text)

    def _truncate_file_path(self, message: str) -> str:
        """Truncate long file paths in messages for better readability."""
        import re
        from pathlib import Path

        # Find path-like strings in the message
        path_candidates = []

        # Look for Windows-style paths
        windows_paths = re.findall(r"[A-Za-z]:\\[^\\]+(?:\\[^\\]+)*", message)
        path_candidates.extend(windows_paths)

        # Look for Unix-style paths
        unix_paths = re.findall(r"/[^/\s]+(?:/[^/\s]+)+", message)
        path_candidates.extend(unix_paths)

        # Truncate each path found
        for path_str in path_candidates:
            if len(path_str) > 60:  # Only truncate if significantly long
                try:
                    path = Path(path_str)
                    # Keep first 2 parts, last 2 parts, and show meaningful truncation
                    parts = path.parts
                    if len(parts) > 4:
                        # For Windows: C:\...\parent\filename
                        # For Unix: /home/...parent/filename
                        truncated = str(Path(*parts[:2]) / "..." / Path(*parts[-2:]))
                        message = message.replace(path_str, truncated)
                except Exception:
                    # Fallback: simple string truncation
                    if len(path_str) > 60:
                        truncated = path_str[:30] + "..." + path_str[-25:]
                        message = message.replace(path_str, truncated)

        return message

    def start_progress(self, description: str, total: int | None = None) -> TaskID:
        """Start a progress task."""
        task = self.progress.add_task(description, total=total)
        if not self.progress.live.is_started:
            self.progress.start()
        return task

    def update_progress(self, task_id: TaskID, advance: int = 1) -> None:
        """Update progress for a task."""
        self.progress.update(task_id, advance=advance)

    def finish_progress(self, task_id: TaskID, success: bool = True) -> None:
        """Finish a progress task."""
        self.progress.update(task_id, completed=True)

    def stop_progress(self) -> None:
        """Stop the progress display and clear all tasks."""
        try:
            if hasattr(self.progress, "live") and self.progress.live.is_started:
                self.progress.stop()
            # Clear any remaining tasks - remove all tasks manually
            for task_id in list(self.progress.task_ids):
                self.progress.remove_task(task_id)
            # Force a console refresh to clear any lingering progress artifacts
            self.console.print("", end="")
        except Exception:
            # Silently handle any progress cleanup issues
            pass

    # State management methods
    def set_step(self, step: str) -> None:
        """Set current step."""
        self.current_step = step

    def set_csv_file(self, csv_path: Path) -> None:
        """Set current CSV file."""
        self.current_csv_path = csv_path

    def set_delimiter(self, delimiter: str) -> None:
        """Set current delimiter."""
        self.current_delimiter = delimiter

    def set_selected_engines(self, engines: List[Dict]) -> None:
        """Set selected engines."""
        self.selected_engines = engines
