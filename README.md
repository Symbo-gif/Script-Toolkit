# Script Toolkit — Production-Ready Developer Tools

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![No Dependencies](https://img.shields.io/badge/dependencies-none-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

A comprehensive, dependency-free toolkit with **114+ production-ready scripts** for code analysis, documentation generation, and project auditing. Perfect for developers, DevOps engineers, and QA teams who need powerful tools without the dependency overhead.

### Key Features

- 🚀 **114+ Scripts**: Comprehensive coverage of development workflows
- 📦 **Zero Dependencies**: Uses only Python standard library (3.8+)
- 🎯 **Production Ready**: Battle-tested scanners and analyzers
- 📊 **LLM-Friendly**: Outputs optimized for AI/ML workflows
- ⚡ **Fast**: Lightweight with minimal overhead
- 🔒 **Secure**: Built-in security scanners and validators
- 📝 **Well Documented**: Complete documentation in SCRIPTS.md

## Quick Start

### Installation

No installation needed! Just clone and run:

```bash
git clone https://github.com/Symbo-gif/Script-Toolkit.git
cd Script-Toolkit
python scripts/code_stats.py  # Run any script
```

**Note**: All scripts should be run from the repository root directory. The scripts automatically find the `llm_context` module when run from this location.

### Basic Usage

**Option 1: Direct Script Execution**
```bash
# Scan for TODO comments
python scripts/todo_scan.py

# Check Python syntax
python scripts/syntax_scan_py.py

# Generate code statistics
python scripts/code_stats.py

# Analyze test coverage
python scripts/test_coverage_analyzer.py
```

**Option 2: Unified CLI**
```bash
# Use the unified CLI with any command
python -m llm_context.toolbelt todo-scan --path ./my-project
python -m llm_context.toolbelt code-complexity-calculator --path ./src
python -m llm_context.toolbelt security-headers-checker --path .
```

### Output

All scripts generate timestamped Markdown reports in `context_out/`:
```
context_out/
├── todo-scan_2026-01-08_101530.md
├── code-stats_2026-01-08_101545.md
└── test-coverage-analyzer_2026-01-08_101600.md
```

## Script Categories

### 🔍 Code Quality Scanners (50+)
Identify code issues, anti-patterns, and improvement opportunities:
- `todo_scan.py`, `fixme_scan.py`, `bug_scan.py` - Track annotations
- `syntax_scan_py.py` - Check Python syntax errors
- `code_complexity_calculator.py` - Calculate cyclomatic complexity
- `code_duplication_detector.py` - Find duplicate code blocks
- `deprecated_api_scan.py` - Find deprecated API usage
- `miss_docstring_scan.py` - Find missing documentation
- `typing_missing_scan.py` - Check type hint coverage
- [See all 50+ scanners in SCRIPTS.md](SCRIPTS.md#code-scanners)

### 🔐 Security Tools (10+)
Security auditing and vulnerability detection:
- `secret_scan.py` - Detect exposed secrets and credentials
- `security_headers_checker.py` - Validate HTTP security headers
- `http_url_scan.py` - Find insecure HTTP URLs
- `eval_exec_scan.py` - Find dangerous eval/exec usage
- `subprocess_shell_scan.py` - Check for shell injection risks
- [See all security tools in SCRIPTS.md](SCRIPTS.md#security-scanners)

### 📊 Project Analysis (15+)
Comprehensive project metrics and insights:
- `test_coverage_analyzer.py` - Analyze test coverage patterns
- `dependency_tree_analyzer.py` - Audit dependencies
- `api_endpoint_inventory.py` - Inventory all API routes
- `database_schema_analyzer.py` - Analyze database schemas
- `performance_profiler_report.py` - Identify performance issues
- [See all analyzers in SCRIPTS.md](SCRIPTS.md#project-analysis-tools)

### 🐳 DevOps & Infrastructure (5+)
Container and deployment analysis:
- `dockerfile_analyzer.py` - Docker best practices checker
- `env_validator.py` - Validate environment variables
- `config_validator.py` - Check config file syntax
- `log_analyzer.py` - Analyze log files and patterns
- `resource_monitor.py` - Monitor resource usage

### 🔄 File Format Converters (20+)
Convert between formats for documentation:
- `json_to_md.py`, `csv_to_md.py`, `yaml_to_md.py` - Convert to Markdown
- `code_to_md.py` - Generate code documentation
- `requirements_to_md.py` - Document Python dependencies
- `package_json_to_md.py` - Document Node.js dependencies
- [See all converters in SCRIPTS.md](SCRIPTS.md#file-format-converters)

### 🐍 Python-Specific Tools (15+)
Deep Python analysis capabilities:
- `code_outline_py.py` - Generate code structure outline
- `import_list_py.py` - List all imports
- `function_metrics_py.py` - Analyze function complexity
- `class_metrics_py.py` - Analyze class structure
- `docstring_summary_py.py` - Extract all docstrings
- [See all Python tools in SCRIPTS.md](SCRIPTS.md#python-specific-analyzers)

### 📝 Documentation & Templates (15+)
Generate consistent project documentation:
- `template_gen.py` - Generate various document templates
- `readme_summary.py` - Summarize README content
- `markdown_heading_index.py` - Create table of contents
- `changelog_summary.py` - Parse changelog entries
- [See all templates in SCRIPTS.md](SCRIPTS.md#template-generators)

## NEW: 15 Production-Ready Scripts 🎉

We've added 15 powerful new scripts for modern development workflows:

1. **api_response_validator.py** - Validate API response formats
2. **config_validator.py** - Check configuration file syntax
3. **dependency_tree_analyzer.py** - Analyze dependency trees
4. **git_commit_linter.py** - Enforce conventional commits
5. **code_complexity_calculator.py** - Calculate code complexity
6. **performance_profiler_report.py** - Find performance issues
7. **test_coverage_analyzer.py** - Analyze test coverage
8. **dockerfile_analyzer.py** - Docker best practices
9. **env_validator.py** - Validate environment variables
10. **api_endpoint_inventory.py** - List all API endpoints
11. **database_schema_analyzer.py** - Analyze database schemas
12. **log_analyzer.py** - Analyze logging patterns
13. **resource_monitor.py** - Monitor resource usage
14. **code_duplication_detector.py** - Find duplicate code
15. **security_headers_checker.py** - Check security headers

## Common Use Cases

### CI/CD Integration
```bash
# Run code quality checks in your pipeline
python scripts/syntax_scan_py.py
python scripts/secret_scan.py
python scripts/test_coverage_analyzer.py
python scripts/security_headers_checker.py
```

### Pre-Commit Hooks
```bash
# Add to .git/hooks/pre-commit
python scripts/git_commit_linter.py
python scripts/secret_scan.py
python scripts/nocommit_scan.py
```

### Code Review
```bash
# Generate comprehensive code review report
python scripts/code_complexity_calculator.py
python scripts/code_duplication_detector.py
python scripts/performance_profiler_report.py
python scripts/miss_docstring_scan.py
```

### Project Documentation
```bash
# Generate project documentation
python scripts/code_stats.py
python scripts/dir_tree_to_md.py
python scripts/dependency_tree_analyzer.py
python scripts/api_endpoint_inventory.py
python scripts/database_schema_analyzer.py
```

### Security Audit
```bash
# Run comprehensive security scan
python scripts/secret_scan.py
python scripts/security_headers_checker.py
python scripts/http_url_scan.py
python scripts/eval_exec_scan.py
python scripts/subprocess_shell_scan.py
```

## Documentation

- **[SCRIPTS.md](SCRIPTS.md)** - Complete documentation for all 114+ scripts
- **[Examples](examples/)** - Usage examples and patterns
- **[Contributing](CONTRIBUTING.md)** - How to add new scripts

## Advanced Usage

### Custom Path
```bash
# Scan a specific directory
python -m llm_context.toolbelt code-stats --path /path/to/project
```

### With Parameters
```bash
# Customize thresholds and limits
python -m llm_context.toolbelt long-func-scan --min-lines 100
python -m llm_context.toolbelt large-file-scan --min-bytes 5000000
python -m llm_context.toolbelt line-length-scan --max-len 100
```

### Batch Processing
```bash
# Run multiple scans
for script in todo_scan fixme_scan bug_scan secret_scan; do
  python scripts/${script}.py
done
```

## Requirements

- Python 3.8 or higher
- No external dependencies required

## Project Structure

```
Script-Toolkit/
├── llm_context/
│   ├── toolbelt.py          # Core engine (2500+ lines)
│   └── __init__.py
├── scripts/                  # 114+ wrapper scripts
│   ├── todo_scan.py
│   ├── code_complexity_calculator.py
│   ├── test_coverage_analyzer.py
│   └── ... (111 more)
├── context_out/             # Generated reports (auto-created)
├── SCRIPTS.md               # Complete script documentation
└── README.md                # This file
```

## Features by Numbers

- ✅ **114+ Scripts** ready to use
- ✅ **15 NEW** production-ready scripts added
- ✅ **50+ Code Quality** scanners
- ✅ **10+ Security** tools
- ✅ **15+ Project Analysis** tools
- ✅ **20+ File Converters**
- ✅ **15+ Python-specific** analyzers
- ✅ **0 Dependencies** (only stdlib)
- ✅ **100% Documentation** coverage

## Best Practices

1. **Run Regularly**: Integrate into CI/CD pipelines
2. **Track History**: Keep historical scan results
3. **Automate**: Use pre-commit hooks
4. **Combine Scans**: Run related scans together
5. **Review Output**: Regularly review generated reports

## Troubleshooting

### Module Not Found
```bash
# Make sure you're in the repository root
cd /path/to/Script-Toolkit
python scripts/todo_scan.py
```

### Permission Denied
```bash
# Make scripts executable
chmod +x scripts/*.py
```

### Large Repositories
```bash
# Scan specific directories for faster results
python -m llm_context.toolbelt code-stats --path ./src
```

## Contributing

Contributions are welcome! To add a new script:

1. Implement the command function in `llm_context/toolbelt.py`
2. Register it in the argument parser and command dispatcher
3. Create a wrapper script in `scripts/`
4. Add documentation to `SCRIPTS.md`
5. Submit a pull request

## Performance

All scripts are optimized for performance:
- Parallel file processing where applicable
- Efficient pattern matching with compiled regex
- Smart caching to avoid redundant operations
- Excluded directories (.git, node_modules, etc.)

## License

MIT License - See LICENSE file for details

## Support

- 📖 [Full Documentation](SCRIPTS.md)
- 🐛 [Report Issues](https://github.com/Symbo-gif/Script-Toolkit/issues)
- 💡 [Request Features](https://github.com/Symbo-gif/Script-Toolkit/issues/new)

---

**Made with ❤️ for developers who value simplicity and power**

*Last Updated: 2026-01-08*
