# Implementation Plan: 轻量级提示词管理CLI工具

**Branch**: `001-prompt-management-cli` | **Date**: 2025-10-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-prompt-management-cli/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

创建一个轻量级的Python CLI工具(sckit-cli)，用于管理和部署AI编辑器的提示词文件。工具通过uv安装，从GitHub Release下载模板，支持在新项目或现有项目中初始化提示词到Cursor或Claude Code的配置目录。核心价值：集中管理分散的提示词文档，一键部署到AI编辑器。

## Technical Context

**Language/Version**: Python 3.8+（为了兼容性，支持较旧的Python版本）
**Primary Dependencies**: 
- `typer` - CLI框架
- `rich` - 终端UI和进度显示
- `httpx` - HTTP客户端，支持进度跟踪
- Python标准库: `pathlib`, `zipfile`, `tempfile`, `shutil`

**Storage**: N/A（无持久化数据存储，临时文件用后即删）
**Testing**: pytest（单元测试和集成测试）
**Target Platform**: 跨平台（Windows、macOS、Linux）
**Project Type**: Single project（CLI工具，单一入口点）
**Performance Goals**: 
- 安装完成时间 < 30秒
- 模板下载和部署 < 10秒（标准网络条件）
- CLI响应时间 < 100ms

**Constraints**: 
- 必须支持离线安装CLI（但init需要网络）
- 临时文件必须自动清理
- 错误处理必须友好，100%提供明确错误消息
- 支持Ctrl+C优雅退出

**Scale/Scope**: 
- 单个CLI工具包
- 2个子命令：`init`, `--version`, `--help`
- 支持2种编辑器：Cursor, Claude Code
- 预期模板包大小 < 5MB

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Status**: ✅ 已通过Constitution检查

基于项目需求，已创建正式的constitution文档（`.specify/memory/constitution.md`）：

### 核心原则验证

| 原则 | 检查结果 | 说明 |
|------|---------|------|
| **简单性优先** | ✅ 通过 | 单一职责工具，无复杂架构，单文件CLI设计 |
| **用户体验优先** | ✅ 通过 | 100%友好错误消息，Rich美化输出，交互式选择 |
| **跨平台一致性** | ✅ 通过 | pathlib路径处理，信号处理跨平台，三平台测试 |
| **测试驱动开发** | ✅ 通过 | 三层测试结构（contract/integration/unit） |
| **最小依赖** | ✅ 通过 | 仅4个轻量依赖（typer、rich、httpx、pytest） |

### 设计决策合规性

- ✅ 无微服务架构
- ✅ 直接HTTP调用，无SDK
- ✅ 无数据库，无持久化
- ✅ 临时文件即用即删
- ✅ 所有外部依赖已审批

**Re-check after Phase 1**: 所有Phase 1设计决策符合Constitution要求。

## Project Structure

### Documentation (this feature)

```text
specs/001-prompt-management-cli/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output - 技术决策和最佳实践
├── data-model.md        # Phase 1 output - 数据结构定义
├── quickstart.md        # Phase 1 output - 快速开始指南
├── contracts/           # Phase 1 output - CLI接口规范
│   └── cli-interface.yaml
├── spec.md              # 功能规格说明
└── checklists/          # 质量检查清单
    └── requirements.md
```

### Source Code (repository root)

参考spec-kit项目结构，采用简化的标准Python包布局：

```text
src/sckit_cli/            # Python源代码包（参考spec-kit/src/specify_cli/）
├── __init__.py           # 主模块，包含CLI应用和所有逻辑
└── py.typed              # PEP 561类型标记文件

tests/                    # 测试目录
├── contract/             # 契约测试
│   ├── test_github_api.py    # GitHub API契约
│   └── test_cli_contract.py  # CLI接口契约
├── integration/          # 集成测试
│   ├── test_init_workflow.py  # 完整初始化流程
│   └── test_update_workflow.py # 更新/强制覆盖流程
└── unit/                 # 单元测试
    ├── test_editor.py
    ├── test_release.py
    ├── test_config.py
    └── test_validators.py

commands/                 # 提示词模板源文件（单份存储，参考spec-kit/templates/commands/）
├── example.md           # 示例提示词（Markdown格式）
└── README.md            # 提示词说明文档

.github/
└── workflows/
    ├── release.yml      # CI/CD主流程：版本管理和Release创建
    └── scripts/         # Release打包脚本（参考spec-kit/.github/workflows/scripts/）
        ├── create-release-packages.sh  # 从commands/打包cursor和claude两种zip
        └── create-github-release.sh    # 上传zip到GitHub Release

pyproject.toml            # 项目配置（uv兼容）
README.md                 # 项目文档（包含安装、快速开始、使用说明）
CHANGELOG.md              # 版本变更记录
LICENSE                   # MIT许可证
.gitignore                # Git忽略文件
```

**Structure Decision**: 

参考spec-kit的简洁设计，采用单文件CLI架构：

1. **单文件设计** (`src/sckit_cli/__init__.py`):
   - 所有代码集中在一个文件中，参考`spec-kit/src/specify_cli/__init__.py`
   - 便于维护和理解，无需在多个文件间跳转
   - 适合中小型CLI工具（预计 < 1000行代码）

2. **简洁文档** (根目录`README.md`):
   - 集中所有文档到单个README（简单优先）
   - 包含：项目简介、安装指南、快速开始、使用说明
   - 降低新用户学习成本，无需在多个文件间跳转

3. **模板源文件** (`commands/`):
   - **单源存储**：仅存一份Markdown格式的提示词文件（参考spec-kit/templates/commands/）
   - **多目标打包**：CI/CD根据编辑器要求打包：
     - `sckit-cursor-{version}.zip` → 包含`.cursor/commands/*.md`
     - `sckit-claude-{version}.zip` → 包含`.claude/commands/*.md`
   - 两个编辑器都使用Markdown格式，内容相同，仅目录结构不同
   - 用户通过`sckit init`下载对应的zip并部署

4. **三层测试** (`tests/`):
   - Contract: 验证GitHub API和编辑器契约
   - Integration: 端到端工作流测试
   - Unit: 单元逻辑测试

5. **标准Python包**:
   - `pyproject.toml`: PEP 517/518标准配置
   - `src/` layout: 现代Python推荐结构
   - 支持`uv tool install`直接安装

## Complexity Tracking

无需填写。该项目遵循简单优先原则，未引入复杂架构：
- 单一CLI工具，无微服务
- 直接HTTP调用GitHub API，无抽象层
- 标准文件系统操作，无ORM
- 轻量级依赖，无重框架
