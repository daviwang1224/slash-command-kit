# 发布指南

## 🎯 概述

本指南涵盖完整的发布流程，包括发布前检查、发布步骤、测试和故障排除。

**当前版本**: v0.1.0 MVP  
**状态**: ✅ 准备发布

---

## 📋 发布前检查清单

### 1. 代码检查

- [x] ✅ 所有基础功能已实现并测试通过
- [x] ✅ CI/CD 脚本已创建
- [ ] ⚠️ 更新 README.md 中的 `yourusername` 为您的 GitHub 用户名
- [ ] ⚠️ 更新 LICENSE 中的作者信息
- [ ] ⚠️ 检查 pyproject.toml 中的仓库 URL

### 2. 更新仓库信息

**必须修改以下文件中的 `yourusername`**:

```bash
# 需要更新的文件:
# - README.md (多处)
# - pyproject.toml ([project.urls])
# - src/sckit_cli/__init__.py (Config 类)
```

**快速方法** (Linux/Mac/Git Bash):
```bash
# 替换所有文件中的 yourusername
find . -type f \( -name "*.md" -o -name "*.toml" -o -name "*.py" \) \
  -not -path "./.git/*" \
  -not -path "./.genreleases/*" \
  -exec sed -i 's/yourusername/YOUR_ACTUAL_USERNAME/g' {} +
```

**手动方法** (Windows PowerShell):
```powershell
# 在以下文件中查找并替换 yourusername:
# 1. README.md
# 2. pyproject.toml
# 3. src/sckit_cli/__init__.py
```

### 3. 更新作者信息

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

### 4. 运行测试

```bash
# 运行基础功能测试
python test_basic.py

# 期望输出：
# ✅ 所有测试通过！
# ✨ CLI 工具基础功能正常！
```

### 5. 本地打包测试 (可选但推荐)

```bash
# 赋予脚本执行权限（Linux/Mac）
chmod +x scripts/test-release-locally.sh
chmod +x .github/workflows/scripts/*.sh

# 运行本地测试
bash scripts/test-release-locally.sh

# 验证生成的 zip 文件
unzip -l .genreleases/sckit-cursor-0.1.0-test.zip
unzip -l .genreleases/sckit-claude-0.1.0-test.zip
```

### 6. 验证 CI/CD 文件

```bash
# 确认文件存在
ls -la .github/workflows/release.yml
ls -la .github/workflows/scripts/*.sh
ls -la commands/*.md

# 所有文件应该都存在
```

---

## 🚀 发布步骤

### 步骤 1: 提交所有更改

```bash
# 查看更改
git status

# 添加所有文件
git add .

# 提交
git commit -m "feat: ready for v0.1.0 release

- Implemented MVP core functionality
- Added CI/CD pipeline for automated releases
- Created release packaging scripts
- Updated documentation
"

# 推送到 GitHub
git push origin main  # 或 master，取决于您的默认分支
```

### 步骤 2: 创建并推送标签

```bash
# 创建版本标签
git tag v0.1.0

# 推送标签到 GitHub（这会触发 GitHub Actions）
git push origin v0.1.0
```

**⚡ 快捷方式**: 一次性推送代码和标签
```bash
git push origin main v0.1.0
```

### 步骤 3: 监控 GitHub Actions (1-2 分钟)

1. **访问**: `https://github.com/yourusername/slash-command-kit/actions`
2. **查看**: 应该有一个 "Release" 工作流正在运行
3. **等待**: 通常需要 1-2 分钟完成

**工作流会自动执行**:
- ✅ 验证 commands/ 目录
- ✅ 创建 Cursor 模板包
- ✅ 创建 Claude 模板包
- ✅ 创建 GitHub Release
- ✅ 上传两个 zip 文件
- ✅ 生成 Release 说明

### 步骤 4: 验证 Release

1. 访问 `https://github.com/yourusername/slash-command-kit/releases`
2. 您应该看到 "Release v0.1.0"
3. 确认有两个附件：
   - `sckit-cursor-0.1.0.zip`
   - `sckit-claude-0.1.0.zip`
4. 点击下载其中一个 zip，验证内容正确

**验证 zip 内容**:
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

## 🧪 发布后测试

**这是最重要的测试！验证整个流程能够工作。**

### 测试 1: 安装 CLI

```bash
# 使用 uv 从 GitHub 安装
uv tool install sckit-cli --from git+https://github.com/yourusername/slash-command-kit.git

# 验证安装
sckit --version
# 期望: sckit version 0.1.0

sckit --help
# 期望: 显示帮助信息
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

# 查看文件内容
cat my-first-project/.cursor/commands/example.md
```

### 测试 4: 编辑器集成

1. 在 Cursor 或 Claude Code 中打开 `my-first-project`
2. 打开聊天窗口
3. 输入 `/`
4. 应该看到新安装的命令
5. 尝试 `/example` 命令

### 测试 5: 清理测试环境

```bash
# 卸载 CLI
uv tool uninstall sckit-cli

# 删除测试目录
rm -rf ~/sckit-test
```

---

## ✨ 发布成功！

如果所有测试都通过了，恭喜您！🎉

您已经成功：
- ✅ 实现了完整的 MVP
- ✅ 设置了 CI/CD 自动化
- ✅ 发布了第一个版本
- ✅ 验证了端到端流程

---

## 📣 发布后的工作

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

### 5. 持续改进

参考 `tasks.md` 中的后续计划：
- 实施阶段 7: 边缘案例处理
- 实施阶段 8: 打磨和优化
- 添加更多提示词模板

---

## 🔧 故障排除

### 问题 1: GitHub Actions 失败

**查看日志**:
1. 访问 Actions 标签
2. 点击失败的工作流
3. 查看具体错误信息

**常见原因**:
- 脚本权限问题：确保脚本有执行权限
- 找不到文件：检查 `commands/` 目录是否存在
- API 错误：检查 GitHub Token 权限

**解决方案**:
```bash
# 检查脚本权限
ls -la .github/workflows/scripts/

# 赋予执行权限
chmod +x .github/workflows/scripts/*.sh
```

### 问题 2: Release 创建但没有文件

检查工作流日志中的 "Upload release packages" 步骤。

**可能需要**:
- 检查 zip 文件是否正确创建
- 验证 GitHub Token 有写入权限
- 确认 .genreleases/ 目录中有 zip 文件

### 问题 3: init 命令下载失败

**可能原因**:
- Release 还没准备好：等待几分钟
- 网络问题：检查网络连接
- 文件格式错误：验证 zip 文件内容

**调试步骤**:
```bash
# 手动下载测试
curl -LO https://github.com/yourusername/slash-command-kit/releases/download/v0.1.0/sckit-cursor-0.1.0.zip

# 验证内容
unzip -l sckit-cursor-0.1.0.zip

# 检查文件完整性
unzip -t sckit-cursor-0.1.0.zip
```

### 问题 4: 安装失败

**可能原因**:
- Python 版本不兼容：需要 >= 3.8
- uv 版本过旧：更新 uv
- 网络连接问题

**解决方案**:
```bash
# 检查 Python 版本
python --version

# 更新 uv
pip install --upgrade uv

# 使用详细输出查看错误
uv tool install sckit-cli --from git+https://... --verbose
```

---

## 📝 后续版本发布清单

创建新版本时使用此清单：

### 发布前
- [ ] 更新版本号（`__init__.py`, `pyproject.toml`）
- [ ] 更新 CHANGELOG.md
- [ ] 运行所有测试
- [ ] 更新文档
- [ ] 本地测试打包

### 发布
- [ ] 提交所有更改
- [ ] 创建并推送 tag
- [ ] 验证 GitHub Actions 成功
- [ ] 检查 Release 页面

### 发布后
- [ ] 测试安装流程
- [ ] 测试完整 init 流程
- [ ] 在编辑器中测试
- [ ] 更新项目看板/TODO
- [ ] 发布公告

---

## 💡 专业建议

### 1. 语义化版本

遵循 [SemVer](https://semver.org/)：
- **MAJOR.MINOR.PATCH** (如 1.0.0)
- 向后不兼容：增加 MAJOR
- 新功能：增加 MINOR
- Bug 修复：增加 PATCH

**示例**:
- v0.1.0 → v0.1.1 (bug 修复)
- v0.1.0 → v0.2.0 (新功能)
- v0.9.0 → v1.0.0 (稳定版本)

### 2. 变更日志

保持 CHANGELOG.md 更新：
- 使用 [Keep a Changelog](https://keepachangelog.com/) 格式
- 记录每个版本的变更
- 分类：Added, Changed, Deprecated, Removed, Fixed, Security

### 3. 测试覆盖

发布前彻底测试：
- 基础功能测试
- 端到端测试
- 跨平台测试（如果可能）
- 边缘案例测试

### 4. 文档同步

确保文档与代码一致：
- README.md
- CHANGELOG.md
- 代码注释
- API 文档

---

## 🎯 快速命令参考

```bash
# === 发布前准备 ===
python test_basic.py                    # 运行测试
bash scripts/test-release-locally.sh    # 本地打包测试

# === 发布 ===
git add .
git commit -m "feat: ready for release"
git tag v0.1.0
git push origin main v0.1.0             # 推送代码和标签

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

## 📚 相关文档

- **任务跟踪**: `tasks.md` - 查看项目进度和任务状态
- **测试指南**: `TESTING.md` - 详细的测试流程
- **快速开始**: `quickstart.md` - 快速上手指南
- **技术规格**: `spec.md` - 完整的技术规格说明

---

## ✅ 准备好了吗？

如果您完成了所有检查清单，现在就可以开始发布流程了！

```bash
# 开始吧！
git tag v0.1.0
git push origin v0.1.0
```

**然后坐下来，看着 GitHub Actions 为您创建 Release！** ✨

---

**祝发布顺利！** 🚀🎉

有任何问题，请查阅相关文档或提交 Issue。


