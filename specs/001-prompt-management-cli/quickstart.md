# Quick Start Guide

**Feature**: 轻量级提示词管理CLI工具  
**Date**: 2025-10-22

从零开始，5分钟内完成工具安装和第一个项目的提示词部署。

## Prerequisites

在开始前，确保您已安装：

- **Python 3.8+**: 运行CLI工具
- **uv**: Python包管理工具

### 安装uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

验证安装:
```bash
uv --version
```

---

## Step 1: 安装CLI工具

使用uv从GitHub仓库直接安装：

```bash
uv tool install sckit-cli --from git+https://github.com/username/slash-command-kit.git
```

验证安装:
```bash
sckit --version
# 输出: sckit version 0.1.0
```

---

## Step 2: 创建新项目

### 场景A: 创建新项目并初始化

```bash
# 创建并初始化新项目
sckit init my-awesome-project
```

**交互流程**:
```
选择AI编辑器:
  1. Cursor
  2. Claude Code
> 1

正在下载模板... ━━━━━━━━━━━━━━━━━━━━ 100% 2.1 MB
正在解压...
正在复制文件...

✅ 安装完成
版本: v0.1.0
编辑器: Cursor
位置: /path/to/my-awesome-project/.cursor/commands
文件: 5 个已复制
```

### 场景B: 在现有项目中初始化

```bash
# 进入您的项目目录
cd /path/to/existing-project

# 在当前目录初始化
sckit init .
```

**交互流程**: 与场景A相同，但文件会复制到当前项目的 `.cursor/commands/` 或 `.claude/commands/` 目录。

---

## Step 3: 使用提示词

### 在Cursor中使用

1. 打开Cursor编辑器
2. 打开您的项目文件夹
3. 在聊天窗口输入 `/` 即可看到新安装的命令
4. 例如: `/speckit.specify` 开始创建功能规格

### 在Claude Code中使用

1. 打开Claude Code编辑器（如VS Code + Claude插件）
2. 打开您的项目文件夹
3. 命令会自动加载到 `.claude/commands/` 目录
4. 使用斜杠命令调用

---

## 常见任务

### 更新已安装的提示词

当slash-command-kit仓库发布新版本时，更新您项目中的提示词：

```bash
cd /path/to/your-project
sckit init . --force
```

`--force` 标志会直接覆盖现有文件，无需确认。

### 在多个项目中使用

为每个项目单独初始化：

```bash
sckit init project-1
sckit init project-2
sckit init project-3
```

每个项目都有独立的提示词副本，互不影响。

### 切换编辑器

如果您从Cursor切换到Claude Code（或反之）：

```bash
cd /path/to/your-project
sckit init . --editor claude --force
```

这会将提示词重新部署到 `.claude/commands/` 目录。

### 非交互式安装（自动化脚本）

```bash
# 跳过所有交互提示
sckit init my-project --editor cursor --force
```

适合在CI/CD或自动化脚本中使用。

---

## 高级配置

### 提升GitHub API速率限制

默认情况下，匿名访问GitHub API限制为60请求/小时。如果您频繁使用，可以设置GitHub token：

```bash
# 创建GitHub Personal Access Token (不需要任何权限，只需公开读取)
# https://github.com/settings/tokens

export GITHUB_TOKEN=ghp_your_token_here
sckit init my-project
```

使用token后，速率限制提升至5000请求/小时。

### 自定义超时时间

如果您的网络较慢，可以增加超时时间：

```bash
SCKIT_TIMEOUT=30 sckit init my-project
```

### 使用Fork仓库

如果您fork了slash-command-kit仓库并做了自定义修改：

```bash
SCKIT_REPO=yourusername/your-fork sckit init my-project
```

---

## 故障排除

### 问题: GitHub API限流

**错误信息**:
```
❌ 错误: GitHub API速率限制
配额重置时间: 2025-10-22 11:30:00
💡 建议: 设置 GITHUB_TOKEN 环境变量
```

**解决方案**: 设置GitHub token（见"高级配置"部分）。

### 问题: 网络连接失败

**错误信息**:
```
❌ 错误: 无法连接到 GitHub
💡 建议: 检查网络连接后重试
```

**解决方案**:
1. 检查网络连接
2. 确认可以访问 https://github.com
3. 如果使用代理，配置HTTP代理:
   ```bash
   export HTTPS_PROXY=http://proxy.example.com:8080
   sckit init my-project
   ```

### 问题: 权限不足

**错误信息**:
```
❌ 错误: 无法写入目录: /path
💡 建议: 使用有写入权限的目录
```

**解决方案**:
1. 在您有权限的目录执行命令
2. 或使用 `sudo`/管理员权限（不推荐）

### 问题: 项目名包含非法字符

**错误信息**:
```
❌ 错误: 项目名 'my<project' 包含非法字符
💡 建议: 只使用字母、数字、下划线和连字符
```

**解决方案**: 使用合法的项目名，例如 `my-project` 或 `my_project_1`。

---

## 更新CLI工具

当CLI工具本身有新版本时，更新它：

```bash
uv tool install sckit-cli --force --from git+https://github.com/username/slash-command-kit.git
```

`--force` 标志会覆盖旧版本。

验证更新:
```bash
sckit --version
# 输出: sckit version 0.2.0
```

---

## 卸载

如果您不再需要该工具：

```bash
uv tool uninstall sckit-cli
```

**注意**: 这只会卸载CLI工具本身，不会删除已经初始化到项目中的提示词文件。如需删除提示词，手动删除项目中的 `.cursor/commands/` 或 `.claude/commands/` 目录。

---

## 5分钟快速回顾

```bash
# 1. 安装CLI工具 (30秒)
uv tool install sckit-cli --from git+https://github.com/username/slash-command-kit.git

# 2. 创建并初始化新项目 (1分钟)
sckit init my-project
# 选择 Cursor

# 3. 打开Cursor，进入项目，使用斜杠命令 (3分钟)
# 输入 / 查看可用命令
# 尝试 /speckit.specify

# 完成！ ✅
```

---

## 下一步

- **探索可用命令**: 在编辑器中输入 `/` 查看所有slash命令
- **阅读文档**: 查看各个命令的帮助文档了解详细用法
- **自定义模板**: Fork仓库并自定义您自己的提示词模板
  - 源文件位置：`commands/` 目录（单份存储）
  - 编辑Markdown文件添加您的提示词
  - 推送后CI/CD自动打包为cursor和claude两种格式
- **分享反馈**: 在GitHub仓库提交issue或PR

---

## 获取帮助

- **命令帮助**: `sckit --help` 或 `sckit init --help`
- **项目README**: 查看根目录README.md获取完整文档
- **GitHub Issues**: https://github.com/username/slash-command-kit/issues

