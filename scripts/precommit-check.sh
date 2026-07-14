#!/bin/bash
# precommit-check.sh — 验证 RST 文档语法
# 使用 Sphinx 的 rst2html 工具检查所有 .rst 文件的语法

set -e

echo "=== Checking RST syntax ==="
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo "$(dirname "$0")/..")"

# 查找所有 .rst 文件并检查语法
ERRORS=0
while IFS= read -r -d '' file; do
    if ! python3 -m sphinx.util.rst check "$file" 2>/dev/null; then
        echo "ERROR: $file"
        ERRORS=$((ERRORS + 1))
    fi
done < <(find source/ -name "*.rst" -print0)

if [ $ERRORS -eq 0 ]; then
    echo "=== All RST files passed ==="
else
    echo "=== $ERRORS file(s) had errors ==="
    exit 1
fi
