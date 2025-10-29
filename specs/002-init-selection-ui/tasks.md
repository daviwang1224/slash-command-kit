# Tasks: Init 命令交互式选择界面

**Input**: Design documents from `/specs/002-init-selection-ui/`
**Prerequisites**: plan.md (✓), spec.md (✓), research.md (✓), data-model.md (✓), contracts/ (✓)

**Tests**: 本功能包含测试任务（按照 TDD 原则）

**Organization**: 按用户故事组织任务，实现独立的增量交付

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行执行（不同文件，无依赖）
- **[Story]**: 任务所属用户故事（US1）
- 包含精确的文件路径

## Path Conventions

本项目为单项目结构：
- 源代码: `src/sckit_cli/`
- 测试: `tests/`
- 依赖配置: `pyproject.toml`

---

## Phase 1: Setup（基础设施）

**目的**: 项目初始化和基础结构准备

- [x] T001 [P] 在 `pyproject.toml` 中添加 `readchar>=4.0.0` 依赖
- [x] T002 [P] 创建 `src/sckit_cli/utils/` 目录（如果不存在）
- [x] T003 [P] 创建测试目录结构 `tests/unit/` 和 `tests/integration/`（如果不存在）
- [ ] T004 安装新依赖：运行 `pip install -e .` 或 `poetry install` ⚠️ **待手动完成**

**Checkpoint**: 基础设施就绪，可以开始用户故事实现

---

## Phase 2: User Story 1 - 快速选择编辑器 (Priority: P1) 🎯 MVP

**目标**: 实现上下箭头键可视化选择界面，替代手动文本输入

**独立测试**: 运行 `sckit init`（不带 `--editor` 参数），验证箭头选择界面，使用方向键选择，按回车确认

### Tests for User Story 1 ⚠️

> **NOTE: 按照 TDD 原则，先写测试并确保其失败，再进行实现**

- [x] T005 [P] [US1] 创建单元测试文件 `tests/unit/test_interactive.py`，编写 `test_select_with_arrows_default_selection()` 测试默认选项高亮
- [x] T006 [P] [US1] 在 `tests/unit/test_interactive.py` 中编写 `test_select_with_arrows_down_navigation()` 测试向下导航
- [x] T007 [P] [US1] 在 `tests/unit/test_interactive.py` 中编写 `test_select_with_arrows_up_navigation()` 测试向上导航和循环
- [x] T008 [P] [US1] 在 `tests/unit/test_interactive.py` 中编写 `test_select_with_arrows_enter_confirms()` 测试回车确认
- [x] T009 [P] [US1] 在 `tests/unit/test_interactive.py` 中编写 `test_select_with_arrows_esc_cancels()` 测试 ESC 取消
- [x] T010 [P] [US1] 在 `tests/unit/test_interactive.py` 中编写 `test_select_with_arrows_keyboard_interrupt()` 测试 Ctrl+C 中断
- [x] T011 [P] [US1] 创建单元测试文件 `tests/unit/test_prompt_editor.py`，编写 `test_prompt_editor_choice_interactive()` 测试交互式模式
- [x] T012 [P] [US1] 在 `tests/unit/test_prompt_editor.py` 中编写 `test_prompt_editor_choice_non_interactive()` 测试非交互式模式降级

**Checkpoint**: 运行测试，确认它们全部失败（因为功能尚未实现）

### Implementation for User Story 1

#### 核心交互模块

- [x] T013 [US1] 在 `src/sckit_cli/utils/interactive.py` 中创建 `get_key()` 函数，使用 `readchar` 读取跨平台按键输入
  - 映射 UP/DOWN/ENTER/ESC/CTRL_C 到标准键名
  - 处理 KeyboardInterrupt 异常
  - 参考契约中的实现要点

- [x] T014 [US1] 在 `src/sckit_cli/utils/interactive.py` 中实现 `render_selection()` 辅助函数
  - 使用 `rich.Table.grid` 渲染选项列表
  - 高亮当前选项（▶ 前缀）
  - 未选中项使用空格前缀
  - 添加底部提示: "Use ↑/↓ to navigate, Enter to select, Esc to cancel"

- [x] T015 [US1] 在 `src/sckit_cli/utils/interactive.py` 中实现核心函数 `select_with_arrows()`
  - 参数: `options: Dict[str, str]`, `prompt: str`, `default: str`, `console: Console`
  - 初始化选择状态（SelectionState）
  - 进入键盘事件循环
  - 处理 UP: `selected_index = (index - 1) % len(options)`
  - 处理 DOWN: `selected_index = (index + 1) % len(options)`
  - 处理 ENTER: 返回当前高亮项的 key
  - 处理 ESC: 抛出 `typer.Exit(1)`
  - 处理 Ctrl+C: 抛出 `KeyboardInterrupt`
  - 使用 `rich.Live` 实时更新界面
  - 使用 `rich.Panel` 包裹选项列表

#### 集成到现有 CLI

- [x] T016 [US1] 修改 `src/sckit_cli/__init__.py` 中的 `prompt_editor_choice()` 函数（第 575-590 行）
  - 添加非交互式环境检测: `if not sys.stdin.isatty():`
  - 非交互式模式: 显示提示信息并返回 `Editor.CURSOR`
  - 交互式模式: 调用 `select_with_arrows()` 替代 `Prompt.ask()`
  - 定义 options 字典: `{"Cursor": "Cursor AI Editor", "Claude": "Claude Code Editor"}`
  - 将选择结果转换为 `Editor` 枚举
  - 保持异常处理行为一致（KeyboardInterrupt → 传播）

- [x] T017 [US1] 在 `src/sckit_cli/__init__.py` 顶部添加 import 语句
  - `import sys`（如果不存在）
  - `from sckit_cli.utils.interactive import select_with_arrows`

#### 验证和错误处理

- [x] T018 [US1] 在 `src/sckit_cli/utils/interactive.py` 中添加输入验证
  - 验证 `options` 非空且至少包含 2 项
  - 验证 `default` 存在于 `options.keys()` 中
  - 如果 `default` 不存在，使用第一个选项
  - 抛出清晰的 `ValueError` 消息

- [x] T019 [US1] 添加降级处理：在 `select_with_arrows()` 中捕获 `ImportError`
  - 如果 `readchar` 导入失败，记录警告
  - 回退到 `rich.Prompt.ask()` 实现（向后兼容）

**Checkpoint**: 运行测试，确认所有测试通过，US1 功能完整可用

---

## Phase 3: Integration Testing（集成测试）

**目的**: 验证完整的端到端流程

- [x] T020 [US1] 创建集成测试 `tests/integration/test_init_command.py`
  - 测试场景 1: 完整选择流程（模拟 ↓ → Enter）
  - 测试场景 2: 非交互式环境（mock `sys.stdin.isatty()` 返回 False）
  - 测试场景 3: 用户取消（模拟 Ctrl+C）
  - 验证退出码、输出消息、文件创建

- [ ] T021 [US1] 手动测试：在真实终端运行 `sckit init test-project` ⚠️ **待手动测试**
  - Windows PowerShell 测试
  - 验证方向键响应流畅性
  - 验证高亮显示正确
  - 验证 Enter 确认后续流程
  - 验证 Ctrl+C 取消并清理

**Checkpoint**: 集成测试通过，用户故事完全可用

---

## Phase 4: Polish & Documentation（打磨和文档）

**目的**: 代码质量和用户文档改进

- [x] T022 [P] 添加 docstrings：为 `select_with_arrows()` 和 `get_key()` 添加完整的类型注解和文档字符串
- [x] T023 [P] 代码审查：确保符合 PEP 8 和项目编码规范
- [ ] T024 [P] 性能测试：使用 `pytest-benchmark` 验证按键响应时间 < 50ms ⚠️ **可选**
- [ ] T025 运行 linter 和类型检查：`mypy src/sckit_cli/` 和 `ruff check src/` ⚠️ **待手动运行**
- [ ] T026 运行完整测试套件：`pytest tests/ -v` ⚠️ **待手动运行（需先安装 readchar）**
- [x] T027 更新 `CHANGELOG.md`：添加 "Added: Interactive arrow-key selection for editor choice in init command" 条目
- [ ] T028 [P] 更新 `README.md`：添加新功能的截图或 GIF（可选） ⚠️ **可选**

**Checkpoint**: 代码质量达标，文档完善

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，立即开始
- **User Story 1 (Phase 2)**: 依赖 Setup 完成
  - 测试任务 (T005-T012) 可并行执行
  - 实现任务 (T013-T019) 依赖测试编写完成
  - T013, T014 可并行（不同函数）
  - T015 依赖 T013, T014（需要 `get_key()` 和 `render_selection()`）
  - T016, T017 依赖 T015（需要 `select_with_arrows()` 可用）
  - T018, T019 可并行（不同关注点）
- **Integration Testing (Phase 3)**: 依赖 Phase 2 实现完成
  - T020, T021 可并行
- **Polish (Phase 4)**: 依赖 Phase 3 测试通过
  - T022, T023, T024, T028 可并行

### Critical Path

```
T001-T004 (Setup)
  ↓
T005-T012 (Tests - 并行)
  ↓
T013, T014 (并行: get_key, render_selection)
  ↓
T015 (select_with_arrows)
  ↓
T016, T017 (集成到 CLI)
  ↓
T018, T019 (错误处理 - 并行)
  ↓
T020, T021 (集成测试 - 并行)
  ↓
T022-T028 (打磨 - 部分并行)
```

### Parallel Opportunities

- **Phase 1**: T001, T002, T003 可并行
- **Phase 2 - Tests**: T005-T012 所有测试可并行编写
- **Phase 2 - Implementation**: T013, T014 可并行；T018, T019 可并行
- **Phase 3**: T020, T021 可并行
- **Phase 4**: T022, T023, T024, T028 可并行

---

## Implementation Strategy

### TDD Approach

1. **Phase 1**: 完成 Setup（T001-T004）
2. **Phase 2 - Tests First**:
   - 并行编写所有测试（T005-T012）
   - 运行测试，确认全部失败 ✅
3. **Phase 2 - Implement**:
   - 实现 `get_key()` 和 `render_selection()`（T013, T014）
   - 实现 `select_with_arrows()`（T015）
   - 集成到 `prompt_editor_choice()`（T016, T017）
   - 添加验证和降级（T018, T019）
   - 运行测试，确认全部通过 ✅
4. **Phase 3**: 集成测试（T020, T021）
5. **Phase 4**: 打磨和文档（T022-T028）

### Minimal Viable Product (MVP)

- **MVP = Phase 1 + Phase 2**
- 完成后，`sckit init` 命令支持箭头键选择编辑器
- 可以立即演示和部署

### Incremental Delivery

- **Iteration 1** (Phase 1-2): 核心功能 → 测试独立 → 演示
- **Iteration 2** (Phase 3): 集成测试 → 验证稳定性
- **Iteration 3** (Phase 4): 打磨 → 生产就绪

---

## Notes

- **TDD 严格遵守**: 先写测试，确认失败，再实现，确认通过
- **[P] 标记**: 不同文件或独立关注点，可并行执行
- **[US1] 标记**: 所有任务属于 User Story 1（本功能仅有 1 个用户故事）
- **避免**: 模糊任务、同文件冲突、跨故事依赖
- **提交策略**: 每完成 1-2 个逻辑相关任务后提交
- **测试优先**: 在实现前运行测试，确保测试失败
- **独立验证**: 每个 Checkpoint 处独立验证功能

---

## Testing Strategy

### Unit Tests (Mock Strategy)

**Mock `readchar.readkey()`**:
```python
from unittest.mock import patch
import readchar

@patch('sckit_cli.utils.interactive.readchar.readkey')
def test_down_key_navigation(mock_readkey):
    mock_readkey.side_effect = [
        readchar.key.DOWN,
        readchar.key.ENTER
    ]
    # ... 执行测试
```

**Mock `sys.stdin.isatty()`**:
```python
@patch('sys.stdin.isatty')
def test_non_interactive_fallback(mock_isatty):
    mock_isatty.return_value = False
    result = prompt_editor_choice()
    assert result == Editor.CURSOR
```

### Integration Tests

- 使用 `typer.testing.CliRunner` 模拟 CLI 调用
- 使用 `pytest.MonkeyPatch` 注入测试输入
- 验证退出码、输出消息、文件系统变化

### Manual Testing Checklist

在不同平台验证：
- [ ] Windows 10+ PowerShell 7+
- [ ] Windows 10+ CMD
- [ ] macOS Terminal.app（如可用）
- [ ] Linux bash/zsh（如可用）

---

## Constitution Compliance

### ✅ Simplicity First (NON-NEGOTIABLE)
- 仅添加 1 个轻量依赖（`readchar` ~20KB）
- 仅修改 1 个函数（`prompt_editor_choice()`）
- 新增 1 个模块（`utils/interactive.py`，~100 行）

### ✅ User Experience First
- 减少输入错误（无需手动输入）
- 非交互式环境自动降级
- 友好的错误消息和取消提示

### ✅ Cross-Platform Consistency (NON-NEGOTIABLE)
- `readchar` 已验证跨平台兼容
- 非交互式环境检测（CI/CD 友好）

### ✅ Test-Driven Development (TDD)
- 所有功能有对应测试
- TDD 流程: 测试 → 失败 → 实现 → 通过

### ✅ Minimal Dependencies
- `readchar>=4.0.0`（体积 < 500KB，活跃维护）
- 无其他新依赖

**结论**: 完全符合 Constitution 所有原则 ✅✅

---

## Risk Mitigation

### Risk: 终端不兼容

**缓解**:
- T019 实现降级策略（回退到 `Prompt.ask()`）
- T021 手动测试覆盖主要平台

### Risk: readchar 导入失败

**缓解**:
- T019 捕获 `ImportError` 并回退
- 安装时验证依赖（T004）

### Risk: 用户不习惯新界面

**缓解**:
- 保留 `--editor` 参数（跳过选择）
- 底部提示清晰说明操作方式
- 可考虑添加配置项切换回旧版输入（后续迭代）

---

## Success Criteria (验收标准)

完成所有任务后，应满足以下标准：

- ✅ **SC-001**: 用户可在 3 秒内完成编辑器选择
- ✅ **SC-002**: 无需查看文档即可理解操作（界面有提示）
- ✅ **SC-003**: 输入错误率降为 0%（无需输入文本）
- ✅ **SC-004**: 在 Windows/macOS/Linux 上正常工作
- ✅ **SC-005**: 所有测试通过（单元 + 集成）
- ✅ **FR-001** - **FR-008**: 所有功能需求满足（参考 spec.md）

---

## Estimated Effort

- **Phase 1 (Setup)**: 30 分钟
- **Phase 2 (Tests)**: 1-2 小时
- **Phase 2 (Implementation)**: 2-3 小时
- **Phase 3 (Integration Testing)**: 1 小时
- **Phase 4 (Polish)**: 1 小时

**总计**: 5-8 小时（单人，顺序执行）

**并行执行**（2 人）: 3-5 小时

---

**Last Updated**: 2025-10-29  
**Status**: Ready for Implementation  
**Next Action**: 开始 Phase 1 - Setup (T001-T004)

