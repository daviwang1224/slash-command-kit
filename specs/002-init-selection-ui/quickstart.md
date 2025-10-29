# Quick Start: Init 命令交互式选择界面

**Feature**: 002-init-selection-ui  
**Date**: 2025-10-29  
**Estimated Time**: 10 分钟

## 概述

本指南帮助开发者快速理解和实现 `sckit init` 命令的交互式选择界面改进。

---

## 功能说明

### 改进前后对比

**改进前** (当前实现):
```
选择 AI 编辑器 [Cursor/Claude] (Cursor): _
```
- 用户需要手动输入 "Cursor" 或 "Claude"
- 容易拼写错误
- 不直观

**改进后** (目标实现):
```
┌─ 选择 AI 编辑器 ─────────────────────┐
│                                      │
│  ▶  Cursor  (Cursor AI Editor)      │
│     Claude  (Claude Code Editor)    │
│                                      │
│  Use ↑/↓ to navigate, Enter to select, Esc to cancel │
└──────────────────────────────────────┘
```
- 使用箭头键选择
- 视觉高亮当前选项
- 无需输入，减少错误

---

## 快速验证

### 1. 安装依赖

在开发环境安装新依赖：

```bash
pip install readchar>=4.0.0
```

或更新 `pyproject.toml`：

```toml
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "httpx>=0.24.0",
    "readchar>=4.0.0",  # 新增
]
```

### 2. 实现核心函数

创建 `src/sckit_cli/utils/interactive.py`（参考 [spec-kit 实现](../../../../spec-kit/src/specify_cli/__init__.py)）：

```python
"""交互式终端选择工具"""
from typing import Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
import readchar
import typer

def get_key() -> str:
    """跨平台读取单个按键"""
    key = readchar.readkey()
    
    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return 'up'
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return 'down'
    if key == readchar.key.ENTER:
        return 'enter'
    if key == readchar.key.ESC:
        return 'escape'
    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt
    
    return key

def select_with_arrows(
    options: Dict[str, str],
    prompt: str,
    default: str,
    console: Console
) -> str:
    """使用箭头键选择选项"""
    option_keys = list(options.keys())
    selected_index = option_keys.index(default) if default in option_keys else 0
    
    def create_panel():
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")
        
        for i, key in enumerate(option_keys):
            prefix = "▶" if i == selected_index else " "
            label = f"[cyan]{key}[/cyan]"
            desc = f"[dim]({options[key]})[/dim]"
            table.add_row(prefix, f"{label} {desc}")
        
        table.add_row("", "")
        table.add_row("", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")
        
        return Panel(table, title=f"[bold]{prompt}[/bold]", border_style="cyan")
    
    console.print()
    selected_key = None
    
    with Live(create_panel(), console=console, transient=True, auto_refresh=False) as live:
        while True:
            try:
                key = get_key()
                if key == 'up':
                    selected_index = (selected_index - 1) % len(option_keys)
                elif key == 'down':
                    selected_index = (selected_index + 1) % len(option_keys)
                elif key == 'enter':
                    selected_key = option_keys[selected_index]
                    break
                elif key == 'escape':
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)
                
                live.update(create_panel(), refresh=True)
            except KeyboardInterrupt:
                console.print("\n[yellow]Selection cancelled[/yellow]")
                raise typer.Exit(2)
    
    return selected_key
```

### 3. 修改 `prompt_editor_choice()`

在 `src/sckit_cli/__init__.py` 中修改：

```python
import sys
from sckit_cli.utils.interactive import select_with_arrows

def prompt_editor_choice() -> Editor:
    """交互式编辑器选择"""
    # 检测非交互式环境
    if not sys.stdin.isatty():
        console.print("[cyan]Non-interactive mode: using Cursor[/cyan]")
        return Editor.CURSOR
    
    # 交互式选择
    options = {
        "Cursor": "Cursor AI Editor",
        "Claude": "Claude Code Editor"
    }
    
    choice = select_with_arrows(
        options=options,
        prompt="选择 AI 编辑器",
        default="Cursor",
        console=console
    )
    
    return Editor.CURSOR if choice == "Cursor" else Editor.CLAUDE
```

### 4. 本地测试

```bash
# 测试交互式选择
sckit init test-project

# 测试非交互式模式
echo "" | sckit init test-project2

# 测试 --editor 参数不受影响
sckit init test-project3 --editor claude
```

**验证点**:
- ✅ 出现箭头选择界面
- ✅ 方向键正常响应
- ✅ Enter 确认选择
- ✅ Esc 取消操作
- ✅ 非交互式自动使用默认值

---

## 开发流程

### Phase 0: 研究 ✅ (已完成)

参见 [research.md](./research.md)

**结论**: 使用 `readchar` + `rich` 自行实现

### Phase 1: 设计 (当前阶段)

- ✅ 数据模型：[data-model.md](./data-model.md)
- ✅ API 契约：[contracts/interactive-selection-api.md](./contracts/interactive-selection-api.md)
- ✅ 快速入门：本文档

### Phase 2: 实施 (下一步)

运行 `/speckit.tasks` 生成具体任务：

```bash
/speckit.tasks
```

预期任务：
1. 创建 `utils/interactive.py` 模块
2. 实现 `select_with_arrows()` 函数
3. 实现 `get_key()` 辅助函数
4. 修改 `prompt_editor_choice()` 函数
5. 更新 `pyproject.toml` 依赖
6. 编写单元测试
7. 编写集成测试
8. 跨平台测试（Windows/macOS/Linux）

---

## 常见问题

### Q1: 为什么不使用 `inquirer` 或 `questionary`？

**A**: 这些库依赖过重（800KB-2.5MB），违反 Constitution V "Minimal Dependencies" 原则。`readchar` 仅 20KB，更符合项目价值观。

参见 [research.md](./research.md#方案对比)。

---

### Q2: 如何处理非交互式环境？

**A**: 使用 `sys.stdin.isatty()` 检测，非交互时自动使用默认值：

```python
if not sys.stdin.isatty():
    console.print("[cyan]Non-interactive mode: using Cursor[/cyan]")
    return Editor.CURSOR
```

这样 CI/CD 环境不会卡住。

---

### Q3: 如何测试键盘输入？

**A**: 使用 `unittest.mock` 模拟 `readchar.readkey()`：

```python
from unittest.mock import patch
import readchar

@patch('sckit_cli.utils.interactive.readchar.readkey')
def test_select_down_key(mock_readkey):
    mock_readkey.side_effect = [
        readchar.key.DOWN,
        readchar.key.ENTER
    ]
    # ... 执行测试
```

参见 [contracts/interactive-selection-api.md](./contracts/interactive-selection-api.md#测试契约)。

---

### Q4: Windows 上方向键不工作怎么办？

**A**: `readchar` 已处理 Windows 特殊情况（使用 `msvcrt` 模块）。如果仍有问题：

1. 检查 PowerShell 版本（建议 7+）
2. 验证 `readchar` 版本（>= 4.0.0）
3. 参考 spec-kit 在 Windows 上的测试

spec-kit 已在生产环境验证跨平台兼容性。

---

### Q5: 如何扩展到更多编辑器？

**A**: 仅需修改 `options` 字典，数据模型已支持任意数量选项：

```python
options = {
    "Cursor": "Cursor AI Editor",
    "Claude": "Claude Code Editor",
    "VSCode": "Visual Studio Code",  # 新增
    "Zed": "Zed Editor",             # 新增
}
```

---

## 性能指标

### 目标

- 按键响应时间: < 50ms
- 界面刷新时间: < 20ms
- CLI 启动时间增加: < 5ms
- 内存占用: < 10KB

### 测量

```bash
# 启动时间测试
time sckit --version

# 按键响应测试（手动计时）
sckit init test-project
# 按方向键观察延迟
```

---

## 参考资源

### 代码参考

- **spec-kit 实现**: `spec-kit/src/specify_cli/__init__.py`
  - `select_with_arrows()` 函数（274-347行）
  - `get_key()` 函数（254-272行）
  - 非交互式检测（1006行）

### 文档

- [research.md](./research.md) - 技术选型研究
- [data-model.md](./data-model.md) - 数据结构定义
- [contracts/](./contracts/) - API 接口契约
- [plan.md](./plan.md) - 完整实施计划

### 外部资源

- [readchar 文档](https://github.com/magmax/python-readchar)
- [rich 文档](https://rich.readthedocs.io/)
- [typer 文档](https://typer.tiangolo.com/)

---

## 下一步

1. **运行 `/speckit.tasks`** 生成详细任务列表
2. **创建分支** (已完成：`002-init-selection-ui`)
3. **实施代码修改** 按任务列表执行
4. **编写测试** 覆盖所有场景
5. **跨平台验证** 在 Windows/macOS/Linux 上测试
6. **提交 PR** 请求代码审查

---

## 预期结果

实施完成后：
- ✅ 用户选择编辑器更流畅（箭头键导航）
- ✅ 输入错误率降为 0%（无需输入）
- ✅ 非交互式环境自动降级
- ✅ 跨平台一致体验
- ✅ 依赖增加最小化（仅 20KB）
- ✅ 符合所有 Constitution 原则

---

**估计工作量**: 4-6 小时（含测试）  
**风险等级**: 低（参考实现已验证）  
**优先级**: 中（用户体验改进）

