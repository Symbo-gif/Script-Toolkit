# Contributing to Script Toolkit

Thank you for your interest in contributing to Script Toolkit! This document provides guidelines for adding new scripts and improving existing ones.

## How to Add a New Script

Adding a new script involves 4 steps:

### 1. Implement the Command Function

Add your command function to `llm_context/toolbelt.py`. Place it in the appropriate section based on its purpose (scanners, converters, analyzers, etc.).

```python
def cmd_your_new_script(path: str) -> str:
    """
    Brief description of what the script does.
    
    Args:
        path: Base path to scan
        
    Returns:
        Formatted markdown output
    """
    out = [md_h1("Your Script Title")]
    
    # Your implementation here
    for fp, rel in iter_files(path, include_exts={".py", ".js"}):
        text = read_text_safe(fp)
        if text:
            # Process the file
            pass
    
    # Build output
    out.append("Results go here\n")
    
    return "".join(out)
```

### 2. Register the Command in the Argument Parser

In the `main()` function, add your command to the argument parser:

```python
def main(argv: Optional[List[str]] = None) -> int:
    # ... existing code ...
    
    # Add your command
    add_path_arg(sub.add_parser("your-new-script"))
    
    # If your script needs additional arguments:
    p = sub.add_parser("your-new-script")
    add_path_arg(p)
    p.add_argument("--threshold", type=int, default=100)
```

### 3. Add the Command Handler

In the main() function's command dispatcher, add your handler:

```python
elif args.cmd == "your-new-script":
    content = cmd_your_new_script(args.path)
    out = report_path("your-new-script")
```

### 4. Create the Wrapper Script

Create a wrapper script in `scripts/`:

```python
#!/usr/bin/env python3
# scripts/your_new_script.py
import sys
from llm_context.toolbelt import run_from_wrapper

if __name__ == "__main__":
    run_from_wrapper("your-new-script", sys.argv[1:])
```

**Note**: Use underscores in the filename, but hyphens in the command name.

### 5. Document Your Script

Add documentation to `SCRIPTS.md`:

```markdown
### your_new_script.py
**Purpose**: Brief description  
**Command**: `python scripts/your_new_script.py` or `python -m llm_context.toolbelt your-new-script`  
**Output**: Description of output  
**Use Case**: When to use this script  
**Example Output**: `context_out/your-new-script_YYYY-MM-DD_HHMMSS.md`
```

## Coding Standards

### Function Naming
- Command functions: `cmd_your_function_name()`
- Use snake_case for function names
- Use descriptive names that indicate what the function does

### Output Format
- Always use Markdown for output
- Start with an h1 heading: `md_h1("Title")`
- Use h2 for subsections: `md_h2("Subsection")`
- Use code blocks for code: `md_codeblock(text)`
- Use lists with `-` for items

### Error Handling
- Use try-except blocks for file operations
- Don't let exceptions crash the entire scan
- Continue processing other files if one fails
- Report errors in the output when appropriate

### Performance
- Use `iter_files()` for file iteration
- Use `read_text_safe()` for reading files
- Respect the `DEFAULT_EXCLUDE_DIRS` patterns
- Don't process binary files unless necessary
- Limit output for large results

### Example: Well-Structured Command Function

```python
def cmd_example_scanner(path: str, threshold: int = 100) -> str:
    """
    Scans for specific patterns in code files.
    
    Args:
        path: Base directory to scan
        threshold: Minimum threshold for reporting
        
    Returns:
        Markdown-formatted report
    """
    out = [md_h1("Example Scanner Report")]
    issues = []
    
    # Process files
    for fp, rel in iter_files(path, include_exts={".py", ".js", ".ts"}):
        text = read_text_safe(fp)
        if not text:
            continue
            
        try:
            lines = text.splitlines()
            for i, line in enumerate(lines, 1):
                # Check for pattern
                if "pattern" in line.lower():
                    issues.append((rel, i, line.strip()))
        except Exception as e:
            # Log but don't fail
            continue
    
    # Generate output
    if issues:
        out.append(md_h2(f"Found {len(issues)} Issues"))
        for rel, line_num, line_text in issues[:50]:  # Limit output
            out.append(f"- {rel}:{line_num} `{line_text[:60]}`\n")
    else:
        out.append("No issues found.\n")
    
    return "".join(out)
```

## Testing Your Script

### Manual Testing
```bash
# From repository root
cd /path/to/Script-Toolkit

# Test using CLI
python -m llm_context.toolbelt your-new-script --path .

# Test wrapper script
python scripts/your_new_script.py

# Check output
cat context_out/your-new-script_*.md
```

### Testing Checklist
- [ ] Script runs without errors
- [ ] Output is properly formatted Markdown
- [ ] Script handles missing files gracefully
- [ ] Script respects excluded directories
- [ ] Output is limited for large results
- [ ] Documentation is complete
- [ ] Script name follows conventions

## Script Categories

When adding a new script, place it in the appropriate category:

### Scanners
Scripts that scan code for specific patterns, issues, or annotations.
Examples: `todo_scan.py`, `secret_scan.py`, `syntax_scan_py.py`

### Analyzers
Scripts that analyze code structure, complexity, or metrics.
Examples: `code_complexity_calculator.py`, `test_coverage_analyzer.py`

### Converters
Scripts that convert between file formats.
Examples: `json_to_md.py`, `csv_to_md.py`

### Validators
Scripts that validate configurations or compliance.
Examples: `config_validator.py`, `env_validator.py`

### Inventories
Scripts that create inventories or lists of resources.
Examples: `api_endpoint_inventory.py`, `file_index.py`

## Best Practices

### Do's
✅ Use standard library only (no external dependencies)  
✅ Return Markdown-formatted output  
✅ Handle errors gracefully  
✅ Limit output for large results  
✅ Include meaningful statistics  
✅ Document all parameters  
✅ Use descriptive variable names  
✅ Follow existing code style  

### Don'ts
❌ Don't add external dependencies  
❌ Don't crash on single file errors  
❌ Don't process binary files unnecessarily  
❌ Don't generate unlimited output  
❌ Don't modify files (read-only operations)  
❌ Don't use print statements (return strings)  
❌ Don't ignore excluded directories  

## Utility Functions Available

The toolbelt provides several utility functions:

```python
# File iteration
iter_files(base: str, include_exts: Optional[Iterable[str]] = None)

# Safe file reading
read_text_safe(path: str, max_bytes: int = 2_000_000)

# Markdown formatting
md_h1(text: str) -> str
md_h2(text: str) -> str
md_h3(text: str) -> str
md_codeblock(text: str, lang: str = "") -> str

# Output management
report_path(name: str, ext: str = "md") -> str
write_text(path: str, content: str) -> None

# Path utilities
safe_relpath(path: str, base: str) -> str

# Time utilities
now_stamp() -> str  # Returns YYYY-MM-DD_HHMMSS
```

## Pull Request Guidelines

When submitting a PR:

1. **Title**: Use descriptive title (e.g., "Add database migration analyzer script")
2. **Description**: Explain what the script does and why it's useful
3. **Testing**: Include evidence that the script works
4. **Documentation**: Ensure SCRIPTS.md is updated
5. **Examples**: Add usage examples if applicable

## Questions or Issues?

- Check existing scripts for examples
- Read the [main documentation](SCRIPTS.md)
- Open an issue for questions
- Review closed PRs for examples

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to Script Toolkit! 🎉
