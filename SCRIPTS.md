# Complete Script Documentation

This document provides comprehensive documentation for all scripts in the Script Toolkit.

## Table of Contents

1. [Code Scanners](#code-scanners)
2. [File Format Converters](#file-format-converters)
3. [Python-Specific Analyzers](#python-specific-analyzers)
4. [Markdown Tools](#markdown-tools)
5. [Security Scanners](#security-scanners)
6. [Template Generators](#template-generators)
7. [Project Analysis Tools](#project-analysis-tools)
8. [Configuration File Converters](#configuration-file-converters)

---

## Code Scanners

### todo_scan.py
**Purpose**: Scans codebase for TODO comments  
**Command**: `python scripts/todo_scan.py` or `python -m llm_context.toolbelt todo-scan`  
**Output**: Lists all TODO comments with file locations and line numbers  
**Use Case**: Track outstanding tasks and reminders in code  
**Example Output**: `context_out/todo-scan_YYYY-MM-DD_HHMMSS.md`

### fixme_scan.py
**Purpose**: Scans codebase for FIXME comments  
**Command**: `python scripts/fixme_scan.py` or `python -m llm_context.toolbelt fixme-scan`  
**Output**: Lists all FIXME comments with file locations and line numbers  
**Use Case**: Identify code sections that need fixing or improvement  
**Example Output**: `context_out/fixme-scan_YYYY-MM-DD_HHMMSS.md`

### error_scan.py
**Purpose**: Scans codebase for ERROR comments  
**Command**: `python scripts/error_scan.py` or `python -m llm_context.toolbelt error-scan`  
**Output**: Lists all ERROR comments with file locations and line numbers  
**Use Case**: Find error-related annotations in code  
**Example Output**: `context_out/error-scan_YYYY-MM-DD_HHMMSS.md`

### bug_scan.py
**Purpose**: Scans codebase for BUG comments  
**Command**: `python scripts/bug_scan.py` or `python -m llm_context.toolbelt bug-scan`  
**Output**: Lists all BUG comments with file locations and line numbers  
**Use Case**: Track known bugs documented in code  
**Example Output**: `context_out/bug-scan_YYYY-MM-DD_HHMMSS.md`

### nocommit_scan.py
**Purpose**: Scans for NOCOMMIT markers that should prevent commits  
**Command**: `python scripts/nocommit_scan.py` or `python -m llm_context.toolbelt nocommit-scan`  
**Output**: Lists all NOCOMMIT markers with file locations  
**Use Case**: Prevent accidental commits of work-in-progress code  
**Example Output**: `context_out/nocommit-scan_YYYY-MM-DD_HHMMSS.md`

### code_stats.py
**Purpose**: Generates comprehensive code statistics  
**Command**: `python scripts/code_stats.py` or `python -m llm_context.toolbelt code-stats`  
**Output**: Line counts, file counts, and language breakdown  
**Use Case**: Get overview of codebase size and composition  
**Example Output**: `context_out/code-stats_YYYY-MM-DD_HHMMSS.md`

### comment_summary.py
**Purpose**: Extracts and summarizes all code comments  
**Command**: `python scripts/comment_summary.py` or `python -m llm_context.toolbelt comment-summary`  
**Output**: All comments grouped by file  
**Use Case**: Review documentation and inline comments  
**Example Output**: `context_out/comment-summary_YYYY-MM-DD_HHMMSS.md`

### long_func_scan.py
**Purpose**: Identifies functions exceeding line count thresholds  
**Command**: `python scripts/long_func_scan.py` or `python -m llm_context.toolbelt long-func-scan`  
**Output**: Lists long functions with line counts  
**Use Case**: Find functions that may need refactoring  
**Example Output**: `context_out/long-func-scan_YYYY-MM-DD_HHMMSS.md`

### large_file_scan.py
**Purpose**: Identifies files exceeding size thresholds  
**Command**: `python scripts/large_file_scan.py` or `python -m llm_context.toolbelt large-file-scan`  
**Output**: Lists large files with sizes  
**Use Case**: Find files that may need splitting or optimization  
**Example Output**: `context_out/large-file-scan_YYYY-MM-DD_HHMMSS.md`

### large_line_scan.py
**Purpose**: Identifies lines exceeding length thresholds  
**Command**: `python scripts/large_line_scan.py` or `python -m llm_context.toolbelt large-line-scan`  
**Output**: Lists long lines with locations  
**Use Case**: Enforce line length standards  
**Example Output**: `context_out/large-line-scan_YYYY-MM-DD_HHMMSS.md`

### line_length_scan.py
**Purpose**: Checks for lines exceeding specified length  
**Command**: `python scripts/line_length_scan.py` or `python -m llm_context.toolbelt line-length-scan`  
**Output**: Lists lines exceeding length limit  
**Use Case**: Maintain consistent line length standards  
**Example Output**: `context_out/line-length-scan_YYYY-MM-DD_HHMMSS.md`

### empty_file_scan.py
**Purpose**: Finds empty or near-empty files  
**Command**: `python scripts/empty_file_scan.py` or `python -m llm_context.toolbelt empty-file-scan`  
**Output**: Lists empty files  
**Use Case**: Clean up unused files  
**Example Output**: `context_out/empty-file-scan_YYYY-MM-DD_HHMMSS.md`

### duplicate_line_scan.py
**Purpose**: Detects duplicate lines in files  
**Command**: `python scripts/duplicate_line_scan.py` or `python -m llm_context.toolbelt duplicate-line-scan`  
**Output**: Lists files with duplicate lines  
**Use Case**: Find potential code duplication  
**Example Output**: `context_out/duplicate-line-scan_YYYY-MM-DD_HHMMSS.md`

### duplicate_filename_scan.py
**Purpose**: Finds files with duplicate names in different directories  
**Command**: `python scripts/duplicate_filename_scan.py` or `python -m llm_context.toolbelt duplicate-filename-scan`  
**Output**: Lists duplicate filenames with paths  
**Use Case**: Avoid naming confusion  
**Example Output**: `context_out/duplicate-filename-scan_YYYY-MM-DD_HHMMSS.md`

### duplicate_file_contents_scan.py
**Purpose**: Identifies files with identical contents  
**Command**: `python scripts/duplicate_file_contents_scan.py` or `python -m llm_context.toolbelt duplicate-file-contents-scan`  
**Output**: Lists files with identical content  
**Use Case**: Find truly duplicate files for cleanup  
**Example Output**: `context_out/duplicate-file-contents-scan_YYYY-MM-DD_HHMMSS.md`

---

## File Format Converters

### json_to_md.py
**Purpose**: Converts JSON files to readable Markdown  
**Command**: `python scripts/json_to_md.py` or `python -m llm_context.toolbelt json-to-md`  
**Output**: JSON content formatted as Markdown  
**Use Case**: Make JSON files more readable for documentation  
**Example Output**: `context_out/json-to-md_YYYY-MM-DD_HHMMSS.md`

### csv_to_md.py
**Purpose**: Converts CSV files to Markdown tables  
**Command**: `python scripts/csv_to_md.py` or `python -m llm_context.toolbelt csv-to-md`  
**Output**: CSV data as Markdown tables  
**Use Case**: Include CSV data in documentation  
**Example Output**: `context_out/csv-to-md_YYYY-MM-DD_HHMMSS.md`

### csv_summary.py
**Purpose**: Generates summary statistics for CSV files  
**Command**: `python scripts/csv_summary.py` or `python -m llm_context.toolbelt csv-summary`  
**Output**: Column counts, row counts, and basic statistics  
**Use Case**: Quick overview of CSV data  
**Example Output**: `context_out/csv-summary_YYYY-MM-DD_HHMMSS.md`

### md_to_txt.py
**Purpose**: Converts Markdown to plain text  
**Command**: `python scripts/md_to_txt.py` or `python -m llm_context.toolbelt md-to-txt`  
**Output**: Plain text version of Markdown files  
**Use Case**: Extract text content from Markdown  
**Example Output**: `context_out/md-to-txt_YYYY-MM-DD_HHMMSS.txt`

### txt_to_md.py
**Purpose**: Converts plain text files to Markdown  
**Command**: `python scripts/txt_to_md.py` or `python -m llm_context.toolbelt txt-to-md`  
**Output**: Text files formatted as Markdown  
**Use Case**: Add formatting to plain text  
**Example Output**: `context_out/txt-to-md_YYYY-MM-DD_HHMMSS.md`

### yaml_to_md.py
**Purpose**: Converts YAML files to Markdown  
**Command**: `python scripts/yaml_to_md.py` or `python -m llm_context.toolbelt yaml-to-md`  
**Output**: YAML content formatted as Markdown  
**Use Case**: Document YAML configurations  
**Example Output**: `context_out/yaml-to-md_YYYY-MM-DD_HHMMSS.md`

### xml_to_md.py
**Purpose**: Converts XML files to Markdown  
**Command**: `python scripts/xml_to_md.py` or `python -m llm_context.toolbelt xml-to-md`  
**Output**: XML content formatted as Markdown  
**Use Case**: Document XML configurations  
**Example Output**: `context_out/xml-to-md_YYYY-MM-DD_HHMMSS.md`

### html_to_md_text.py
**Purpose**: Extracts text content from HTML files  
**Command**: `python scripts/html_to_md_text.py` or `python -m llm_context.toolbelt html-to-md-text`  
**Output**: HTML text content as Markdown  
**Use Case**: Extract readable content from HTML  
**Example Output**: `context_out/html-to-md-text_YYYY-MM-DD_HHMMSS.md`

### code_to_md.py
**Purpose**: Converts code files to formatted Markdown with syntax highlighting  
**Command**: `python scripts/code_to_md.py` or `python -m llm_context.toolbelt code-to-md`  
**Output**: Code files with proper Markdown code blocks  
**Use Case**: Generate code documentation  
**Example Output**: `context_out/code-to-md_YYYY-MM-DD_HHMMSS.md`

---

## Python-Specific Analyzers

### syntax_scan_py.py
**Purpose**: Checks Python files for syntax errors  
**Command**: `python scripts/syntax_scan_py.py` or `python -m llm_context.toolbelt syntax-scan-py`  
**Output**: Lists Python files with syntax errors  
**Use Case**: Identify syntax issues before runtime  
**Example Output**: `context_out/syntax-scan-py_YYYY-MM-DD_HHMMSS.md`

### miss_docstring_scan.py
**Purpose**: Finds Python functions/classes missing docstrings  
**Command**: `python scripts/miss_docstring_scan.py` or `python -m llm_context.toolbelt miss-docstring-scan`  
**Output**: Lists functions and classes without docstrings  
**Use Case**: Improve code documentation  
**Example Output**: `context_out/miss-docstring-scan_YYYY-MM-DD_HHMMSS.md`

### typing_missing_scan.py
**Purpose**: Finds Python functions missing type hints  
**Command**: `python scripts/typing_missing_scan.py` or `python -m llm_context.toolbelt typing-missing-scan`  
**Output**: Lists functions without type annotations  
**Use Case**: Improve type safety  
**Example Output**: `context_out/typing-missing-scan_YYYY-MM-DD_HHMMSS.md`

### broad_except_scan.py
**Purpose**: Finds overly broad exception handlers  
**Command**: `python scripts/broad_except_scan.py` or `python -m llm_context.toolbelt broad-except-scan`  
**Output**: Lists broad except clauses  
**Use Case**: Improve error handling specificity  
**Example Output**: `context_out/broad-except-scan_YYYY-MM-DD_HHMMSS.md`

### dead_except_scan.py
**Purpose**: Finds exception handlers that may be unreachable  
**Command**: `python scripts/dead_except_scan.py` or `python -m llm_context.toolbelt dead-except-scan`  
**Output**: Lists potentially dead except blocks  
**Use Case**: Clean up unreachable error handlers  
**Example Output**: `context_out/dead-except-scan_YYYY-MM-DD_HHMMSS.md`

### eval_exec_scan.py
**Purpose**: Finds dangerous eval() and exec() calls  
**Command**: `python scripts/eval_exec_scan.py` or `python -m llm_context.toolbelt eval-exec-scan`  
**Output**: Lists eval/exec usage with locations  
**Use Case**: Security audit for code execution risks  
**Example Output**: `context_out/eval-exec-scan_YYYY-MM-DD_HHMMSS.md`

### unreachable_code_scan_py.py
**Purpose**: Detects unreachable code in Python files  
**Command**: `python scripts/unreachable_code_scan_py.py` or `python -m llm_context.toolbelt unreachable-code-scan-py`  
**Output**: Lists unreachable code sections  
**Use Case**: Clean up dead code  
**Example Output**: `context_out/unreachable-code-scan-py_YYYY-MM-DD_HHMMSS.md`

### traceback_usage_scan.py
**Purpose**: Finds traceback module usage  
**Command**: `python scripts/traceback_usage_scan.py` or `python -m llm_context.toolbelt traceback-usage-scan`  
**Output**: Lists traceback usage  
**Use Case**: Review error handling patterns  
**Example Output**: `context_out/traceback-usage-scan_YYYY-MM-DD_HHMMSS.md`

### logger_debug_scan.py
**Purpose**: Finds logger.debug() calls  
**Command**: `python scripts/logger_debug_scan.py` or `python -m llm_context.toolbelt logger-debug-scan`  
**Output**: Lists debug logging statements  
**Use Case**: Review debug logging before production  
**Example Output**: `context_out/logger-debug-scan_YYYY-MM-DD_HHMMSS.md`

### print_debug_scan.py
**Purpose**: Finds print() statements used for debugging  
**Command**: `python scripts/print_debug_scan.py` or `python -m llm_context.toolbelt print-debug-scan`  
**Output**: Lists print statements  
**Use Case**: Remove debug prints before production  
**Example Output**: `context_out/print-debug-scan_YYYY-MM-DD_HHMMSS.md`

### code_outline_py.py
**Purpose**: Generates outline of Python classes and functions  
**Command**: `python scripts/code_outline_py.py` or `python -m llm_context.toolbelt code-outline-py`  
**Output**: Hierarchical outline of code structure  
**Use Case**: Quick overview of code organization  
**Example Output**: `context_out/code-outline-py_YYYY-MM-DD_HHMMSS.md`

### import_list_py.py
**Purpose**: Lists all imports in Python files  
**Command**: `python scripts/import_list_py.py` or `python -m llm_context.toolbelt import-list-py`  
**Output**: All import statements by file  
**Use Case**: Understand dependencies  
**Example Output**: `context_out/import-list-py_YYYY-MM-DD_HHMMSS.md`

### function_metrics_py.py
**Purpose**: Analyzes Python function metrics (lines, complexity)  
**Command**: `python scripts/function_metrics_py.py` or `python -m llm_context.toolbelt function-metrics-py`  
**Output**: Function statistics  
**Use Case**: Identify complex functions  
**Example Output**: `context_out/function-metrics-py_YYYY-MM-DD_HHMMSS.md`

### class_metrics_py.py
**Purpose**: Analyzes Python class metrics  
**Command**: `python scripts/class_metrics_py.py` or `python -m llm_context.toolbelt class-metrics-py`  
**Output**: Class statistics  
**Use Case**: Analyze class design  
**Example Output**: `context_out/class-metrics-py_YYYY-MM-DD_HHMMSS.md`

### docstring_summary_py.py
**Purpose**: Extracts and summarizes Python docstrings  
**Command**: `python scripts/docstring_summary_py.py` or `python -m llm_context.toolbelt docstring-summary-py`  
**Output**: All docstrings by file  
**Use Case**: Review documentation coverage  
**Example Output**: `context_out/docstring-summary-py_YYYY-MM-DD_HHMMSS.md`

### many_params_scan.py
**Purpose**: Finds functions with too many parameters  
**Command**: `python scripts/many_params_scan.py` or `python -m llm_context.toolbelt many-params-scan`  
**Output**: Lists functions with many parameters  
**Use Case**: Identify functions that may need refactoring  
**Example Output**: `context_out/many-params-scan_YYYY-MM-DD_HHMMSS.md`

---

## Markdown Tools

### markdown_heading_index.py
**Purpose**: Creates index of all headings in Markdown files  
**Command**: `python scripts/markdown_heading_index.py` or `python -m llm_context.toolbelt markdown-heading-index`  
**Output**: Table of contents from all Markdown files  
**Use Case**: Navigate documentation structure  
**Example Output**: `context_out/markdown-heading-index_YYYY-MM-DD_HHMMSS.md`

### markdown_image_check.py
**Purpose**: Validates image links in Markdown files  
**Command**: `python scripts/markdown_image_check.py` or `python -m llm_context.toolbelt markdown-image-check`  
**Output**: Lists broken or missing images  
**Use Case**: Ensure documentation images are accessible  
**Example Output**: `context_out/markdown-image-check_YYYY-MM-DD_HHMMSS.md`

### markdown_word_count.py
**Purpose**: Counts words in Markdown files  
**Command**: `python scripts/markdown_word_count.py` or `python -m llm_context.toolbelt markdown-word-count`  
**Output**: Word counts by file  
**Use Case**: Track documentation size  
**Example Output**: `context_out/markdown-word-count_YYYY-MM-DD_HHMMSS.md`

### link_check_md.py
**Purpose**: Validates all links in Markdown files  
**Command**: `python scripts/link_check_md.py` or `python -m llm_context.toolbelt link-check-md`  
**Output**: Lists broken or invalid links  
**Use Case**: Maintain documentation quality  
**Example Output**: `context_out/link-check-md_YYYY-MM-DD_HHMMSS.md`

### readme_links.py
**Purpose**: Extracts all links from README files  
**Command**: `python scripts/readme_links.py` or `python -m llm_context.toolbelt readme-links`  
**Output**: All links found in README  
**Use Case**: Review external references  
**Example Output**: `context_out/readme-links_YYYY-MM-DD_HHMMSS.md`

### readme_summary.py
**Purpose**: Generates summary of README content  
**Command**: `python scripts/readme_summary.py` or `python -m llm_context.toolbelt readme-summary`  
**Output**: README content summary  
**Use Case**: Quick project overview  
**Example Output**: `context_out/readme-summary_YYYY-MM-DD_HHMMSS.md`

---

## Security Scanners

### secret_scan.py
**Purpose**: Scans for potential secrets and credentials  
**Command**: `python scripts/secret_scan.py` or `python -m llm_context.toolbelt secret-scan`  
**Output**: Lists potential secrets with locations  
**Use Case**: Prevent credential leaks  
**Example Output**: `context_out/secret-scan_YYYY-MM-DD_HHMMSS.md`

### http_url_scan.py
**Purpose**: Finds HTTP URLs that should be HTTPS  
**Command**: `python scripts/http_url_scan.py` or `python -m llm_context.toolbelt http-url-scan`  
**Output**: Lists insecure HTTP URLs  
**Use Case**: Security hardening  
**Example Output**: `context_out/http-url-scan_YYYY-MM-DD_HHMMSS.md`

### subprocess_shell_scan.py
**Purpose**: Finds subprocess calls with shell=True  
**Command**: `python scripts/subprocess_shell_scan.py` or `python -m llm_context.toolbelt subprocess-shell-scan`  
**Output**: Lists potentially dangerous shell calls  
**Use Case**: Security audit for command injection risks  
**Example Output**: `context_out/subprocess-shell-scan_YYYY-MM-DD_HHMMSS.md`

### hardcoded_path_scan.py
**Purpose**: Finds hardcoded file paths  
**Command**: `python scripts/hardcoded_path_scan.py` or `python -m llm_context.toolbelt hardcoded-path-scan`  
**Output**: Lists hardcoded paths  
**Use Case**: Improve portability  
**Example Output**: `context_out/hardcoded-path-scan_YYYY-MM-DD_HHMMSS.md`

### sleep_call_scan.py
**Purpose**: Finds sleep() calls that may indicate timing issues  
**Command**: `python scripts/sleep_call_scan.py` or `python -m llm_context.toolbelt sleep-call-scan`  
**Output**: Lists sleep calls  
**Use Case**: Review timing dependencies  
**Example Output**: `context_out/sleep-call-scan_YYYY-MM-DD_HHMMSS.md`

---

## Code Quality Scanners

### tabs_scan.py
**Purpose**: Finds files using tabs instead of spaces  
**Command**: `python scripts/tabs_scan.py` or `python -m llm_context.toolbelt tabs-scan`  
**Output**: Lists files with tab characters  
**Use Case**: Enforce consistent indentation  
**Example Output**: `context_out/tabs-scan_YYYY-MM-DD_HHMMSS.md`

### mixed_indent_scan.py
**Purpose**: Finds files mixing tabs and spaces  
**Command**: `python scripts/mixed_indent_scan.py` or `python -m llm_context.toolbelt mixed-indent-scan`  
**Output**: Lists files with mixed indentation  
**Use Case**: Fix inconsistent formatting  
**Example Output**: `context_out/mixed-indent-scan_YYYY-MM-DD_HHMMSS.md`

### trailing_whitespace_scan.py
**Purpose**: Finds trailing whitespace in lines  
**Command**: `python scripts/trailing_whitespace_scan.py` or `python -m llm_context.toolbelt trailing-whitespace-scan`  
**Output**: Lists lines with trailing whitespace  
**Use Case**: Clean up formatting  
**Example Output**: `context_out/trailing-whitespace-scan_YYYY-MM-DD_HHMMSS.md`

### trailing_empty_lines_scan.py
**Purpose**: Finds files with trailing empty lines  
**Command**: `python scripts/trailing_empty_lines_scan.py` or `python -m llm_context.toolbelt trailing-empty-lines-scan`  
**Output**: Lists files with trailing empty lines  
**Use Case**: Standardize file endings  
**Example Output**: `context_out/trailing-empty-lines-scan_YYYY-MM-DD_HHMMSS.md`

### newline_consistency_scan.py
**Purpose**: Checks for consistent line ending styles  
**Command**: `python scripts/newline_consistency_scan.py` or `python -m llm_context.toolbelt newline-consistency-scan`  
**Output**: Lists files with inconsistent line endings  
**Use Case**: Ensure cross-platform compatibility  
**Example Output**: `context_out/newline-consistency-scan_YYYY-MM-DD_HHMMSS.md`

### utf_bom_scan.py
**Purpose**: Finds files with UTF-8 BOM markers  
**Command**: `python scripts/utf_bom_scan.py` or `python -m llm_context.toolbelt utf-bom-scan`  
**Output**: Lists files with BOM  
**Use Case**: Remove problematic byte order marks  
**Example Output**: `context_out/utf-bom-scan_YYYY-MM-DD_HHMMSS.md`

### non_ascii_scan.py
**Purpose**: Finds non-ASCII characters in code  
**Command**: `python scripts/non_ascii_scan.py` or `python -m llm_context.toolbelt non-ascii-scan`  
**Output**: Lists non-ASCII characters  
**Use Case**: Ensure ASCII compatibility  
**Example Output**: `context_out/non-ascii-scan_YYYY-MM-DD_HHMMSS.md`

### shebang_scan.py
**Purpose**: Checks shebang lines in scripts  
**Command**: `python scripts/shebang_scan.py` or `python -m llm_context.toolbelt shebang-scan`  
**Output**: Lists shebang inconsistencies  
**Use Case**: Ensure proper script execution  
**Example Output**: `context_out/shebang-scan_YYYY-MM-DD_HHMMSS.md`

### magic_number_scan.py
**Purpose**: Finds magic numbers in code  
**Command**: `python scripts/magic_number_scan.py` or `python -m llm_context.toolbelt magic-number-scan`  
**Output**: Lists numeric literals  
**Use Case**: Replace with named constants  
**Example Output**: `context_out/magic-number-scan_YYYY-MM-DD_HHMMSS.md`

### commented_out_code_scan.py
**Purpose**: Finds commented-out code blocks  
**Command**: `python scripts/commented_out_code_scan.py` or `python -m llm_context.toolbelt commented-out-code-scan`  
**Output**: Lists commented code  
**Use Case**: Clean up dead code  
**Example Output**: `context_out/commented-out-code-scan_YYYY-MM-DD_HHMMSS.md`

### deprecated_api_scan.py
**Purpose**: Finds usage of deprecated APIs  
**Command**: `python scripts/deprecated_api_scan.py` or `python -m llm_context.toolbelt deprecated-api-scan`  
**Output**: Lists deprecated API calls  
**Use Case**: Modernize codebase  
**Example Output**: `context_out/deprecated-api-scan_YYYY-MM-DD_HHMMSS.md`

### annotation_scan.py
**Purpose**: Finds special annotations in code  
**Command**: `python scripts/annotation_scan.py` or `python -m llm_context.toolbelt annotation-scan`  
**Output**: Lists annotations like @deprecated, @todo  
**Use Case**: Track annotated code  
**Example Output**: `context_out/annotation-scan_YYYY-MM-DD_HHMMSS.md`

---

## Project Analysis Tools

### license_detect.py
**Purpose**: Detects license information in files  
**Command**: `python scripts/license_detect.py` or `python -m llm_context.toolbelt license-detect`  
**Output**: Lists detected licenses  
**Use Case**: Audit licensing compliance  
**Example Output**: `context_out/license-detect_YYYY-MM-DD_HHMMSS.md`

### license_header_missing_scan.py
**Purpose**: Finds files missing license headers  
**Command**: `python scripts/license_header_missing_scan.py` or `python -m llm_context.toolbelt license-header-missing-scan`  
**Output**: Lists files without license headers  
**Use Case**: Ensure licensing compliance  
**Example Output**: `context_out/license-header-missing-scan_YYYY-MM-DD_HHMMSS.md`

### env_var_scan.py
**Purpose**: Finds environment variable usage  
**Command**: `python scripts/env_var_scan.py` or `python -m llm_context.toolbelt env-var-scan`  
**Output**: Lists environment variable references  
**Use Case**: Document configuration requirements  
**Example Output**: `context_out/env-var-scan_YYYY-MM-DD_HHMMSS.md`

### test_file_scan.py
**Purpose**: Identifies test files in the project  
**Command**: `python scripts/test_file_scan.py` or `python -m llm_context.toolbelt test-file-scan`  
**Output**: Lists test files  
**Use Case**: Analyze test coverage  
**Example Output**: `context_out/test-file-scan_YYYY-MM-DD_HHMMSS.md`

### version_number_scan.py
**Purpose**: Finds version numbers in code and configs  
**Command**: `python scripts/version_number_scan.py` or `python -m llm_context.toolbelt version-number-scan`  
**Output**: Lists version references  
**Use Case**: Track version consistency  
**Example Output**: `context_out/version-number-scan_YYYY-MM-DD_HHMMSS.md`

### pinned_versions_scan.py
**Purpose**: Checks if dependencies use pinned versions  
**Command**: `python scripts/pinned_versions_scan.py` or `python -m llm_context.toolbelt pinned-versions-scan`  
**Output**: Lists unpinned dependencies  
**Use Case**: Improve build reproducibility  
**Example Output**: `context_out/pinned-versions-scan_YYYY-MM-DD_HHMMSS.md`

### dir_tree_to_md.py
**Purpose**: Generates directory tree visualization  
**Command**: `python scripts/dir_tree_to_md.py` or `python -m llm_context.toolbelt dir-tree-to-md`  
**Output**: Tree structure of directories  
**Use Case**: Document project structure  
**Example Output**: `context_out/dir-tree-to-md_YYYY-MM-DD_HHMMSS.md`

### file_index.py
**Purpose**: Creates searchable index of all files  
**Command**: `python scripts/file_index.py` or `python -m llm_context.toolbelt file-index`  
**Output**: Complete file listing with metadata  
**Use Case**: Navigate large codebases  
**Example Output**: `context_out/file-index_YYYY-MM-DD_HHMMSS.md`

### dir_size_report.py
**Purpose**: Analyzes directory sizes  
**Command**: `python scripts/dir_size_report.py` or `python -m llm_context.toolbelt dir-size-report`  
**Output**: Directory sizes sorted by size  
**Use Case**: Find space usage  
**Example Output**: `context_out/dir-size-report_YYYY-MM-DD_HHMMSS.md`

### extension_inventory.py
**Purpose**: Lists all file extensions in project  
**Command**: `python scripts/extension_inventory.py` or `python -m llm_context.toolbelt extension-inventory`  
**Output**: File extension counts  
**Use Case**: Understand project composition  
**Example Output**: `context_out/extension-inventory_YYYY-MM-DD_HHMMSS.md`

### binary_file_inventory.py
**Purpose**: Lists all binary files  
**Command**: `python scripts/binary_file_inventory.py` or `python -m llm_context.toolbelt binary-file-inventory`  
**Output**: Binary files with sizes  
**Use Case**: Track non-text files  
**Example Output**: `context_out/binary-file-inventory_YYYY-MM-DD_HHMMSS.md`

### image_inventory.py
**Purpose**: Lists all image files with metadata  
**Command**: `python scripts/image_inventory.py` or `python -m llm_context.toolbelt image-inventory`  
**Output**: Image files with dimensions and sizes  
**Use Case**: Manage image assets  
**Example Output**: `context_out/image-inventory_YYYY-MM-DD_HHMMSS.md`

### recent_files_report.py
**Purpose**: Lists recently modified files  
**Command**: `python scripts/recent_files_report.py` or `python -m llm_context.toolbelt recent-files-report`  
**Output**: Files modified in specified timeframe  
**Use Case**: Track recent changes  
**Example Output**: `context_out/recent-files-report_YYYY-MM-DD_HHMMSS.md`

### file_age_report.py
**Purpose**: Shows oldest and newest files  
**Command**: `python scripts/file_age_report.py` or `python -m llm_context.toolbelt file-age-report`  
**Output**: Files sorted by modification time  
**Use Case**: Identify stale files  
**Example Output**: `context_out/file-age-report_YYYY-MM-DD_HHMMSS.md`

### changelog_summary.py
**Purpose**: Summarizes CHANGELOG content  
**Command**: `python scripts/changelog_summary.py` or `python -m llm_context.toolbelt changelog-summary`  
**Output**: Parsed changelog entries  
**Use Case**: Review project history  
**Example Output**: `context_out/changelog-summary_YYYY-MM-DD_HHMMSS.md`

---

## NEW: Production-Ready Utility Scripts

### api_response_validator.py
**Purpose**: Validates API response formats in JSON files  
**Command**: `python scripts/api_response_validator.py` or `python -m llm_context.toolbelt api-response-validator`  
**Output**: Lists validation issues in API responses  
**Use Case**: Ensure API responses follow consistent patterns  
**Example Output**: `context_out/api-response-validator_YYYY-MM-DD_HHMMSS.md`

### config_validator.py
**Purpose**: Validates configuration files (JSON, YAML) for common issues  
**Command**: `python scripts/config_validator.py` or `python -m llm_context.toolbelt config-validator`  
**Output**: Lists configuration validation errors  
**Use Case**: Catch config file errors before deployment  
**Example Output**: `context_out/config-validator_YYYY-MM-DD_HHMMSS.md`

### dependency_tree_analyzer.py
**Purpose**: Analyzes project dependencies from package.json and requirements.txt  
**Command**: `python scripts/dependency_tree_analyzer.py` or `python -m llm_context.toolbelt dependency-tree-analyzer`  
**Output**: Complete dependency tree with versions  
**Use Case**: Audit and document project dependencies  
**Example Output**: `context_out/dependency-tree-analyzer_YYYY-MM-DD_HHMMSS.md`

### git_commit_linter.py
**Purpose**: Analyzes git commit messages for conventional commit compliance  
**Command**: `python scripts/git_commit_linter.py` or `python -m llm_context.toolbelt git-commit-linter`  
**Output**: Lists commits that don't follow conventional commit format  
**Use Case**: Maintain consistent commit message standards  
**Example Output**: `context_out/git-commit-linter_YYYY-MM-DD_HHMMSS.md`

### code_complexity_calculator.py
**Purpose**: Calculates cyclomatic complexity for functions  
**Command**: `python scripts/code_complexity_calculator.py` or `python -m llm_context.toolbelt code-complexity-calculator`  
**Output**: Functions ranked by complexity  
**Use Case**: Identify functions that need refactoring  
**Example Output**: `context_out/code-complexity-calculator_YYYY-MM-DD_HHMMSS.md`

### performance_profiler_report.py
**Purpose**: Identifies performance anti-patterns in code  
**Command**: `python scripts/performance_profiler_report.py` or `python -m llm_context.toolbelt performance-profiler-report`  
**Output**: Lists potential performance issues  
**Use Case**: Optimize application performance  
**Example Output**: `context_out/performance-profiler-report_YYYY-MM-DD_HHMMSS.md`

### test_coverage_analyzer.py
**Purpose**: Analyzes test coverage patterns and test-to-source ratio  
**Command**: `python scripts/test_coverage_analyzer.py` or `python -m llm_context.toolbelt test-coverage-analyzer`  
**Output**: Test coverage statistics and file lists  
**Use Case**: Ensure adequate test coverage  
**Example Output**: `context_out/test-coverage-analyzer_YYYY-MM-DD_HHMMSS.md`

### dockerfile_analyzer.py
**Purpose**: Analyzes Dockerfile for best practices and security  
**Command**: `python scripts/dockerfile_analyzer.py` or `python -m llm_context.toolbelt dockerfile-analyzer`  
**Output**: Dockerfile best practices and issues  
**Use Case**: Improve container security and efficiency  
**Example Output**: `context_out/dockerfile-analyzer_YYYY-MM-DD_HHMMSS.md`

### env_validator.py
**Purpose**: Validates environment variable usage against .env files  
**Command**: `python scripts/env_validator.py` or `python -m llm_context.toolbelt env-validator`  
**Output**: Lists undefined and unused environment variables  
**Use Case**: Prevent runtime configuration errors  
**Example Output**: `context_out/env-validator_YYYY-MM-DD_HHMMSS.md`

### api_endpoint_inventory.py
**Purpose**: Inventories all API endpoints in the codebase  
**Command**: `python scripts/api_endpoint_inventory.py` or `python -m llm_context.toolbelt api-endpoint-inventory`  
**Output**: Complete list of API routes by HTTP method  
**Use Case**: Document API surface area  
**Example Output**: `context_out/api-endpoint-inventory_YYYY-MM-DD_HHMMSS.md`

### database_schema_analyzer.py
**Purpose**: Analyzes database schema definitions and migrations  
**Command**: `python scripts/database_schema_analyzer.py` or `python -m llm_context.toolbelt database-schema-analyzer`  
**Output**: Lists tables/models and migration files  
**Use Case**: Document database structure  
**Example Output**: `context_out/database-schema-analyzer_YYYY-MM-DD_HHMMSS.md`

### log_analyzer.py
**Purpose**: Analyzes log files and logging patterns in code  
**Command**: `python scripts/log_analyzer.py` or `python -m llm_context.toolbelt log-analyzer`  
**Output**: Log file sizes and logging call patterns  
**Use Case**: Optimize logging strategy  
**Example Output**: `context_out/log-analyzer_YYYY-MM-DD_HHMMSS.md`

### resource_monitor.py
**Purpose**: Monitors resource usage patterns (files, memory, threads)  
**Command**: `python scripts/resource_monitor.py` or `python -m llm_context.toolbelt resource-monitor`  
**Output**: Lists potential resource leaks and issues  
**Use Case**: Prevent resource exhaustion  
**Example Output**: `context_out/resource-monitor_YYYY-MM-DD_HHMMSS.md`

### code_duplication_detector.py
**Purpose**: Detects duplicated code blocks across the codebase  
**Command**: `python scripts/code_duplication_detector.py` or `python -m llm_context.toolbelt code-duplication-detector`  
**Output**: Groups of similar/duplicate functions  
**Use Case**: Identify refactoring opportunities  
**Example Output**: `context_out/code-duplication-detector_YYYY-MM-DD_HHMMSS.md`

### security_headers_checker.py
**Purpose**: Checks for security headers in web applications  
**Command**: `python scripts/security_headers_checker.py` or `python -m llm_context.toolbelt security-headers-checker`  
**Output**: Lists found and missing security headers  
**Use Case**: Harden web application security  
**Example Output**: `context_out/security-headers-checker_YYYY-MM-DD_HHMMSS.md`

---

## Configuration File Converters

### requirements_to_md.py
**Purpose**: Converts requirements.txt to Markdown  
**Command**: `python scripts/requirements_to_md.py` or `python -m llm_context.toolbelt requirements-to-md`  
**Output**: Python dependencies as Markdown  
**Use Case**: Document Python dependencies  
**Example Output**: `context_out/requirements-to-md_YYYY-MM-DD_HHMMSS.md`

### package_json_to_md.py
**Purpose**: Converts package.json to Markdown  
**Command**: `python scripts/package_json_to_md.py` or `python -m llm_context.toolbelt package-json-to-md`  
**Output**: Node.js dependencies as Markdown  
**Use Case**: Document Node.js dependencies  
**Example Output**: `context_out/package-json-to-md_YYYY-MM-DD_HHMMSS.md`

### pyproject_to_md.py
**Purpose**: Converts pyproject.toml to Markdown  
**Command**: `python scripts/pyproject_to_md.py` or `python -m llm_context.toolbelt pyproject-to-md`  
**Output**: Python project config as Markdown  
**Use Case**: Document project configuration  
**Example Output**: `context_out/pyproject-to-md_YYYY-MM-DD_HHMMSS.md`

### ini_to_md.py
**Purpose**: Converts INI files to Markdown  
**Command**: `python scripts/ini_to_md.py` or `python -m llm_context.toolbelt ini-to-md`  
**Output**: INI config as Markdown  
**Use Case**: Document INI configurations  
**Example Output**: `context_out/ini-to-md_YYYY-MM-DD_HHMMSS.md`

### toml_to_md.py
**Purpose**: Converts TOML files to Markdown  
**Command**: `python scripts/toml_to_md.py` or `python -m llm_context.toolbelt toml-to-md`  
**Output**: TOML config as Markdown  
**Use Case**: Document TOML configurations  
**Example Output**: `context_out/toml-to-md_YYYY-MM-DD_HHMMSS.md`

### properties_to_md.py
**Purpose**: Converts .properties files to Markdown  
**Command**: `python scripts/properties_to_md.py` or `python -m llm_context.toolbelt properties-to-md`  
**Output**: Java properties as Markdown  
**Use Case**: Document Java configurations  
**Example Output**: `context_out/properties-to-md_YYYY-MM-DD_HHMMSS.md`

### gitignore_to_md.py
**Purpose**: Converts .gitignore to Markdown  
**Command**: `python scripts/gitignore_to_md.py` or `python -m llm_context.toolbelt gitignore-to-md`  
**Output**: .gitignore content as Markdown  
**Use Case**: Document ignored files  
**Example Output**: `context_out/gitignore-to-md_YYYY-MM-DD_HHMMSS.md`

### editorconfig_to_md.py
**Purpose**: Converts .editorconfig to Markdown  
**Command**: `python scripts/editorconfig_to_md.py` or `python -m llm_context.toolbelt editorconfig-to-md`  
**Output**: Editor config as Markdown  
**Use Case**: Document editor settings  
**Example Output**: `context_out/editorconfig-to-md_YYYY-MM-DD_HHMMSS.md`

### license_to_md.py
**Purpose**: Converts LICENSE file to Markdown  
**Command**: `python scripts/license_to_md.py` or `python -m llm_context.toolbelt license-to-md`  
**Output**: License text as Markdown  
**Use Case**: Include license in documentation  
**Example Output**: `context_out/license-to-md_YYYY-MM-DD_HHMMSS.md`

---

## Syntax Validators

### yaml_syntax_scan.py
**Purpose**: Validates YAML file syntax  
**Command**: `python scripts/yaml_syntax_scan.py` or `python -m llm_context.toolbelt yaml-syntax-scan`  
**Output**: Lists YAML syntax errors  
**Use Case**: Validate configuration files  
**Example Output**: `context_out/yaml-syntax-scan_YYYY-MM-DD_HHMMSS.md`

### json_syntax_scan.py
**Purpose**: Validates JSON file syntax  
**Command**: `python scripts/json_syntax_scan.py` or `python -m llm_context.toolbelt json-syntax-scan`  
**Output**: Lists JSON syntax errors  
**Use Case**: Validate data files  
**Example Output**: `context_out/json-syntax-scan_YYYY-MM-DD_HHMMSS.md`

### xml_syntax_scan.py
**Purpose**: Validates XML file syntax  
**Command**: `python scripts/xml_syntax_scan.py` or `python -m llm_context.toolbelt xml-syntax-scan`  
**Output**: Lists XML syntax errors  
**Use Case**: Validate XML documents  
**Example Output**: `context_out/xml-syntax-scan_YYYY-MM-DD_HHMMSS.md`

### html_syntax_scan.py
**Purpose**: Validates HTML file syntax  
**Command**: `python scripts/html_syntax_scan.py` or `python -m llm_context.toolbelt html-syntax-scan`  
**Output**: Lists HTML syntax errors  
**Use Case**: Validate HTML documents  
**Example Output**: `context_out/html-syntax-scan_YYYY-MM-DD_HHMMSS.md`

---

## Test and Build Tools

### junit_xml_to_md.py
**Purpose**: Converts JUnit XML test results to Markdown  
**Command**: `python scripts/junit_xml_to_md.py` or `python -m llm_context.toolbelt junit-xml-to-md`  
**Output**: Test results formatted as Markdown  
**Use Case**: Document test results  
**Example Output**: `context_out/junit-xml-to-md_YYYY-MM-DD_HHMMSS.md`

---

## Template Generators

### template_gen.py
**Purpose**: Generates various document templates  
**Command**: `python scripts/template_gen.py` or `python -m llm_context.toolbelt template-gen --name <template>`  
**Available Templates**:
- `issue` - GitHub issue template
- `pr` - Pull request template
- `bug-report` - Bug report template
- `feature-request` - Feature request template
- `code-review-checklist` - Code review checklist
- `security-report` - Security report template
- `release-notes` - Release notes template
- `testing-plan` - Testing plan template
- `adr` - Architecture decision record
- `contributing` - Contributing guidelines
- `roadmap` - Project roadmap
- `design-doc` - Design document
- `api-spec` - API specification
- `sprint-planning` - Sprint planning template
- `meeting-notes` - Meeting notes template
**Use Case**: Standardize project documentation  
**Example Output**: `context_out/template-<name>_YYYY-MM-DD_HHMMSS.md`

---

## Advanced Analysis Tools

### metadata_pack.py
**Purpose**: Generates comprehensive metadata about the project  
**Command**: `python scripts/metadata_pack.py` or `python -m llm_context.toolbelt metadata-pack`  
**Output**: Complete project metadata bundle  
**Use Case**: Create project snapshot  
**Example Output**: `context_out/metadata-pack_YYYY-MM-DD_HHMMSS.md`

### prompt_pack.py
**Purpose**: Creates LLM-optimized context packages  
**Command**: `python scripts/prompt_pack.py` or `python -m llm_context.toolbelt prompt-pack`  
**Output**: Formatted context for LLM prompts  
**Use Case**: Generate AI-ready documentation  
**Example Output**: `context_out/prompt-pack_YYYY-MM-DD_HHMMSS.md`

### chunk.py
**Purpose**: Splits large files into manageable chunks  
**Command**: `python scripts/chunk.py` or `python -m llm_context.toolbelt chunk`  
**Output**: File chunks with specified size  
**Use Case**: Process large files  
**Example Output**: `context_out/chunk_YYYY-MM-DD_HHMMSS.md`

### token_estimate.py
**Purpose**: Estimates token count for LLM processing  
**Command**: `python scripts/token_estimate.py` or `python -m llm_context.toolbelt token-estimate`  
**Output**: Token count estimates by file  
**Use Case**: Plan LLM API usage  
**Example Output**: `context_out/token-estimate_YYYY-MM-DD_HHMMSS.md`

### json_schema_extract.py
**Purpose**: Extracts JSON schemas from files  
**Command**: `python scripts/json_schema_extract.py` or `python -m llm_context.toolbelt json-schema-extract`  
**Output**: JSON schema definitions  
**Use Case**: Document data structures  
**Example Output**: `context_out/json-schema-extract_YYYY-MM-DD_HHMMSS.md`

### api_spec_from_openapi.py
**Purpose**: Converts OpenAPI specs to readable Markdown  
**Command**: `python scripts/api_spec_from_openapi.py` or `python -m llm_context.toolbelt api-spec-from-openapi`  
**Output**: API documentation from OpenAPI/Swagger  
**Use Case**: Generate API documentation  
**Example Output**: `context_out/api-spec-from-openapi_YYYY-MM-DD_HHMMSS.md`

---

## Usage Examples

### Basic Usage
```bash
# Scan for TODO comments
python scripts/todo_scan.py

# Convert JSON files to Markdown
python scripts/json_to_md.py

# Check Python syntax
python scripts/syntax_scan_py.py
```

### Using the Unified CLI
```bash
# Scan for secrets
python -m llm_context.toolbelt secret-scan --path /path/to/project

# Generate directory tree
python -m llm_context.toolbelt dir-tree-to-md --path /path/to/project

# Create bug report template
python -m llm_context.toolbelt template-gen --name bug-report
```

### Combining Multiple Scans
```bash
# Run multiple scanners for comprehensive analysis
python scripts/todo_scan.py
python scripts/fixme_scan.py
python scripts/bug_scan.py
python scripts/secret_scan.py
```

---

## Output Format

All scripts generate output in the `context_out/` directory with timestamped filenames:
- Format: `<script-name>_YYYY-MM-DD_HHMMSS.md`
- Example: `todo-scan_2026-01-08_041900.md`

The output files are formatted in Markdown for easy reading and integration into documentation.

---

## Best Practices

1. **Run regularly**: Schedule regular scans as part of CI/CD pipeline
2. **Review outputs**: Regularly review scan results to maintain code quality
3. **Combine scans**: Use multiple related scans for comprehensive analysis
4. **Archive results**: Keep historical scan results to track improvements
5. **Automate**: Integrate into pre-commit hooks or CI workflows

---

## Troubleshooting

### Module Not Found Error
If you get `ModuleNotFoundError: No module named 'llm_context'`, run scripts from the repository root:
```bash
cd /path/to/Script-Toolkit
python scripts/todo_scan.py
```

### Large Repositories
For very large repositories, some scans may take time. Consider:
- Using `--path` to scan specific directories
- Running scans in parallel
- Excluding directories using .gitignore patterns

### Output Directory
All outputs go to `context_out/`. Create this directory if it doesn't exist:
```bash
mkdir -p context_out
```

---

## Contributing

To add a new script:
1. Implement the command function in `llm_context/toolbelt.py`
2. Register it in the argument parser
3. Create a wrapper script in `scripts/`
4. Update this documentation

---

*Last Updated: 2026-01-08*
