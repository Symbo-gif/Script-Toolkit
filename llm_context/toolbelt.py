import argparse
import ast
import csv
import datetime as _dt
import fnmatch
import io
import json
import os
import platform
import re
import sys
import textwrap
import time
import traceback
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from typing import Iterable, Iterator, List, Optional, Tuple


# ----------------------------
# Core utilities
# ----------------------------

DEFAULT_EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "__pycache__",
    ".idea",
    ".vscode",
    ".pytest_cache",
    ".mypy_cache",
}

TEXT_EXTS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".css", ".scss", ".html", ".xml",
    ".json", ".md", ".rst", ".txt", ".csv", ".yml", ".yaml", ".toml", ".ini",
    ".java", ".kt", ".swift", ".go", ".rb", ".rs", ".cpp", ".c", ".h",
}

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp"}


def now_stamp() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")


def ensure_out_dir() -> str:
    out_dir = os.path.join(os.getcwd(), "context_out")
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def report_path(name: str, ext: str = "md") -> str:
    out_dir = ensure_out_dir()
    fname = f"{name}_{now_stamp()}.{ext}"
    return os.path.join(out_dir, fname)


def write_text(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def safe_relpath(path: str, base: str) -> str:
    try:
        return os.path.relpath(path, base)
    except Exception:
        return path


def is_binary_bytes(chunk: bytes) -> bool:
    if b"\0" in chunk:
        return True
    # Heuristic: if too many non-text bytes
    text_characters = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)))
    nontext = chunk.translate(None, text_characters)
    return float(len(nontext)) / max(1, len(chunk)) > 0.30


def read_text_safe(path: str, max_bytes: int = 2_000_000) -> Optional[str]:
    try:
        size = os.path.getsize(path)
        if size > max_bytes:
            return None
        with open(path, "rb") as f:
            data = f.read()
        if is_binary_bytes(data[:1024]):
            return None
        return data.decode("utf-8", errors="replace")
    except Exception:
        return None


def iter_files(base: str, include_exts: Optional[Iterable[str]] = None) -> Iterator[Tuple[str, str]]:
    base = os.path.abspath(base)
    for root, dirs, files in os.walk(base):
        # exclude dirs
        dirs[:] = [d for d in dirs if d not in DEFAULT_EXCLUDE_DIRS and not d.startswith('.')]
        for name in files:
            full = os.path.join(root, name)
            rel = safe_relpath(full, base)
            if include_exts is not None:
                ext = os.path.splitext(name)[1].lower()
                if ext not in include_exts:
                    continue
            yield full, rel


def md_h1(title: str) -> str:
    return f"# {title}\n\n"


def md_h2(title: str) -> str:
    return f"## {title}\n\n"


def md_codeblock(code: str, lang: str = "") -> str:
    if lang:
        return f"```{lang}\n{code}\n```\n\n"
    return f"```
{code}
```\n\n"


def estimate_tokens(text: str) -> int:
    # Naive char/token heuristic: ~4 chars/token (very rough)
    return max(1, int(len(text) / 4))


def _http_head(url: str, timeout: float = 5.0) -> Tuple[int, str]:
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.reason
    except Exception as e:
        return 0, str(e)


# ----------------------------
# Command implementations
# ----------------------------


def cmd_todo_scan(path: str) -> str:
    findings = []
    pat = re.compile(r"\bTODO\b", re.IGNORECASE)
    for fp, rel in iter_files(path):
        text = read_text_safe(fp)
        if text is None:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if pat.search(line):
                findings.append((rel, i, line.strip()))
    out = [md_h1("TODO Scan"), f"Scanned path: {path}\n\n", md_h2("Findings")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No TODOs found.\n")
    return "".join(out)


def cmd_fixme_scan(path: str) -> str:
    findings = []
    pat = re.compile(r"\bFIXME\b", re.IGNORECASE)
    for fp, rel in iter_files(path):
        text = read_text_safe(fp)
        if text is None:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if pat.search(line):
                findings.append((rel, i, line.strip()))
    out = [md_h1("FIXME Scan"), f"Scanned path: {path}\n\n", md_h2("Findings")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No FIXMEs found.\n")
    return "".join(out)


def cmd_error_scan(path: str) -> str:
    findings = []
    pats = [re.compile(r"\bERROR\b"), re.compile(r"\braise\b"), re.compile(r"\bException\b")]
    for fp, rel in iter_files(path):
        text = read_text_safe(fp)
        if text is None:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if any(p.search(line) for p in pats):
                findings.append((rel, i, line.strip()))
    out = [md_h1("Error Scanner"), md_h2("Findings")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No error patterns found.\n")
    return "".join(out)


def cmd_bug_scan(path: str) -> str:
    findings = []
    pats = [r"\bBUG\b", r"\bworkaround\b", r"\bhack\b", r"\bkludge\b"]
    comp = [re.compile(p, re.IGNORECASE) for p in pats]
    for fp, rel in iter_files(path):
        text = read_text_safe(fp)
        if text is None:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if any(p.search(line) for p in comp):
                findings.append((rel, i, line.strip()))
    out = [md_h1("Bug Scanner"), md_h2("Findings")]
    out.extend([f"- {rel}:{ln}: {line}\n" for rel, ln, line in findings])
    if not findings:
        out.append("No bug patterns found.\n")
    return "".join(out)


def cmd_secret_scan(path: str) -> str:
    findings = []
    patterns = [
        re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS Access Key
        re.compile(r"(?i)secret\s*[:=]\s*['\"][^'\"]+['\"]"),
        re.compile(r"(?i)password\s*[:=]\s*['\"][^'\"]+['\"]"),
        re.compile(r"(?i)token\s*[:=]\s*['\"][^'\"]+['\"]"),
        re.compile(r"(^|[^a-zA-Z0-9])[a-f0-9]{32}([^a-zA-Z0-9]|$)"),
    ]
    for fp, rel in iter_files(path):
        text = read_text_safe(fp)
        if text is None:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            for p in patterns:
                if p.search(line):
                    findings.append((rel, i, line.strip()))
                    break
    out = [md_h1("Secret Scanner"), md_h2("Potential Secrets")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No potential secrets found.\n")
    return "".join(out)


def cmd_code_stats(path: str) -> str:
    total_files = 0
    total_bytes = 0
    loc = 0
    by_ext = Counter()
    for fp, rel in iter_files(path):
        total_files += 1
        try:
            size = os.path.getsize(fp)
        except Exception:
            size = 0
        total_bytes += size
        ext = os.path.splitext(fp)[1].lower()
        by_ext[ext] += 1
        text = read_text_safe(fp)
        if text is not None:
            loc += text.count("\n") + 1 if text else 0
    out = [md_h1("Code Stats"), f"Path: {path}\n\n"]
    out.append(f"- Total files: {total_files}\n")
    out.append(f"- Total size: {total_bytes} bytes\n")
    out.append(f"- Estimated LOC: {loc}\n\n")
    out.append(md_h2("By Extension"))
    for ext, count in by_ext.most_common():
        out.append(f"- {ext or '(no ext)'}: {count}\n")
    return "".join(out)


def cmd_comment_summary(path: str) -> str:
    counts = Counter()
    for fp, rel in iter_files(path):
        text = read_text_safe(fp)
        if text is None:
            continue
        for line in text.splitlines():
            if "#" in line:
                counts['hash'] += 1
            if "//" in line:
                counts['slash'] += 1
            if "/*" in line:
                counts['block_open'] += 1
            if "*/" in line:
                counts['block_close'] += 1
    out = [md_h1("Comment Summary")]
    for k, v in counts.items():
        out.append(f"- {k}: {v}\n")
    if not counts:
        out.append("No comment markers found.\n")
    return "".join(out)


def _ast_funcs_with_spans(py_path: str) -> List[Tuple[str, int, int]]:
    text = read_text_safe(py_path)
    if text is None:
        return []
    try:
        tree = ast.parse(text)
    except Exception:
        return []
    funcs = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start = getattr(node, 'lineno', None)
            end = getattr(node, 'end_lineno', None)
            if start is not None and end is not None:
                funcs.append((node.name, start, end))
    return funcs


def cmd_long_func_scan(path: str, min_lines: int = 50) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts={".py"}):
        for name, start, end in _ast_funcs_with_spans(fp):
            ln = end - start + 1
            if ln >= min_lines:
                findings.append((rel, name, ln))
    out = [md_h1("Long Function Scanner"), f"Threshold: {min_lines} lines\n\n"]
    for rel, name, ln in sorted(findings, key=lambda x: (-x[2], x[0])):
        out.append(f"- {rel}::{name} — {ln} lines\n")
    if not findings:
        out.append("No long functions found.\n")
    return "".join(out)


def cmd_miss_docstring_scan(path: str) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if text is None:
            continue
        try:
            tree = ast.parse(text)
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if ast.get_docstring(node) is None:
                    name = getattr(node, 'name', '<anonymous>')
                    kind = type(node).__name__
                    findings.append((rel, kind, name))
    out = [md_h1("Missing Docstring Scanner")]
    for rel, kind, name in findings:
        out.append(f"- {rel}: {kind} {name} missing docstring\n")
    if not findings:
        out.append("All Python defs/classes have docstrings or none found.\n")
    return "".join(out)


def cmd_duplicate_line_scan(path: str, min_dupes: int = 3) -> str:
    out_lines = [md_h1("Duplicate Line Scanner"), f"Threshold: {min_dupes} occurrences\n\n"]
    for fp, rel in iter_files(path):
        text = read_text_safe(fp)
        if text is None:
            continue
        cnt = Counter([ln.rstrip() for ln in text.splitlines() if ln.strip()])
        dups = [(line, c) for line, c in cnt.items() if c >= min_dupes]
        if dups:
            out_lines.append(md_h2(rel))
            for line, c in sorted(dups, key=lambda x: -x[1]):
                out_lines.append(f"- ({c}x) {line[:120]}\n")
    if len(out_lines) == 2:
        out_lines.append("No duplicate lines detected above threshold.\n")
    return "".join(out_lines)


def cmd_large_file_scan(path: str, min_bytes: int = 1_000_000) -> str:
    findings = []
    for fp, rel in iter_files(path):
        try:
            size = os.path.getsize(fp)
        except Exception:
            size = 0
        if size >= min_bytes:
            findings.append((rel, size))
    out = [md_h1("Large File Scanner"), f"Threshold: {min_bytes} bytes\n\n"]
    for rel, size in sorted(findings, key=lambda x: -x[1]):
        out.append(f"- {rel} — {size} bytes\n")
    if not findings:
        out.append("No large files found.\n")
    return "".join(out)


def cmd_syntax_scan_py(path: str) -> str:
    problems = []
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if text is None:
            continue
        try:
            ast.parse(text)
        except SyntaxError as e:
            problems.append((rel, e.lineno or 0, e.msg))
        except Exception as e:
            problems.append((rel, 0, f"Parse error: {e}"))
    out = [md_h1("Python Syntax Scanner")]
    for rel, ln, msg in problems:
        out.append(f"- {rel}:{ln}: {msg}\n")
    if not problems:
        out.append("No Python syntax errors detected.\n")
    return "".join(out)


def cmd_env_var_scan(path: str) -> str:
    pat = re.compile(r"(os\.environ\[|os\.getenv\(|\$\{[A-Z0-9_]+\}|%[A-Z0-9_]+%)", re.IGNORECASE)
    findings = []
    for fp, rel in iter_files(path):
        text = read_text_safe(fp)
        if text is None:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if pat.search(line):
                findings.append((rel, i, line.strip()))
    out = [md_h1("Env Var Scanner")]
    if findings:
        for rel, ln, line in findings:
            out.append(f"- {rel}:{ln}: {line}\n")
    else:
        out.append("No environment variable patterns found.\n")
    return "".join(out)


def cmd_license_detect(path: str) -> str:
    licenses = []
    for name in ["LICENSE", "LICENSE.txt", "COPYING", "COPYING.txt"]:
        p = os.path.join(path, name)
        if os.path.exists(p):
            text = read_text_safe(p, max_bytes=5_000_000)
            if text:
                kind = "Unknown"
                if "MIT License" in text:
                    kind = "MIT"
                elif "Apache License" in text:
                    kind = "Apache"
                elif "GNU GENERAL PUBLIC LICENSE" in text:
                    kind = "GPL"
                elif "BSD License" in text:
                    kind = "BSD"
                licenses.append((safe_relpath(p, path), kind))
    out = [md_h1("License Detection")]
    if licenses:
        for rel, kind in licenses:
            out.append(f"- {rel}: {kind}\n")
    else:
        out.append("No license files detected.\n")
    return "".join(out)


def cmd_link_check_md(path: str, offline: bool = False) -> str:
    url_re = re.compile(r"https?://[\w\-./?%&=#:]+", re.IGNORECASE)
    results = []
    for fp, rel in iter_files(path, include_exts={".md"}):
        text = read_text_safe(fp)
        if not text:
            continue
        urls = set(url_re.findall(text))
        for url in sorted(urls):
            if offline:
                results.append((rel, url, 0, "offline"))
            else:
                status, reason = _http_head(url)
                results.append((rel, url, status, reason))
                # be polite
                time.sleep(0.05)
    out = [md_h1("Markdown Link Check"), f"Mode: {'offline' if offline else 'online'}\n\n"]
    for rel, url, status, reason in results:
        out.append(f"- {rel}: {url} — {status} {reason}\n")
    if not results:
        out.append("No links found in Markdown files.\n")
    return "".join(out)


def cmd_test_file_scan(path: str) -> str:
    tests = []
    for fp, rel in iter_files(path):
        base = os.path.basename(fp)
        if fnmatch.fnmatch(base, "test_*.py") or fnmatch.fnmatch(base, "*_test.py") or "tests" in os.path.normpath(fp).split(os.sep):
            tests.append(rel)
    out = [md_h1("Test File Scanner")]
    out += [f"- {rel}\n" for rel in sorted(tests)]
    if not tests:
        out.append("No test files found.\n")
    return "".join(out)


def cmd_deprecated_api_scan(path: str) -> str:
    patterns = [r"\bimp\b", r"\boptparse\b", r"\bdistutils\b", r"asyncio\.get_event_loop\("]
    comp = [re.compile(p) for p in patterns]
    findings = []
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if any(p.search(line) for p in comp):
                findings.append((rel, i, line.strip()))
    out = [md_h1("Deprecated API Scanner")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No deprecated API patterns found.\n")
    return "".join(out)


def cmd_print_debug_scan(path: str) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if ("print(" in line) or ("console.log" in line):
                findings.append((rel, i, line.strip()))
    out = [md_h1("Print/Debug Scanner")]
    out += [f"- {rel}:{ln}: {line}\n" for rel, ln, line in findings]
    if not findings:
        out.append("No print/console.log occurrences found.\n")
    return "".join(out)


def cmd_magic_number_scan(path: str) -> str:
    findings = []
    num_re = re.compile(r"(?<![\w.])(\d{3,})(?![\w.])")
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if num_re.search(line) and not line.strip().startswith(('#', '//')):
                findings.append((rel, i, line.strip()))
    out = [md_h1("Magic Number Scanner")]
    out += [f"- {rel}:{ln}: {line}\n" for rel, ln, line in findings]
    if not findings:
        out.append("No magic numbers (>=3 digits) found.\n")
    return "".join(out)


def cmd_tabs_scan(path: str) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if "\t" in line:
                findings.append((rel, i))
                break
    out = [md_h1("Tabs Scanner")]
    out += [f"- Tabs found in {rel} (first occurrence line {ln})\n" for rel, ln in findings]
    if not findings:
        out.append("No tabs found.\n")
    return "".join(out)


def cmd_trailing_whitespace_scan(path: str) -> str:
    files = []
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                files.append((rel, i))
                break
    out = [md_h1("Trailing Whitespace Scanner")]
    out += [f"- Trailing spaces in {rel} (first occurrence line {ln})\n" for rel, ln in files]
    if not files:
        out.append("No trailing whitespace found.\n")
    return "".join(out)


def cmd_utf_bom_scan(path: str) -> str:
    files = []
    bom = b"\xef\xbb\xbf"
    for fp, rel in iter_files(path):
        try:
            with open(fp, "rb") as f:
                start = f.read(3)
            if start == bom:
                files.append(rel)
        except Exception:
            pass
    out = [md_h1("UTF-8 BOM Scanner")]
    out += [f"- {rel}\n" for rel in files]
    if not files:
        out.append("No UTF-8 BOM files found.\n")
    return "".join(out)


def cmd_non_ascii_scan(path: str) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if any(ord(ch) > 127 for ch in line):
                findings.append((rel, i))
                break
    out = [md_h1("Non-ASCII Scanner")]
    out += [f"- {rel} (first non-ASCII at line {ln})\n" for rel, ln in findings]
    if not findings:
        out.append("No non-ASCII characters detected.\n")
    return "".join(out)


def cmd_newline_consistency_scan(path: str) -> str:
    counts = Counter()
    for fp, rel in iter_files(path):
        try:
            with open(fp, "rb") as f:
                data = f.read(50_000)
        except Exception:
            continue
        counts['CRLF'] += data.count(b"\r\n")
        counts['LF'] += data.count(b"\n") - data.count(b"\r\n")
        counts['CR'] += data.count(b"\r") - data.count(b"\r\n")
    out = [md_h1("Newline Consistency Scanner")]
    for k, v in counts.items():
        out.append(f"- {k}: {v}\n")
    return "".join(out)


def cmd_json_to_md(path: str) -> str:
    out = [md_h1("JSON to Markdown")]
    for fp, rel in iter_files(path, include_exts={".json"}):
        text = read_text_safe(fp)
        if not text:
            continue
        out.append(md_h2(rel))
        out.append(md_codeblock(text, "json"))
    if len(out) == 1:
        out.append("No JSON files found.\n")
    return "".join(out)


def cmd_csv_to_md(path: str, max_rows: int = 50) -> str:
    out = [md_h1("CSV to Markdown"), f"Previewing up to {max_rows} rows per file.\n\n"]
    for fp, rel in iter_files(path, include_exts={".csv"}):
        try:
            with open(fp, newline='', encoding='utf-8', errors='replace') as f:
                rdr = csv.reader(f)
                rows = []
                for i, row in enumerate(rdr):
                    rows.append(row)
                    if i + 1 >= max_rows:
                        break
        except Exception as e:
            rows = [["<error reading file>", str(e)]]
        out.append(md_h2(rel))
        if rows:
            # compute widths
            cols = max(len(r) for r in rows)
            widths = [0] * cols
            for r in rows:
                for i, cell in enumerate(r):
                    widths[i] = max(widths[i], len(str(cell)))
            # header
            header = rows[0] if rows else []
            out.append("| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(header)) + " |\n")
            out.append("| " + " | ".join("-" * widths[i] for i in range(len(widths))) + " |\n")
            # body
            for r in rows[1:]:
                out.append("| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)) + " |\n")
        else:
            out.append("(empty)\n")
        out.append("\n")
    if len(out) <= 2:
        out.append("No CSV files found.\n")
    return "".join(out)


def _strip_md(text: str) -> str:
    # very naive markdown stripping
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"^\s*#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*|__|\*|_|~~|> ", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^\)]*\)", "", text)
    text = re.sub(r"\[[^\]]*\]\([^\)]*\)", "", text)
    return text


def cmd_md_to_txt(path: str) -> str:
    out = [md_h1("Markdown to Text")]
    for fp, rel in iter_files(path, include_exts={".md"}):
        text = read_text_safe(fp)
        if not text:
            continue
        out.append(md_h2(rel))
        out.append(md_codeblock(_strip_md(text), "") )
    if len(out) == 1:
        out.append("No Markdown files found.\n")
    return "".join(out)


def cmd_txt_to_md(path: str) -> str:
    out = [md_h1("Text to Markdown")]
    for fp, rel in iter_files(path, include_exts={".txt"}):
        text = read_text_safe(fp)
        if not text:
            continue
        out.append(md_h2(rel))
        out.append(md_codeblock(text))
    if len(out) == 1:
        out.append("No text files found.\n")
    return "".join(out)


def cmd_code_to_md(path: str, max_bytes_per_file: int = 50_000) -> str:
    out = [md_h1("Code to Markdown"), f"Limit per file: {max_bytes_per_file} bytes\n\n"]
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp, max_bytes=max_bytes_per_file)
        if not text:
            continue
        lang = os.path.splitext(fp)[1].lstrip('.')
        out.append(md_h2(rel))
        out.append(md_codeblock(text, lang))
    if len(out) <= 2:
        out.append("No code files found.\n")
    return "".join(out)


def cmd_requirements_to_md(path: str) -> str:
    out = [md_h1("requirements.txt to Markdown")]
    for fp, rel in iter_files(path, include_exts={".txt"}):
        if os.path.basename(fp).lower() == "requirements.txt":
            text = read_text_safe(fp)
            if text:
                out.append(md_h2(rel))
                out.append(md_codeblock(text))
    if len(out) == 1:
        out.append("No requirements.txt found.\n")
    return "".join(out)


def cmd_package_json_to_md(path: str) -> str:
    out = [md_h1("package.json to Markdown")]
    for fp, rel in iter_files(path, include_exts={".json"}):
        if os.path.basename(fp) == "package.json":
            text = read_text_safe(fp)
            if text:
                out.append(md_h2(rel))
                out.append(md_codeblock(text, "json"))
    if len(out) == 1:
        out.append("No package.json found.\n")
    return "".join(out)


def cmd_junit_xml_to_md(path: str) -> str:
    out = [md_h1("JUnit XML to Markdown")]
    for fp, rel in iter_files(path, include_exts={".xml"}):
        if fnmatch.fnmatch(os.path.basename(fp).lower(), "*junit*.xml"):
            try:
                tree = ET.parse(fp)
                root = tree.getroot()
                tests = int(root.attrib.get('tests', 0))
                failures = int(root.attrib.get('failures', 0))
                errors = int(root.attrib.get('errors', 0))
                skipped = int(root.attrib.get('skipped', 0))
                out.append(md_h2(rel))
                out.append(f"- tests: {tests}\n- failures: {failures}\n- errors: {errors}\n- skipped: {skipped}\n\n")
            except Exception as e:
                out.append(md_h2(rel))
                out.append(f"Error parsing: {e}\n\n")
    if len(out) == 1:
        out.append("No JUnit-style XML files found.\n")
    return "".join(out)


def _tree_lines(base: str) -> List[str]:
    lines = []
    base = os.path.abspath(base)
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in DEFAULT_EXCLUDE_DIRS and not d.startswith('.')]
        level = len(os.path.relpath(root, base).split(os.sep)) - 1
        prefix = "    " * max(0, level)
        if root == base:
            lines.append(os.path.basename(base) or base)
        else:
            lines.append(f"{prefix}{os.path.basename(root)}/")
        for name in sorted(files):
            lines.append(f"{prefix}    {name}")
    return lines


def cmd_dir_tree_to_md(path: str) -> str:
    return md_h1("Directory Tree") + md_codeblock("\n".join(_tree_lines(path)))


def cmd_file_index(path: str) -> str:
    out = [md_h1("File Index")]
    for fp, rel in iter_files(path):
        try:
            size = os.path.getsize(fp)
        except Exception:
            size = 0
        out.append(f"- {rel} — {size} bytes\n")
    return "".join(out)


def _read_first_md(path: str, pat: str) -> Optional[Tuple[str, str]]:
    for fp, rel in iter_files(path, include_exts={".md"}):
        if fnmatch.fnmatch(os.path.basename(fp).lower(), pat):
            text = read_text_safe(fp)
            if text:
                return rel, text
    return None


def cmd_changelog_summary(path: str) -> str:
    data = _read_first_md(path, "changelog*.md")
    out = [md_h1("Changelog Summary")]
    if not data:
        out.append("No CHANGELOG.md found.\n")
    else:
        rel, text = data
        out.append(md_h2(rel))
        # Extract top 10 headings
        heads = re.findall(r"^#+\s+.*$", text, flags=re.MULTILINE)[:10]
        out += [f"- {h.lstrip('# ').strip()}\n" for h in heads]
        if not heads:
            out.append("No headings found.\n")
    return "".join(out)


def cmd_readme_summary(path: str) -> str:
    data = _read_first_md(path, "readme*.md")
    out = [md_h1("README Summary")]
    if not data:
        out.append("No README found.\n")
    else:
        rel, text = data
        out.append(md_h2(rel))
        # first paragraph
        paras = [p.strip() for p in text.split('\n\n') if p.strip()]
        if paras:
            out.append(paras[0] + "\n\n")
        heads = re.findall(r"^#+\s+.*$", text, flags=re.MULTILINE)[:10]
        for h in heads:
            out.append(f"- {h.lstrip('# ').strip()}\n")
    return "".join(out)


def cmd_metadata_pack(path: str) -> str:
    out = [md_h1("Metadata Pack")]
    out.append(md_h2("Environment"))
    out.append(f"- OS: {platform.platform()}\n")
    out.append(f"- Python: {platform.python_version()}\n")
    out.append(f"- Working dir: {os.getcwd()}\n")
    out.append(f"- Scan path: {path}\n\n")
    out.append(md_h2("File counts"))
    out.append(cmd_code_stats(path))
    return "".join(out)


def cmd_prompt_pack(path: str) -> str:
    sections = [
        cmd_readme_summary(path),
        cmd_code_stats(path),
        cmd_todo_scan(path),
        cmd_bug_scan(path),
        cmd_secret_scan(path),
        cmd_dir_tree_to_md(path),
    ]
    return md_h1("Prompt Pack") + "\n".join(sections)


def cmd_chunk(path: str, file: str, lines_per_chunk: int = 120) -> str:
    fp = os.path.join(path, file)
    text = read_text_safe(fp, max_bytes=5_000_000)
    out = [md_h1("Chunked File"), f"File: {file}\nLines per chunk: {lines_per_chunk}\n\n"]
    if not text:
        out.append("File not found or not readable.\n")
        return "".join(out)
    lines = text.splitlines()
    for i in range(0, len(lines), lines_per_chunk):
        chunk = "\n".join(lines[i:i + lines_per_chunk])
        out.append(md_h2(f"Chunk {i//lines_per_chunk + 1}"))
        out.append(md_codeblock(chunk))
    return "".join(out)


def cmd_token_estimate(path: str) -> str:
    out = [md_h1("Token Estimate")]
    total = 0
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        tokens = estimate_tokens(text)
        total += tokens
        out.append(f"- {rel}: ~{tokens} tokens\n")
    out.append(f"\nTotal estimated tokens: ~{total}\n")
    return "".join(out)


def cmd_image_inventory(path: str) -> str:
    out = [md_h1("Image Inventory")]
    for fp, rel in iter_files(path):
        ext = os.path.splitext(fp)[1].lower()
        if ext in IMAGE_EXTS:
            try:
                size = os.path.getsize(fp)
            except Exception:
                size = 0
            out.append(f"- {rel} — {size} bytes\n")
    if len(out) == 1:
        out.append("No images found.\n")
    return "".join(out)


def cmd_dir_size_report(path: str) -> str:
    sizes = defaultdict(int)
    base = os.path.abspath(path)
    for fp, rel in iter_files(path):
        try:
            size = os.path.getsize(fp)
        except Exception:
            size = 0
        d = os.path.dirname(rel)
        sizes[d] += size
    out = [md_h1("Directory Size Report")]
    for d, s in sorted(sizes.items(), key=lambda x: -x[1]):
        out.append(f"- {d or '.'}: {s} bytes\n")
    return "".join(out)


def cmd_csv_summary(path: str) -> str:
    out = [md_h1("CSV Summary")]
    for fp, rel in iter_files(path, include_exts={".csv"}):
        rows = 0
        cols = 0
        try:
            with open(fp, newline='', encoding='utf-8', errors='replace') as f:
                rdr = csv.reader(f)
                for r in rdr:
                    rows += 1
                    cols = max(cols, len(r))
        except Exception as e:
            out.append(f"- {rel}: error {e}\n")
            continue
        out.append(f"- {rel}: {rows} rows, {cols} columns\n")
    if len(out) == 1:
        out.append("No CSV files found.\n")
    return "".join(out)


def cmd_json_schema_extract(path: str, max_files: int = 50) -> str:
    out = [md_h1("JSON Schema Extract (heuristic)")]
    count = 0
    for fp, rel in iter_files(path, include_exts={".json"}):
        if count >= max_files:
            break
        text = read_text_safe(fp)
        if not text:
            continue
        try:
            data = json.loads(text)
        except Exception:
            continue
        schema = {}
        def walk(x, prefix="$"):
            if isinstance(x, dict):
                for k, v in x.items():
                    schema[f"{prefix}.{k}"] = type(v).__name__
                    walk(v, f"{prefix}.{k}")
            elif isinstance(x, list) and x:
                schema[f"{prefix}[]"] = type(x[0]).__name__
                walk(x[0], f"{prefix}[]")
        walk(data)
        out.append(md_h2(rel))
        for k, v in sorted(schema.items()):
            out.append(f"- {k}: {v}\n")
        count += 1
    if len(out) == 1:
        out.append("No JSON files found.\n")
    return "".join(out)


def cmd_api_spec_from_openapi(path: str) -> str:
    out = [md_h1("API Spec from OpenAPI (best-effort)")]
    # JSON only; YAML will be included verbatim
    for fp, rel in iter_files(path, include_exts={".json", ".yaml", ".yml"}):
        name = os.path.basename(fp).lower()
        if "openapi" in name or "swagger" in name:
            text = read_text_safe(fp)
            if not text:
                continue
            if fp.endswith(".json"):
                try:
                    data = json.loads(text)
                    title = data.get('info', {}).get('title', 'API')
                    version = data.get('info', {}).get('version', '')
                    out.append(md_h2(f"{rel} — {title} {version}"))
                    paths = data.get('paths', {})
                    for pth, ops in paths.items():
                        out.append(f"- {pth}: {', '.join(ops.keys())}\n")
                except Exception:
                    out.append(md_h2(rel))
                    out.append(md_codeblock(text))
            else:
                out.append(md_h2(rel))
                out.append(md_codeblock(text))
    if len(out) == 1:
        out.append("No OpenAPI/Swagger files found.\n")
    return "".join(out)


# ----------------------------
# Additional scanners/reporters/converters (50+ new commands)
# ----------------------------


def cmd_line_length_scan(path: str, max_len: int = 120) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if len(line) > max_len:
                findings.append((rel, i, len(line)))
    out = [md_h1("Line Length Scanner"), f"Max length: {max_len}\n\n"]
    for rel, ln, lnlen in findings:
        out.append(f"- {rel}:{ln} — {lnlen} chars\n")
    if not findings:
        out.append("No overlong lines found.\n")
    return "".join(out)


def cmd_mixed_indent_scan(path: str) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        has_tab = any(line.startswith("\t") for line in text.splitlines())
        has_space_indent = any(re.match(r"^ +\S", line) for line in text.splitlines())
        if has_tab and has_space_indent:
            findings.append(rel)
    out = [md_h1("Mixed Indentation Scanner")]
    for rel in findings:
        out.append(f"- {rel}\n")
    if not findings:
        out.append("No files with mixed indentation found.\n")
    return "".join(out)


def cmd_shebang_scan(path: str) -> str:
    results = []
    for fp, rel in iter_files(path):
        try:
            with open(fp, "rb") as f:
                first = f.read(2)
            if first == b"#!":
                results.append(rel)
        except Exception:
            continue
    out = [md_h1("Shebang Scanner")]
    out += [f"- {rel}\n" for rel in results]
    if not results:
        out.append("No shebang files found.\n")
    return "".join(out)


def cmd_empty_file_scan(path: str) -> str:
    empties = []
    for fp, rel in iter_files(path):
        try:
            if os.path.getsize(fp) == 0:
                empties.append(rel)
        except Exception:
            continue
    out = [md_h1("Empty File Scanner")]
    out += [f"- {rel}\n" for rel in empties]
    if not empties:
        out.append("No empty files found.\n")
    return "".join(out)


def cmd_dead_except_scan(path: str) -> str:
    findings = []
    pat = re.compile(r"^\s*except\b[\s\S]*?:\s*(#.*)?$")
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            if pat.match(line):
                # look ahead 1 line for pass/ellipsis
                nxt = lines[i].strip() if i < len(lines) else ""
                if nxt in ("pass", "..."):
                    findings.append((rel, i, nxt))
    out = [md_h1("Dead Except Scanner (except: pass/...)")]
    for rel, ln, what in findings:
        out.append(f"- {rel}:{ln} — {what}\n")
    if not findings:
        out.append("No dead except blocks found.\n")
    return "".join(out)


def cmd_broad_except_scan(path: str) -> str:
    findings = []
    pat = re.compile(r"^\s*except\s+(Exception|BaseException)\s*:")
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if pat.match(line):
                findings.append((rel, i))
    out = [md_h1("Broad Except Scanner")]
    for rel, ln in findings:
        out.append(f"- {rel}:{ln}\n")
    if not findings:
        out.append("No broad exception handlers found.\n")
    return "".join(out)


def cmd_eval_exec_scan(path: str) -> str:
    findings = []
    pat = re.compile(r"\b(eval|exec)\s*\(")
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if "eval(" in line or re.search(r"\bexec\b", line):
                findings.append((rel, i, line.strip()))
    out = [md_h1("eval/exec Scanner")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No eval/exec usages found.\n")
    return "".join(out)


def cmd_subprocess_shell_scan(path: str) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if "subprocess" in line and "shell=True" in line:
                findings.append((rel, i, line.strip()))
    out = [md_h1("subprocess shell=True Scanner")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No subprocess shell=True usage found.\n")
    return "".join(out)


def cmd_hardcoded_path_scan(path: str) -> str:
    findings = []
    pat = re.compile(r"([A-Za-z]:\\\\|/home/|/Users/)")
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if pat.search(line):
                findings.append((rel, i, line.strip()))
    out = [md_h1("Hardcoded Path Scanner")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No hardcoded absolute paths found.\n")
    return "".join(out)


def cmd_http_url_scan(path: str) -> str:
    findings = []
    pat = re.compile(r"http://[\w\-./?%&=#:]+", re.IGNORECASE)
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, m in enumerate(pat.finditer(text), 1):
            url = m.group(0)
            findings.append((rel, url))
    out = [md_h1("HTTP URL Scanner (non-HTTPS)")]
    for rel, url in findings:
        out.append(f"- {rel}: {url}\n")
    if not findings:
        out.append("No http:// URLs found.\n")
    return "".join(out)


def cmd_version_number_scan(path: str) -> str:
    findings = []
    pat = re.compile(r"\b\d+\.\d+\.\d+\b")
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        if pat.search(text):
            findings.append(rel)
    out = [md_h1("Version Number Scanner (semver)")]
    for rel in findings:
        out.append(f"- {rel}\n")
    if not findings:
        out.append("No semantic version numbers found.\n")
    return "".join(out)


def cmd_traceback_usage_scan(path: str) -> str:
    findings = []
    pats = ["traceback.print_exc", "traceback.format_exc"]
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if any(p in line for p in pats):
                findings.append((rel, i, line.strip()))
    out = [md_h1("Traceback Usage Scanner")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No traceback usage found.\n")
    return "".join(out)


def cmd_unreachable_code_scan_py(path: str) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        try:
            tree = ast.parse(text)
        except Exception:
            continue
        # Scan simple blocks for return/raise not last
        def scan_body(body):
            for idx, node in enumerate(body):
                if isinstance(node, (ast.Return, ast.Raise)) and idx < len(body) - 1:
                    findings.append((rel, getattr(node, 'lineno', 0)))
                # Recurse into compound statements
                for child_list in (
                    getattr(node, 'body', None),
                    getattr(node, 'orelse', None),
                    getattr(node, 'finalbody', None),
                ):
                    if isinstance(child_list, list):
                        scan_body(child_list)
        for node in ast.walk(tree):
            if hasattr(node, 'body') and isinstance(getattr(node, 'body'), list):
                scan_body(getattr(node, 'body'))
    out = [md_h1("Unreachable Code Scanner (Python)")]
    for rel, ln in findings:
        out.append(f"- {rel}:{ln}\n")
    if not findings:
        out.append("No potentially unreachable code found (heuristic).\n")
    return "".join(out)


def cmd_commented_out_code_scan(path: str) -> str:
    findings = []
    pat = re.compile(r"^\s*#\s*(def |class |if |for |while |import |from )")
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if pat.search(line):
                findings.append((rel, i, line.strip()))
    out = [md_h1("Commented-out Code Scanner (Python)")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No commented-out Python code patterns found.\n")
    return "".join(out)


def cmd_many_params_scan(path: str, max_params: int = 6) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts={".py"}):
        for name, start, end in _ast_funcs_with_spans(fp):
            text = read_text_safe(fp)
            if not text:
                continue
            try:
                tree = ast.parse(text)
            except Exception:
                continue
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    total = len(node.args.args) + len(node.args.kwonlyargs)
                    if node.args.vararg:
                        total += 1
                    if node.args.kwarg:
                        total += 1
                    if total >= max_params:
                        findings.append((rel, getattr(node, 'name', '<func>'), total))
    out = [md_h1("Many Parameters Scanner (Python)"), f"Threshold: {max_params}\n\n"]
    for rel, name, total in findings:
        out.append(f"- {rel}::{name} — {total} params\n")
    if not findings:
        out.append("No functions over threshold.\n")
    return "".join(out)


def cmd_license_header_missing_scan(path: str) -> str:
    findings = []
    header_pats = ("Copyright", "License")
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        first_block = "\n".join(text.splitlines()[:5])
        if not any(p in first_block for p in header_pats):
            findings.append(rel)
    out = [md_h1("License Header Missing (heuristic)")]
    for rel in findings:
        out.append(f"- {rel}\n")
    if not findings:
        out.append("All files appear to have a header or none scanned.\n")
    return "".join(out)


def cmd_typing_missing_scan(path: str) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        try:
            tree = ast.parse(text)
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                has_ann = any(a.annotation is not None for a in node.args.args + node.args.kwonlyargs) or node.returns is not None
                if not has_ann:
                    findings.append((rel, node.name, getattr(node, 'lineno', 0)))
    out = [md_h1("Typing Missing Scanner (Python)")]
    for rel, name, ln in findings:
        out.append(f"- {rel}:{ln}::{name}\n")
    if not findings:
        out.append("All functions have some annotations or none found.\n")
    return "".join(out)


def cmd_logger_debug_scan(path: str) -> str:
    findings = []
    pat = re.compile(r"logging\.debug\(")
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if "logging.debug(" in line:
                findings.append((rel, i, line.strip()))
    out = [md_h1("Logger Debug Scanner")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No logging.debug calls found.\n")
    return "".join(out)


def cmd_sleep_call_scan(path: str) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if "time.sleep(" in line:
                findings.append((rel, i, line.strip()))
    out = [md_h1("time.sleep Usage Scanner")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No time.sleep calls found.\n")
    return "".join(out)


def cmd_annotation_scan(path: str) -> str:
    tags = ["TODO", "FIXME", "NOTE", "XXX", "HACK", "TBD", "BUG"]
    comp = [re.compile(rf"\b{t}\b", re.IGNORECASE) for t in tags]
    findings = []
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if any(p.search(line) for p in comp):
                findings.append((rel, i, line.strip()))
    out = [md_h1("Annotation Scanner")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No annotation tags found.\n")
    return "".join(out)


def cmd_pinned_versions_scan(path: str) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts={".txt"}):
        if os.path.basename(fp).lower() == "requirements.txt":
            text = read_text_safe(fp)
            if not text:
                continue
            for line in text.splitlines():
                if "==" in line and not line.strip().startswith("#"):
                    findings.append((rel, line.strip()))
    out = [md_h1("Pinned Versions in requirements.txt")]
    for rel, line in findings:
        out.append(f"- {rel}: {line}\n")
    if not findings:
        out.append("No pinned dependencies found.\n")
    return "".join(out)


def cmd_duplicate_filename_scan(path: str) -> str:
    names = defaultdict(list)
    for fp, rel in iter_files(path):
        names[os.path.basename(fp)].append(rel)
    out = [md_h1("Duplicate Filename Scanner")]
    for name, rels in sorted(names.items()):
        if len(rels) > 1:
            out.append(md_h2(name))
            out += [f"- {r}\n" for r in rels]
    if len(out) == 1:
        out.append("No duplicate filenames found.\n")
    return "".join(out)


def cmd_duplicate_file_contents_scan(path: str, max_bytes: int = 1_000_000) -> str:
    import hashlib
    hashes = defaultdict(list)
    for fp, rel in iter_files(path):
        try:
            size = os.path.getsize(fp)
            if size > max_bytes:
                continue
            with open(fp, "rb") as f:
                data = f.read()
            h = hashlib.sha256(data).hexdigest()
            hashes[h].append(rel)
        except Exception:
            continue
    out = [md_h1("Duplicate File Contents Scanner"), f"Only files <= {max_bytes} bytes considered.\n\n"]
    found = False
    for h, rels in hashes.items():
        if len(rels) > 1:
            found = True
            out.append(md_h2(h))
            out += [f"- {r}\n" for r in rels]
    if not found:
        out.append("No duplicate file contents found.\n")
    return "".join(out)


def cmd_binary_file_inventory(path: str) -> str:
    out = [md_h1("Binary File Inventory")]
    for fp, rel in iter_files(path):
        try:
            with open(fp, "rb") as f:
                data = f.read(1024)
            if is_binary_bytes(data):
                out.append(f"- {rel}\n")
        except Exception:
            continue
    if len(out) == 1:
        out.append("No binary files detected.\n")
    return "".join(out)


def cmd_large_line_scan(path: str, min_len: int = 500) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if len(line) >= min_len:
                findings.append((rel, i, len(line)))
    out = [md_h1("Large Line Scanner"), f"Threshold: {min_len} chars\n\n"]
    for rel, ln, lnlen in findings:
        out.append(f"- {rel}:{ln} — {lnlen} chars\n")
    if not findings:
        out.append("No lines over threshold found.\n")
    return "".join(out)


def cmd_trailing_empty_lines_scan(path: str, min_trailing: int = 2) -> str:
    findings = []
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if text is None:
            continue
        # Count trailing newlines
        trail = 0
        for ch in reversed(text):
            if ch == '\n':
                trail += 1
            else:
                break
        if trail >= min_trailing:
            findings.append((rel, trail))
    out = [md_h1("Trailing Empty Lines Scanner"), f"Min trailing: {min_trailing}\n\n"]
    for rel, trail in findings:
        out.append(f"- {rel} — {trail} trailing newlines\n")
    if not findings:
        out.append("No files with excessive trailing newlines.\n")
    return "".join(out)


def cmd_markdown_heading_index(path: str) -> str:
    out = [md_h1("Markdown Heading Index")]
    for fp, rel in iter_files(path, include_exts={".md"}):
        text = read_text_safe(fp)
        if not text:
            continue
        heads = re.findall(r"^(#+)\s+(.*)$", text, flags=re.MULTILINE)
        out.append(md_h2(rel))
        for hashes, title in heads:
            level = len(hashes)
            out.append(f"- {'  ' * (level-1)}{title}\n")
    if len(out) == 1:
        out.append("No Markdown files with headings found.\n")
    return "".join(out)


def cmd_markdown_image_check(path: str) -> str:
    out = [md_h1("Markdown Image Check")]
    img_re = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    base = os.path.abspath(path)
    findings = []
    for fp, rel in iter_files(path, include_exts={".md"}):
        text = read_text_safe(fp)
        if not text:
            continue
        for m in img_re.finditer(text):
            ref = m.group(1)
            if re.match(r"https?://", ref):
                continue
            p = os.path.normpath(os.path.join(os.path.dirname(fp), ref))
            if not os.path.exists(p):
                findings.append((rel, ref))
    for rel, ref in findings:
        out.append(f"- {rel}: missing image {ref}\n")
    if not findings:
        out.append("All local images referenced in Markdown seem present.\n")
    return "".join(out)


def cmd_markdown_word_count(path: str) -> str:
    total = 0
    out = [md_h1("Markdown Word Count")]
    for fp, rel in iter_files(path, include_exts={".md"}):
        text = read_text_safe(fp)
        if not text:
            continue
        words = re.findall(r"\b\w+\b", _strip_md(text))
        total += len(words)
        out.append(f"- {rel}: {len(words)} words\n")
    out.append(f"\nTotal words: {total}\n")
    return "".join(out)


def cmd_yaml_syntax_scan(path: str) -> str:
    out = [md_h1("YAML Syntax Scan (heuristic)")]
    # Without PyYAML, only basic heuristics: flag tabs and inconsistent indent (mix of 2 and 4 spaces)
    for fp, rel in iter_files(path, include_exts={".yaml", ".yml"}):
        text = read_text_safe(fp)
        if not text:
            continue
        has_tab = any("\t" in ln for ln in text.splitlines())
        indents = {len(m.group(0)) for ln in text.splitlines() for m in [re.match(r"^( +)\S", ln)] if m}
        inconsistent = (2 in indents and 4 in indents)
        if has_tab or inconsistent:
            issues = []
            if has_tab:
                issues.append("tabs present")
            if inconsistent:
                issues.append("mixed 2/4 space indents")
            out.append(f"- {rel}: {', '.join(issues)}\n")
    if len(out) == 1:
        out.append("No YAML heuristic issues found.\n")
    return "".join(out)


def cmd_json_syntax_scan(path: str) -> str:
    out = [md_h1("JSON Syntax Scan")]
    for fp, rel in iter_files(path, include_exts={".json"}):
        text = read_text_safe(fp)
        if not text:
            continue
        try:
            json.loads(text)
        except Exception as e:
            out.append(f"- {rel}: {e}\n")
    if len(out) == 1:
        out.append("No JSON syntax errors found.\n")
    return "".join(out)


def cmd_xml_syntax_scan(path: str) -> str:
    out = [md_h1("XML Syntax Scan")]
    for fp, rel in iter_files(path, include_exts={".xml"}):
        try:
            ET.parse(fp)
        except Exception as e:
            out.append(f"- {rel}: {e}\n")
    if len(out) == 1:
        out.append("No XML syntax errors found.\n")
    return "".join(out)


def cmd_html_syntax_scan(path: str) -> str:
    out = [md_h1("HTML Syntax Scan (heuristic)")]
    tag_re = re.compile(r"<(/?)([a-zA-Z0-9]+)[^>]*>")
    void = {"br", "hr", "img", "input", "meta", "link", "source", "area", "base", "col", "embed", "param", "track", "wbr"}
    for fp, rel in iter_files(path, include_exts={".html", ".htm"}):
        text = read_text_safe(fp)
        if not text:
            continue
        stack = []
        for m in tag_re.finditer(text):
            closing, tag = m.group(1), m.group(2).lower()
            if tag in void:
                continue
            if closing:
                if stack and stack[-1] == tag:
                    stack.pop()
                else:
                    stack.append("?"+tag)
            else:
                stack.append(tag)
        if stack:
            out.append(f"- {rel}: unbalanced/mismatched tags (heuristic)\n")
    if len(out) == 1:
        out.append("No obvious HTML tag balance issues detected.\n")
    return "".join(out)


def cmd_nocommit_scan(path: str) -> str:
    findings = []
    pats = [re.compile(r"\bNOCOMMIT\b", re.IGNORECASE), re.compile(r"DO\s*NOT\s*COMMIT", re.IGNORECASE)]
    for fp, rel in iter_files(path, include_exts=TEXT_EXTS):
        text = read_text_safe(fp)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if any(p.search(line) for p in pats):
                findings.append((rel, i, line.strip()))
    out = [md_h1("Do Not Commit Scanner")]
    for rel, ln, line in findings:
        out.append(f"- {rel}:{ln}: {line}\n")
    if not findings:
        out.append("No do-not-commit markers found.\n")
    return "".join(out)


def cmd_yaml_to_md(path: str) -> str:
    out = [md_h1("YAML to Markdown")]
    for fp, rel in iter_files(path, include_exts={".yaml", ".yml"}):
        text = read_text_safe(fp)
        if text:
            out.append(md_h2(rel))
            out.append(md_codeblock(text, "yaml"))
    if len(out) == 1:
        out.append("No YAML files found.\n")
    return "".join(out)


def cmd_xml_to_md(path: str) -> str:
    out = [md_h1("XML to Markdown")]
    for fp, rel in iter_files(path, include_exts={".xml"}):
        text = read_text_safe(fp)
        if text:
            out.append(md_h2(rel))
            out.append(md_codeblock(text, "xml"))
    if len(out) == 1:
        out.append("No XML files found.\n")
    return "".join(out)


def cmd_html_to_md_text(path: str) -> str:
    out = [md_h1("HTML to Text (Markdown fenced)")]
    for fp, rel in iter_files(path, include_exts={".html", ".htm"}):
        text = read_text_safe(fp)
        if text:
            plain = re.sub(r"<[^>]+>", "", text)
            out.append(md_h2(rel))
            out.append(md_codeblock(plain))
    if len(out) == 1:
        out.append("No HTML files found.\n")
    return "".join(out)


def cmd_ini_to_md(path: str) -> str:
    import configparser
    out = [md_h1("INI to Markdown")]
    for fp, rel in iter_files(path, include_exts={".ini"}):
        cp = configparser.ConfigParser()
        try:
            cp.read(fp, encoding='utf-8')
            out.append(md_h2(rel))
            for sect in cp.sections():
                out.append(f"### [{sect}]\n\n")
                for k, v in cp.items(sect):
                    out.append(f"- {k} = {v}\n")
                out.append("\n")
        except Exception as e:
            out.append(md_h2(rel))
            out.append(f"Error: {e}\n\n")
    if len(out) == 1:
        out.append("No INI files found.\n")
    return "".join(out)


def cmd_toml_to_md(path: str) -> str:
    out = [md_h1("TOML to Markdown")]
    try:
        import tomllib  # py311+
    except Exception:
        tomllib = None
    for fp, rel in iter_files(path, include_exts={".toml"}):
        text = read_text_safe(fp)
        if not text:
            continue
        out.append(md_h2(rel))
        if tomllib:
            try:
                data = tomllib.loads(text)
                # Simple pretty print as JSON-like
                out.append(md_codeblock(json.dumps(data, indent=2), "json"))
            except Exception:
                out.append(md_codeblock(text, "toml"))
        else:
            out.append(md_codeblock(text, "toml"))
    if len(out) == 1:
        out.append("No TOML files found.\n")
    return "".join(out)


def cmd_properties_to_md(path: str) -> str:
    out = [md_h1(".properties to Markdown")]
    for fp, rel in iter_files(path, include_exts={".properties"}):
        text = read_text_safe(fp)
        if not text:
            continue
        out.append(md_h2(rel))
        for ln in text.splitlines():
            ln = ln.strip()
            if not ln or ln.startswith(('#', '!')):
                continue
            if '=' in ln:
                k, v = ln.split('=', 1)
            elif ':' in ln:
                k, v = ln.split(':', 1)
            else:
                k, v = ln, ''
            out.append(f"- {k.strip()} = {v.strip()}\n")
        out.append("\n")
    if len(out) == 1:
        out.append("No .properties files found.\n")
    return "".join(out)


def cmd_pyproject_to_md(path: str) -> str:
    out = [md_h1("pyproject.toml to Markdown")]
    for fp, rel in iter_files(path, include_exts={".toml"}):
        if os.path.basename(fp) == "pyproject.toml":
            text = read_text_safe(fp)
            if text:
                out.append(md_h2(rel))
                out.append(md_codeblock(text, "toml"))
    if len(out) == 1:
        out.append("No pyproject.toml found.\n")
    return "".join(out)


def cmd_gitignore_to_md(path: str) -> str:
    out = [md_h1(".gitignore to Markdown")]
    for fp, rel in iter_files(path, include_exts={".gitignore"}):
        text = read_text_safe(fp)
        if text:
            out.append(md_h2(rel))
            out.append(md_codeblock(text))
    # Fallback: manually check common locations
    gitignore = os.path.join(path, ".gitignore")
    if os.path.exists(gitignore):
        text = read_text_safe(gitignore)
        if text:
            out.append(md_h2(safe_relpath(gitignore, path)))
            out.append(md_codeblock(text))
    if len(out) == 1:
        out.append("No .gitignore found.\n")
    return "".join(out)


def cmd_editorconfig_to_md(path: str) -> str:
    out = [md_h1(".editorconfig to Markdown")]
    p = os.path.join(path, ".editorconfig")
    if os.path.exists(p):
        text = read_text_safe(p)
        if text:
            out.append(md_h2(safe_relpath(p, path)))
            out.append(md_codeblock(text))
    else:
        out.append("No .editorconfig found.\n")
    return "".join(out)


def cmd_license_to_md(path: str) -> str:
    out = [md_h1("License file to Markdown")]
    for name in ["LICENSE", "LICENSE.txt", "COPYING", "COPYING.txt"]:
        p = os.path.join(path, name)
        if os.path.exists(p):
            text = read_text_safe(p, max_bytes=5_000_000)
            if text:
                out.append(md_h2(safe_relpath(p, path)))
                out.append(md_codeblock(text))
    if len(out) == 1:
        out.append("No license files found.\n")
    return "".join(out)


def _ast_outline_py(text: str) -> List[str]:
    lines = []
    try:
        tree = ast.parse(text)
    except Exception:
        return lines
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            lines.append(f"class {node.name} (line {getattr(node, 'lineno', 0)})")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            lines.append(f"def {node.name} (line {getattr(node, 'lineno', 0)})")
    return sorted(lines)


def cmd_code_outline_py(path: str) -> str:
    out = [md_h1("Python Code Outline")]
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if text:
            out.append(md_h2(rel))
            out.append(md_codeblock("\n".join(_ast_outline_py(text))))
    if len(out) == 1:
        out.append("No Python files found.\n")
    return "".join(out)


def cmd_import_list_py(path: str) -> str:
    out = [md_h1("Python Import List")]
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        try:
            tree = ast.parse(text)
        except Exception:
            continue
        imps = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imps.append(n.name)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                for n in node.names:
                    imps.append(f"{mod}.{n.name}")
        if imps:
            out.append(md_h2(rel))
            for i in sorted(set(imps)):
                out.append(f"- {i}\n")
    if len(out) == 1:
        out.append("No imports found.\n")
    return "".join(out)


def cmd_function_metrics_py(path: str) -> str:
    out = [md_h1("Python Function Metrics")]
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        try:
            tree = ast.parse(text)
        except Exception:
            continue
        funcs = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                start = getattr(node, 'lineno', 0)
                end = getattr(node, 'end_lineno', start)
                ln = end - start + 1 if end and start else 0
                total = len(node.args.args) + len(node.args.kwonlyargs)
                if node.args.vararg:
                    total += 1
                if node.args.kwarg:
                    total += 1
                funcs.append((getattr(node, 'name', '<func>'), ln, total))
        if funcs:
            out.append(md_h2(rel))
            for name, ln, total in sorted(funcs, key=lambda x: -x[1]):
                out.append(f"- {name}: {ln} lines, {total} params\n")
    if len(out) == 1:
        out.append("No Python functions found.\n")
    return "".join(out)


def cmd_class_metrics_py(path: str) -> str:
    out = [md_h1("Python Class Metrics")]
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        try:
            tree = ast.parse(text)
        except Exception:
            continue
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = sum(isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)) for ch in node.body)
                start = getattr(node, 'lineno', 0)
                end = getattr(node, 'end_lineno', start)
                ln = end - start + 1 if end and start else 0
                classes.append((node.name, methods, ln))
        if classes:
            out.append(md_h2(rel))
            for name, methods, ln in sorted(classes, key=lambda x: -x[2]):
                out.append(f"- {name}: {methods} methods, {ln} lines\n")
    if len(out) == 1:
        out.append("No Python classes found.\n")
    return "".join(out)


def cmd_docstring_summary_py(path: str) -> str:
    out = [md_h1("Python Docstring Summary")]
    for fp, rel in iter_files(path, include_exts={".py"}):
        text = read_text_safe(fp)
        if not text:
            continue
        try:
            tree = ast.parse(text)
        except Exception:
            continue
        items = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                doc = ast.get_docstring(node) or ""
                summary = doc.strip().splitlines()[0] if doc.strip() else ""
                if summary:
                    items.append((getattr(node, 'name', '<def>'), summary))
        if items:
            out.append(md_h2(rel))
            for name, summary in items:
                out.append(f"- {name}: {summary}\n")
    if len(out) == 1:
        out.append("No docstring summaries found.\n")
    return "".join(out)


def cmd_extension_inventory(path: str) -> str:
    counts = Counter()
    for fp, rel in iter_files(path):
        ext = os.path.splitext(fp)[1].lower()
        counts[ext] += 1
    out = [md_h1("Extension Inventory")]
    for ext, n in counts.most_common():
        out.append(f"- {ext or '(no ext)'}: {n}\n")
    return "".join(out)


def cmd_recent_files_report(path: str, days: int = 7) -> str:
    cutoff = time.time() - days * 86400
    out = [md_h1("Recent Files Report"), f"Window: last {days} days\n\n"]
    items = []
    for fp, rel in iter_files(path):
        try:
            mtime = os.path.getmtime(fp)
        except Exception:
            continue
        if mtime >= cutoff:
            items.append((rel, _dt.datetime.fromtimestamp(mtime).isoformat()))
    for rel, ts in sorted(items, key=lambda x: x[1], reverse=True):
        out.append(f"- {rel}: {ts}\n")
    if not items:
        out.append("No files modified in the given window.\n")
    return "".join(out)


def cmd_file_age_report(path: str, top: int = 20) -> str:
    items = []
    for fp, rel in iter_files(path):
        try:
            mtime = os.path.getmtime(fp)
        except Exception:
            continue
        items.append((rel, mtime))
    out = [md_h1("File Age Report")]
    if not items:
        out.append("No files found.\n")
        return "".join(out)
    out.append(md_h2("Newest"))
    for rel, mt in sorted(items, key=lambda x: -x[1])[:top]:
        out.append(f"- {rel}: {_dt.datetime.fromtimestamp(mt).isoformat()}\n")
    out.append("\n")
    out.append(md_h2("Oldest"))
    for rel, mt in sorted(items, key=lambda x: x[1])[:top]:
        out.append(f"- {rel}: {_dt.datetime.fromtimestamp(mt).isoformat()}\n")
    return "".join(out)


def cmd_readme_links(path: str) -> str:
    data = _read_first_md(path, "readme*.md")
    out = [md_h1("README Links")]
    if not data:
        out.append("No README found.\n")
    else:
        rel, text = data
        url_re = re.compile(r"https?://[\w\-./?%&=#:]+", re.IGNORECASE)
        links = sorted(set(url_re.findall(text)))
        out.append(md_h2(rel))
        for url in links:
            out.append(f"- {url}\n")
        if not links:
            out.append("(no links)\n")
    return "".join(out)


# ----------------------------
# Template generator
# ----------------------------


TEMPLATES = {
    "issue": """# Issue Template\n\n## Summary\nDescribe the issue concisely.\n\n## Steps to Reproduce\n1. ...\n\n## Expected Behavior\n\n## Actual Behavior\n\n## Additional Context\n- OS: \n- Version: \n""",
    "pr": """# Pull Request Template\n\n## Summary\nWhat does this PR change?\n\n## Motivation\n\n## Changes\n- ...\n\n## Checklist\n- [ ] Tests added/updated\n- [ ] Docs updated\n""",
    "bug-report": """# Bug Report\n\n## Description\n\n## Steps to Reproduce\n\n## Expected\n\n## Actual\n\n## Logs / Screenshots\n\n## Environment\n\n""",
    "feature-request": """# Feature Request\n\n## Problem\n\n## Proposal\n\n## Alternatives\n\n## Additional Context\n\n""",
    "code-review-checklist": """# Code Review Checklist\n\n- [ ] Correctness\n- [ ] Tests\n- [ ] Performance\n- [ ] Security\n- [ ] Readability\n- [ ] Documentation\n""",
    "security-report": """# Security Report\n\n## Summary\n\n## Impact\n\n## Affected Components\n\n## Reproduction\n\n## Mitigation\n\n""",
    "release-notes": """# Release Notes\n\n## Version X.Y.Z — YYYY-MM-DD\n\n### Highlights\n- ...\n\n### Changes\n- ...\n\n### Migration Notes\n- ...\n""",
    "testing-plan": """# Testing Plan\n\n## Scope\n\n## Test Cases\n- ...\n\n## Environments\n\n## Risks\n\n""",
    "adr": """# Architecture Decision Record (ADR)\n\n## Context\n\n## Decision\n\n## Consequences\n\n""",
    "contributing": """# Contributing\n\nThanks for contributing!\n\n## Development Setup\n\n## Pull Requests\n\n## Coding Standards\n\n""",
    "roadmap": """# Roadmap\n\n## Q1\n- ...\n\n## Q2\n- ...\n\n""",
    "design-doc": """# Design Document\n\n## Background\n\n## Goals\n\n## Non-Goals\n\n## Design\n\n## Alternatives\n\n""",
    "api-spec": """# API Spec\n\n## Overview\n\n## Endpoints\n- GET /...\n- POST /...\n\n## Models\n\n""",
    "sprint-planning": """# Sprint Planning\n\n## Goals\n\n## Stories\n- ...\n\n## Risks\n\n""",
    "meeting-notes": """# Meeting Notes\n\n- Date: \n- Attendees: \n\n## Notes\n- ...\n\n## Actions\n- [ ] ...\n""",
}


def cmd_template_gen(name: str) -> str:
    tpl = TEMPLATES.get(name)
    if not tpl:
        return md_h1("Template Generator") + f"Unknown template: {name}\n"
    return tpl


# ----------------------------
# CLI wiring
# ----------------------------


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="llm_context.toolbelt", description="LLM Context Toolbelt")
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add_path_arg(p):
        p.add_argument("--path", default=".", help="Path to scan (default: .)")

    # Scanner commands
    add_path_arg(sub.add_parser("todo-scan"))
    add_path_arg(sub.add_parser("fixme-scan"))
    add_path_arg(sub.add_parser("error-scan"))
    add_path_arg(sub.add_parser("bug-scan"))
    add_path_arg(sub.add_parser("secret-scan"))
    add_path_arg(sub.add_parser("code-stats"))
    add_path_arg(sub.add_parser("comment-summary"))
    p = sub.add_parser("long-func-scan")
    add_path_arg(p)
    p.add_argument("--min-lines", type=int, default=50)
    add_path_arg(sub.add_parser("miss-docstring-scan"))
    p = sub.add_parser("duplicate-line-scan")
    add_path_arg(p)
    p.add_argument("--min-dupes", type=int, default=3)
    p = sub.add_parser("large-file-scan")
    add_path_arg(p)
    p.add_argument("--min-bytes", type=int, default=1_000_000)
    add_path_arg(sub.add_parser("syntax-scan-py"))
    add_path_arg(sub.add_parser("env-var-scan"))
    add_path_arg(sub.add_parser("license-detect"))
    p = sub.add_parser("link-check-md")
    add_path_arg(p)
    p.add_argument("--offline", action="store_true")
    add_path_arg(sub.add_parser("test-file-scan"))
    add_path_arg(sub.add_parser("deprecated-api-scan"))
    add_path_arg(sub.add_parser("print-debug-scan"))
    add_path_arg(sub.add_parser("magic-number-scan"))
    add_path_arg(sub.add_parser("tabs-scan"))
    add_path_arg(sub.add_parser("trailing-whitespace-scan"))
    add_path_arg(sub.add_parser("utf-bom-scan"))
    add_path_arg(sub.add_parser("non-ascii-scan"))
    add_path_arg(sub.add_parser("newline-consistency-scan"))
    p = sub.add_parser("line-length-scan")
    add_path_arg(p)
    p.add_argument("--max-len", type=int, default=120)
    add_path_arg(sub.add_parser("mixed-indent-scan"))
    add_path_arg(sub.add_parser("shebang-scan"))
    add_path_arg(sub.add_parser("empty-file-scan"))
    add_path_arg(sub.add_parser("dead-except-scan"))
    add_path_arg(sub.add_parser("broad-except-scan"))
    add_path_arg(sub.add_parser("eval-exec-scan"))
    add_path_arg(sub.add_parser("subprocess-shell-scan"))
    add_path_arg(sub.add_parser("hardcoded-path-scan"))
    add_path_arg(sub.add_parser("http-url-scan"))
    add_path_arg(sub.add_parser("version-number-scan"))
    add_path_arg(sub.add_parser("traceback-usage-scan"))
    add_path_arg(sub.add_parser("unreachable-code-scan-py"))
    add_path_arg(sub.add_parser("commented-out-code-scan"))
    p = sub.add_parser("many-params-scan")
    add_path_arg(p)
    p.add_argument("--max-params", type=int, default=6)
    add_path_arg(sub.add_parser("license-header-missing-scan"))
    add_path_arg(sub.add_parser("typing-missing-scan"))
    add_path_arg(sub.add_parser("logger-debug-scan"))
    add_path_arg(sub.add_parser("sleep-call-scan"))
    add_path_arg(sub.add_parser("annotation-scan"))
    add_path_arg(sub.add_parser("pinned-versions-scan"))
    add_path_arg(sub.add_parser("duplicate-filename-scan"))
    p = sub.add_parser("duplicate-file-contents-scan")
    add_path_arg(p)
    p.add_argument("--max-bytes", type=int, default=1_000_000)
    add_path_arg(sub.add_parser("binary-file-inventory"))
    p = sub.add_parser("large-line-scan")
    add_path_arg(p)
    p.add_argument("--min-len", type=int, default=500)
    p = sub.add_parser("trailing-empty-lines-scan")
    add_path_arg(p)
    p.add_argument("--min-trailing", type=int, default=2)
    add_path_arg(sub.add_parser("markdown-heading-index"))
    add_path_arg(sub.add_parser("markdown-image-check"))
    add_path_arg(sub.add_parser("markdown-word-count"))
    add_path_arg(sub.add_parser("yaml-syntax-scan"))
    add_path_arg(sub.add_parser("json-syntax-scan"))
    add_path_arg(sub.add_parser("xml-syntax-scan"))
    add_path_arg(sub.add_parser("html-syntax-scan"))
    add_path_arg(sub.add_parser("nocommit-scan"))

    # Converters/reporters
    add_path_arg(sub.add_parser("json-to-md"))
    p = sub.add_parser("csv-to-md")
    add_path_arg(p)
    p.add_argument("--max-rows", type=int, default=50)
    add_path_arg(sub.add_parser("md-to-txt"))
    add_path_arg(sub.add_parser("txt-to-md"))
    p = sub.add_parser("code-to-md")
    add_path_arg(p)
    p.add_argument("--max-bytes-per-file", type=int, default=50_000)
    add_path_arg(sub.add_parser("requirements-to-md"))
    add_path_arg(sub.add_parser("package-json-to-md"))
    add_path_arg(sub.add_parser("junit-xml-to-md"))
    add_path_arg(sub.add_parser("dir-tree-to-md"))
    add_path_arg(sub.add_parser("file-index"))
    add_path_arg(sub.add_parser("changelog-summary"))
    add_path_arg(sub.add_parser("readme-summary"))
    add_path_arg(sub.add_parser("metadata-pack"))
    add_path_arg(sub.add_parser("prompt-pack"))
    p = sub.add_parser("chunk")
    add_path_arg(p)
    p.add_argument("--file", required=True)
    p.add_argument("--lines-per-chunk", type=int, default=120)
    add_path_arg(sub.add_parser("token-estimate"))
    add_path_arg(sub.add_parser("image-inventory"))
    add_path_arg(sub.add_parser("dir-size-report"))
    add_path_arg(sub.add_parser("csv-summary"))
    p = sub.add_parser("json-schema-extract")
    add_path_arg(p)
    p.add_argument("--max-files", type=int, default=50)
    add_path_arg(sub.add_parser("api-spec-from-openapi"))
    add_path_arg(sub.add_parser("yaml-to-md"))
    add_path_arg(sub.add_parser("xml-to-md"))
    add_path_arg(sub.add_parser("html-to-md-text"))
    add_path_arg(sub.add_parser("ini-to-md"))
    add_path_arg(sub.add_parser("toml-to-md"))
    add_path_arg(sub.add_parser("properties-to-md"))
    add_path_arg(sub.add_parser("pyproject-to-md"))
    add_path_arg(sub.add_parser("gitignore-to-md"))
    add_path_arg(sub.add_parser("editorconfig-to-md"))
    add_path_arg(sub.add_parser("license-to-md"))
    add_path_arg(sub.add_parser("code-outline-py"))
    add_path_arg(sub.add_parser("import-list-py"))
    add_path_arg(sub.add_parser("function-metrics-py"))
    add_path_arg(sub.add_parser("class-metrics-py"))
    add_path_arg(sub.add_parser("docstring-summary-py"))
    add_path_arg(sub.add_parser("extension-inventory"))
    p = sub.add_parser("recent-files-report")
    add_path_arg(p)
    p.add_argument("--days", type=int, default=7)
    p = sub.add_parser("file-age-report")
    add_path_arg(p)
    p.add_argument("--top", type=int, default=20)
    add_path_arg(sub.add_parser("readme-links"))

    # Templates
    tp = sub.add_parser("template-gen")
    tp.add_argument("--name", required=True, choices=sorted(TEMPLATES.keys()))

    args = parser.parse_args(argv)

    try:
        if args.cmd == "todo-scan":
            content = cmd_todo_scan(args.path)
            out = report_path("todo-scan")
        elif args.cmd == "fixme-scan":
            content = cmd_fixme_scan(args.path)
            out = report_path("fixme-scan")
        elif args.cmd == "error-scan":
            content = cmd_error_scan(args.path)
            out = report_path("error-scan")
        elif args.cmd == "bug-scan":
            content = cmd_bug_scan(args.path)
            out = report_path("bug-scan")
        elif args.cmd == "secret-scan":
            content = cmd_secret_scan(args.path)
            out = report_path("secret-scan")
        elif args.cmd == "code-stats":
            content = cmd_code_stats(args.path)
            out = report_path("code-stats")
        elif args.cmd == "comment-summary":
            content = cmd_comment_summary(args.path)
            out = report_path("comment-summary")
        elif args.cmd == "long-func-scan":
            content = cmd_long_func_scan(args.path, args.min_lines)
            out = report_path("long-func-scan")
        elif args.cmd == "miss-docstring-scan":
            content = cmd_miss_docstring_scan(args.path)
            out = report_path("miss-docstring-scan")
        elif args.cmd == "duplicate-line-scan":
            content = cmd_duplicate_line_scan(args.path, args.min_dupes)
            out = report_path("duplicate-line-scan")
        elif args.cmd == "large-file-scan":
            content = cmd_large_file_scan(args.path, args.min_bytes)
            out = report_path("large-file-scan")
        elif args.cmd == "syntax-scan-py":
            content = cmd_syntax_scan_py(args.path)
            out = report_path("syntax-scan-py")
        elif args.cmd == "env-var-scan":
            content = cmd_env_var_scan(args.path)
            out = report_path("env-var-scan")
        elif args.cmd == "license-detect":
            content = cmd_license_detect(args.path)
            out = report_path("license-detect")
        elif args.cmd == "link-check-md":
            content = cmd_link_check_md(args.path, args.offline)
            out = report_path("link-check-md")
        elif args.cmd == "test-file-scan":
            content = cmd_test_file_scan(args.path)
            out = report_path("test-file-scan")
        elif args.cmd == "deprecated-api-scan":
            content = cmd_deprecated_api_scan(args.path)
            out = report_path("deprecated-api-scan")
        elif args.cmd == "print-debug-scan":
            content = cmd_print_debug_scan(args.path)
            out = report_path("print-debug-scan")
        elif args.cmd == "magic-number-scan":
            content = cmd_magic_number_scan(args.path)
            out = report_path("magic-number-scan")
        elif args.cmd == "tabs-scan":
            content = cmd_tabs_scan(args.path)
            out = report_path("tabs-scan")
        elif args.cmd == "trailing-whitespace-scan":
            content = cmd_trailing_whitespace_scan(args.path)
            out = report_path("trailing-whitespace-scan")
        elif args.cmd == "utf-bom-scan":
            content = cmd_utf_bom_scan(args.path)
            out = report_path("utf-bom-scan")
        elif args.cmd == "non-ascii-scan":
            content = cmd_non_ascii_scan(args.path)
            out = report_path("non-ascii-scan")
        elif args.cmd == "newline-consistency-scan":
            content = cmd_newline_consistency_scan(args.path)
            out = report_path("newline-consistency-scan")
        elif args.cmd == "json-to-md":
            content = cmd_json_to_md(args.path)
            out = report_path("json-to-md")
        elif args.cmd == "csv-to-md":
            content = cmd_csv_to_md(args.path, args.max_rows)
            out = report_path("csv-to-md")
        elif args.cmd == "md-to-txt":
            content = cmd_md_to_txt(args.path)
            out = report_path("md-to-txt")
        elif args.cmd == "txt-to-md":
            content = cmd_txt_to_md(args.path)
            out = report_path("txt-to-md")
        elif args.cmd == "code-to-md":
            content = cmd_code_to_md(args.path, args.max_bytes_per_file)
            out = report_path("code-to-md")
        elif args.cmd == "requirements-to-md":
            content = cmd_requirements_to_md(args.path)
            out = report_path("requirements-to-md")
        elif args.cmd == "package-json-to-md":
            content = cmd_package_json_to_md(args.path)
            out = report_path("package-json-to-md")
        elif args.cmd == "junit-xml-to-md":
            content = cmd_junit_xml_to_md(args.path)
            out = report_path("junit-xml-to-md")
        elif args.cmd == "dir-tree-to-md":
            content = cmd_dir_tree_to_md(args.path)
            out = report_path("dir-tree-to-md")
        elif args.cmd == "file-index":
            content = cmd_file_index(args.path)
            out = report_path("file-index")
        elif args.cmd == "changelog-summary":
            content = cmd_changelog_summary(args.path)
            out = report_path("changelog-summary")
        elif args.cmd == "readme-summary":
            content = cmd_readme_summary(args.path)
            out = report_path("readme-summary")
        elif args.cmd == "metadata-pack":
            content = cmd_metadata_pack(args.path)
            out = report_path("metadata-pack")
        elif args.cmd == "prompt-pack":
            content = cmd_prompt_pack(args.path)
            out = report_path("prompt-pack")
        elif args.cmd == "chunk":
            content = cmd_chunk(args.path, args.file, args.lines_per_chunk)
            out = report_path("chunk")
        elif args.cmd == "token-estimate":
            content = cmd_token_estimate(args.path)
            out = report_path("token-estimate")
        elif args.cmd == "image-inventory":
            content = cmd_image_inventory(args.path)
            out = report_path("image-inventory")
        elif args.cmd == "dir-size-report":
            content = cmd_dir_size_report(args.path)
            out = report_path("dir-size-report")
        elif args.cmd == "csv-summary":
            content = cmd_csv_summary(args.path)
            out = report_path("csv-summary")
        elif args.cmd == "json-schema-extract":
            content = cmd_json_schema_extract(args.path, args.max_files)
            out = report_path("json-schema-extract")
        elif args.cmd == "api-spec-from-openapi":
            content = cmd_api_spec_from_openapi(args.path)
            out = report_path("api-spec-from-openapi")
        elif args.cmd == "line-length-scan":
            content = cmd_line_length_scan(args.path, args.max_len)
            out = report_path("line-length-scan")
        elif args.cmd == "mixed-indent-scan":
            content = cmd_mixed_indent_scan(args.path)
            out = report_path("mixed-indent-scan")
        elif args.cmd == "shebang-scan":
            content = cmd_shebang_scan(args.path)
            out = report_path("shebang-scan")
        elif args.cmd == "empty-file-scan":
            content = cmd_empty_file_scan(args.path)
            out = report_path("empty-file-scan")
        elif args.cmd == "dead-except-scan":
            content = cmd_dead_except_scan(args.path)
            out = report_path("dead-except-scan")
        elif args.cmd == "broad-except-scan":
            content = cmd_broad_except_scan(args.path)
            out = report_path("broad-except-scan")
        elif args.cmd == "eval-exec-scan":
            content = cmd_eval_exec_scan(args.path)
            out = report_path("eval-exec-scan")
        elif args.cmd == "subprocess-shell-scan":
            content = cmd_subprocess_shell_scan(args.path)
            out = report_path("subprocess-shell-scan")
        elif args.cmd == "hardcoded-path-scan":
            content = cmd_hardcoded_path_scan(args.path)
            out = report_path("hardcoded-path-scan")
        elif args.cmd == "http-url-scan":
            content = cmd_http_url_scan(args.path)
            out = report_path("http-url-scan")
        elif args.cmd == "version-number-scan":
            content = cmd_version_number_scan(args.path)
            out = report_path("version-number-scan")
        elif args.cmd == "traceback-usage-scan":
            content = cmd_traceback_usage_scan(args.path)
            out = report_path("traceback-usage-scan")
        elif args.cmd == "unreachable-code-scan-py":
            content = cmd_unreachable_code_scan_py(args.path)
            out = report_path("unreachable-code-scan-py")
        elif args.cmd == "commented-out-code-scan":
            content = cmd_commented_out_code_scan(args.path)
            out = report_path("commented-out-code-scan")
        elif args.cmd == "many-params-scan":
            content = cmd_many_params_scan(args.path, args.max_params)
            out = report_path("many-params-scan")
        elif args.cmd == "license-header-missing-scan":
            content = cmd_license_header_missing_scan(args.path)
            out = report_path("license-header-missing-scan")
        elif args.cmd == "typing-missing-scan":
            content = cmd_typing_missing_scan(args.path)
            out = report_path("typing-missing-scan")
        elif args.cmd == "logger-debug-scan":
            content = cmd_logger_debug_scan(args.path)
            out = report_path("logger-debug-scan")
        elif args.cmd == "sleep-call-scan":
            content = cmd_sleep_call_scan(args.path)
            out = report_path("sleep-call-scan")
        elif args.cmd == "annotation-scan":
            content = cmd_annotation_scan(args.path)
            out = report_path("annotation-scan")
        elif args.cmd == "pinned-versions-scan":
            content = cmd_pinned_versions_scan(args.path)
            out = report_path("pinned-versions-scan")
        elif args.cmd == "duplicate-filename-scan":
            content = cmd_duplicate_filename_scan(args.path)
            out = report_path("duplicate-filename-scan")
        elif args.cmd == "duplicate-file-contents-scan":
            content = cmd_duplicate_file_contents_scan(args.path, args.max_bytes)
            out = report_path("duplicate-file-contents-scan")
        elif args.cmd == "binary-file-inventory":
            content = cmd_binary_file_inventory(args.path)
            out = report_path("binary-file-inventory")
        elif args.cmd == "large-line-scan":
            content = cmd_large_line_scan(args.path, args.min_len)
            out = report_path("large-line-scan")
        elif args.cmd == "trailing-empty-lines-scan":
            content = cmd_trailing_empty_lines_scan(args.path, args.min_trailing)
            out = report_path("trailing-empty-lines-scan")
        elif args.cmd == "markdown-heading-index":
            content = cmd_markdown_heading_index(args.path)
            out = report_path("markdown-heading-index")
        elif args.cmd == "markdown-image-check":
            content = cmd_markdown_image_check(args.path)
            out = report_path("markdown-image-check")
        elif args.cmd == "markdown-word-count":
            content = cmd_markdown_word_count(args.path)
            out = report_path("markdown-word-count")
        elif args.cmd == "yaml-syntax-scan":
            content = cmd_yaml_syntax_scan(args.path)
            out = report_path("yaml-syntax-scan")
        elif args.cmd == "json-syntax-scan":
            content = cmd_json_syntax_scan(args.path)
            out = report_path("json-syntax-scan")
        elif args.cmd == "xml-syntax-scan":
            content = cmd_xml_syntax_scan(args.path)
            out = report_path("xml-syntax-scan")
        elif args.cmd == "html-syntax-scan":
            content = cmd_html_syntax_scan(args.path)
            out = report_path("html-syntax-scan")
        elif args.cmd == "nocommit-scan":
            content = cmd_nocommit_scan(args.path)
            out = report_path("nocommit-scan")
        elif args.cmd == "yaml-to-md":
            content = cmd_yaml_to_md(args.path)
            out = report_path("yaml-to-md")
        elif args.cmd == "xml-to-md":
            content = cmd_xml_to_md(args.path)
            out = report_path("xml-to-md")
        elif args.cmd == "html-to-md-text":
            content = cmd_html_to_md_text(args.path)
            out = report_path("html-to-md-text")
        elif args.cmd == "ini-to-md":
            content = cmd_ini_to_md(args.path)
            out = report_path("ini-to-md")
        elif args.cmd == "toml-to-md":
            content = cmd_toml_to_md(args.path)
            out = report_path("toml-to-md")
        elif args.cmd == "properties-to-md":
            content = cmd_properties_to_md(args.path)
            out = report_path("properties-to-md")
        elif args.cmd == "pyproject-to-md":
            content = cmd_pyproject_to_md(args.path)
            out = report_path("pyproject-to-md")
        elif args.cmd == "gitignore-to-md":
            content = cmd_gitignore_to_md(args.path)
            out = report_path("gitignore-to-md")
        elif args.cmd == "editorconfig-to-md":
            content = cmd_editorconfig_to_md(args.path)
            out = report_path("editorconfig-to-md")
        elif args.cmd == "license-to-md":
            content = cmd_license_to_md(args.path)
            out = report_path("license-to-md")
        elif args.cmd == "code-outline-py":
            content = cmd_code_outline_py(args.path)
            out = report_path("code-outline-py")
        elif args.cmd == "import-list-py":
            content = cmd_import_list_py(args.path)
            out = report_path("import-list-py")
        elif args.cmd == "function-metrics-py":
            content = cmd_function_metrics_py(args.path)
            out = report_path("function-metrics-py")
        elif args.cmd == "class-metrics-py":
            content = cmd_class_metrics_py(args.path)
            out = report_path("class-metrics-py")
        elif args.cmd == "docstring-summary-py":
            content = cmd_docstring_summary_py(args.path)
            out = report_path("docstring-summary-py")
        elif args.cmd == "extension-inventory":
            content = cmd_extension_inventory(args.path)
            out = report_path("extension-inventory")
        elif args.cmd == "recent-files-report":
            content = cmd_recent_files_report(args.path, args.days)
            out = report_path("recent-files-report")
        elif args.cmd == "file-age-report":
            content = cmd_file_age_report(args.path, args.top)
            out = report_path("file-age-report")
        elif args.cmd == "readme-links":
            content = cmd_readme_links(args.path)
            out = report_path("readme-links")
        elif args.cmd == "template-gen":
            content = cmd_template_gen(args.name)
            out = report_path(f"template-{args.name}")
        else:
            parser.error("Unknown command")
            return 2
        write_text(out, content)
        print(out)
        return 0
    except Exception:
        print("Encountered an unexpected error:")
        traceback.print_exc()
        return 1


def run_from_wrapper(subcommand: str, extra_args: Optional[List[str]] = None) -> None:
    argv = [subcommand]
    if extra_args:
        argv.extend(extra_args)
    sys.exit(main(argv))


if __name__ == "__main__":
    sys.exit(main())
