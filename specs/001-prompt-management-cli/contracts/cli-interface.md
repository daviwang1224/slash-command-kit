# CLI Interface Specification

**Feature**: 轻量级提示词管理CLI工具  
**Date**: 2025-10-22  
**Version**: 1.0

本文档定义 `sckit` 命令行工具的接口规范。

## Command: sckit

根命令，提供全局帮助和版本信息。

### Synopsis

```bash
sckit [OPTIONS] COMMAND [ARGS]...
```

### Global Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--version` | `-v` | flag | - | 显示版本号并退出 |
| `--help` | `-h` | flag | - | 显示帮助信息并退出 |

### Examples

```bash
# 显示版本
sckit --version
# Output: sckit version 0.1.0

# 显示帮助
sckit --help
# Output: 命令列表和使用说明
```

---

## Command: sckit init

在项目中初始化或更新提示词模板。

### Synopsis

```bash
sckit init [OPTIONS] [PATH]
```

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `PATH` | string | No | `.` | 项目路径。使用 `.` 表示当前目录，或指定目录名创建新项目 |

### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--force` | `-f` | flag | false | 强制覆盖已存在的文件，跳过确认 |
| `--editor` | `-e` | choice | - | 指定编辑器，跳过交互式选择。可选值: `cursor`, `claude` |
| `--help` | `-h` | flag | - | 显示命令帮助 |

### Behavior

**1. 新项目初始化**
```bash
sckit init my-project
```
- 创建 `my-project/` 目录
- 提示选择编辑器（或使用 `--editor`）
- 下载最新模板
- 复制到 `my-project/.cursor/commands/` 或 `my-project/.claude/commands/`
- 显示成功消息

**2. 当前目录初始化**
```bash
sckit init .
# 或
sckit init
```
- 不创建新目录
- 提示选择编辑器
- 下载最新模板
- 复制到当前目录的 `.cursor/commands/` 或 `.claude/commands/`
- 如果文件已存在，询问是否覆盖（除非使用 `--force`）

**3. 强制更新**
```bash
sckit init . --force
```
- 直接覆盖所有已存在的文件
- 不提示确认
- 适合自动化脚本或更新场景

**4. 指定编辑器**
```bash
sckit init my-project --editor cursor
```
- 跳过交互式选择
- 直接使用指定的编辑器

### Interactive Prompts

**编辑器选择** (当未使用 `--editor` 时):
```
选择AI编辑器:
  1. Cursor
  2. Claude Code
> 
```

**文件覆盖确认** (当文件已存在且未使用 `--force` 时):
```
文件 'speckit.specify.md' 已存在
[o]覆盖 / [s]跳过 / [a]全部覆盖 / [q]取消: 
```

### Exit Codes

| Code | Description |
|------|-------------|
| 0 | 成功 |
| 1 | 一般错误（网络、文件系统等） |
| 2 | 用户取消操作（Ctrl+C或选择取消） |
| 3 | 验证错误（非法项目名等） |

### Output Format

**成功输出** (stdout):
```
✅ 安装完成
版本: v0.1.0
编辑器: Cursor
位置: /path/to/project/.cursor/commands
文件: 5 个已复制
```

**进度输出** (stdout):
```
正在下载模板... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 2.1 MB
正在解压...
正在复制文件...
```

**错误输出** (stderr):
```
❌ 错误: 网络连接失败
💡 建议: 检查网络连接后重试
```

### Examples

```bash
# 示例 1: 创建新项目
sckit init my-awesome-project
# 交互选择Cursor
# 输出: 成功消息 + 文件数量

# 示例 2: 在当前目录初始化
sckit init .
# 或
sckit init

# 示例 3: 强制更新（覆盖现有文件）
sckit init . --force

# 示例 4: 指定编辑器，非交互式
sckit init my-project --editor cursor

# 示例 5: 组合使用
sckit init . --editor claude --force
```

### Error Scenarios

**1. 项目名包含非法字符**
```bash
sckit init "my<project"
```
输出:
```
❌ 错误: 项目名 'my<project' 包含非法字符
💡 建议: 项目名只能包含字母、数字、下划线和连字符
```
退出码: 3

**2. 网络连接失败**
```bash
sckit init my-project
```
输出:
```
❌ 错误: 无法连接到 GitHub
💡 建议: 检查网络连接后重试
```
退出码: 1

**3. GitHub API限流**
```bash
sckit init my-project
```
输出:
```
❌ 错误: GitHub API速率限制
配额重置时间: 2025-10-22 11:30:00
💡 建议: 设置 GITHUB_TOKEN 环境变量以获取更高配额
```
退出码: 1

**4. Release未找到模板**
```bash
sckit init my-project --editor cursor
```
输出:
```
❌ 错误: 未找到 Cursor 的模板包
期望文件: sckit-cursor-*.zip
💡 建议: 检查仓库Release是否包含正确的模板文件
```
退出码: 1

**5. 磁盘空间不足**
```bash
sckit init my-project
```
输出:
```
❌ 错误: 磁盘空间不足
需要: 5 MB, 可用: 1 MB
💡 建议: 清理磁盘空间后重试
```
退出码: 1

**6. 权限不足**
```bash
sckit init /root/my-project  # 无写入权限
```
输出:
```
❌ 错误: 无法写入目录: /root
💡 建议: 使用有写入权限的目录或以管理员身份运行
```
退出码: 1

---

## Environment Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `GITHUB_TOKEN` | string | - | GitHub个人访问令牌，用于提升API速率限制（60 → 5000请求/小时） |
| `SCKIT_TIMEOUT` | int | 10 | HTTP请求超时时间（秒） |
| `SCKIT_REPO` | string | `username/slash-command-kit` | 自定义源仓库（高级用途） |

### Example

```bash
# 使用GitHub token
export GITHUB_TOKEN=ghp_your_token_here
sckit init my-project

# 自定义超时
SCKIT_TIMEOUT=30 sckit init my-project

# 使用自定义仓库（fork）
SCKIT_REPO=myusername/my-fork sckit init my-project
```

---

## Configuration Files

**不使用配置文件**。所有配置通过命令行参数和环境变量传递，保持工具的简单性。

---

## API Contract

### GitHub API Requirements

**Endpoint**: `GET https://api.github.com/repos/{owner}/{repo}/releases/latest`

**Expected Response**:
```json
{
  "tag_name": "v0.1.0",
  "name": "Release 0.1.0",
  "assets": [
    {
      "name": "sckit-cursor-0.1.0.zip",
      "browser_download_url": "https://github.com/.../sckit-cursor-0.1.0.zip",
      "size": 2048000
    },
    {
      "name": "sckit-claude-0.1.0.zip",
      "browser_download_url": "https://github.com/.../sckit-claude-0.1.0.zip",
      "size": 2048000
    }
  ]
}
```

**Required Fields**:
- `tag_name`: Release版本标签
- `assets[]`: 资源数组
  - `name`: 文件名（必须匹配 `sckit-{editor}-*.zip`）
  - `browser_download_url`: 下载URL
  - `size`: 文件大小（字节）

**Error Handling**:
- HTTP 403 + `X-RateLimit-Remaining: 0` → 显示限流错误
- HTTP 404 → 显示"未找到Release"错误
- HTTP 5xx → 显示"服务器错误"并建议重试

---

## Template Archive Requirements

### Archive Structure

模板zip文件包含编辑器特定的目录结构（从`commands/`单源打包生成）：

**Cursor编辑器包** (`sckit-cursor-0.1.0.zip`):
```
sckit-cursor-0.1.0.zip
└── .cursor/
    └── commands/
        ├── example.md
        └── ...其他.md文件
```

**Claude Code编辑器包** (`sckit-claude-0.1.0.zip`):
```
sckit-claude-0.1.0.zip
└── .claude/
    └── commands/
        ├── example.md
        └── ...其他.md文件
```

**源文件说明**:
- 源仓库`commands/`目录只存一份Markdown格式文件
- CI/CD打包时根据编辑器生成不同的目录结构
- 内容完全相同，仅路径不同（参考spec-kit单源多目标策略）

### Naming Convention

- 文件名格式: `sckit-{editor}-{version}.zip`
- `{editor}`: `cursor` 或 `claude`
- `{version}`: 与`tag_name`匹配（去掉`v`前缀）

示例:
- Release `v0.1.0` → `sckit-cursor-0.1.0.zip`
- Release `v1.2.3-beta` → `sckit-cursor-1.2.3-beta.zip`

---

## Testing Contract

### Unit Test Requirements

1. **CLI参数解析**: 验证所有参数组合
2. **路径验证**: 测试各种路径输入
3. **错误处理**: 每种错误场景都有测试
4. **跨平台**: Windows/macOS/Linux路径处理

### Integration Test Requirements

1. **GitHub API交互**: 
   - Mock API响应
   - 测试限流处理
   - 测试404场景

2. **完整工作流**:
   - 新项目初始化
   - 当前目录初始化  
   - 强制覆盖更新
   - 用户取消操作

3. **文件系统操作**:
   - 创建目录
   - 复制文件
   - 处理已存在文件
   - 清理临时文件

### Contract Test Requirements

验证与外部系统的契约：

1. **GitHub API契约**: 
   - Response schema匹配
   - 下载URL可访问
   - 资源文件名格式正确

2. **编辑器契约**:
   - `.cursor/commands/` 路径
   - `.claude/commands/` 路径
   - Markdown文件格式

---

## Versioning

CLI工具遵循语义化版本（Semantic Versioning）：

- **MAJOR**: 不兼容的API变更（如删除命令或参数）
- **MINOR**: 向后兼容的功能新增（如新增 `--editor` 参数）
- **PATCH**: 向后兼容的问题修复

当前版本: `0.1.0` （初始MVP版本）

