# API Contract: 交互式选择界面

**Feature**: 002-init-selection-ui  
**Version**: 1.0  
**Date**: 2025-10-29

## 概述

定义交互式选择功能的公共 API 接口，包括核心选择函数和辅助工具。

---

## 模块: `sckit_cli.utils.interactive`

### 函数: `select_with_arrows()`

**签名**:
```python
def select_with_arrows(
    options: Dict[str, str],
    prompt: str,
    default: str,
    console: Console
) -> str
```

**描述**: 使用箭头键从选项列表中进行选择。

**参数**:

| 参数 | 类型 | 必需 | 描述 | 约束 |
|------|------|------|------|------|
| `options` | `Dict[str, str]` | 是 | 选项字典，key 为返回值，value 为显示文本 | 至少2项，key 和 value 非空 |
| `prompt` | `str` | 是 | 提示文本 | 非空字符串 |
| `default` | `str` | 是 | 默认选项的 key | 必须在 options 中存在 |
| `console` | `Console` | 是 | Rich Console 实例 | 有效的 Console 对象 |

**返回值**:
- **类型**: `str`
- **描述**: 用户选择的选项 key
- **可能值**: `options` 字典中的任意 key

**异常**:

| 异常类型 | 触发条件 | 处理建议 |
|---------|---------|---------|
| `KeyboardInterrupt` | 用户按 Ctrl+C | 捕获后显示取消消息，退出程序（退出码 2） |
| `typer.Exit(1)` | 用户按 ESC 取消 | 正常退出流程，显示 "[yellow]Selection cancelled[/yellow]" |
| `ValueError` | options 为空或 default 不在 options 中 | 开发错误，修复调用代码 |

**行为规范**:

1. **初始状态**:
   - 高亮 `default` 对应的选项
   - 如果 `default` 不存在，高亮第一个选项

2. **键盘交互**:
   - `↑` (UP): 选择上一项，循环到末尾
   - `↓` (DOWN): 选择下一项，循环到开头
   - `Enter`: 确认选择，返回当前高亮项的 key
   - `Esc`: 取消选择，抛出 `typer.Exit(1)`
   - `Ctrl+C`: 中断程序，抛出 `KeyboardInterrupt`

3. **界面渲染**:
   - 使用 `rich.Panel` 包裹选项列表
   - 使用 `rich.Table.grid` 渲染选项
   - 高亮项前缀：`▶` 符号
   - 未选中项前缀：空格
   - 底部提示：`Use ↑/↓ to navigate, Enter to select, Esc to cancel`

4. **非交互式环境**:
   - 函数内部不检测非交互式环境（由调用方检测）
   - 仅在交互式环境中调用此函数

**示例用法**:
```python
from rich.console import Console
from sckit_cli.utils.interactive import select_with_arrows

console = Console()

options = {
    "Cursor": "Cursor AI Editor",
    "Claude": "Claude Code Editor"
}

try:
    choice = select_with_arrows(
        options=options,
        prompt="选择 AI 编辑器",
        default="Cursor",
        console=console
    )
    print(f"Selected: {choice}")
except KeyboardInterrupt:
    console.print("\n[yellow]操作已取消[/yellow]")
    raise typer.Exit(2)
```

**性能要求**:
- 按键响应时间: < 50ms（从按下到界面更新）
- 内存占用: < 10KB（运行时状态）
- CPU 使用: < 5%（等待输入时）

---

## 模块: `sckit_cli`

### 函数: `prompt_editor_choice()` (修改后)

**签名**:
```python
def prompt_editor_choice() -> Editor
```

**描述**: 交互式选择编辑器，支持非交互式环境自动降级。

**参数**: 无

**返回值**:
- **类型**: `Editor` (枚举)
- **可能值**: `Editor.CURSOR` 或 `Editor.CLAUDE`

**异常**:
- `KeyboardInterrupt`: 用户取消操作（由 `select_with_arrows` 传播）
- `typer.Exit(1)`: 用户按 ESC 取消（由 `select_with_arrows` 传播）

**行为规范**:

1. **非交互式环境检测**:
   ```python
   if not sys.stdin.isatty():
       console.print("[cyan]Non-interactive mode: using Cursor[/cyan]")
       return Editor.CURSOR
   ```

2. **交互式选择**:
   ```python
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
   ```

3. **结果转换**:
   ```python
   return Editor.CURSOR if choice == "Cursor" else Editor.CLAUDE
   ```

**向后兼容性**:
- ✅ 函数签名不变（无参数，返回 `Editor`）
- ✅ 返回值类型不变
- ✅ 异常行为保持一致（`KeyboardInterrupt` → 退出码 2）
- ✅ `--editor` 参数不受影响（跳过此函数）

**对比当前实现**:

| 维度 | 当前实现 | 新实现 |
|------|---------|--------|
| 输入方式 | 手动输入 "Cursor" 或 "Claude" | 箭头键选择 |
| 默认值 | "Cursor" | 高亮 "Cursor" |
| 错误处理 | 输入错误重试 | 无输入错误（仅选择） |
| 非交互式 | 无检测（可能卡住） | 自动降级到默认值 |
| 视觉效果 | 简单提示 | Panel + 高亮选项 |

---

## 辅助函数: `get_key()` (内部使用)

**签名**:
```python
def get_key() -> str
```

**描述**: 跨平台读取单个按键输入（参考 spec-kit 实现）。

**返回值**:
- **类型**: `str`
- **可能值**: `'up'`, `'down'`, `'enter'`, `'escape'`, 或其他字符

**异常**:
- `KeyboardInterrupt`: 用户按 Ctrl+C

**实现要点**:
```python
import readchar

def get_key():
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
```

**跨平台兼容性**:
- ✅ Windows: 使用 `msvcrt` 模块
- ✅ macOS/Linux: 使用 `termios` 模块
- ✅ 通过 `readchar` 库统一接口

---

## 测试契约

### 单元测试要求

1. **`select_with_arrows()` 测试**:
   ```python
   def test_select_with_arrows_default_selection():
       """测试默认选项高亮"""
       
   def test_select_with_arrows_up_navigation():
       """测试向上导航循环"""
       
   def test_select_with_arrows_down_navigation():
       """测试向下导航循环"""
       
   def test_select_with_arrows_enter_confirms():
       """测试回车确认选择"""
       
   def test_select_with_arrows_esc_cancels():
       """测试 ESC 取消选择"""
       
   def test_select_with_arrows_keyboard_interrupt():
       """测试 Ctrl+C 中断"""
   ```

2. **`prompt_editor_choice()` 测试**:
   ```python
   def test_prompt_editor_choice_interactive():
       """测试交互式模式"""
       
   def test_prompt_editor_choice_non_interactive():
       """测试非交互式模式降级"""
   ```

### Mock 策略

**Mock `readchar.readkey()`**:
```python
from unittest.mock import patch, MagicMock

@patch('sckit_cli.utils.interactive.readchar.readkey')
def test_down_key_navigation(mock_readkey):
    # 模拟按键序列：DOWN, DOWN, ENTER
    mock_readkey.side_effect = [
        readchar.key.DOWN,
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

---

## 集成测试要求

### 场景 1: 完整选择流程

**步骤**:
1. 运行 `sckit init test-project`
2. 出现选择界面
3. 按 ↓ 键选择 "Claude"
4. 按 Enter 确认
5. 验证后续流程使用 Claude 配置

**预期**:
- 选择界面正常显示
- 按键响应流畅
- 最终创建 `.claude/commands/` 目录

### 场景 2: 非交互式环境

**步骤**:
1. 在 CI 环境运行 `sckit init test-project`
2. 验证自动使用默认值（Cursor）

**预期**:
- 不卡在输入等待
- 显示提示信息
- 创建 `.cursor/commands/` 目录

### 场景 3: 用户取消

**步骤**:
1. 运行 `sckit init test-project`
2. 按 Ctrl+C 取消
3. 验证退出码为 2

**预期**:
- 显示 "[yellow]操作已取消[/yellow]"
- 退出码 = 2
- 不创建项目目录

---

## 性能基准

### 响应时间

| 操作 | 目标 | 测量方式 |
|------|------|----------|
| 按键响应 | < 50ms | 手动计时（按键到界面更新） |
| 界面渲染 | < 20ms | `time.perf_counter()` |
| 函数调用开销 | < 5ms | `pytest-benchmark` |

### 资源使用

| 指标 | 限制 | 测量方式 |
|------|------|----------|
| 内存占用 | < 10KB | `memory_profiler` |
| CPU 使用 | < 5% | `psutil` |
| 启动时间影响 | < 5ms | `time sckit --version` |

---

## 兼容性矩阵

| 平台 | 终端 | Python 版本 | 状态 |
|------|------|-------------|------|
| Windows 10+ | PowerShell 7+ | 3.8-3.12 | ✅ 支持 |
| Windows 10+ | CMD | 3.8-3.12 | ✅ 支持 |
| macOS 12+ | Terminal.app | 3.8-3.12 | ✅ 支持 |
| macOS 12+ | iTerm2 | 3.8-3.12 | ✅ 支持 |
| Linux | bash/zsh | 3.8-3.12 | ✅ 支持 |
| CI/CD | 非交互式 | 3.8-3.12 | ✅ 降级支持 |

---

## 变更日志

### v1.0 (2025-10-29)
- 初始契约定义
- 定义 `select_with_arrows()` 公共 API
- 定义 `prompt_editor_choice()` 修改规范
- 定义测试契约和性能基准

---

## 维护者

- **负责人**: AI Assistant
- **审核人**: 项目维护者
- **联系方式**: GitHub Issues

