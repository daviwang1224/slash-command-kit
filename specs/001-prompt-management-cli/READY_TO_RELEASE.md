# ✅ 准备发布检查清单

## 🎉 恭喜！您的 CLI 工具已准备好发布

所有核心功能已实现并测试通过。按照此清单完成最后的准备工作。

---

## 📋 发布前最后检查（5-10 分钟）

### ✅ 第 1 步: 更新仓库信息

**必须修改以下文件中的 `yourusername`**:

```bash
# 1. 全局搜索替换（推荐）
# 将 yourusername 替换为您的实际 GitHub 用户名

# 需要更新的文件:
# - README.md (多处)
# - pyproject.toml ([project.urls])
# - src/sckit_cli/__init__.py (Config 类)
```

**快速方法**（Linux/Mac/Git Bash）:
```bash
# 替换所有文件中的 yourusername
find . -type f \( -name "*.md" -o -name "*.toml" -o -name "*.py" \) \
  -not -path "./.git/*" \
  -not -path "./.genreleases/*" \
  -exec sed -i 's/yourusername/YOUR_ACTUAL_USERNAME/g' {} +
```

**手动方法**（Windows PowerShell）:
```powershell
# 在以下文件中查找并替换 yourusername:
# 1. README.md
# 2. pyproject.toml
# 3. src/sckit_cli/__init__.py
```

### ✅ 第 2 步: 更新作者信息

**编辑 `pyproject.toml`**:
```toml
[project]
authors = [
    {name = "你的名字", email = "your.email@example.com"}
]
```

**编辑 `LICENSE`**:
```
Copyright (c) 2025 你的名字
```

### ✅ 第 3 步: 最后测试

```bash
# 运行基础功能测试
python test_basic.py

# 期望输出：
# ✅ 所有测试通过！
# ✨ CLI 工具基础功能正常！
```

### ✅ 第 4 步: 验证 CI/CD 文件

```bash
# 确认文件存在
ls -la .github/workflows/release.yml
ls -la .github/workflows/scripts/*.sh
ls -la commands/*.md

# 所有文件应该都存在
```

---

## 🚀 发布流程（3 个命令）

### 方式 A: 标准流程（推荐）

```bash
# 1. 提交所有更改
git add .
git commit -m "feat: ready for v0.1.0 release

- Implemented MVP core functionality  
- Added CI/CD automation
- Complete documentation
- Ready for production use
"

# 2. 推送到 GitHub
git push origin main

# 3. 创建并推送标签（这会触发自动发布！）
git tag v0.1.0
git push origin v0.1.0
```

### 方式 B: 本地测试后发布

```bash
# 1. 先本地测试打包
bash scripts/test-release-locally.sh

# 2. 验证生成的 zip 文件
unzip -l .genreleases/sckit-cursor-0.1.0-test.zip
unzip -l .genreleases/sckit-claude-0.1.0-test.zip

# 3. 如果测试通过，按方式 A 发布
```

---

## ⏱️ 发布后等待（1-2 分钟）

### 监控 GitHub Actions

1. **访问**: `https://github.com/yourusername/slash-command-kit/actions`
2. **查看**: 应该有一个 "Release" 工作流正在运行
3. **等待**: 通常需要 1-2 分钟完成

### 工作流步骤

GitHub Actions 会自动：
- ✅ 验证 commands/ 目录
- ✅ 创建 Cursor 模板包
- ✅ 创建 Claude 模板包
- ✅ 创建 GitHub Release
- ✅ 上传两个 zip 文件
- ✅ 生成 Release 说明

---

## 🎊 验证 Release（1 分钟）

### 检查 Release 页面

```bash
# 访问（替换 yourusername）
https://github.com/yourusername/slash-command-kit/releases/tag/v0.1.0
```

**应该看到**:
- ✅ Release v0.1.0 标题
- ✅ Release 说明（自动生成）
- ✅ 两个附件:
  - `sckit-cursor-0.1.0.zip`
  - `sckit-claude-0.1.0.zip`

### 下载并验证

```bash
# 下载其中一个 zip
curl -LO https://github.com/yourusername/slash-command-kit/releases/download/v0.1.0/sckit-cursor-0.1.0.zip

# 查看内容
unzip -l sckit-cursor-0.1.0.zip

# 应该看到：
# .cursor/commands/example.md
# .cursor/commands/README.md
```

---

## 🧪 端到端测试（5 分钟）

**这是最重要的测试！验证整个流程能够工作。**

### 测试 1: 安装 CLI

```bash
# 使用 uv 从 GitHub 安装
uv tool install sckit-cli --from git+https://github.com/yourusername/slash-command-kit.git

# 验证安装
sckit --version
# 期望: sckit version 0.1.0
```

### 测试 2: 创建新项目

```bash
# 创建测试目录
mkdir ~/sckit-test
cd ~/sckit-test

# 运行 init（会下载 Release 中的 zip！）
sckit init my-first-project
```

**交互流程**:
1. 选择编辑器（Cursor 或 Claude）
2. 等待下载和解压
3. 看到成功消息

### 测试 3: 验证部署

```bash
# 检查文件
ls my-first-project/.cursor/commands/
# 或
ls my-first-project/.claude/commands/

# 应该看到：
# - example.md
# - README.md
```

### 测试 4: 编辑器集成

1. 在 Cursor 或 Claude Code 中打开 `my-first-project`
2. 打开聊天窗口
3. 输入 `/`
4. 应该看到新安装的命令
5. 尝试 `/example`

---

## ✨ 成功！

如果所有测试都通过了，恭喜您！🎉

您已经成功：
- ✅ 实现了完整的 MVP
- ✅ 设置了 CI/CD 自动化
- ✅ 发布了第一个版本
- ✅ 验证了端到端流程

---

## 📣 下一步：分享您的工作

### 1. 更新项目看板

在 GitHub 项目中：
- 标记 MVP 任务为完成
- 创建 v0.2.0 里程碑
- 规划下一阶段功能

### 2. 编写发布公告

```markdown
## 🎉 sckit-cli v0.1.0 发布！

轻量级提示词管理工具，一键部署 AI 编辑器提示词。

### 特性
- 🚀 简单安装：uv tool install
- 📦 自动部署：sckit init
- 🎯 双编辑器支持：Cursor + Claude Code

### 安装
\`\`\`bash
uv tool install sckit-cli --from git+https://github.com/yourusername/slash-command-kit.git
\`\`\`

[查看文档](https://github.com/yourusername/slash-command-kit)
```

### 3. 分享渠道

- Twitter/X
- Reddit (r/python, r/programming)
- Hacker News
- Dev.to
- 个人博客

### 4. 收集反馈

- 监控 GitHub Issues
- 创建讨论区
- 设置反馈表单

---

## 🔧 遇到问题？

### GitHub Actions 失败

**查看日志**:
- Actions → 点击工作流 → 查看详细日志

**常见问题**:
- 脚本权限：确保 `.sh` 文件有执行权限
- 文件缺失：确认 `commands/` 目录存在
- Token 权限：检查 GITHUB_TOKEN 设置

### init 命令失败

**可能原因**:
- Release 还没准备好：等待几分钟
- 网络问题：检查网络连接
- 文件格式错误：验证 zip 文件内容

**调试**:
```bash
# 手动下载测试
curl -LO https://github.com/yourusername/slash-command-kit/releases/download/v0.1.0/sckit-cursor-0.1.0.zip

# 验证内容
unzip -l sckit-cursor-0.1.0.zip
```

---

## 📚 参考文档

- **详细发布流程**: `RELEASE_GUIDE.md`
- **测试指南**: `TESTING.md`
- **实施总结**: `IMPLEMENTATION_SUMMARY.md`
- **下一步计划**: `NEXT_STEPS.md`

---

## 🎯 快速命令参考

```bash
# === 发布 ===
git add .
git commit -m "feat: ready for release"
git tag v0.1.0
git push origin main v0.1.0

# === 验证 ===
# 访问: https://github.com/yourusername/slash-command-kit/releases

# === 测试 ===
uv tool install sckit-cli --from git+https://github.com/yourusername/slash-command-kit.git
sckit init test-project

# === 清理测试环境 ===
uv tool uninstall sckit-cli
rm -rf test-project
```

---

## ✅ 准备好了吗？

**完成所有检查后，运行：**

```bash
git tag v0.1.0
git push origin v0.1.0
```

**然后坐下来，看着魔法发生！** ✨

---

**祝发布顺利！** 🚀🎉

有任何问题，请查阅文档或提交 Issue。

