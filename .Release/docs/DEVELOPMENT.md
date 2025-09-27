# Development Guide

This guide provides information for developers working on the AutoCSV Profiler Suite.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Commit Message Conventions](#commit-message-conventions)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Review Process](#review-process)
- [Release Procedures](#release-procedures)
- [Development Workflow](#development-workflow)
- [Testing Strategy](#testing-strategy)
- [Debugging and Troubleshooting](#debugging-and-troubleshooting)
- [Contributing to Core Components](#contributing-to-core-components)
- [Resources](#resources)

## Development Environment Setup

### Prerequisites

- **Anaconda or Miniconda** (required for multi-environment architecture)
- **Python 3.10 or higher** for base environment
- **Git** for version control
- **At least 3GB free disk space** (2GB for conda environments, 1GB for data/outputs)

### Initial Setup

**Install first** by following the [Installation Guide](INSTALLATION.md).

**Additional development setup:**

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Verify development tools
conda env list | grep csv-profiler
pytest --version
mypy --version
```

### Environment Structure

The project uses **4 isolated conda environments**:

- **Base Environment** (Python 3.10+): Development tools, orchestration
- **csv-profiler-main** (Python 3.11): Core statistical analysis
- **csv-profiler-profiling** (Python 3.10): YData Profiling, SweetViz
- **csv-profiler-dataprep** (Python 3.10): DataPrep EDA

### Development Tools

**Code Tools:** Black, isort, MyPy, flake8, pytest

## Code Style Guidelines

### Formatting Standards

- **Line Length**: 88 characters (Black default)
- **Indentation**: 4 spaces (no tabs)
- **String Quotes**: Double quotes preferred, single quotes acceptable
- **Import Organization**: Standard library, third-party, local imports

### Type Annotations

- **Required**: All public functions and methods
- **Coverage**: Type annotation coverage
- **Style**: Use `typing` module for complex types
- **Optional Dependencies**: Use `TYPE_CHECKING` for import isolation

### Documentation Standards

- **Docstrings**: Google-style format required
- **Examples**: Include usage examples in docstrings
- **Type Information**: Document parameter and return types
- **Edge Cases**: Document limitations and edge cases

### Code Guidelines

- No wildcard imports
- Import handling for optional dependencies
- Memory management for large files
- Environment isolation for engines

## Commit Message Conventions

Use conventional commit format for consistency and automated changelog generation:

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (no logic changes)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Scopes

- **engine**: Engine-related changes (main, profiling, dataprep)
- **ui**: User interface components
- **config**: Configuration system
- **core**: Core utilities and base classes
- **tests**: Test-related changes
- **docs**: Documentation updates

### Examples

```bash
feat(engine): add memory optimization for large CSV files
fix(ui): resolve delimiter detection issue with special characters
docs(api): update BaseProfiler class documentation
refactor(core): improve error handling in validation module
test(integration): add multi-environment test coverage
chore(deps): update conda environment specifications
```

## Branch Naming Conventions

### Format

```
<type>/<short-description>
```

### Types

- **feature**: New functionality
- **bugfix**: Bug fixes
- **hotfix**: Critical fixes
- **docs**: Documentation updates
- **refactor**: Code refactoring
- **test**: Test improvements
- **chore**: Maintenance tasks

### Examples

```bash
feature/memory-optimization
bugfix/delimiter-detection-error
docs/api-reference-update
refactor/engine-base-class
test/performance-benchmarks
chore/dependency-updates
```

## Review Process

### Code Review Requirements

1. **All changes require review** before merging
2. **Tests required** for new functionality
3. **Documentation updates** for API changes
4. **Performance impact assessment** for core changes
5. **Security review** for file processing changes

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass and coverage maintained
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced
- [ ] Performance impact acceptable
- [ ] Backward compatibility maintained
- [ ] Multi-environment compatibility verified

### Review Process

1. **Create pull request** from feature branch
2. **Automated checks** run (CI/CD, pre-commit hooks)
3. **Code review** by maintainer or senior developer
4. **Address feedback** and update code as needed
5. **Final approval** and merge to main branch

## Release Procedures

### Version Management

- **Version Location**: `autocsv_profiler/version.py`
- **Format**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Current Version**: 2.0.0

### Release Checklist

#### Pre-Release

- [ ] All tests pass in all environments
- [ ] Documentation updated
- [ ] CHANGELOG.md updated with changes
- [ ] Version number incremented in `version.py`
- [ ] Environment specifications tested
- [ ] Security scan passed

#### Release Process

1. **Update version** in `autocsv_profiler/version.py`
2. **Update CHANGELOG.md** with release notes
3. **Create release tag** using semantic versioning
4. **Update documentation** with new version info
5. **Verify conda environments** work with release
6. **Create GitHub release** with release notes

#### Post-Release

- [ ] Verify release artifacts
- [ ] Monitor for issues
- [ ] Update project documentation links
- [ ] Announce release (if major version)

### Version Numbering

- **Major**: Breaking changes, API changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, minor improvements

## Development Workflow


1. **Update local repository**
   ```bash
   git pull origin main
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make changes** in appropriate environment (see [Environment-Specific Development](#environment-specific-development) section below)

4. **Run quality checks**
   ```bash
   # Format code
   black autocsv_profiler/ tests/ bin/
   isort autocsv_profiler/ tests/ bin/

   # Type checking (environment-specific)
   mypy --config-file=mypy_main.ini autocsv_profiler/

   # Linting
   flake8 autocsv_profiler/ bin/
   ```

5. **Run tests**
   ```bash
   # All tests
   pytest

   # Fast tests only
   pytest -m "not slow"

   # Specific test categories
   pytest -m unit
   pytest -m integration
   ```

6. **Commit changes**
   ```bash
   git add .
   git commit -m "feat(engine): add new feature description"
   ```

7. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Environment-Specific Development

**For complete engine testing commands and examples, see [Engine Testing Guide](api/engines/ENGINE_TESTING.md).**

Quick reference for development testing:
```bash
# Main engine
conda activate csv-profiler-main
python autocsv_profiler/engines/main/analyzer.py test.csv "," output/

# Profiling engines (YData and SweetViz)
conda activate csv-profiler-profiling
python autocsv_profiler/engines/profiling/ydata_report.py test.csv "," output/

# DataPrep engine
conda activate csv-profiler-dataprep
python autocsv_profiler/engines/dataprep/dataprep_report.py test.csv "," output/
```

## Testing Strategy

### Test Organization

- **Unit Tests** (`tests/unit/`): Component isolation
- **Integration Tests** (`tests/integration/`): Cross-component workflows
- **Functional Tests** (`tests/functional/`): End-to-end features
- **Performance Tests** (`tests/performance/`): Resource validation

### Running Tests

```bash
# All tests with coverage
pytest

# Fast tests only (exclude slow tests)
pytest -m "not slow"

# Specific test categories
pytest -m unit
pytest -m integration
pytest -m performance

# Parallel testing
pytest -n auto

# HTML coverage report
pytest --cov-report=html
```

### Writing Tests

- **Follow AAA pattern**: Arrange, Act, Assert
- **Use fixtures** for test data and setup
- **Test edge cases** and error conditions
- **Maintain coverage** above 50% minimum
- **Mock external dependencies** appropriately

## Debugging and Troubleshooting

### Debug Mode

Enable debug mode for error information:

```bash
export DEBUG=1
python bin/run_analysis.py --debug
```

### Common Issues

#### Environment Problems
```bash
# Check environment status
conda env list | grep csv-profiler

# Recreate environment
python bin/setup_environments.py recreate csv-profiler-main
```

#### Import Errors
```bash
# Test specific environment imports
conda activate csv-profiler-main
python -c "import pandas, numpy, scipy; print('Main env OK')"
```

#### Memory Issues
- Reduce chunk size in `config/master_config.yml`
- Monitor memory usage with debug mode
- Use smaller test files for development

## Contributing to Core Components

### Adding New Engines

1. **Create engine file** in appropriate `engines/` subdirectory
2. **Inherit from BaseProfiler** abstract base class
3. **Implement required methods**: `generate_report()`, `get_report_name()`
4. **Add environment specification** to `config/master_config.yml`
5. **Update lazy loading** in `autocsv_profiler/__init__.py`
6. **Add tests** for new engine functionality

### Modifying Configuration

1. **Update master config** in `config/master_config.yml`
2. **Regenerate environments** using `setup_environments.py generate`
3. **Test all environments** after configuration changes
4. **Update documentation** if configuration options change

### Performance Optimization

1. **Profile code** with appropriate tools
2. **Test with large files** (>100MB)
3. **Monitor memory usage** during development
4. **Benchmark changes** against baseline performance
5. **Document performance implications** in code and commits

## Resources

**Key docs:** [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture and dependency conflict analysis
**External:** [Pre-commit](https://pre-commit.com/), [Conventional Commits](https://www.conventionalcommits.org/)

---

This development guide is maintained alongside the codebase. Please keep it updated as development practices evolve.
