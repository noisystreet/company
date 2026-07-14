#!/usr/bin/env python3
"""Check CJK spacing in RST files - ensure proper spacing between CJK and Latin characters."""
import re
import sys
from pathlib import Path


def check_file(filepath: Path) -> list[str]:
    issues = []
    content = filepath.read_text(encoding="utf-8")
    # Pattern: Latin char followed directly by CJK char (missing space)
    pattern = re.compile(r"([a-zA-Z0-9])([\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])")
    for lineno, line in enumerate(content.split("\n"), 1):
        if pattern.search(line):
            issues.append(f"{filepath}:{lineno}: {line.strip()}")
    return issues


def main():
    root = Path("source")
    all_issues = []
    for rst_file in root.rglob("*.rst"):
        all_issues.extend(check_file(rst_file))
    if all_issues:
        print("CJK spacing issues found:")
        for issue in all_issues:
            print(f"  {issue}")
        sys.exit(1)
    else:
        print("All files pass CJK spacing check.")


if __name__ == "__main__":
    main()
