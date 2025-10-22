#!/bin/bash
# T059 & T063: 创建 GitHub Release 并上传资源文件

set -e

VERSION=$1
GITHUB_TOKEN=$2

if [ -z "$VERSION" ]; then
    echo "❌ 错误: 需要提供版本号"
    echo "用法: $0 v0.1.0 [GITHUB_TOKEN]"
    exit 1
fi

# 如果没有提供 token，尝试从环境变量获取
if [ -z "$GITHUB_TOKEN" ]; then
    GITHUB_TOKEN="${GITHUB_TOKEN:-}"
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 错误: 需要 GITHUB_TOKEN"
    echo "设置环境变量: export GITHUB_TOKEN=your_token"
    exit 1
fi

echo "🚀 创建 GitHub Release: $VERSION"
echo ""

# 检查 Release 包是否存在
RELEASE_DIR=".genreleases"
if [ ! -d "$RELEASE_DIR" ]; then
    echo "❌ 错误: $RELEASE_DIR 目录不存在"
    echo "请先运行 create-release-packages.sh"
    exit 1
fi

CURSOR_ZIP="$RELEASE_DIR/sckit-cursor-${VERSION#v}.zip"
CLAUDE_ZIP="$RELEASE_DIR/sckit-claude-${VERSION#v}.zip"

if [ ! -f "$CURSOR_ZIP" ] || [ ! -f "$CLAUDE_ZIP" ]; then
    echo "❌ 错误: Release 包不存在"
    echo "请先运行 create-release-packages.sh"
    exit 1
fi

# 获取仓库信息（从 git remote）
REPO_URL=$(git config --get remote.origin.url)
if [[ $REPO_URL == git@github.com:* ]]; then
    # SSH URL: git@github.com:user/repo.git
    REPO_FULL=$(echo "$REPO_URL" | sed -e 's/git@github.com://' -e 's/\.git$//')
elif [[ $REPO_URL == https://github.com/* ]]; then
    # HTTPS URL: https://github.com/user/repo.git
    REPO_FULL=$(echo "$REPO_URL" | sed -e 's|https://github.com/||' -e 's/\.git$//')
else
    echo "❌ 错误: 无法识别的 Git remote URL: $REPO_URL"
    exit 1
fi

echo "📂 仓库: $REPO_FULL"
echo "🏷️  版本: $VERSION"
echo ""

# 生成 Release 说明
RELEASE_NOTES="# sckit-cli $VERSION

## 🎉 轻量级提示词管理工具

从 GitHub 部署 AI 编辑器（Cursor/Claude Code）的提示词模板到项目中。

## 📦 安装

\`\`\`bash
uv tool install sckit-cli --from git+https://github.com/$REPO_FULL.git
\`\`\`

## 🚀 快速开始

\`\`\`bash
# 创建新项目并初始化提示词
sckit init my-project

# 在当前目录初始化
sckit init .

# 强制更新
sckit init . --force
\`\`\`

## 📄 模板文件

本 Release 包含两种编辑器的模板包：
- \`sckit-cursor-${VERSION#v}.zip\` - 适用于 Cursor 编辑器
- \`sckit-claude-${VERSION#v}.zip\` - 适用于 Claude Code 编辑器

CLI 工具会自动下载对应的模板包并部署到项目中。

## 📖 文档

- [README](https://github.com/$REPO_FULL/blob/main/README.md)
- [测试指南](https://github.com/$REPO_FULL/blob/main/TESTING.md)
- [下一步计划](https://github.com/$REPO_FULL/blob/main/NEXT_STEPS.md)

## 🐛 问题反馈

https://github.com/$REPO_FULL/issues
"

# 使用 GitHub API 创建 Release
echo "📤 创建 GitHub Release..."

API_URL="https://api.github.com/repos/$REPO_FULL/releases"

# 创建 Release
RELEASE_RESPONSE=$(curl -s -X POST "$API_URL" \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    -d @- <<EOF
{
  "tag_name": "$VERSION",
  "name": "Release $VERSION",
  "body": $(echo "$RELEASE_NOTES" | jq -Rs .),
  "draft": false,
  "prerelease": false
}
EOF
)

# 检查是否成功
RELEASE_ID=$(echo "$RELEASE_RESPONSE" | jq -r '.id')
if [ "$RELEASE_ID" = "null" ] || [ -z "$RELEASE_ID" ]; then
    echo "❌ 错误: 创建 Release 失败"
    echo "$RELEASE_RESPONSE" | jq -r '.message'
    exit 1
fi

RELEASE_URL=$(echo "$RELEASE_RESPONSE" | jq -r '.html_url')
UPLOAD_URL=$(echo "$RELEASE_RESPONSE" | jq -r '.upload_url' | sed 's/{?name,label}//')

echo "   ✅ Release 创建成功: $RELEASE_URL"
echo ""

# 上传 Cursor 模板包
echo "📤 上传 Cursor 模板包..."
CURSOR_NAME=$(basename "$CURSOR_ZIP")
curl -s -X POST "$UPLOAD_URL?name=$CURSOR_NAME" \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Content-Type: application/zip" \
    --data-binary "@$CURSOR_ZIP" > /dev/null

echo "   ✅ $CURSOR_NAME 上传完成"

# 上传 Claude 模板包
echo "📤 上传 Claude 模板包..."
CLAUDE_NAME=$(basename "$CLAUDE_ZIP")
curl -s -X POST "$UPLOAD_URL?name=$CLAUDE_NAME" \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Content-Type: application/zip" \
    --data-binary "@$CLAUDE_ZIP" > /dev/null

echo "   ✅ $CLAUDE_NAME 上传完成"

echo ""
echo "✨ GitHub Release 创建完成！"
echo ""
echo "🌐 Release URL: $RELEASE_URL"
echo ""
echo "🎯 下一步:"
echo "   1. 访问 Release 页面验证文件"
echo "   2. 测试安装: uv tool install sckit-cli --from git+https://github.com/$REPO_FULL.git"
echo "   3. 测试 init: sckit init test-project"

