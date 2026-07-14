# agents.md — 公司制度全景解析 项目

## 项目概述

本项目编写一本 **公司制度全景解析** 技术文档，使用 reStructuredText（`.rst`）格式，基于 Sphinx 构建。

- 文档源目录：`source/`
- 构建输出：`./_build/html/`（`make html` 后生成）
- 目标读者：创业者、投资人、企业法务、商学院学生
- 参考材料：`公司治理_参考手册.md`、`中国资本市场基础_参考手册.md`、`初创公司股权结构_参考手册.md`

## 项目文件说明

| 文件 | 说明 |
|------|------|
| `source/preface/index.rst` | 前言：写作动机、目标读者、预备知识、全书结构 |
| `source/index.rst` | Sphinx 根文档（toctree 入口） |
| `source/chapter_01_intro/` | 公司制度概述（公司的本质、制度演进、核心架构） |
| `source/chapter_02_governance/` | 公司治理架构（股东会、董事会、管理层、监事会、独立董事） |
| `source/chapter_03_charter/` | 公司章程与股东协议（章程条款、投资协议、一票否决权、对赌协议） |
| `source/chapter_04_equity/` | 股权结构设计（AB股、持股平台、融资阶段演变、VIE结构） |
| `source/chapter_05_financing/` | 融资与资本运作（融资路径、估值方法、投资条款、并购） |
| `source/chapter_06_esop/` | 员工激励与ESOP（期权池、归属安排、税务考量） |
| `source/chapter_07_capital_market/` | 中国资本市场体系（多层次市场、各板块对比、注册制、境外上市） |
| `source/chapter_08_compliance/` | 合规与风险管理（信息披露、关联交易、内控、D&O保险） |
| `source/chapter_09_cases/` | 公司治理实践案例（治理失败、控制权争夺、创始人保卫战） |
| `source/chapter_10_trends/` | 未来趋势与制度创新（ESG、数字化治理、跨境治理） |
| `source/appendix/` | 附录（参考资源、术语表、法律法规索引） |
| `source/conf.py` | Sphinx 构建配置 |
| `Makefile` | 构建入口（`make html` / `make clean`） |
| `scripts/precommit-check.sh` | 预提交检查脚本（验证 RST 文档语法） |
| `requirements.txt` | 构建依赖（sphinx, sphinx-rtd-theme, sphinxcontrib-mermaid） |
| `.readthedocs.yaml` | Read the Docs 构建配置 |
| `LICENSE` | CC BY-SA 4.0 许可证 |
| `.gitignore` | 版本控制忽略规则 |
| `agents.md` | **本文件**：AI 助手的工作上下文和约束 |

## 通用约束

1. **许可证**：本文档采用 CC BY-SA 4.0（Creative Commons Attribution-ShareAlike 4.0 International），详见 `LICENSE` 文件
2. **文档格式**：使用 reStructuredText（`.rst`）格式，中文写作
3. **git hooks**：clone 后首次提交前，运行以下命令启用 pre-commit 检查：

   ```bash
   git config --local core.hooksPath .githooks
   ```

   否则 pre-commit 检查不会自动生效。
4. **引用资料**：使用绝对路径的 `file:///` 链接引用参考手册，格式为 `` `链接文本 <file:///绝对路径/文件>`__ ``
5. **避免冗余**：不创建不必要的文件，优先编辑已有文件
6. **权限**：不做 `git push --force`、`reset --hard` 等破坏性操作

## 写作规范

### 文档结构
- 每篇文档应有标题
- 按章节组织，章节层级不超过三级
- 内容末尾标注生成日期和项目名称

### 引用规范
- 引用参考手册使用绝对路径 markdown 链接
- 引用法律法规使用正式名称和文号
- 关键案例应提供数据来源

### 内容深度
- 概念讲解与真实案例相结合
- 复杂流程配合 Mermaid 图表说明
- 关键对比用表格列出
- 避免大段堆叠法律条文，优先提炼核心要点

### 写作风格

**避免罗列结论**。每个知识点都应有推导过程。

- **实践驱动**：从真实商业场景出发引出概念，读者能"看见"问题在哪儿，再揭示制度设计的逻辑。每一节都遵循：现实问题 → 制度解法 → 利弊权衡 → 案例印证。
- **案例丰富**：每个制度概念必须有真实公司案例支撑。没有案例支撑的观点都是空谈。
- **过渡自然**：章节之间、段落之间要有承上启下的过渡句。禁止生硬切换话题。

## 写作路线图

按以下顺序推进内容编写：

1. **第 1 章：公司制度概述** — 公司的本质、制度演进历史、核心架构
2. **第 2 章：公司治理架构** — 股东会→董事会→管理层→监事会的权力划分与博弈
3. **第 3 章：公司章程与股东协议** — 章程关键条款、投资协议条款、一票否决权、对赌协议
4. **第 4 章：股权结构设计** — 一元/二元/多元股权结构、AB股、持股平台、VIE结构
5. **第 5 章：融资与资本运作** — 融资路径、估值方法、投资条款、并购重组
6. **第 6 章：员工激励与ESOP** — 期权池设计、归属安排、限制性股票、税务考量
7. **第 7 章：中国资本市场体系** — 多层次资本市场、各板块对比、注册制改革、境外上市
8. **第 8 章：合规与风险管理** — 信息披露、关联交易、内控体系、D&O保险
9. **第 9 章：公司治理实践案例** — 经典治理失败、控制权争夺、创始人保卫战
10. **第 10 章：未来趋势与制度创新** — ESG、数字化治理、跨境治理、制度变革

## 构建方法

```bash
# 安装依赖
pip install -r requirements.txt

# 构建 HTML 文档
make html

# 构建产物位于 _build/html/
```

自动部署到 Read the Docs 后，文档会自动构建并托管。本地构建也可通过 `make html` 完成。

## 开发提示

- **构建**：`make html`（产物在 `_build/html/`）。本地开发用 `make html` 即可。
- **预览**：`make serve` 会先构建再用 `python3 -m http.server` 启动预览，默认端口 8000。
- **语法检查**：`bash scripts/precommit-check.sh`
- **git hooks**（仅在需要提交触发 pre-commit 检查时）：`git config --local core.hooksPath .githooks`。
- 修改 `.rst` 内容后无热重载，需重新 `make html` 才能在预览中看到更新。
