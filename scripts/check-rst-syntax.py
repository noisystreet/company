#!/usr/bin/env python3
"""Real RST syntax check via docutils.

docutils 不认识 Sphinx 特有指令/角色（toctree、ref、todolist、mermaid 等），
这些报错加入白名单忽略；其余（标题下划线长度、缩进错位、表格断裂等）
全部视为失败。最终语义正确性仍由 sphinx 构建（CI 中的 make html -W）兜底。

用法:
    python3 scripts/check-rst-syntax.py            # 检查 source/ 下所有 .rst
    python3 scripts/check-rst-syntax.py FILE.rst   # 只检查指定文件
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

from docutils.core import publish_doctree

ROOT = Path(__file__).resolve().parent.parent / "source"

# Sphinx-only 语法，docutils 必然误报，忽略
WHITELIST = (
    "Unknown directive type",
    "Unknown interpreted text role",
    "No directive entry",
    "No role entry",
    'No directive handler',  # docutils 版本差异
)


def check_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    # warning_stream 指向 StringIO，避免 docutils 重复输出到 stderr
    doctree = publish_doctree(
        text,
        source_path=str(path),
        settings_overrides={
            "report_level": 2,
            "halt_level": 5,
            "warning_stream": io.StringIO(),
        },
    )
    problems: list[str] = []
    for node in doctree.findall(lambda n: n.tagname == "system_message"):
        level = node.get("level", 0)
        line = node.get("line", "?")
        # system_message 的 astext() 带 source:line 前缀，纯文本在 children 里
        message = node.children[0].astext() if node.children else node.astext()
        if level >= 2 and not any(w in message for w in WHITELIST):
            problems.append(f"{path}:{line}: (level {level}) {message}")
    return problems


def main() -> int:
    targets = [Path(a) for a in sys.argv[1:]] or sorted(ROOT.rglob("*.rst"))
    all_problems: list[str] = []
    for path in targets:
        all_problems.extend(check_file(path))
    if all_problems:
        for problem in all_problems:
            print(problem)
        print(f"=== {len(all_problems)} RST problem(s) found ===")
        return 1
    print("=== All RST files passed syntax check ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
