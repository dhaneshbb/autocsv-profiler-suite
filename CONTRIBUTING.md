# Contributing to AutoCSV Profiler Suite

This project accepts contributions from the community.

## Contribution Types

Accepted contributions include:

- **Bug Reports**: Report issues
- **Feature Requests**: Suggest improvements
- **Code Contributions**: Fix bugs, add features, improve performance
- **Documentation**: Update guides, API docs, examples
- **Testing**: Add tests, improve coverage

## Setup for Contributors

### 1. Environment Setup

Required steps to run the project:

1. Fork this repository on GitHub
2. Clone the fork: `git clone https://github.com/YOUR_USERNAME/autocsv-profiler-suite.git`
3. Set up conda environments: `python bin/setup_environments.py create --parallel`
4. Install development tools:
   ```bash
   pip install -r requirements-dev.txt
   pre-commit install
   ```

### 2. Architecture Understanding

Required reading:
- [Architecture Guide](docs/ARCHITECTURE.md) - multi-environment design
- [Development Guide](docs/DEVELOPMENT.md) - setup and workflows

## Code Quality Standards

Code quality tools:
- **Black** for code formatting (88 character limit)
- **isort** for import organization
- **MyPy** for type checking
- **pytest** for testing (minimum 50% coverage)

Run quality checks: `pre-commit run --all-files`

## Development Workflow

### 1. Planning Work

**For Bug Fixes:**
1. Check existing issues for the bug
2. Create new issue if not tracked
3. Identify root cause and plan solution
4. Consider impact on all environments (main, profiling, dataprep)

**For New Features:**
1. Review existing feature requests and roadmap
2. Create feature request issue to discuss approach
3. Get community feedback before implementation
4. Assess impact on all profiling engines

### 2. Making Changes

**Create branch:**
```bash
git checkout main
git pull upstream main
git checkout -b feature/feature-name
```

**Development process:**
1. Make changes in appropriate environment
2. Write tests (unit tests required, integration tests when needed)
3. Update documentation if changing APIs or adding features
4. Run quality checks: `pre-commit run --all-files`
5. Test changes: `python bin/run_analysis.py test.csv --debug`

### 3. Commit Work

Use conventional commit format: `<type>(<scope>): <description>`

Examples:
- `feat(analyzer): add statistical summary export`
- `fix(dataprep): handle missing data properly`
- `docs(readme): update installation instructions`

Common types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`

## Testing Changes

Test commands:

```bash
pytest                    # Run all tests
pytest -m "not slow"      # Skip slow tests
pytest -m unit            # Unit tests only
pytest -m integration     # Integration tests only
```

Test categories: Unit, Integration, Functional, Performance

## Submitting Changes

### 1. Pull Request Process

1. **Push branch:**
   ```bash
   git push origin feature/feature-name
   ```

2. **Open pull request on GitHub:**
   - Write title using conventional commit format
   - Describe changes and reasoning
   - Link related issues ("fixes #123" or "closes #456")

3. **Review process:**
   - Automated tests run first
   - Maintainers review code
   - Address feedback

### 2. Pre-submission Checklist

Required before submission:

- [ ] Code follows project style
- [ ] Tests added for changes
- [ ] Documentation updated (if needed)
- [ ] All tests pass locally
- [ ] Pre-commit hooks pass
- [ ] No conflicts with main branch
- [ ] Commit messages follow format
- [ ] PR description explains changes

### 3. Review Process

Steps after submission:

1. **Automated checks** run (tests, linting, security scans)
2. **Code review** by maintainers examining:
   - Code quality and style
   - Test coverage
   - Documentation
   - Architecture compatibility
   - Security implications
3. **Discussion** if changes needed
4. **Merge** when approved

## Reporting Issues

Use GitHub issue templates:

- **[Bug Report](.github/ISSUE_TEMPLATE/bug_report.md)**: Report broken functionality
- **[Feature Request](.github/ISSUE_TEMPLATE/feature_request.md)**: Suggest improvements

## Getting Help

### Documentation Resources

- **[README.md](README.md)**: Project overview and setup
- **[Architecture Guide](docs/ARCHITECTURE.md)**: Multi-environment system explanation
- **[Development Guide](docs/DEVELOPMENT.md)**: Setup and development workflows
- **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)**: Common problems and solutions

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussion
- **Pull Request Reviews**: Code feedback and learning

## Project Maintainer

Maintained by [@dhaneshbb](https://github.com/dhaneshbb).

---

Questions can be submitted through GitHub Discussions or by contacting maintainers directly.
