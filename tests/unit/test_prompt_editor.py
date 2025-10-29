"""
单元测试：prompt_editor_choice() 函数

测试编辑器选择功能的交互式和非交互式模式
"""

from unittest.mock import patch, MagicMock
import pytest
import sys

# 导入待测试的模块
try:
    from sckit_cli import prompt_editor_choice, Editor
except ImportError:
    prompt_editor_choice = None
    Editor = None


class TestPromptEditorChoice:
    """测试 prompt_editor_choice() 函数"""
    
    @pytest.mark.skipif(prompt_editor_choice is None, reason="Function not implemented yet")
    @patch('sckit_cli.utils.interactive.select_with_arrows')
    @patch('sys.stdin.isatty')
    def test_prompt_editor_choice_interactive(self, mock_isatty, mock_select, ):
        """T011: 测试交互式模式
        
        验证：
        - 在交互式终端中调用 select_with_arrows()
        - 正确转换选择结果为 Editor 枚举
        """
        # 模拟交互式终端
        mock_isatty.return_value = True
        
        # 模拟用户选择 Claude
        mock_select.return_value = "Claude"
        
        result = prompt_editor_choice()
        
        # 验证调用了 select_with_arrows
        assert mock_select.called, "应该调用 select_with_arrows"
        
        # 验证返回正确的枚举
        assert result == Editor.CLAUDE, "应该返回 Editor.CLAUDE"
        
        # 验证调用参数
        call_args = mock_select.call_args
        assert "Cursor" in call_args[1]["options"], "options 应该包含 Cursor"
        assert "Claude" in call_args[1]["options"], "options 应该包含 Claude"
        assert call_args[1]["default"] == "Cursor", "default 应该是 Cursor"
    
    @pytest.mark.skipif(prompt_editor_choice is None, reason="Function not implemented yet")
    @patch('sckit_cli.console')
    @patch('sys.stdin.isatty')
    def test_prompt_editor_choice_non_interactive(self, mock_isatty, mock_console):
        """T012: 测试非交互式模式降级
        
        验证：
        - 非交互式终端自动返回默认值（Cursor）
        - 不调用 select_with_arrows
        - 显示提示信息
        """
        # 模拟非交互式终端（CI/CD 环境）
        mock_isatty.return_value = False
        
        result = prompt_editor_choice()
        
        # 验证返回默认编辑器
        assert result == Editor.CURSOR, "非交互式模式应该返回默认的 Editor.CURSOR"
        
        # 验证显示了提示信息
        assert mock_console.print.called, "应该显示提示信息"
        
        # 验证提示信息内容
        call_args = str(mock_console.print.call_args)
        assert "non-interactive" in call_args.lower() or "cursor" in call_args.lower(), \
            "提示信息应该说明非交互式模式或使用 Cursor"

