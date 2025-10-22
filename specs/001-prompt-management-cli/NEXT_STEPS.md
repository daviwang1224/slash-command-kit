# 下一步行动计划

## 📊 当前状态

### ✅ 已完成

**阶段 1-4: MVP 核心功能**（42 个任务）
- ✅ 项目设置（8 个任务）
- ✅ 基础设施（11 个任务）
- ✅ 用户故事 1: CLI 安装（8 个任务）
- ✅ 用户故事 2: 新项目初始化（15 个任务）

**基础测试**
- ✅ 所有数据模型测试通过
- ✅ CLI 命令（--version, --help）工作正常
- ✅ 8 项基础功能测试全部通过

### 📋 待完成

**MVP 相关**：
- 🔄 阶段 6: CI/CD & Release 自动化（7 个任务）- **关键！**
- 🔄 用户故事 3: 现有项目更新（大部分已实现）

**非 MVP**：
- ⏸ 测试任务（4 个跳过）
- ⏸ 阶段 7: 边缘案例处理（10 个任务）
- ⏸ 阶段 8: 打磨与优化（15 个任务）

---

## 🎯 推荐路线图

### 路线 A: 快速 MVP（最快看到效果）

**目标**: 尽快创建可用的 CLI 工具

#### 第 1 步: 实施 CI/CD（阶段 6）⭐ **最重要**

为什么要先做这个？
- `sckit init` 命令需要从 GitHub Release 下载模板
- 没有 Release，无法完整测试和使用工具

**任务清单**:

```bash
# T058: 创建打包脚本
mkdir -p .github/workflows/scripts
touch .github/workflows/scripts/create-release-packages.sh
touch .github/workflows/scripts/create-github-release.sh

# T060: 创建 GitHub Actions 工作流
touch .github/workflows/release.yml
```

**实施指南**: 参考 `spec-kit` 项目的 Release 流程

#### 第 2 步: 创建第一个 Release

```bash
# 1. 提交所有更改
git add .
git commit -m "feat: implement MVP - CLI tool with init command"

# 2. 创建标签
git tag v0.1.0

# 3. 推送到 GitHub
git push origin main
git push origin v0.1.0

# 4. GitHub Actions 自动创建 Release 并上传模板
```

#### 第 3 步: 端到端测试

```bash
# 安装 CLI（从 GitHub）
uv tool install sckit-cli --from git+https://github.com/yourusername/slash-command-kit.git

# 测试完整流程
sckit init test-project
cd test-project
ls .cursor/commands/  # 验证文件已部署

# 在 Cursor 中打开项目测试
```

#### 第 4 步: 发布和分享 🎉

- 更新 README.md 替换 `yourusername` 为实际用户名
- 创建 GitHub Release 说明
- 分享给用户使用

**时间估计**: 2-3 小时

---

### 路线 B: 完整实施（更稳健）

如果想要生产就绪的质量：

#### 第 1 步: CI/CD（同路线 A）

#### 第 2 步: 边缘案例处理（阶段 7）

完善错误处理：
- T065-T074: 网络超时、限流、磁盘空间等

#### 第 3 步: 编写自动化测试（阶段 8）

```bash
# 补充测试
mkdir tests/unit tests/integration tests/contract
touch tests/unit/test_editor.py
touch tests/unit/test_release.py
touch tests/integration/test_init_workflow.py
```

#### 第 4 步: 打磨和优化

- 文档完善
- 性能测试
- 跨平台测试
- 代码审查

**时间估计**: 1-2 天

---

## 🚀 立即可做（无需 Release）

### 测试已实现的功能

```bash
# 1. 基础功能测试（已通过）
python test_basic.py

# 2. 命令测试
python -m sckit_cli --version
python -m sckit_cli --help
python -m sckit_cli init --help

# 3. 本地文件复制测试
# 创建测试脚本验证文件复制功能
```

### 创建示例模板

在 `commands/` 目录添加更多有用的提示词：

```bash
# 添加常用提示词
commands/
├── code-review.md       # 代码审查
├── generate-tests.md    # 测试生成
├── refactor.md          # 重构建议
├── document.md          # 文档生成
└── explain.md           # 代码解释
```

### 完善文档

- 补充 README.md 中的示例
- 添加故障排除指南
- 录制演示视频或 GIF

---

## 📝 CI/CD 实施详细步骤

### 1. 创建 Release 打包脚本

**文件**: `.github/workflows/scripts/create-release-packages.sh`

```bash
#!/bin/bash
set -e

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "错误: 需要提供版本号"
    echo "用法: $0 v0.1.0"
    exit 1
fi

# 移除 'v' 前缀
VERSION_NUM=${VERSION#v}

echo "📦 创建 Release 包: $VERSION_NUM"

# 创建临时目录
mkdir -p .genreleases

# 打包 Cursor 版本
echo "🔨 打包 Cursor 模板..."
mkdir -p .genreleases/cursor-package/.cursor/commands
cp commands/*.md .genreleases/cursor-package/.cursor/commands/
cd .genreleases/cursor-package
zip -r ../sckit-cursor-${VERSION_NUM}.zip .
cd ../..

# 打包 Claude 版本
echo "🔨 打包 Claude 模板..."
mkdir -p .genreleases/claude-package/.claude/commands
cp commands/*.md .genreleases/claude-package/.claude/commands/
cd .genreleases/claude-package
zip -r ../sckit-claude-${VERSION_NUM}.zip .
cd ../..

echo "✅ 打包完成!"
ls -lh .genreleases/*.zip
```

### 2. 创建 GitHub Release 脚本

**文件**: `.github/workflows/scripts/create-github-release.sh`

```bash
#!/bin/bash
set -e

VERSION=$1
GITHUB_TOKEN=$2

if [ -z "$VERSION" ] || [ -z "$GITHUB_TOKEN" ]; then
    echo "错误: 缺少参数"
    exit 1
fi

echo "🚀 创建 GitHub Release: $VERSION"

# 使用 GitHub CLI 创建 Release
gh release create "$VERSION" \
    .genreleases/*.zip \
    --title "Release $VERSION" \
    --notes "轻量级提示词管理工具 - 版本 $VERSION"

echo "✅ Release 创建完成!"
```

### 3. 创建 GitHub Actions 工作流

**文件**: `.github/workflows/release.yml`

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    permissions:
      contents: write
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Get version from tag
        id: get_version
        run: echo "VERSION=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT
      
      - name: Create release packages
        run: |
          chmod +x .github/workflows/scripts/create-release-packages.sh
          .github/workflows/scripts/create-release-packages.sh ${{ steps.get_version.outputs.VERSION }}
      
      - name: Create GitHub Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          chmod +x .github/workflows/scripts/create-github-release.sh
          .github/workflows/scripts/create-github-release.sh \
            ${{ steps.get_version.outputs.VERSION }} \
            $GITHUB_TOKEN
```

---

## 🔍 验证清单

发布前检查：

- [ ] README.md 中的 `yourusername` 已替换为实际用户名
- [ ] 所有测试通过（`python test_basic.py`）
- [ ] 命令帮助信息正确（`--help`）
- [ ] LICENSE 文件作者信息已更新
- [ ] CHANGELOG.md 版本信息已更新
- [ ] .gitignore 包含所有必要的忽略项

---

## 💡 建议

### 当前最佳路线

**推荐**: 路线 A（快速 MVP）

**理由**:
1. ✅ 核心功能已实现且测试通过
2. 🎯 只差 CI/CD 就能完整使用
3. ⚡ 用户可以立即获得价值
4. 🔄 后续可以持续改进

### 第一个 Release 的内容

**包含**:
- ✅ CLI 工具（可安装）
- ✅ init 命令（完整功能）
- ✅ 2 个示例模板文件
- ✅ 基础文档

**暂不包含**（可后续添加）:
- 单元测试（可选）
- 边缘案例完整处理
- 性能优化
- 更多模板文件

---

## 🎊 完成后的成就

一旦完成 CI/CD 并创建 Release，你将拥有：

1. ✨ **可工作的 CLI 工具** - 用户可以通过 `uv` 安装
2. 📦 **自动化发布流程** - Git tag 自动创建 Release
3. 🚀 **完整的用户体验** - 从安装到使用一气呵成
4. 📝 **清晰的文档** - README 和 TESTING 指南
5. 🎯 **MVP 就绪** - 可以分享给用户使用

---

## ❓ 遇到问题？

参考以下资源：
- **测试指南**: 查看 `TESTING.md`
- **设计文档**: `specs/001-prompt-management-cli/`
- **参考项目**: `spec-kit` 的 CI/CD 实现

---

**当前建议**: 立即实施 **阶段 6: CI/CD**，创建第一个 Release！

