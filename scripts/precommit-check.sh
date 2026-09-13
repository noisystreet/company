#!/bin/bash
# precommit-check.sh — 提交前检查
# 1. RST 语法：docutils 真实解析（scripts/check-rst-syntax.py）
# 2. 中文排版：盘古之白间距 + 引号成对（scripts/check-cjk-spacing.py）

set -e

cd "$(git rev-parse --show-toplevel 2>/dev/null || echo "$(dirname "$0")/..")"

echo "=== Checking RST syntax ==="
python3 scripts/check-rst-syntax.py

echo "=== Checking CJK spacing & quotes ==="
python3 scripts/check-cjk-spacing.py

echo "=== All checks passed ==="
