# Research: Init 命令交互式选择界面

**Feature**: 002-init-selection-ui  
**Date**: 2025-10-29  
**Researcher**: AI Assistant

## 研究目标

解决 Technical Context 中的 "NEEDS CLARIFICATION"：选择适合的交互式选择实现方案，满足 Constitution 要求（轻量、跨平台、无复杂依赖）。

## 方案对比

### 方案 1: 使用 `inquirer` 库

**描述**: Python 命令行交互库，提供多种输入类型（列表、复选框、文本等）。

**优点**:
- API 简洁：`inquirer.list_input("Choose:", choices=["A", "B"])`
- 内置箭头键导航
- 视觉效果良好

**缺点**:
- 依赖较重：依赖 `readchar`, `blessed` 等多个子包
- 安装包体积：~800KB（超出 Constitution V 限制 500KB）
- Windows 兼容性：历史上有键盘输入问题
- 最后更新：2021年（维护不活跃）

**结论**: ❌ 不推荐（依赖过重，维护不活跃）

---

### 方案 2: 使用 `questionary` 库

**描述**: 基于 `prompt_toolkit` 的现代交互式提示库。

**优点**:
- 现代化 API：`questionary.select("Choose:", choices=["A", "B"]).ask()`
- 功能丰富：自动补全、验证、样式定制
- 活跃维护：持续更新
- 跨平台支持良好

**缺点**:
- 依赖 `prompt_toolkit`：重量级依赖（~2MB）
- 安装包体积：~2.5MB（严重超出限制）
- 功能过剩：对于仅选择2个选项来说过于复杂

**结论**: ❌ 不推荐（依赖过重，违反 Constitution V "Minimal Dependencies"）

---

### 方案 3: 使用 `simple-term-menu` 库

**描述**: 轻量级终端菜单库，专注于列表选择。

**优点**:
- 轻量：无外部依赖（仅标准库）
- 安装包体积：~50KB（符合要求）
- 简单 API：`TerminalMenu(["A", "B"]).show()`
- 跨平台支持：Windows/macOS/Linux

**缺点**:
- 样式定制有限（但对本功能足够）
- 社区相对小众
- 需要额外测试非交互式终端兼容性

**评估**: ⚠️ 可行，但需验证与现有 `rich` 样式的集成

---

### 方案 4: 自行实现（参考 spec-kit）✅ 推荐

**描述**: 使用 `readchar` + `rich` 自行实现选择逻辑，参考 `spec-kit/src/specify_cli/__init__.py` 的 `select_with_arrows()` 函数（274-347行）。

**技术栈**:
- `readchar`: 跨平台键盘输入（~20KB）
- `rich`: 已有依赖，用于终端 UI
- 自行实现：选择逻辑、循环导航、样式渲染

**优点**:
- ✅ 最轻量：仅新增 `readchar`（~20KB，远低于500KB限制）
- ✅ 完全控制：可精确集成 `rich` 样式，保持CLI视觉一致性
- ✅ 跨平台验证：spec-kit 已在生产环境验证
- ✅ 符合 Constitution V：最小化依赖
- ✅ 学习参考：spec-kit 开源代码可直接复用

**实现参考** (spec-kit `__init__.py`):
```python
# 274-347行：select_with_arrows() 函数
def select_with_arrows(options: dict, prompt_text: str, default_key: str) -> str:
    # 使用 readchar.readkey() 捕获键盘输入
    # 使用 rich.Live 实时更新选择界面
    # 使用 rich.Panel + rich.Table 渲染选项列表
    # 支持循环导航：(index ± 1) % len(options)
    # 返回选中的 key
```

**实现要点**:
1. **键盘处理** (254-272行)：
   - `readchar.key.UP/DOWN`: 方向键
   - `readchar.key.ENTER`: 确认
   - `readchar.key.ESC`: 取消
   - `readchar.key.CTRL_C`: 中断（抛出 KeyboardInterrupt）

2. **界面渲染** (294-314行)：
   - 使用 `rich.Table.grid` 创建无边框表格
   - 高亮当前项：`▶ [cyan]选项[/cyan]`
   - 未选中项：`  [cyan]选项[/cyan]`
   - 底部提示：`[dim]Use ↑/↓ to navigate, Enter to select[/dim]`

3. **非交互式兼容** (1006行示例)：
   ```python
   if sys.stdin.isatty():
       selected = select_with_arrows(...)
   else:
       selected = default_value  # CI/CD环境
   ```

**缺点**:
- 需要编写~100行实现代码（但可直接参考 spec-kit）
- 需要自行测试跨平台兼容性

**结论**: ✅ **最佳方案**（最符合 Constitution 原则）

---

## 最终决策

**选择方案 4**：自行实现（使用 `readchar` + `rich`）

**理由**:
1. **轻量**: 仅新增 20KB 依赖（`readchar`），符合 Constitution V
2. **可控**: 完全控制实现，保持与现有 CLI 样式一致
3. **验证**: spec-kit 已在生产环境验证跨平台兼容性
4. **简单**: 代码量少（~100行），易于维护
5. **学习成本低**: 可直接参考 spec-kit 开源实现

**依赖更新**:
```toml
# pyproject.toml
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "httpx>=0.24.0",
    "readchar>=4.0.0",  # 新增
]
```

**依赖合规性检查**:
- ✅ 体积：~20KB < 500KB
- ✅ 维护：活跃维护（最新版本 2024年）
- ✅ 跨平台：支持 Windows/macOS/Linux
- ✅ Python版本：支持 3.8+

---

## 跨平台键盘兼容性研究

### Windows (PowerShell/CMD)
- ✅ `readchar` 通过 `msvcrt` 模块处理 Windows 键盘输入
- ✅ 方向键码：`\xe0` 前缀 + 方向码
- ✅ spec-kit 已验证 PowerShell 兼容性

### macOS/Linux (Terminal)
- ✅ `readchar` 通过 `termios` 模块处理 POSIX 键盘输入
- ✅ 方向键码：ANSI 转义序列（`\x1b[A/B/C/D`）
- ✅ spec-kit 已验证 bash/zsh 兼容性

### 非交互式终端（CI/CD）
- ✅ 使用 `sys.stdin.isatty()` 检测
- ✅ 非交互时自动使用默认值（Cursor）
- ✅ 不抛出错误，静默降级

---

## 非交互式终端处理模式

**检测方法**:
```python
import sys

if sys.stdin.isatty():
    # 交互式终端：显示选择界面
    editor = prompt_editor_choice()
else:
    # 非交互式终端：使用默认值
    editor = Editor.CURSOR
    console.print("[cyan]Non-interactive mode: using default editor (Cursor)[/cyan]")
```

**应用场景**:
- CI/CD 管道（GitHub Actions, GitLab CI）
- Docker 容器内执行
- 脚本自动化调用
- 重定向输入/输出时

**规格要求对应** (spec.md FR-008):
- ✅ 满足：非交互环境使用默认值
- ✅ 满足：显示提示信息而非报错

---

## 实现策略

### 阶段 1: 新增 `utils/interactive.py` 模块

```python
"""交互式终端选择工具"""
from typing import Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
import readchar
import sys

def select_with_arrows(
    options: Dict[str, str],
    prompt: str,
    default: str,
    console: Console
) -> str:
    """
    使用箭头键选择选项
    
    Args:
        options: {key: description} 选项字典
        prompt: 提示文本
        default: 默认选项 key
        console: Rich Console 实例
        
    Returns:
        选中的 key
    """
    # 实现逻辑（参考 spec-kit）
    ...
```

### 阶段 2: 重构 `prompt_editor_choice()`

```python
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

---

## 替代方案评估（如方案4不可行）

如果自行实现遇到技术障碍，备选方案：

**备选方案**: `simple-term-menu`
- 体积可接受（50KB）
- 需验证与 `rich` 的样式兼容性
- 需在所有平台上测试

**启用条件**: 
- 自行实现遇到无法解决的跨平台问题
- 团队评估后认为维护成本过高

---

## 测试策略

### 单元测试
- Mock `readchar.readkey()` 模拟键盘输入
- 测试循环导航逻辑
- 测试非交互式降级

### 集成测试
- 使用 `pexpect` 或 `ptyprocess` 模拟真实终端
- 测试完整 `sckit init` 流程
- 验证 `--editor` 参数不受影响

### 跨平台测试
- ✅ Windows: GitHub Actions (windows-latest)
- ✅ macOS: GitHub Actions (macos-latest)
- ✅ Linux: GitHub Actions (ubuntu-latest)

---

## 性能评估

**预期性能**:
- 按键响应时间：< 50ms（`readchar` 直接系统调用）
- 界面刷新：< 20ms（`rich.Live` 高效渲染）
- CLI 启动时间：+5ms（`readchar` 轻量导入）

**基准测试** (Phase 1 后执行):
```bash
# 启动时间测试
time sckit --version

# 选择响应测试（手动计时）
sckit init test-project
```

---

## 风险与缓解

### 风险 1: Windows 键盘输入兼容性
- **概率**: 低（spec-kit 已验证）
- **影响**: 高（Windows 用户无法使用）
- **缓解**: Phase 1 立即在 Windows 上测试

### 风险 2: 非交互式终端检测失败
- **概率**: 中（某些 CI 环境可能误判）
- **影响**: 中（CI 失败）
- **缓解**: 提供 `--editor` 参数强制指定

### 风险 3: `readchar` 未来不维护
- **概率**: 低（活跃项目）
- **影响**: 低（功能简单，可接管维护）
- **缓解**: 代码足够简单，可自行实现键盘读取

---

## 结论

**技术决策已确认**:
- ✅ 使用 `readchar` + `rich` 自行实现选择界面
- ✅ 参考 spec-kit `select_with_arrows()` 实现
- ✅ 新增依赖：`readchar>=4.0.0`
- ✅ 符合所有 Constitution 原则

**下一步**: 进入 Phase 1（设计数据模型和契约）

