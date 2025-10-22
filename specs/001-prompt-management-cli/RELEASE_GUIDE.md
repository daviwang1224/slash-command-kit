# 发布指南

## 🎯 准备发布 v0.1.0

恭喜！您的 CLI 工具已经准备好发布了。按照以下步骤创建第一个 Release。

---

## 📋 发布前检查清单

### 1. 代码检查

- [x] ✅ 所有基础功能已实现并测试通过
- [x] ✅ CI/CD 脚本已创建
- [ ] ⚠️ 更新 README.md 中的 `yourusername` 为您的 GitHub 用户名
- [ ] ⚠️ 更新 LICENSE 中的作者信息
- [ ] ⚠️ 检查 pyproject.toml 中的仓库 URL

### 2. 测试检查

```bash
# 运行基础功能测试
python test_basic.py

# 应该看到：
# ✅ 所有测试通过！
```

### 3. 本地打包测试（可选但推荐）

```bash
# 赋予脚本执行权限（Linux/Mac）
chmod +x scripts/test-release-locally.sh
chmod +x .github/workflows/scripts/*.sh

# 运行本地测试
bash scripts/test-release-locally.sh
```

这会创建测试版本的 zip 包，验证打包流程是否正常。

---

## 🚀 发布步骤

### 步骤 1: 最后的代码清理

```bash
# 1. 更新 README.md（重要！）
# 将所有 yourusername 替换为您的实际 GitHub 用户名
# 例如: sed -i 's/yourusername/your-actual-username/g' README.md

# 2. 更新 pyproject.toml 中的作者信息
# [project.authors]
# name = "Your Name"
# email = "your.email@example.com"

# 3. 更新 Config 中的仓库信息（如果还没改）
# src/sckit_cli/__init__.py 中的 Config 类
```

### 步骤 2: 提交所有更改

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

### 步骤 3: 创建并推送标签

```bash
# 创建版本标签
git tag v0.1.0

# 推送标签到 GitHub（这会触发 GitHub Actions）
git push origin v0.1.0
```

### 步骤 4: 监控 GitHub Actions

1. 访问您的 GitHub 仓库
2. 点击 "Actions" 标签
3. 您应该看到 "Release" 工作流正在运行
4. 等待工作流完成（通常需要 1-2 分钟）

工作流会自动：
- ✅ 打包 Cursor 和 Claude 模板
- ✅ 创建 GitHub Release
- ✅ 上传 zip 文件

### 步骤 5: 验证 Release

1. 访问 `https://github.com/yourusername/slash-command-kit/releases`
2. 您应该看到 "Release v0.1.0"
3. 确认有两个附件：
   - `sckit-cursor-0.1.0.zip`
   - `sckit-claude-0.1.0.zip`
4. 点击下载其中一个 zip，验证内容正确

---

## 🧪 发布后测试

### 测试完整安装流程

```bash
# 1. 安装 CLI 工具（从 GitHub）
uv tool install sckit-cli --from git+https://github.com/yourusername/slash-command-kit.git

# 2. 验证安装
sckit --version
# 应该显示: sckit version 0.1.0

# 3. 测试 init 命令（完整流程！）
mkdir test-sckit
cd test-sckit
sckit init my-test-project

# 4. 按提示选择 Cursor 或 Claude

# 5. 验证结果
ls my-test-project/.cursor/commands/  # 如果选择了 Cursor
# 或
ls my-test-project/.claude/commands/   # 如果选择了 Claude

# 应该看到:
# - example.md
# - README.md
```

### 在 Cursor/Claude Code 中测试

1. 在 Cursor 或 Claude Code 中打开 `my-test-project`
2. 打开聊天窗口
3. 输入 `/` 应该看到可用的斜杠命令
4. 尝试运行 `/example` 命令

---

## 🎉 发布成功！

如果所有测试都通过了，恭喜！您已经成功发布了 v0.1.0。

### 下一步做什么？

#### 1. 分享您的工具

- 在 Twitter/X 上分享
- 在相关社区发布（Reddit, Discord 等）
- 添加到 awesome lists

#### 2. 完善文档

- 添加更多示例提示词到 `commands/`
- 录制使用演示视频
- 创建 GIF 演示

#### 3. 收集反馈

- 监控 GitHub Issues
- 记录用户建议
- 计划下一个版本的功能

#### 4. 持续改进

参考 `NEXT_STEPS.md` 中的路线图：
- 实施边缘案例处理（阶段 7）
- 添加自动化测试（阶段 8）
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

### 问题 2: Release 创建但没有文件

检查工作流日志中的 "Upload release packages" 步骤。

可能需要：
- 检查 zip 文件是否正确创建
- 验证 GitHub Token 有写入权限

### 问题 3: init 命令下载失败

**原因**: Release 可能还没有准备好

**解决**:
- 等待几分钟
- 刷新 Release 页面
- 确认 zip 文件已上传

---

## 📝 版本发布清单模板

创建新版本时使用此清单：

```markdown
## Release v0.1.0 清单

### 发布前
- [ ] 更新版本号（__init__.py, pyproject.toml）
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
```

---

## 💡 专业建议

1. **语义化版本**: 遵循 [SemVer](https://semver.org/)
   - MAJOR.MINOR.PATCH (如 1.0.0)
   - 向后不兼容：增加 MAJOR
   - 新功能：增加 MINOR
   - Bug 修复：增加 PATCH

2. **变更日志**: 保持 CHANGELOG.md 更新
   - 使用 [Keep a Changelog](https://keepachangelog.com/) 格式
   - 记录每个版本的变更

3. **测试覆盖**: 发布前彻底测试
   - 基础功能测试
   - 端到端测试
   - 跨平台测试（如果可能）

4. **文档同步**: 确保文档与代码一致
   - README
   - CHANGELOG
   - API 文档

---

## 🎊 准备好了吗？

如果您完成了所有检查清单，现在就可以开始发布流程了！

```bash
# 开始吧！
git tag v0.1.0
git push origin v0.1.0
```

然后坐下来，看着 GitHub Actions 为您创建 Release！🚀

---

**祝发布顺利！** 🎉

如有问题，请参考 `TESTING.md` 和 `NEXT_STEPS.md`。

