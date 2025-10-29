# Implementation Plan: Init 命令交互式选择界面

**Branch**: `002-init-selection-ui` | **Date**: 2025-10-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-init-selection-ui/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

将 `sckit init` 命令的编辑器选择方式从手动文本输入改为上下箭头键可视化选择界面。使用 `inquirer` 或类似轻量级交互库替代当前的 `rich.Prompt.ask()`，提供跨平台的键盘导航体验，减少输入错误，提升操作流畅度。改进仅限于 `prompt_editor_choice()` 函数，保持其他功能不变。

## Technical Context

**Language/Version**: Python 3.8+（当前项目要求）  
**Primary Dependencies**: 
  - `typer>=0.9.0`（CLI框架，已有）
  - `rich>=13.0.0`（终端UI，已有）
  - NEEDS CLARIFICATION: 交互式选择库（`inquirer`, `questionary`, `simple-term-menu` 三选一）
  
**Storage**: N/A（仅内存状态管理）  
**Testing**: `pytest>=7.0.0`（已有）  
**Target Platform**: 跨平台（Windows PowerShell, macOS/Linux Shell）  
**Project Type**: 单一CLI项目（src/sckit_cli/）  
**Performance Goals**: 
  - 选择界面响应时间 < 50ms（按键到界面更新）
  - CLI启动时间保持 < 100ms（不因新库增加启动负担）
  
**Constraints**: 
  - 跨平台键盘兼容性（方向键在不同终端中的表现）
  - 非交互式环境兼容（CI/CD自动回退到默认值）
  - 依赖体积限制（新库安装包 < 500KB，满足 Constitution V）
  
**Scale/Scope**: 
  - 仅修改1个函数（`prompt_editor_choice()`）
  - 影响1个命令（`sckit init`）
  - 选项数量固定为2（Cursor, Claude）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Simplicity First (NON-NEGOTIABLE)
- ✅ **通过**: 仅改进交互方式，不添加新功能
- ✅ **通过**: 不引入数据库、缓存等复杂架构
- ⚠️ **待评估**: 新增依赖（需在 Phase 0 研究中选择最轻量库）

### II. User Experience First
- ✅ **通过**: 提升用户体验，减少输入错误
- ✅ **通过**: 保留非交互模式（`--editor` 参数不变）
- ✅ **通过**: 错误处理与现有方式一致（Ctrl+C 退出）

### III. Cross-Platform Consistency (NON-NEGOTIABLE)
- ⚠️ **关键**: 必须在 Windows/macOS/Linux 上测试键盘响应
- ⚠️ **关键**: 必须处理非交互式终端（使用 `sys.stdin.isatty()` 检测）

### IV. Test-Driven Development (TDD)
- ✅ **承诺**: Phase 1 后创建单元测试（mock 键盘输入）
- ✅ **承诺**: 集成测试覆盖交互式和非交互式场景

### V. Minimal Dependencies
- ⚠️ **待审批**: 新增1个交互式选择库
  - 必须满足：体积 < 500KB，有长期维护，跨平台兼容
  - 替代方案：参考 spec-kit 使用 `readchar` 自行实现（避免新库）

**GATE 结论 (Phase 0 前)**: ✅ 可进入 Phase 0，但需在研究阶段解决：
1. 选择最轻量的交互库（或评估自行实现可行性）
2. 确认跨平台兼容性
3. Phase 1 后重新检查依赖合规性

---

### Constitution Re-check (Phase 1 后)

#### I. Simplicity First (NON-NEGOTIABLE)
- ✅ **通过**: 自行实现方案，无复杂架构
- ✅ **通过**: 仅新增 `readchar` (~20KB)，远低于 500KB 限制
- ✅ **通过**: 代码量少（~100行），易于维护

#### II. User Experience First
- ✅ **通过**: 非交互式环境检测已实现（`sys.stdin.isatty()`）
- ✅ **通过**: 错误消息友好（取消、中断都有明确提示）

#### III. Cross-Platform Consistency (NON-NEGOTIABLE)
- ✅ **通过**: `readchar` 已验证跨平台兼容（Windows/macOS/Linux）
- ✅ **通过**: spec-kit 生产环境验证通过

#### IV. Test-Driven Development (TDD)
- ✅ **计划**: 测试契约已定义（单元测试 + 集成测试）
- ✅ **计划**: Mock 策略已明确

#### V. Minimal Dependencies
- ✅ **通过**: 新增依赖：`readchar>=4.0.0`
  - 体积：~20KB (< 500KB 限制) ✅
  - 维护：活跃维护（2024年更新） ✅
  - 跨平台：支持所有目标平台 ✅
  - Python 版本：支持 3.8+ ✅

**最终结论**: ✅✅ **完全合规，可进入 Phase 2（实施）**

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/sckit_cli/
├── __init__.py           # 主CLI入口，包含 prompt_editor_choice() [修改]
├── __main__.py           # CLI启动器 [无修改]
└── utils/                # 工具函数 [可能新增交互工具]
    └── interactive.py    # [新增] 封装选择逻辑（如自行实现）

tests/
├── unit/
│   └── test_prompt_editor_choice.py  # [新增] 单元测试
└── integration/
    └── test_init_command.py          # [修改] 扩展集成测试

pyproject.toml            # [修改] 添加新依赖
```

**Structure Decision**: 
单一项目结构，仅修改 `src/sckit_cli/__init__.py` 中的 `prompt_editor_choice()` 函数。如果选择自行实现（使用 `readchar`），则新增 `utils/interactive.py` 模块封装选择逻辑；如果使用第三方库，则直接在 `__init__.py` 中调用库函数。

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

无需追踪复杂度。此功能不违反 Constitution 原则，新增依赖将在 Phase 0 研究中评估合规性。
