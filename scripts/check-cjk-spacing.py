#!/usr/bin/env python3
"""Check/fix Chinese typography in RST sources.

Rules (盘古之白，参考《中文文案排版指北》):
1. CJK 字符与英文字母/数字之间加一个空格，双向检查；
   全角标点（（）、。等）与任何字符之间不加空格，不检查。
2. 正文中的 ASCII 直引号 "..." 按行内成对转为中文引号 “...”。

以下内容一律跳过、不做修改：
- 字面块（段落结尾 :: 引导的缩进块）及 code-block / mermaid 等字面类指令
- 注释行、指令选项字段行（如 :header-rows: 1）、链接目标行（.. _x:）
- 行内代码（``code``）与行内链接中的 <URI> 部分

用法:
    python3 scripts/check-cjk-spacing.py          # 仅报告
    python3 scripts/check-cjk-spacing.py --fix    # 原地修复
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "source"

CJK = "\u4e00-\u9fff"
LATIN = "A-Za-z0-9"

RE_SPACE_PATTERNS = [
    re.compile(rf"([{LATIN}]+)([{CJK}])"),
    re.compile(rf"([{CJK}])([{LATIN}]+)"),
]
RE_QUOTE_PAIR = re.compile(r'"([^"\n]+)"')
RE_DBL_LITERAL = re.compile(r"``[^`\n]*``")
RE_URI = re.compile(r"<[^<>\n]*>")
RE_FIELD = re.compile(r"^\s+:[\w-]+:")
RE_TARGET = re.compile(r"^\s*\.\.\s*_")
RE_DIRECTIVE = re.compile(r"^\s*\.\.\s+([\w:-]+)(::)?")

# 内容属于原样文本、整体跳过的指令
LITERAL_DIRECTIVES = {
    "code", "code-block", "sourcecode", "literalinclude",
    "mermaid", "math", "raw", "aafig", "productionlist",
}


def compute_skips(lines: list[str]) -> list[bool]:
    """标记整行跳过（不参与检查/修复）的行。"""
    n = len(lines)
    skip = [False] * n
    i = 0
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if stripped == "":
            i += 1
            continue
        if stripped.startswith(".."):
            if RE_TARGET.match(line):
                skip[i] = True
                i += 1
                continue
            m = RE_DIRECTIVE.match(line)
            # [\w:-]+ 会贪婪吞掉尾部 "::"，须剥离后才能比对指令名
            name = m.group(1).rstrip(":") if m else ""
            is_literal = (m is None) or (name in LITERAL_DIRECTIVES)
            base = len(line) - len(line.lstrip())
            skip[i] = True
            if is_literal:
                # 注释或字面类指令：整块跳过
                j = i + 1
                while j < n:
                    if lines[j].strip() == "":
                        j += 1
                        continue
                    if len(lines[j]) - len(lines[j].lstrip()) > base:
                        skip[j] = True
                        j += 1
                    else:
                        break
                i = j
            else:
                # 正文类指令（list-table/note 等）：仅跳过指令行，
                # 其内容照常检查（字段行由下方规则跳过）
                i += 1
            continue
        if RE_FIELD.match(line):
            skip[i] = True
            i += 1
            continue
        if stripped == "::" or stripped.endswith("::"):
            # 字面块引导行/段落：引导行本身若是纯 "::" 则跳过，
            # 随后更深的缩进块整体跳过
            if stripped == "::":
                skip[i] = True
            base = len(line) - len(line.lstrip())
            j = i + 1
            while j < n and lines[j].strip() == "":
                j += 1
            if j < n:
                first = len(lines[j]) - len(lines[j].lstrip())
                if first > base:
                    while j < n:
                        if lines[j].strip() == "":
                            j += 1
                            continue
                        ind = len(lines[j]) - len(lines[j].lstrip())
                        if ind >= first:
                            skip[j] = True
                            j += 1
                        else:
                            break
            i += 1
            continue
        i += 1
    return skip


def protect_inline(line: str) -> tuple[str, dict[str, str]]:
    """把行内不可修改片段换成哨兵，返回掩码行与还原表。"""
    stash: dict[str, str] = {}

    def keep(m: re.Match) -> str:
        token = f"\x00{len(stash)}\x00"
        stash[token] = m.group(0)
        return token

    line = RE_DBL_LITERAL.sub(keep, line)
    # 单反引号 span（链接/角色）：仅保护其中嵌入的 <URI>
    def mask_uri(m: re.Match) -> str:
        return "`" + RE_URI.sub(keep, m.group(1)) + "`"

    line = re.sub(r"`([^`\n]*)`", mask_uri, line)
    return line, stash


def fix_line(line: str) -> str:
    masked, stash = protect_inline(line)
    for pat in RE_SPACE_PATTERNS:
        masked = pat.sub(r"\1 \2", masked)
    if masked.count('"') >= 2 and masked.count('"') % 2 == 0:
        masked = RE_QUOTE_PAIR.sub(lambda m: "\u201c" + m.group(1) + "\u201d", masked)
    for token, original in stash.items():
        masked = masked.replace(token, original)
    return masked


def iter_rst_files():
    for path in sorted(ROOT.rglob("*.rst")):
        yield path


def main() -> int:
    fix = "--fix" in sys.argv[1:]
    total_issues = 0
    for path in iter_rst_files():
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        skip = compute_skips(lines)
        issues: list[str] = []
        changed = False
        for idx, line in enumerate(lines):
            if skip[idx]:
                continue
            fixed = fix_line(line)
            if fixed != line:
                issues.append(f"  {path}:{idx + 1}: {line.strip()[:60]}")
                if fix:
                    lines[idx] = fixed
                    changed = True
        if issues:
            total_issues += len(issues)
            mode = "FIXED" if fix else "ISSUE"
            print(f"{mode} {path} ({len(issues)} line(s))")
            for item in issues[:5]:
                print(item)
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")
            if fix:
                path.write_text("\n".join(lines), encoding="utf-8")
    if total_issues == 0:
        print("All files pass CJK spacing & quote checks.")
        return 0
    print(f"{total_issues} line(s) {'fixed' if fix else 'with issues'}.")
    return 0 if fix else 1


if __name__ == "__main__":
    sys.exit(main())
