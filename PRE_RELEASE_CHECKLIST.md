# 🚀 发布前检查清单

## 必须完成的 3 件事

### ✅ 第 1 步：更新 GitHub 用户名

**需要替换的文件**（将 `yourusername` 改为您的 GitHub 用户名）：

1. **README.md**
   ```bash
   # 查找并替换
   - uv tool install sckit-cli --from git+https://github.com/yourusername/slash-command-kit.git
   # 改为：
   - uv tool install sckit-cli --from git+https://github.com/您的用户名/slash-command-kit.git
   ```

2. **pyproject.toml**
   ```toml
   [project.urls]
   Homepage = "https://github.com/yourusername/slash-command-kit"
   # 改为您的用户名
   ```

3. **src/sckit_cli/__init__.py**（第 105 行）
   ```python
   GITHUB_OWNER: str = os.getenv("SCKIT_REPO_OWNER", "yourusername")
   # 改为您的用户名
   ```

4. **可选更新**：pyproject.toml 中的作者信息
   ```toml
   [project]
   authors = [
       {name = "Your Name", email = "your.email@example.com"}
   ]
   ```

**快速替换命令**（Linux/Mac/Git Bash）：
```bash
# 自动替换所有 yourusername（请先替换 YOUR_GITHUB_USERNAME）
find . -type f \( -name "*.md" -o -name "*.toml" -o -name "*.py" \) \
  -not -path "./.git/*" \
  -not -path "./spec-kit/*" \
  -exec sed -i 's/yourusername/YOUR_GITHUB_USERNAME/g' {} +
```

---

### ✅ 第 2 步：运行测试

```bash
# 确保基础功能正常
python -m sckit_cli --version
python -m sckit_cli --help
```

预期输出：
```
sckit version 0.1.0
```

---

### ✅ 第 3 步：提交并创建 Release

```bash
# 1. 查看更改
git status

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "feat: ready for v0.1.0 release

- Implemented MVP core functionality
- Added CI/CD automation  
- Complete documentation
- Ready for production use
"

# 4. 推送到 GitHub
git push origin main

# 5. 创建并推送标签（这会触发自动发布！）
git tag v0.1.0
git push origin v0.1.0
```

---

## 🎊 发布后验证（1-2 分钟）

### 1. 查看 GitHub Actions

访问：`https://github.com/您的用户名/slash-command-kit/actions`

应该看到 "Release" 工作流正在运行。

### 2. 查看 Release 页面

访问：`https://github.com/您的用户名/slash-command-kit/releases`

应该看到：
- ✅ Release v0.1.0
- ✅ sckit-cursor-0.1.0.zip
- ✅ sckit-claude-0.1.0.zip

### 3. 端到端测试

```bash
# 安装 CLI
uv tool install sckit-cli --from git+https://github.com/您的用户名/slash-command-kit.git

# 验证
sckit --version

# 测试完整流程（这会下载 Release 中的模板！）
sckit init test-project

# 验证文件
ls test-project/.cursor/commands/
# 或
ls test-project/.claude/commands/
```

---

## 🎯 快速命令参考

```bash
# === 更新后测试 ===
python -m sckit_cli --version

# === 发布 ===
git add .
git commit -m "feat: ready for v0.1.0 release"
git push origin main
git tag v0.1.0
git push origin v0.1.0

# === 等待 1-2 分钟后测试 ===
uv tool install sckit-cli --from git+https://github.com/您的用户名/slash-command-kit.git
sckit init test-project
```

---

## ❓ 常见问题

**Q: 如何知道我的 GitHub 用户名？**
A: 访问 https://github.com，右上角头像 → Settings，URL 中的就是您的用户名。

**Q: GitHub Actions 失败了怎么办？**
A: 查看 Actions 标签页的详细日志，通常是脚本权限或文件路径问题。

**Q: init 命令找不到 Release 怎么办？**
A: 等待几分钟让 Release 完成，然后重试。

---

## 📚 详细文档

需要更详细的说明？查看：
- `specs/001-prompt-management-cli/READY_TO_RELEASE.md` - 完整发布指南
- `specs/001-prompt-management-cli/TESTING.md` - 测试指南
- `specs/001-prompt-management-cli/RELEASE_GUIDE.md` - Release 流程

---

**准备好了就开始吧！** 🚀

完成第 1-3 步后，您就有了一个完整可用的 CLI 工具！

