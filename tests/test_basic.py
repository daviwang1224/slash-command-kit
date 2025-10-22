#!/usr/bin/env python3
"""快速基础功能测试脚本"""

import sys
from pathlib import Path
from sckit_cli import (
    Editor, Config, Release, ReleaseAsset,
    InstallConfig, InstallResult, is_valid_project_name,
    __version__
)

def test_version():
    """测试版本信息"""
    print("🧪 测试版本信息...")
    assert __version__ == "0.1.0"
    print(f"   ✅ 版本: {__version__}")

def test_editor():
    """测试 Editor 枚举"""
    print("\n🧪 测试 Editor 枚举...")
    
    # 测试值
    assert Editor.CURSOR.value == "cursor"
    assert Editor.CLAUDE.value == "claude"
    print("   ✅ Editor 值正确")
    
    # 测试显示名
    assert Editor.CURSOR.display_name == "Cursor"
    assert Editor.CLAUDE.display_name == "Claude Code"
    print("   ✅ 显示名称正确")
    
    # 测试配置目录
    assert Editor.CURSOR.config_dir == ".cursor"
    assert Editor.CLAUDE.config_dir == ".claude"
    print("   ✅ 配置目录正确")
    
    # 测试路径生成
    test_path = Path("/test/project")
    cursor_path = Editor.CURSOR.get_commands_path(test_path)
    # 使用 Path 比较而不是字符串（跨平台兼容）
    expected = test_path / ".cursor" / "commands"
    assert cursor_path == expected, f"期望 {expected}，得到 {cursor_path}"
    print("   ✅ 路径生成正确")

def test_config():
    """测试 Config 配置"""
    print("\n🧪 测试 Config 配置...")
    
    config = Config()
    assert config.CLI_VERSION == "0.1.0"
    assert "github.com" in config.release_api_url
    assert config.REQUEST_TIMEOUT > 0
    assert config.MAX_TEMPLATE_SIZE > 0
    print(f"   ✅ Config 配置正确")
    print(f"   - API URL: {config.release_api_url}")
    print(f"   - 超时: {config.REQUEST_TIMEOUT}s")

def test_release_asset():
    """测试 ReleaseAsset"""
    print("\n🧪 测试 ReleaseAsset...")
    
    asset = ReleaseAsset(
        name="sckit-cursor-0.1.0.zip",
        download_url="https://example.com/file.zip",
        size=1024000
    )
    
    assert asset.is_template_for(Editor.CURSOR) == True
    assert asset.is_template_for(Editor.CLAUDE) == False
    print("   ✅ ReleaseAsset 模板识别正确")

def test_release():
    """测试 Release"""
    print("\n🧪 测试 Release...")
    
    # 模拟 API 响应
    api_data = {
        "tag_name": "v0.1.0",
        "name": "Release 0.1.0",
        "assets": [
            {
                "name": "sckit-cursor-0.1.0.zip",
                "browser_download_url": "https://example.com/cursor.zip",
                "size": 1024000
            },
            {
                "name": "sckit-claude-0.1.0.zip",
                "browser_download_url": "https://example.com/claude.zip",
                "size": 1024000
            }
        ]
    }
    
    release = Release.from_api_response(api_data)
    assert release.version == "0.1.0"
    assert len(release.assets) == 2
    
    cursor_asset = release.get_template_asset(Editor.CURSOR)
    assert cursor_asset is not None
    assert cursor_asset.name == "sckit-cursor-0.1.0.zip"
    
    claude_asset = release.get_template_asset(Editor.CLAUDE)
    assert claude_asset is not None
    
    print("   ✅ Release 解析正确")
    print(f"   - 版本: {release.version}")
    print(f"   - 资源数: {len(release.assets)}")

def test_project_name_validation():
    """测试项目名验证"""
    print("\n🧪 测试项目名验证...")
    
    valid_names = [
        "my-project",
        "my_project",
        "MyProject",
        "project123",
        "a"
    ]
    
    invalid_names = [
        "my<project",
        "my>project",
        "my:project",
        "my\"project",
        "my/project",
        "my\\project",
        "my|project",
        "my?project",
        "my*project"
    ]
    
    for name in valid_names:
        assert is_valid_project_name(name), f"应该有效: {name}"
    print(f"   ✅ {len(valid_names)} 个有效名称通过")
    
    for name in invalid_names:
        assert not is_valid_project_name(name), f"应该无效: {name}"
    print(f"   ✅ {len(invalid_names)} 个无效名称正确拒绝")

def test_install_config():
    """测试 InstallConfig"""
    print("\n🧪 测试 InstallConfig...")
    
    config = InstallConfig(
        target_path=Path("/test/project"),
        editor=Editor.CURSOR,
        force=False
    )
    
    assert config.target_path == Path("/test/project")
    assert config.editor == Editor.CURSOR
    assert config.force == False
    assert config.commands_dir == Path("/test/project/.cursor/commands")
    print("   ✅ InstallConfig 配置正确")

def test_install_result():
    """测试 InstallResult"""
    print("\n🧪 测试 InstallResult...")
    
    result = InstallResult(
        success=True,
        version="0.1.0",
        files_copied=5,
        target_path=Path("/test/project"),
        editor=Editor.CURSOR,
        files_skipped=2,
        files_overwritten=1
    )
    
    assert result.success == True
    assert result.total_files == 7  # 5 + 2
    summary = result.format_summary()
    assert "安装完成" in summary
    assert "0.1.0" in summary
    print("   ✅ InstallResult 结果格式化正确")

def main():
    """运行所有测试"""
    print("=" * 60)
    print("🚀 sckit-cli 基础功能测试")
    print("=" * 60)
    
    tests = [
        test_version,
        test_editor,
        test_config,
        test_release_asset,
        test_release,
        test_project_name_validation,
        test_install_config,
        test_install_result,
    ]
    
    failed = []
    
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"   ❌ 测试失败: {e}")
            failed.append(test.__name__)
        except Exception as e:
            print(f"   ❌ 未预期的错误: {e}")
            failed.append(test.__name__)
    
    print("\n" + "=" * 60)
    if not failed:
        print("✅ 所有测试通过！")
        print("\n📋 测试总结:")
        print(f"   - 运行测试: {len(tests)}")
        print(f"   - 通过: {len(tests)}")
        print(f"   - 失败: 0")
        print("\n✨ CLI 工具基础功能正常！")
        print("\n📝 下一步:")
        print("   1. 实施 CI/CD（阶段 6）创建 GitHub Release")
        print("   2. 测试完整的 init 命令")
        print("   3. 查看 TESTING.md 了解详细测试步骤")
        return 0
    else:
        print(f"❌ {len(failed)} 个测试失败:")
        for name in failed:
            print(f"   - {name}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

