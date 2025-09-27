# ui

User interface components and interactive methods for the AutoCSV Profiler Suite.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Core Classes](#core-classes)
- [Configuration Integration](#configuration-integration)
- [User Interaction Patterns](#user-interaction-patterns)
- [Visual Components](#visual-components)
- [Error Handling and Logging](#error-handling-and-logging)
- [Terminal Compatibility](#terminal-compatibility)
- [Integration Examples](#integration-examples)
- [Performance Considerations](#performance-considerations)
- [Troubleshooting](#troubleshooting)
- [See Also](#see-also)

## Overview

The `ui` package provides Rich-based console interface system for interactive CSV analysis workflows. It implements multi-step process with progress tracking, error handling, and graceful degradation for terminal environments.

## Architecture

### Interface Design

The UI system uses component-based architecture:

```
ui/
├── interface.py      # Main interface class (CleanCSVInterface)
├── interactive.py    # Interactive workflow methods (CleanInteractiveMethods)
└── components.py     # Rich-styled UI components (RichInteractiveComponents)
```

### Design Principles

- **Console Design**: No complex layouts or live displays that cause conflicts
- **Progressive Enhancement**: Works in basic terminals, adds Rich when available
- **Graceful Degradation**: Falls back to plain text when Rich components fail
- **Step Workflow**: Progression through analysis tasks
- **Visual Theme**: Unified color scheme and styling across components

## Core Classes

### CleanCSVInterface (`interface.py`)

Main interface class providing UI framework.

```python
from autocsv_profiler.ui import CleanCSVInterface

# Initialize with default configuration
ui = CleanCSVInterface()

# Initialize with custom config path
ui = CleanCSVInterface(config_path=Path("custom/config.yml"))
```

**Features:**
- Rich console initialization with Windows legacy support
- Configuration loading from YAML files
- System information tracking (memory, CPU, Python version)
- Progress tracking with customizable progress bars
- Unified color theme management
- Step-based workflow state tracking

**Key Attributes:**
- `console`: Rich Console instance for output
- `config`: Loaded configuration dictionary
- `system_info`: SystemInfo dataclass with system details
- `theme`: Color theme dictionary for consistent styling
- `progress`: Rich Progress instance for task tracking

### CleanInteractiveMethods (`interactive.py`)

Interactive workflow methods for analysis process.

```python
from autocsv_profiler.ui import CleanCSVInterface, CleanInteractiveMethods

ui = CleanCSVInterface()
interactive = CleanInteractiveMethods(ui)

# Run complete workflow
csv_path = interactive.get_csv_path()
delimiter = interactive.detect_delimiter(csv_path)
engines = interactive.select_engines()
```

**Workflow Steps:**

#### Step 1: Welcome Banner
```python
interactive.display_welcome_banner()
```
- Displays application information
- Shows system status
- Workflow overview

#### Step 2: File Selection
```python
csv_path = interactive.get_csv_path()
```
- File path input with validation
- Existence checking
- Extension validation with override option
- Retry for invalid paths

#### Step 3: Delimiter Detection
```python
delimiter = interactive.detect_delimiter(csv_path)
```
- Delimiter detection
- Confidence reporting (0.0 to 1.0)
- Manual override option
- Supported delimiters: `,`, `;`, `\t`, `|`, `:`, space

#### Step 4: Engine Selection
```python
engines = interactive.select_engines()
```
- Engine listing with descriptions
- Multi-engine selection
- Environment availability check
- Engine feature descriptions

#### Step 5: Analysis Execution
```python
results = interactive.run_analysis(csv_path, delimiter, engines)
```
- Progress tracking for each engine
- Status updates
- Error handling with continuation
- Memory usage monitoring

### RichInteractiveComponents (`components.py`)

UI components for analysis tasks.

```python
from autocsv_profiler.ui.components import RichInteractiveComponents

components = RichInteractiveComponents()

# Rich-styled column exclusion
modified_data = components.exclude_columns_rich(data, save_dir)

# Rich-styled TableOne analysis
components.tableone_groupby_rich(data, save_dir)

# Rich-styled visualization selection
components.visualizations_rich(data, save_dir)
```

**Components:**
- **Column Exclusion Interface**: Interactive column selection with tables
- **TableOne Analysis**: Medical/research data grouping with output
- **Visualization Selection**: Chart type selection with descriptions

## Configuration Integration

### System Information Tracking

```python
from autocsv_profiler.ui.interface import SystemInfo

# Automatic system information collection
system_info = SystemInfo()
print(f"Python: {system_info.python_version}")
print(f"Memory: {system_info.memory_usage:.1f} MB")
print(f"Environment: {system_info.active_environment}")
```

**Information:**
- Application name and version
- Python version (automatic detection)
- Memory usage (via psutil when available)
- CPU usage (via psutil when available)
- Conda environment

### Theme Configuration

```python
# Access theme colors
ui = CleanCSVInterface()
theme = ui.theme

# Usage in components
ui.console.print(f"[{theme['success']}]Success message[/]")
ui.console.print(f"[{theme['error']}]Error message[/]")
ui.console.print(f"[{theme['warning']}]Warning message[/]")
```

**Colors:**
- `primary`: "cyan" - Main interface elements
- `secondary`: "blue" - Secondary elements
- `success`: "green" - Success messages
- `warning`: "yellow" - Warning messages
- `error`: "red" - Error messages
- `info`: "blue" - Information messages
- `accent`: "magenta" - Accent elements
- `muted`: "dim white" - Secondary text

## User Interaction Patterns

### File Input with Validation

```python
def get_csv_path(self) -> Optional[Path]:
    while True:
        csv_path_str = Prompt.ask("Enter CSV file path")
        csv_path = Path(csv_path_str.strip().strip("\"'"))

        if not csv_path.exists():
            self.ui.log("ERROR", f"File not found: {csv_path}")
            if not Confirm.ask("Try again?"):
                return None
            continue

        if not csv_path.suffix.lower() == ".csv":
            if not Confirm.ask("Not a .csv file. Continue anyway?"):
                continue

        return csv_path
```

### Engine Selection Interface

```python
def select_engines(self) -> List[Dict]:
    # Display available engines in formatted table
    table = Table(title="Available Analysis Engines")
    table.add_column("ID")
    table.add_column("Engine")
    table.add_column("Environment")
    table.add_column("Description")

    for i, engine in enumerate(available_engines):
        table.add_row(
            str(i+1),
            engine["name"],
            engine["environment"],
            engine["description"]
        )

    # Get user selection
    selection = Prompt.ask(
        "Select engines (comma-separated IDs, 'all', or Enter for all)"
    )

    return parse_engine_selection(selection, available_engines)
```

### Progress Tracking

```python
def run_analysis(self, csv_path, delimiter, engines):
    with self.ui.progress:
        for engine in engines:
            task = self.ui.progress.add_task(
                f"Running {engine['name']}...",
                total=100
            )

            result = self._run_engine(engine, csv_path, delimiter)
            self.ui.progress.update(task, completed=100)

            if result:
                self.ui.log("SUCCESS", f"{engine['name']} completed")
            else:
                self.ui.log("ERROR", f"{engine['name']} failed")
```

## Visual Components

### Step Headers

```python
def _show_workflow_step(self, step_number: int, step_name: str, description: str):
    step_header = Text.assemble(
        (f"Step {step_number}: ", f"bold {self.ui.theme['primary']}"),
        (f"{step_name}", f"bold {self.ui.theme['primary']}"),
        (f"\n{description}", f"{self.ui.theme['muted']}"),
    )

    step_panel = Panel(
        step_header,
        border_style=self.ui.theme["primary"],
        box=box.ROUNDED,
        padding=(0, 1),
    )

    self.ui.console.print(step_panel)
```

### Data Tables

```python
def display_engine_table(self, engines):
    table = Table(
        title="Available Analysis Engines",
        box=box.ROUNDED,
        border_style=self.theme["primary"]
    )

    table.add_column("ID", justify="center", style=self.theme["accent"])
    table.add_column("Engine", style=self.theme["primary"])
    table.add_column("Environment", justify="center", style=self.theme["secondary"])
    table.add_column("Description", style=self.theme["muted"])

    for i, engine in enumerate(engines):
        status_style = self.theme["success"] if engine["available"] else self.theme["error"]
        table.add_row(
            str(i + 1),
            engine["name"],
            f"[{status_style}]{engine['environment']}[/]",
            engine["description"]
        )

    self.console.print(table)
```

### Progress Indicators

```python
# Initialize progress tracking
progress = Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    console=self.console,
    transient=False,
)

# Usage in analysis workflow
with progress:
    task_id = progress.add_task("Loading data...", total=100)

    for chunk_num, chunk in enumerate(data_chunks):
        process_chunk(chunk)
        progress.update(task_id, advance=10)
```

## Error Handling and Logging

### Consistent Error Display

```python
def log(self, level: str, message: str):
    level_styles = {
        "ERROR": self.theme["error"],
        "WARNING": self.theme["warning"],
        "SUCCESS": self.theme["success"],
        "INFO": self.theme["info"]
    }

    style = level_styles.get(level, self.theme["info"])
    self.console.print(f"[{style}]{level}:[/] {message}")
```

### Graceful Degradation

```python
def safe_rich_print(console, content, fallback_text):
    """Print Rich content with fallback to plain text."""
    try:
        console.print(content)
    except Exception:
        # Fallback to plain text if Rich rendering fails
        print(fallback_text)

# Usage
safe_rich_print(
    self.console,
    Panel("Rich panel content", border_style="cyan"),
    "Plain text fallback"
)
```

## Terminal Compatibility

### Windows Support

```python
# Console initialization with Windows compatibility
self.console = Console(force_terminal=True, legacy_windows=True)
```

**Features:**
- Windows legacy terminal support
- UTF-8 encoding handling
- Color fallbacks for older terminals

### Terminal Detection

```python
def is_rich_compatible():
    """Check if terminal supports Rich features."""
    try:
        console = Console()
        return console.is_terminal and console.color_system
    except Exception:
        return False

# Conditional Rich usage
if is_rich_compatible():
    display_rich_interface()
else:
    display_plain_interface()
```

## Integration Examples

### Main Application Integration

```python
from autocsv_profiler.ui import CleanCSVInterface, CleanInteractiveMethods

def main():
    # Initialize UI system
    ui = CleanCSVInterface()
    interactive = CleanInteractiveMethods(ui)

    # Run interactive workflow
    if not interactive.display_welcome_banner():
        return

    csv_path = interactive.get_csv_path()
    if not csv_path:
        return

    delimiter = interactive.detect_delimiter(csv_path)
    engines = interactive.select_engines()
    results = interactive.run_analysis(csv_path, delimiter, engines)

    interactive.display_results_summary(results)
```

### Component Integration

```python
from autocsv_profiler.ui.components import RichInteractiveComponents

class CustomAnalysis:
    def __init__(self):
        self.components = RichInteractiveComponents()

    def run_custom_workflow(self, data, save_dir):
        # Use Rich components for interaction
        filtered_data = self.components.exclude_columns_rich(data, save_dir)
        self.components.tableone_groupby_rich(filtered_data, save_dir)
        self.components.visualizations_rich(filtered_data, save_dir)
```

### Engine Integration

```python
# Engine with UI feedback
class UIAwareEngine:
    def __init__(self, ui_interface):
        self.ui = ui_interface

    def generate_report(self, data):
        with self.ui.progress:
            task = self.ui.progress.add_task("Processing data...", total=100)

            # Processing steps with progress updates
            self.preprocess_data(data)
            self.ui.progress.update(task, advance=25)

            self.analyze_data(data)
            self.ui.progress.update(task, advance=50)

            report = self.create_report(data)
            self.ui.progress.update(task, advance=100)

            return report
```

## Performance Considerations

### Lazy Loading

```python
# Lazy import pattern for optional dependencies
def _import_pandas():
    try:
        import pandas as pd
        return pd
    except ImportError:
        return None

# Usage
def process_dataframe(self, data):
    pd = _import_pandas()
    if pd is None:
        raise ImportError("pandas required for this operation")

    # Continue with pandas operations
```

### Memory Management Progress Tracking

```python
# Transient progress for memory management
progress = Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    transient=True,  # Remove completed tasks from display
    console=self.console,
)
```

### Console Resource Management

```python
class ManagedInterface:
    def __init__(self):
        self._console = None

    @property
    def console(self):
        if self._console is None:
            self._console = Console(force_terminal=True)
        return self._console

    def cleanup(self):
        if self._console is not None:
            self._console.file.close()
            self._console = None
```

## Troubleshooting

### Common UI Issues

**Rich Rendering Issues:**
```python
try:
    self.console.print(rich_content)
except Exception as e:
    print(f"Rich rendering failed: {e}")
    print(fallback_text)
```

**Terminal Encoding Issues:**
```python
# Set encoding for Windows compatibility
import os
os.environ["PYTHONIOENCODING"] = "utf-8"
```

**Progress Bar Issues:**
```python
# Use transient=False to avoid layout issues
progress = Progress(..., transient=False)
```

### Debug Mode Support

```python
def debug_print(self, message):
    if os.environ.get("DEBUG") == "1":
        self.console.print(f"[dim][DEBUG UI] {message}[/]")
```

## See Also

- [autocsv_profiler](../autocsv_profiler.md) - Main package interface
- [base](../base.md) - BaseProfiler abstract class
- [config](../config.md) - Configuration system integration
- [core modules](../README.md#core-modules) - Core utilities and logging
- [engines](../engines/) - Engine implementations with UI integration