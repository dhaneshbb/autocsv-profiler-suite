# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

**Do NOT create a public GitHub issue for security vulnerabilities.**



### What to Include
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Suggested fix (if known)


## Security Considerations

### Data Handling
- AutoCSV Profiler processes CSV files locally
- No data is transmitted to external servers
- Generated reports are saved locally only

### Dependencies
- All dependencies are from trusted PyPI sources
- Regular security updates are applied
- Minimal dependency footprint to reduce attack surface

### File Processing
- Only processes user-specified CSV files
- Does not execute or import CSV content as code
- Validates file formats before processing

## Best Practices for Users

### Safe Usage
- Only analyze CSV files from trusted sources
- Review generated HTML reports before sharing
- Keep the package updated to latest version
- Use appropriate file permissions for sensitive data

### Environment Security
- Install in isolated virtual environments when possible
- Regularly update Python and dependencies
- Monitor package installations for unexpected changes
