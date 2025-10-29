# Data Model: Init 命令交互式选择界面

**Feature**: 002-init-selection-ui  
**Date**: 2025-10-29

## 概述

本功能不涉及持久化数据，仅包含运行时内存状态管理。以下定义选择界面的数据结构和状态转换。

---

## 实体定义

### 1. SelectionState（选择状态）

**描述**: 表示当前选择界面的状态

**字段**:

| 字段名 | 类型 | 描述 | 验证规则 |
|--------|------|------|----------|
| `options` | `Dict[str, str]` | 选项字典，key 为选项值，value 为显示文本 | 非空，至少2项 |
| `selected_index` | `int` | 当前高亮的选项索引 | 0 ≤ index < len(options) |
| `default_key` | `str` | 默认选项的 key | 必须在 options 中存在 |
| `prompt_text` | `str` | 提示文本 | 非空字符串 |

**示例**:
```python
SelectionState(
    options={"Cursor": "Cursor AI Editor", "Claude": "Claude Code Editor"},
    selected_index=0,
    default_key="Cursor",
    prompt_text="选择 AI 编辑器"
)
```

**状态约束**:
- `selected_index` 在方向键操作时保持在有效范围内（循环）
- `default_key` 仅用于初始化 `selected_index`

---

### 2. KeyEvent（键盘事件）

**描述**: 表示用户键盘输入事件

**字段**:

| 字段名 | 类型 | 描述 | 可能值 |
|--------|------|------|--------|
| `key_type` | `str` | 键类型 | `'up'`, `'down'`, `'enter'`, `'escape'`, `'ctrl_c'` |
| `raw_input` | `str` | 原始输入字符（调试用） | 任意字符串 |

**映射规则** (来自 `readchar`):
```python
readchar.key.UP       → 'up'
readchar.key.DOWN     → 'down'
readchar.key.ENTER    → 'enter'
readchar.key.ESC      → 'escape'
readchar.key.CTRL_C   → 抛出 KeyboardInterrupt
```

---

### 3. SelectionResult（选择结果）

**描述**: 表示选择操作的最终结果

**字段**:

| 字段名 | 类型 | 描述 | 可能值 |
|--------|------|------|--------|
| `selected_key` | `str` | 用户选择的选项 key | options 中的任意 key |
| `cancelled` | `bool` | 是否被用户取消 | `True`（按 Esc）或 `False` |

**示例**:
```python
# 成功选择
SelectionResult(selected_key="Cursor", cancelled=False)

# 用户取消
SelectionResult(selected_key=None, cancelled=True)
```

---

## 状态转换

### 选择流程状态机

```
[初始化] 
    ↓
    - 创建 SelectionState
    - selected_index = 0 (或 default_key 对应的索引)
    ↓
[等待输入] ←──────┐
    ↓              │
    读取键盘事件    │
    ↓              │
[处理事件]         │
    ├─ UP键   → selected_index = (index - 1) % len(options) ─┘
    ├─ DOWN键 → selected_index = (index + 1) % len(options) ─┘
    ├─ ENTER  → 返回 SelectionResult(selected_key, False)
    ├─ ESC    → 返回 SelectionResult(None, True)
    └─ CTRL_C → 抛出 KeyboardInterrupt → 退出程序
```

### 非交互式模式

```
[检测终端类型]
    ↓
    sys.stdin.isatty() == False
    ↓
[直接返回默认值]
    ↓
    返回 SelectionResult(default_key, False)
    (跳过交互式流程)
```

---

## 数据验证规则

### 输入验证

1. **options 验证**:
   - 必须包含至少2个选项
   - 所有 key 必须是非空字符串
   - 所有 value 必须是非空字符串
   - key 不允许重复

2. **default_key 验证**:
   - 必须存在于 options 的 keys 中
   - 如果不存在，回退到第一个选项

3. **selected_index 边界检查**:
   - 方向键操作时使用模运算保证循环
   - `(index - 1) % len(options)` 处理上溢
   - `(index + 1) % len(options)` 处理下溢

---

## 错误处理

### 异常类型

| 异常 | 触发条件 | 处理方式 |
|------|----------|----------|
| `KeyboardInterrupt` | 用户按 Ctrl+C | 捕获后显示 "[yellow]操作已取消[/yellow]"，退出码 2 |
| `EOFError` | 输入流意外关闭 | 捕获后显示错误信息，退出码 1 |
| `Exception` | 其他未预期错误 | 捕获后显示通用错误信息，退出码 1 |

### 降级策略

| 场景 | 检测方式 | 降级行为 |
|------|----------|----------|
| 非交互式终端 | `sys.stdin.isatty() == False` | 使用 default_key，跳过选择界面 |
| readchar 导入失败 | `ImportError` | 回退到 `rich.Prompt.ask()`（当前实现） |
| 终端不支持控制字符 | 运行时错误 | 回退到 `rich.Prompt.ask()` |

---

## 内存使用分析

**估算**:
- `SelectionState` 对象：~200 bytes
- `options` 字典（2项）：~150 bytes
- 界面渲染缓冲区（`rich.Live`）：~5KB
- **总计**：< 10KB（可忽略不计）

**生命周期**:
- 创建：进入选择函数时
- 销毁：返回选择结果后（自动GC）
- 持续时间：< 30秒（用户选择时间）

---

## 与现有数据模型的关系

### Editor 枚举（已存在）

```python
class Editor(str, Enum):
    CURSOR = "cursor"
    CLAUDE = "claude"
```

**转换逻辑**:
```python
def selection_key_to_editor(key: str) -> Editor:
    """将选择结果转换为 Editor 枚举"""
    mapping = {
        "Cursor": Editor.CURSOR,
        "Claude": Editor.CLAUDE
    }
    return mapping.get(key, Editor.CURSOR)
```

---

## 扩展性考虑

### 未来支持更多编辑器

**当前**（2个选项）:
```python
options = {
    "Cursor": "Cursor AI Editor",
    "Claude": "Claude Code Editor"
}
```

**扩展示例**（5个选项）:
```python
options = {
    "Cursor": "Cursor AI Editor",
    "Claude": "Claude Code Editor",
    "VSCode": "Visual Studio Code",
    "Zed": "Zed Editor",
    "Neovim": "Neovim with AI Plugin"
}
```

**数据模型无需修改**: `SelectionState` 已支持任意数量选项。

---

## 总结

**核心数据结构**:
1. `SelectionState`: 选择界面运行时状态
2. `KeyEvent`: 键盘输入事件
3. `SelectionResult`: 选择结果

**关键特性**:
- ✅ 无持久化存储
- ✅ 轻量内存占用（< 10KB）
- ✅ 支持循环导航
- ✅ 降级兼容非交互式环境
- ✅ 可扩展至更多选项

