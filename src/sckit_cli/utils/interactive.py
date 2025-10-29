"""
交互式选择界面

提供跨平台的箭头键选择功能，用于 CLI 交互
"""

from typing import Dict
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

try:
    import readchar
    READCHAR_AVAILABLE = True
except ImportError:
    READCHAR_AVAILABLE = False
    readchar = None


def get_key() -> str:
    """
    跨平台读取单个按键输入
    
    Returns:
        str: 标准化的键名 ('up', 'down', 'enter', 'escape')
    
    Raises:
        KeyboardInterrupt: 用户按 Ctrl+C
        ImportError: readchar 未安装
    """
    if not READCHAR_AVAILABLE:
        raise ImportError(
            "readchar is not installed. "
            "Please install it: pip install readchar>=4.0.0"
        )
    
    key = readchar.readkey()
    
    # 映射按键到标准名称
    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return 'up'
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return 'down'
    if key == readchar.key.ENTER or key == '\r' or key == '\n':
        return 'enter'
    if key == readchar.key.ESC:
        return 'escape'
    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt
    
    return key


def render_selection(
    options: Dict[str, str],
    selected_index: int,
    prompt: str
) -> Panel:
    """
    渲染选择界面
    
    Args:
        options: 选项字典 {key: display_text}
        selected_index: 当前高亮的索引
        prompt: 提示文本
    
    Returns:
        Panel: 渲染好的面板
    """
    # 创建网格表格
    grid = Table.grid(padding=(0, 2))
    grid.add_column(style="cyan", justify="left")
    
    # 添加选项
    keys = list(options.keys())
    for idx, key in enumerate(keys):
        display_text = options[key]
        
        if idx == selected_index:
            # 高亮当前选项
            grid.add_row(f"▶ [bold green]{display_text}[/bold green]")
        else:
            # 普通选项
            grid.add_row(f"  {display_text}")
    
    # 添加底部提示
    grid.add_row("")
    grid.add_row("[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")
    
    # 包裹在面板中
    return Panel(
        grid,
        title=f"[bold]{prompt}[/bold]",
        border_style="cyan",
        padding=(1, 2)
    )


def select_with_arrows(
    options: Dict[str, str],
    prompt: str,
    default: str,
    console: Console
) -> str:
    """
    使用箭头键从选项列表中进行选择
    
    Args:
        options: 选项字典，key 为返回值，value 为显示文本
        prompt: 提示文本
        default: 默认选项的 key
        console: Rich Console 实例
    
    Returns:
        str: 用户选择的选项 key
    
    Raises:
        KeyboardInterrupt: 用户按 Ctrl+C
        typer.Exit: 用户按 ESC 取消 (退出码 1)
        ValueError: 参数验证失败
        ImportError: readchar 未安装，回退到文本输入
    """
    # 验证输入
    if not options or len(options) < 2:
        raise ValueError("options must contain at least 2 items")
    
    if not default or default not in options:
        # 回退到第一个选项
        default = list(options.keys())[0]
    
    # 如果 readchar 不可用，回退到文本输入
    if not READCHAR_AVAILABLE:
        console.print(
            "[yellow]Warning: readchar not installed, falling back to text input[/yellow]"
        )
        from rich.prompt import Prompt
        choice = Prompt.ask(
            prompt,
            choices=list(options.keys()),
            default=default
        )
        return choice
    
    # 初始化选择状态
    keys = list(options.keys())
    selected_index = keys.index(default) if default in keys else 0
    
    try:
        # 使用 Live 实时更新界面
        with Live(
            render_selection(options, selected_index, prompt),
            console=console,
            refresh_per_second=10
        ) as live:
            while True:
                # 读取按键
                key = get_key()
                
                # 处理按键
                if key == 'up':
                    # 向上循环
                    selected_index = (selected_index - 1) % len(keys)
                    live.update(render_selection(options, selected_index, prompt))
                
                elif key == 'down':
                    # 向下循环
                    selected_index = (selected_index + 1) % len(keys)
                    live.update(render_selection(options, selected_index, prompt))
                
                elif key == 'enter':
                    # 确认选择
                    return keys[selected_index]
                
                elif key == 'escape':
                    # 取消选择
                    console.print("[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)
    
    except KeyboardInterrupt:
        # Ctrl+C 中断
        raise

