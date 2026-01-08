# Usage Examples

This document provides practical examples for using the Script Toolkit in various scenarios.

## Quick Start Examples

### Example 1: Basic Code Scan
```bash
# Scan your project for common issues
cd /path/to/your/project

# Check for TODOs and FIXMEs
python /path/to/Script-Toolkit/scripts/todo_scan.py
python /path/to/Script-Toolkit/scripts/fixme_scan.py

# Check for potential secrets
python /path/to/Script-Toolkit/scripts/secret_scan.py

# Get code statistics
python /path/to/Script-Toolkit/scripts/code_stats.py
```

### Example 2: Python Project Analysis
```bash
# Complete Python project analysis
cd /path/to/python/project

# Check syntax
python /path/to/Script-Toolkit/scripts/syntax_scan_py.py

# Find missing docstrings
python /path/to/Script-Toolkit/scripts/miss_docstring_scan.py

# Check type hints
python /path/to/Script-Toolkit/scripts/typing_missing_scan.py

# Calculate code complexity
python /path/to/Script-Toolkit/scripts/code_complexity_calculator.py

# Check for code duplication
python /path/to/Script-Toolkit/scripts/code_duplication_detector.py
```

### Example 3: Security Audit
```bash
# Run comprehensive security checks
cd /path/to/your/project

# Scan for secrets and credentials
python /path/to/Script-Toolkit/scripts/secret_scan.py

# Check for HTTP URLs (should be HTTPS)
python /path/to/Script-Toolkit/scripts/http_url_scan.py

# Find dangerous eval/exec usage
python /path/to/Script-Toolkit/scripts/eval_exec_scan.py

# Check subprocess shell usage
python /path/to/Script-Toolkit/scripts/subprocess_shell_scan.py

# Validate security headers
python /path/to/Script-Toolkit/scripts/security_headers_checker.py
```

### Example 4: Code Quality Metrics
```bash
# Generate comprehensive quality report
cd /path/to/your/project

# Code complexity
python /path/to/Script-Toolkit/scripts/code_complexity_calculator.py

# Test coverage
python /path/to/Script-Toolkit/scripts/test_coverage_analyzer.py

# Long functions that need refactoring
python /path/to/Script-Toolkit/scripts/long_func_scan.py

# Large files
python /path/to/Script-Toolkit/scripts/large_file_scan.py

# Code duplication
python /path/to/Script-Toolkit/scripts/code_duplication_detector.py
```

## CI/CD Integration Example

```bash
#!/bin/bash
# ci-checks.sh - Run in your CI pipeline

SCRIPT_DIR="/path/to/Script-Toolkit"
FAILED=0

echo "Running code quality checks..."

# Syntax check
python $SCRIPT_DIR/scripts/syntax_scan_py.py

# Secret scan
python $SCRIPT_DIR/scripts/secret_scan.py

# Check for NOCOMMIT markers
python $SCRIPT_DIR/scripts/nocommit_scan.py

# Test coverage check
python $SCRIPT_DIR/scripts/test_coverage_analyzer.py

echo "✅ All CI checks completed!"
```

## Pre-Commit Hook Example

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
SCRIPT_DIR="/path/to/Script-Toolkit"

echo "Running pre-commit checks..."

# Check for NOCOMMIT markers
python $SCRIPT_DIR/scripts/nocommit_scan.py

# Check for potential secrets
python $SCRIPT_DIR/scripts/secret_scan.py

echo "✅ Pre-commit checks passed"
```

## Using with Different Languages

### JavaScript/TypeScript Projects
```bash
python scripts/code_stats.py      # Count JS/TS files
python scripts/todo_scan.py       # Works on JS/TS
python scripts/secret_scan.py     # Works on JS/TS
```

### Java Projects
```bash
python scripts/code_stats.py
python scripts/api_endpoint_inventory.py  # Finds Spring Boot endpoints
```

## Tips and Tricks

### Create Aliases
Add to your `~/.bashrc`:
```bash
alias scan-todo='python /path/to/Script-Toolkit/scripts/todo_scan.py'
alias scan-secrets='python /path/to/Script-Toolkit/scripts/secret_scan.py'
```

### Combine with Other Tools
```bash
# Filter results with grep
python scripts/todo_scan.py
grep "URGENT" context_out/todo-scan_*.md
```

---

**Need more examples?** Check out the [main documentation](../SCRIPTS.md)!
