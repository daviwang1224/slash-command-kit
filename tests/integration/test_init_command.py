"""
集成测试：init 命令

测试 sckit init 命令的完整流程，包括交互式选择
"""

from unittest.mock import patch, MagicMock
import pytest
from pathlib import Path
from typer.testing import CliRunner

try:
    from sckit_cli import app, Editor
except ImportError:
    app = None
    Editor = None


runner = CliRunner()


class TestInitCommandSelection:
    """测试 init 命令的编辑器选择功能"""
    
    @pytest.mark.skipif(app is None, reason="CLI not available")
    @patch('sckit_cli.install_template')
    @patch('sckit_cli.utils.interactive.readchar.readkey')
    @patch('sys.stdin.isatty')
    def test_init_complete_selection_flow(
        self,
        mock_isatty,
        mock_readkey,
        mock_install
    ):
        """
        测试场景 1: 完整选择流程
        
        步骤:
        1. 运行 sckit init test-project
        2. 出现选择界面
        3. 按 ↓ 键选择 "Claude"
        4. 按 Enter 确认
        5. 验证后续流程使用 Claude 配置
        """
        # 模拟交互式终端
        mock_isatty.return_value = True
        
        # 模拟按键序列：DOWN, ENTER
        import readchar
        mock_readkey.side_effect = [
            readchar.key.DOWN,
            readchar.key.ENTER
        ]
        
        # 模拟安装成功
        from sckit_cli import InstallResult
        mock_install.return_value = InstallResult(
            success=True,
            version="0.3.0",
            files_copied=5,
            target_path=Path("test-project"),
            editor=Editor.CLAUDE
        )
        
        # 运行命令
        result = runner.invoke(app, ["init", "test-project"])
        
        # 验证命令成功
        assert result.exit_code == 0, f"Command should succeed, got: {result.stdout}"
        
        # 验证安装函数被调用，且使用了 Claude
        assert mock_install.called, "install_template should be called"
        install_config = mock_install.call_args[0][0]
        assert install_config.editor == Editor.CLAUDE, "Should use Claude editor"
    
    @pytest.mark.skipif(app is None, reason="CLI not available")
    @patch('sckit_cli.install_template')
    @patch('sys.stdin.isatty')
    def test_init_non_interactive_environment(
        self,
        mock_isatty,
        mock_install
    ):
        """
        测试场景 2: 非交互式环境
        
        步骤:
        1. 在 CI 环境运行 sckit init test-project
        2. 验证自动使用默认值（Cursor）
        3. 不卡在输入等待
        """
        # 模拟非交互式终端（CI/CD）
        mock_isatty.return_value = False
        
        # 模拟安装成功
        from sckit_cli import InstallResult
        mock_install.return_value = InstallResult(
            success=True,
            version="0.3.0",
            files_copied=5,
            target_path=Path("test-project"),
            editor=Editor.CURSOR
        )
        
        # 运行命令
        result = runner.invoke(app, ["init", "test-project"])
        
        # 验证命令成功
        assert result.exit_code == 0, f"Command should succeed, got: {result.stdout}"
        
        # 验证使用了默认编辑器 Cursor
        assert mock_install.called, "install_template should be called"
        install_config = mock_install.call_args[0][0]
        assert install_config.editor == Editor.CURSOR, "Should use default Cursor editor"
        
        # 验证输出包含非交互式模式提示
        assert "non-interactive" in result.stdout.lower() or "cursor" in result.stdout.lower(), \
            "Should indicate non-interactive mode"
    
    @pytest.mark.skipif(app is None, reason="CLI not available")
    @patch('sckit_cli.install_template')
    @patch('sckit_cli.utils.interactive.readchar.readkey')
    @patch('sys.stdin.isatty')
    def test_init_user_cancels_with_ctrl_c(
        self,
        mock_isatty,
        mock_readkey,
        mock_install
    ):
        """
        测试场景 3: 用户取消（Ctrl+C）
        
        步骤:
        1. 运行 sckit init test-project
        2. 按 Ctrl+C 取消
        3. 验证退出码为 2
        4. 验证显示取消消息
        """
        # 模拟交互式终端
        mock_isatty.return_value = True
        
        # 模拟 Ctrl+C
        mock_readkey.side_effect = KeyboardInterrupt()
        
        # 运行命令
        result = runner.invoke(app, ["init", "test-project"])
        
        # 验证退出码为 2（用户取消）
        assert result.exit_code == 2, f"Exit code should be 2 for Ctrl+C, got {result.exit_code}"
        
        # 验证显示取消消息
        assert "取消" in result.stdout or "cancelled" in result.stdout.lower(), \
            "Should show cancellation message"
        
        # 验证没有调用安装函数
        assert not mock_install.called, "install_template should not be called after cancellation"
    
    @pytest.mark.skipif(app is None, reason="CLI not available")
    @patch('sckit_cli.install_template')
    def test_init_with_editor_parameter_skips_selection(
        self,
        mock_install
    ):
        """
        测试: 使用 --editor 参数跳过选择界面
        
        验证:
        - --editor 参数直接指定编辑器
        - 不进入交互式选择
        - 正常执行安装流程
        """
        # 模拟安装成功
        from sckit_cli import InstallResult
        mock_install.return_value = InstallResult(
            success=True,
            version="0.3.0",
            files_copied=5,
            target_path=Path("test-project"),
            editor=Editor.CLAUDE
        )
        
        # 运行命令with --editor 参数
        result = runner.invoke(app, ["init", "test-project", "--editor", "claude"])
        
        # 验证命令成功
        assert result.exit_code == 0, f"Command should succeed, got: {result.stdout}"
        
        # 验证使用了指定的编辑器
        assert mock_install.called, "install_template should be called"
        install_config = mock_install.call_args[0][0]
        assert install_config.editor == Editor.CLAUDE, "Should use specified Claude editor"

