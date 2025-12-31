LLM Context Toolbelt — 80+ Ready-to-Run Scripts

Overview

This repository now includes a lightweight, dependency-free toolbelt for generating LLM-friendly context from your codebase. It ships with 80+ small scripts covering scanners, converters, and template generators. All outputs are saved to the context_out directory as Markdown or text files, designed to be copy-paste friendly for prompts.

How it works

- Each script in the scripts directory runs a specific task and writes a timestamped report into context_out/.
- All scripts are thin wrappers around a single core engine at llm_context/toolbelt.py.
- No external dependencies are required; only the Python standard library is used.

Quick start

1) Ensure you have Python 3.8+ installed.
2) Run any script from the scripts directory. Examples:

- python scripts/todo_scan.py
- python scripts/syntax_scan_py.py
- python scripts/json_to_md.py
- python scripts/template_issue.py

3) Find the generated report in context_out/.

Notes

- By default, scripts scan the current directory (.). You can override with --path PATH when using the unified CLI in llm_context/toolbelt.py directly.
- The toolbelt avoids hidden and vendor directories like .git, node_modules, .venv, dist, build, and __pycache__ by default.

Unified CLI (optional)

You can also use the single unified CLI directly:

- python -m llm_context.toolbelt --help
- python -m llm_context.toolbelt todo-scan --path .
- python -m llm_context.toolbelt json-to-md --path .
- python -m llm_context.toolbelt template-gen --name issue

Included commands (by category)

Scanners

1. todo-scan
2. fixme-scan
3. error-scan
4. bug-scan
5. secret-scan
6. code-stats
7. comment-summary
8. long-func-scan
9. miss-docstring-scan
10. duplicate-line-scan
11. large-file-scan
12. syntax-scan-py
13. env-var-scan
14. license-detect
15. link-check-md
16. test-file-scan
17. deprecated-api-scan
18. print-debug-scan
19. magic-number-scan
20. tabs-scan
21. trailing-whitespace-scan
22. utf-bom-scan
23. non-ascii-scan
24. newline-consistency-scan

Converters and reporters

25. json-to-md
26. csv-to-md
27. md-to-txt
28. txt-to-md
29. code-to-md
30. requirements-to-md
31. package-json-to-md
32. junit-xml-to-md
33. dir-tree-to-md
34. file-index
35. changelog-summary
36. readme-summary
37. metadata-pack
38. prompt-pack
39. chunk
40. token-estimate
41. image-inventory
42. dir-size-report
43. csv-summary
44. json-schema-extract
45. api-spec-from-openapi

Template generators

46. template-issue
47. template-pr
48. template-bug-report
49. template-feature-request
50. template-code-review-checklist
51. template-security-report
52. template-release-notes
53. template-testing-plan
54. template-adr
55. template-contributing
56. template-roadmap
57. template-design-doc
58. template-api-spec
59. template-sprint-planning
60. template-meeting-notes

Output location

All outputs are saved to context_out/ with timestamps, e.g., context_out/todo-scan_2025-12-30_2302.md

Customization

Invoke the unified CLI directly for extra parameters (e.g., thresholds). Each subcommand provides --help.

License

No license is defined in this repository. Add one if needed.
