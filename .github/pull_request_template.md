# Pull Request

## Description
Clear description of changes in this PR.

## Type of Change
- [ ] **Bug fix** (non-breaking)
- [ ] **New feature** (non-breaking)
- [ ] **Breaking change** (affects existing functionality)
- [ ] **Documentation update**
- [ ] **Performance improvement**
- [ ] **Refactoring** (no functional changes)

## Related Issues
- Fixes #(issue_number)
- Related to #(issue_number)

## Environment Impact
- [ ] **Base environment** (orchestration, UI)
- [ ] **Main environment** (csv-profiler-main, Python 3.11)
- [ ] **Profiling environment** (csv-profiler-profiling, Python 3.10)
- [ ] **DataPrep environment** (csv-profiler-dataprep, Python 3.10)

## Testing
```bash
# Test commands run
pytest
python bin/run_analysis.py test.csv --debug
```

**Test results:**
```text
# Paste test results summary
```

## Quality Checks
- [ ] **Code formatted:** `black autocsv_profiler/ tests/ bin/`
- [ ] **Imports sorted:** `isort autocsv_profiler/ tests/ bin/`
- [ ] **Linting passed:** `flake8 autocsv_profiler/ bin/`
- [ ] **Type checking:** `mypy --config-file=mypy_main.ini autocsv_profiler/`
- [ ] **Security scan:** `bandit -r autocsv_profiler/ bin/`
- [ ] **Tests pass:** `pytest`

## Breaking Changes
List any breaking changes and migration instructions:

## Documentation
- [ ] Updated relevant documentation
- [ ] Added/updated API examples
- [ ] Updated changelog

**For development standards:** See [Development Guide](docs/DEVELOPMENT.md)