"""
单元测试：交互式选择界面

测试 sckit_cli.utils.interactive 模块的选择功能
"""

from unittest.mock import patch, MagicMock
import pytest
import typer
from rich.console import Console


# 导入待测试的模块（在实现之前会失败）
try:
    from sckit_cli.utils.interactive import select_with_arrows
except ImportError:
    # 测试阶段模块还不存在，这是预期的
    select_with_arrows = None


@pytest.fixture
def console():
    """提供 Rich Console 实例"""
    return Console()


@pytest.fixture
def sample_options():
    """提供测试用的选项字典"""
    return {
        "Cursor": "Cursor AI Editor",
        "Claude": "Claude Code Editor"
    }


class TestSelectWithArrows:
    """测试 select_with_arrows() 函数"""
    
    @pytest.mark.skipif(select_with_arrows is None, reason="Module not implemented yet")
    @patch('sckit_cli.utils.interactive.readchar.readkey')
    def test_select_with_arrows_default_selection(self, mock_readkey, console, sample_options):
        """T005: 测试默认选项高亮
        
        验证：
        - 函数初始化时高亮 default 指定的选项
        - 直接按 Enter 返回 default 选项
        """
        # 模拟按键序列：直接按 ENTER
        import readchar
        mock_readkey.side_effect = [readchar.key.ENTER]
        
        result = select_with_arrows(
            options=sample_options,
            prompt="选择编辑器",
            default="Cursor",
            console=console
        )
        
        # 验证返回默认选项
        assert result == "Cursor", "应该返回默认选项 Cursor"
    
    @pytest.mark.skipif(select_with_arrows is None, reason="Module not implemented yet")
    @patch('sckit_cli.utils.interactive.readchar.readkey')
    def test_select_with_arrows_down_navigation(self, mock_readkey, console, sample_options):
        """T006: 测试向下导航
        
        验证：
        - DOWN 键移动到下一个选项
        - 按 Enter 确认选择
        """
        # 模拟按键序列：DOWN, ENTER
        import readchar
        mock_readkey.side_effect = [
            readchar.key.DOWN,
            readchar.key.ENTER
        ]
        
        result = select_with_arrows(
            options=sample_options,
            prompt="选择编辑器",
            default="Cursor",
            console=console
        )
        
        # 验证选择了第二个选项
        assert result == "Claude", "按 DOWN 后应该选择 Claude"
    
    @pytest.mark.skipif(select_with_arrows is None, reason="Module not implemented yet")
    @patch('sckit_cli.utils.interactive.readchar.readkey')
    def test_select_with_arrows_up_navigation(self, mock_readkey, console, sample_options):
        """T007: 测试向上导航和循环
        
        验证：
        - UP 键从第一个选项循环到最后一个选项
        - 循环导航正确工作
        """
        # 模拟按键序列：UP（从 Cursor 循环到 Claude）, ENTER
        import readchar
        mock_readkey.side_effect = [
            readchar.key.UP,
            readchar.key.ENTER
        ]
        
        result = select_with_arrows(
            options=sample_options,
            prompt="选择编辑器",
            default="Cursor",
            console=console
        )
        
        # 验证循环到最后一个选项
        assert result == "Claude", "从第一项按 UP 应该循环到最后一项 Claude"
    
    @pytest.mark.skipif(select_with_arrows is None, reason="Module not implemented yet")
    @patch('sckit_cli.utils.interactive.readchar.readkey')
    def test_select_with_arrows_enter_confirms(self, mock_readkey, console, sample_options):
        """T008: 测试回车确认
        
        验证：
        - Enter 键确认当前高亮的选项
        - 返回正确的选项 key
        """
        # 模拟按键序列：DOWN, DOWN（循环回 Cursor）, ENTER
        import readchar
        mock_readkey.side_effect = [
            readchar.key.DOWN,
            readchar.key.DOWN,
            readchar.key.ENTER
        ]
        
        result = select_with_arrows(
            options=sample_options,
            prompt="选择编辑器",
            default="Cursor",
            console=console
        )
        
        # 两次 DOWN 后循环回第一个选项
        assert result == "Cursor", "两次 DOWN 后应该循环回 Cursor"
    
    @pytest.mark.skipif(select_with_arrows is None, reason="Module not implemented yet")
    @patch('sckit_cli.utils.interactive.readchar.readkey')
    def test_select_with_arrows_esc_cancels(self, mock_readkey, console, sample_options):
        """T009: 测试 ESC 取消
        
        验证：
        - ESC 键抛出 typer.Exit(1)
        - 用户可以取消选择
        """
        # 模拟按键序列：ESC
        import readchar
        mock_readkey.side_effect = [readchar.key.ESC]
        
        with pytest.raises(typer.Exit) as exc_info:
            select_with_arrows(
                options=sample_options,
                prompt="选择编辑器",
                default="Cursor",
                console=console
            )
        
        # 验证退出码为 1
        assert exc_info.value.exit_code == 1, "ESC 应该导致退出码 1"
    
    @pytest.mark.skipif(select_with_arrows is None, reason="Module not implemented yet")
    @patch('sckit_cli.utils.interactive.readchar.readkey')
    def test_select_with_arrows_keyboard_interrupt(self, mock_readkey, console, sample_options):
        """T010: 测试 Ctrl+C 中断
        
        验证：
        - Ctrl+C 抛出 KeyboardInterrupt
        - 中断被正确传播
        """
        # 模拟 Ctrl+C
        mock_readkey.side_effect = KeyboardInterrupt()
        
        with pytest.raises(KeyboardInterrupt):
            select_with_arrows(
                options=sample_options,
                prompt="选择编辑器",
                default="Cursor",
                console=console
            )

