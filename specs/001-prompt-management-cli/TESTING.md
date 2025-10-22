# sckit-cli 测试指南

本文档说明如何测试 `sckit-cli` 工具的各项功能。

## 测试环境准备

### 1. 安装依赖

```bash
# 开发模式安装（推荐）
pip install -e .

# 或安装开发依赖
pip install -e ".[dev]"
```

### 2. 验证安装

```bash
# 测试版本命令
python -m sckit_cli --version
# 预期输出: sckit version 0.1.0

# 测试帮助命令
python -m sckit_cli --help

# 测试 init 命令帮助
python -m sckit_cli init --help
```

## 阶段 1: 本地基础功能测试 ✅

**目标**: 验证 CLI 工具基本结构和命令正常工作

### 测试 1.1: 版本命令

```bash
python -m sckit_cli --version
```

**预期**: 显示 `sckit version 0.1.0`

### 测试 1.2: 帮助命令

```bash
python -m sckit_cli --help
python -m sckit_cli init --help
```

**预期**: 显示格式化的帮助信息

### 测试 1.3: 数据模型验证

创建测试脚本 `test_models.py`:

```python
from pathlib import Path
from sckit_cli import (
    Editor, Config, Release, ReleaseAsset,
    InstallConfig, is_valid_project_name
)

# 测试 Editor 枚举
def test_editor():
    assert Editor.CURSOR.value == "cursor"
    assert Editor.CLAUDE.value == "claude"
    assert Editor.CURSOR.display_name == "Cursor"
    assert Editor.CURSOR.config_dir == ".cursor"
    
    path = Editor.CURSOR.get_commands_path(Path("/test"))
    assert str(path) == "/test/.cursor/commands"
    print("✓ Editor 枚举测试通过")

# 测试 Config
def test_config():
    config = Config()
    assert config.CLI_VERSION == "0.1.0"
    assert "github.com" in config.release_api_url
    print("✓ Config 测试通过")

# 测试项目名验证
def test_project_name():
    assert is_valid_project_name("my-project") == True
    assert is_valid_project_name("my_project") == True
    assert is_valid_project_name("my<project") == False
    assert is_valid_project_name("my:project") == False
    print("✓ 项目名验证测试通过")

if __name__ == "__main__":
    test_editor()
    test_config()
    test_project_name()
    print("\n✅ 所有数据模型测试通过！")
```

运行测试:
```bash
python test_models.py
```

## 阶段 2: 创建模拟 Release（为完整测试做准备）

**重要**: 由于 `sckit init` 需要从 GitHub Release 下载模板，我们需要先创建 Release。

### 选项 A: 创建本地测试 Release（推荐用于开发测试）

1. **手动创建测试 ZIP 文件**:

```bash
# 创建测试目录结构
mkdir -p test-release/.cursor/commands
cp commands/example.md test-release/.cursor/commands/
cp commands/README.md test-release/.cursor/commands/

# 打包
cd test-release
zip -r ../sckit-cursor-0.1.0.zip .
cd ..

# 为 Claude 创建类似的包
mkdir -p test-release-claude/.claude/commands
cp commands/example.md test-release-claude/.claude/commands/
cp commands/README.md test-release-claude/.claude/commands/
cd test-release-claude
zip -r ../sckit-claude-0.1.0.zip .
cd ..
```

2. **修改代码使用本地文件**（临时测试用）:

创建 `test_init_local.py`:

```python
"""本地测试 init 功能（不依赖 GitHub）"""
from pathlib import Path
import shutil
from sckit_cli import Editor, InstallConfig, copy_template_files

def test_local_init():
    # 创建测试目录
    test_project = Path("test-project-local")
    if test_project.exists():
        shutil.rmtree(test_project)
    test_project.mkdir()
    
    # 创建测试模板源
    template_source = Path("commands")
    target_dir = Editor.CURSOR.get_commands_path(test_project)
    
    # 复制文件
    files_copied, files_skipped, files_overwritten = copy_template_files(
        template_source,
        target_dir,
        force=True
    )
    
    print(f"✓ 复制了 {files_copied} 个文件到 {target_dir}")
    print(f"✓ 目标目录存在: {target_dir.exists()}")
    
    # 验证文件
    expected_files = ["example.md", "README.md"]
    for file in expected_files:
        file_path = target_dir / file
        assert file_path.exists(), f"文件不存在: {file}"
        print(f"✓ 找到文件: {file}")
    
    print("\n✅ 本地初始化测试通过！")
    print(f"   项目位置: {test_project.absolute()}")
    
    # 清理（可选）
    # shutil.rmtree(test_project)

if __name__ == "__main__":
    test_local_init()
```

运行:
```bash
python test_init_local.py
```

### 选项 B: 创建真实的 GitHub Release

**这是生产环境的方式，需要先完成 CI/CD（阶段 6）**

## 阶段 3: CI/CD 和 Release 自动化（推荐下一步）

### 为什么需要先做这个？

`sckit init` 命令需要从 GitHub Release 下载模板 ZIP 文件。要进行完整的端到端测试，我们需要：

1. **实现阶段 6 的 CI/CD 任务**（T058-T064）:
   - 创建 `.github/workflows/release.yml`
   - 创建打包脚本
   - 设置 GitHub Actions

2. **创建第一个 Release**:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

3. **然后才能完整测试 `sckit init`**

## 阶段 4: 完整端到端测试（需要 Release）

一旦有了 GitHub Release，可以进行完整测试：

### 测试 4.1: 新项目初始化

```bash
# 创建新项目（需要选择编辑器）
python -m sckit_cli init test-project-1

# 非交互式创建
python -m sckit_cli init test-project-2 --editor cursor

# 验证结果
ls test-project-2/.cursor/commands/
```

### 测试 4.2: 当前目录初始化

```bash
mkdir test-current
cd test-current
python -m sckit_cli init .
```

### 测试 4.3: 强制更新

```bash
# 再次初始化（应该询问覆盖）
python -m sckit_cli init .

# 强制覆盖
python -m sckit_cli init . --force
```

### 测试 4.4: 错误处理

```bash
# 非法项目名
python -m sckit_cli init "my<project"
# 预期: 显示错误消息

# 无网络（断网测试）
python -m sckit_cli init test-no-network
# 预期: 显示网络错误消息
```

## 测试检查清单

### ✅ 已完成（当前可测试）

- [x] 版本命令 (`--version`)
- [x] 帮助命令 (`--help`)
- [x] 数据模型（Editor, Config 等）
- [x] 项目名验证
- [x] 本地文件复制功能
- [x] 命令行参数解析

### 🔄 待完成（需要 Release）

- [ ] GitHub API 调用
- [ ] 文件下载（带进度）
- [ ] ZIP 解压
- [ ] 完整的 init 工作流
- [ ] 编辑器选择交互
- [ ] 文件冲突处理
- [ ] 错误处理（网络错误、限流等）

### 📋 待完成（需要编写测试）

- [ ] 单元测试（pytest）
- [ ] 集成测试
- [ ] 契约测试
- [ ] 跨平台测试

## 下一步建议

**推荐顺序**:

1. **✅ 完成阶段 1 测试**（当前可做）
   - 运行上述基础功能测试
   - 验证所有命令正常工作

2. **🚀 实施阶段 6: CI/CD**（T058-T064）
   - 创建 GitHub Actions 工作流
   - 实现自动打包脚本
   - 创建第一个 Release

3. **🧪 完成阶段 4 测试**（有 Release 后）
   - 端到端测试 init 命令
   - 验证下载和部署流程

4. **🔧 实施阶段 7-8**（可选）
   - 边缘案例处理
   - 编写自动化测试
   - 文档和优化

## 快速测试命令汇总

```bash
# 基础测试（立即可做）
python -m sckit_cli --version
python -m sckit_cli --help
python -m sckit_cli init --help
python test_models.py
python test_init_local.py

# 完整测试（需要 Release）
python -m sckit_cli init test-project --editor cursor
python -m sckit_cli init . --force

# 清理测试环境
rm -rf test-project* test-current
```

## 遇到问题？

1. **ImportError**: 确保已运行 `pip install -e .`
2. **命令not found**: 使用 `python -m sckit_cli` 而不是 `sckit`
3. **网络错误**: 需要先创建 GitHub Release
4. **权限错误**: 在有写入权限的目录测试

## 测试报告模板

测试后，可以创建测试报告：

```markdown
# 测试报告

**日期**: 2025-10-22
**版本**: 0.1.0
**测试人**: Your Name

## 测试环境
- OS: Windows 10 / macOS / Linux
- Python: 3.x
- 网络: 有/无

## 测试结果

### 基础功能
- [x] --version: ✅ 通过
- [x] --help: ✅ 通过
- [x] init --help: ✅ 通过

### 数据模型
- [x] Editor: ✅ 通过
- [x] Config: ✅ 通过
- [x] 项目名验证: ✅ 通过

### init 命令
- [ ] 新项目创建: 待测试（需要 Release）
- [ ] 当前目录初始化: 待测试
- [ ] 强制更新: 待测试

## 发现的问题

1. [描述问题]
2. [描述问题]

## 建议

[改进建议]
```

---

**当前状态**: ✅ 基础功能可测试，完整功能需要先创建 GitHub Release

