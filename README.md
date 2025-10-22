# sckit-cli

> 轻量级提示词管理工具 - 一键部署 AI 编辑器提示词模板

## 概览

`sckit-cli` 是一个命令行工具，用于从 GitHub 仓库快速部署提示词（slash commands）模板到 Cursor 或 Claude Code 编辑器。集中管理分散的提示词文档，一键部署到项目中。

## 特性

- 🚀 **快速安装**: 通过 `uv` 从 GitHub 直接安装
- 📦 **自动下载**: 从 GitHub Release 获取最新模板
- 🎯 **多编辑器支持**: 支持 Cursor 和 Claude Code
- 💡 **交互式选择**: 友好的命令行界面
- ⚡ **智能更新**: 支持强制覆盖和增量更新
- 🌍 **跨平台**: Windows、macOS、Linux

## 安装

### 前置要求

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) 包管理器

### 安装 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 安装 sckit-cli

```bash
uv tool install sckit-cli --from git+https://github.com/daviwang1224/slash-command-kit.git
```

验证安装：
```bash
sckit --version
```

## 快速开始

### 1. 创建新项目并初始化提示词

```bash
sckit init my-project
```

按提示选择编辑器（Cursor 或 Claude Code），工具会自动：
- 创建项目目录
- 下载最新模板
- 部署到对应的编辑器配置目录

### 2. 在现有项目中初始化

```bash
cd your-project
sckit init .
```

### 3. 更新现有提示词

```bash
sckit init . --force
```

使用 `--force` 标志跳过覆盖确认，直接更新所有文件。

## 使用说明

### 命令

#### `sckit init [PATH]`

在项目中初始化或更新提示词模板。

**参数**:
- `PATH` - 项目路径（默认为 `.` 当前目录）

**选项**:
- `--editor, -e` - 指定编辑器（`cursor` 或 `claude`），跳过交互选择
- `--force, -f` - 强制覆盖已存在的文件，跳过确认
- `--help` - 显示帮助信息

**示例**:
```bash
# 创建新项目
sckit init my-awesome-project

# 在当前目录初始化
sckit init .

# 指定编辑器，非交互式
sckit init my-project --editor cursor

# 强制更新
sckit init . --force

# 组合使用
sckit init . --editor claude --force
```

#### `sckit --version`

显示 CLI 工具版本号。

#### `sckit --help`

显示帮助信息和可用命令。

## 配置

### 环境变量

- `GITHUB_TOKEN` - GitHub 个人访问令牌，用于提升 API 速率限制（可选）
- `SCKIT_TIMEOUT` - HTTP 请求超时时间（秒，默认 10）
- `SCKIT_REPO` - 自定义源仓库（默认 `daviwang1224/slash-command-kit`）

**示例**:
```bash
export GITHUB_TOKEN=ghp_your_token_here
export SCKIT_TIMEOUT=30
sckit init my-project
```

## 故障排除

### GitHub API 限流

**问题**: `❌ 错误: GitHub API速率限制`

**解决**: 设置 `GITHUB_TOKEN` 环境变量以获取更高的速率限制（60 → 5000 请求/小时）

### 网络连接失败

**问题**: `❌ 错误: 无法连接到 GitHub`

**解决**: 
1. 检查网络连接
2. 如果使用代理，配置 `HTTPS_PROXY` 环境变量
3. 稍后重试

### 权限不足

**问题**: `❌ 错误: 无法写入目录`

**解决**: 在有写入权限的目录执行命令

## 更新 CLI 工具

```bash
uv tool install sckit-cli --force --from git+https://github.com/daviwang1224/slash-command-kit.git
```

## 卸载

```bash
uv tool uninstall sckit-cli
```

**注意**: 这只会卸载 CLI 工具，不会删除已部署到项目中的提示词文件。

## 开发

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/daviwang1224/slash-command-kit.git
cd slash-command-kit

# 安装开发依赖
uv pip install -e ".[dev]"

# 运行测试
pytest

# 类型检查
mypy src/sckit_cli
```

### 项目结构

```
slash-command-kit/
├── src/sckit_cli/       # CLI 工具源代码
├── commands/            # 提示词模板源文件（单份存储）
├── tests/               # 测试
│   ├── contract/        # 契约测试
│   ├── integration/     # 集成测试
│   └── unit/            # 单元测试
├── .github/workflows/   # CI/CD 流程
├── pyproject.toml       # 项目配置
└── README.md            # 本文件
```

## Release 流程

### 创建新版本

本项目使用 GitHub Actions 自动化 Release 流程。

#### 1. 本地测试打包（可选）

```bash
# 测试打包脚本
bash scripts/test-release-locally.sh
```

这会创建测试用的 zip 包并验证内容。

#### 2. 创建 Release

```bash
# 1. 确保所有更改已提交
git add .
git commit -m "feat: ready for v0.1.0 release"

# 2. 创建版本标签
git tag v0.1.0

# 3. 推送代码和标签
git push origin main
git push origin v0.1.0
```

#### 3. 自动化流程

推送标签后，GitHub Actions 会自动：

1. ✅ 创建 Release 包（sckit-cursor-*.zip 和 sckit-claude-*.zip）
2. ✅ 创建 GitHub Release
3. ✅ 上传模板包作为 Release Assets
4. ✅ 生成 Release 说明

#### 4. 验证 Release

访问 GitHub Release 页面确认：
- 两个 zip 文件已上传
- Release 说明正确
- 文件可以下载

### 发布后测试

```bash
# 安装发布的版本
uv tool install sckit-cli --from git+https://github.com/daviwang1224/slash-command-kit.git

# 测试完整流程
sckit init test-project
cd test-project
ls .cursor/commands/  # 或 .claude/commands/
```

### 模板包结构

Release 包含两种编辑器的模板：

**sckit-cursor-0.1.0.zip**:
```
.cursor/
  └── commands/
      ├── example.md
      └── README.md
```

**sckit-claude-0.1.0.zip**:
```
.claude/
  └── commands/
      ├── example.md
      └── README.md
```

CLI 工具会根据用户选择的编辑器自动下载对应的包。

### 更新版本号

发布新版本时，需要更新以下文件：

1. `src/sckit_cli/__init__.py` - `__version__ = "x.y.z"`
2. `pyproject.toml` - `version = "x.y.z"`
3. `CHANGELOG.md` - 添加版本说明

然后按照上述流程创建 tag 和 Release。

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 链接

- [GitHub 仓库](https://github.com/daviwang1224/slash-command-kit)
- [问题跟踪](https://github.com/daviwang1224/slash-command-kit/issues)
- [变更日志](CHANGELOG.md)

---

Made with ❤️ for AI-powered development
