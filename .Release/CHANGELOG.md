# Changelog

All notable changes to autocsv-profiler-suite will be documented in this file.

## [v2.0.0] - sep

### Added
- **Unified orchestrator**: `bin/run_analysis.py` replacing platform-specific batch scripts
- **Lazy loading system**: Engines load only when needed for faster startup
- **Rich console interface**: Progress tracking and enhanced user experience
- **Memory management**: Automatic chunking for files >50MB with 1GB default limits
- **Cross-platform support**: Python-based entry points work on Windows/Linux/macOS
- **BaseProfiler class**: Abstract base class for all engines with consistent interface
- **Configuration as code**: Single `config/master_config.yml` source of truth

### Changed
- **Entry point**: Use `python bin/run_analysis.py` instead of `run_analysis.bat/.sh`
- **Performance**: 20-30% improvement with modern pandas 2.3.1 and numpy 2.2.6
- **Package structure**: Reorganized as `autocsv_profiler` Python package
- **Engine isolation**: Multi-environment architecture (base orchestrator + 3 specialized conda environments)

### Breaking Changes
- **API changes**: BaseProfiler constructor now includes `chunk_size` and `memory_limit_gb` parameters
- **Script replacement**: Batch files no longer provided, use Python orchestrator
- **Import changes**: Module renamed from individual scripts to unified `autocsv_profiler` package

## [v1.1.0] - agu

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

## [v1.0.0] - apr

### Added
- Initial release with virtual environment support
- Core analysis modules:
  - `auto_csv_profiler.py` - Comprehensive statistical analysis
  - `profile_ydata_profiling_report.py` - YData profiling reports
  - `profile_sweetviz_report.py` - SweetViz visual reports
  - `profile_dataprep_report.py` - DataPrep EDA reports
  - `recognize_delimiter.py` - Automatic delimiter detection
- Batch orchestration script (`run_analysis.bat`)
- Three specialized conda environments plus base environment for tool execution
- Output artifacts (HTML reports, visualizations, cleaned data)
- Sample dataset and example outputs
- MIT License

### Features
- Automated CSV analysis workflow
- Multiple profiling engines integration
- Interactive user prompts for customization
- Cross-platform path handling
- Statistical analysis and visualization suite
