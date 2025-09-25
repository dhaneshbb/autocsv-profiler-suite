# Changelog

All notable changes to autocsv-profiler-suite will be documented in this file.

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
- Documentation with workflow diagrams
- Legal documentation (LICENSE, NOTICE files)
- Environment status display and management tools
- Source file license headers for MIT License compliance
- Multi-environment exclusive focus (removed PyPI package references)

### Improved
- **Dependency Management**: Eliminated package conflicts through conda isolation
- **Installation Process**: Environment setup through conda
- **Documentation**: Added visual guides with mermaid diagrams
- **Error Handling**: Better user feedback and troubleshooting guidance
- **Code Quality**: Removed auto-installation code for more reliable execution

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
  - `recognize_delimiter.py` - Automatic delimiter detection
- Batch orchestration script (`run_analysis.bat`)
- Three isolated environments for tool execution
- Output artifacts (HTML reports, visualizations, cleaned data)
- Sample dataset and example outputs
- MIT License

### Features
- Automated CSV analysis workflow
- Multiple profiling engines integration
- Interactive user prompts for customization
- Cross-platform path handling
- Statistical analysis and visualization suite