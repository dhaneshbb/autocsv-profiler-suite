# Changelog

All notable changes to AutoCSV Profiler Suite will be documented in this file.

## [1.1.0] 

### Changed
- **Environment System**: Migrated from virtual environments to conda environments for better dependency management
- **Environment Names**: Renamed environments for clarity:
  - `ds_ml` → `csv-profiler-main`
  - `sweetz_ydata_profiler` → `csv-profiler-profiling`
  - `dataprep` → `csv-profiler-dataprep`
- **Python Versions**: Updated to Python 3.11.7 for main environment, 3.10.4 for profiling tools
- **Dependencies**: Replaced requirements.txt with conda environment.yml files
- **Project Structure**: Reorganized to follow Python packaging standards

### Added
- Interactive environment manager (`setup_environments.ps1`)
- Comprehensive documentation with workflow diagrams
- Modern Python packaging configuration (`pyproject.toml`)
- Environment status display and management tools

### Improved
- **Dependency Management**: Eliminated package conflicts through conda isolation
- **Installation Process**: One-click environment setup with automatic dependency resolution
- **Documentation**: Added visual guides with mermaid diagrams for better understanding
- **Error Handling**: Enhanced user feedback and troubleshooting guidance

### Fixed
- Package version conflicts between profiling tools
- Environment activation reliability on Windows systems
- Consistent package versions across installations

## [1.0.0] 

### Added
- Initial release with virtual environment support
- Core analysis modules:
  - `auto_csv_profiler.py` - Comprehensive statistical analysis
  - `profile_ydata_profiling_report.py` - YData profiling reports
  - `profile_sweetviz_report.py` - SweetViz visual reports
  - `profile_dataprep_report.py` - DataPrep EDA reports
  - `cerberus_validator_specific_columns.py` - Schema validation
  - `recognize_delimiter.py` - Automatic delimiter detection
- Batch orchestration script (`run_analysis.bat`)
- Three isolated environments for conflict-free tool execution
- Comprehensive output artifacts (HTML reports, visualizations, cleaned data)
- Sample dataset and example outputs
- MIT License

### Features
- Automated CSV analysis workflow
- Multiple profiling engines integration
- Interactive user prompts for customization
- Cross-platform path handling
- Statistical analysis and visualization suite