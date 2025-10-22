#!/bin/bash
# T058 & T061-T062: 创建 Release 打包脚本
# 参考 spec-kit 的打包流程，从单份 commands/ 源文件生成两种编辑器的 zip 包

set -e

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "❌ 错误: 需要提供版本号"
    echo "用法: $0 v0.1.0"
    exit 1
fi

# 移除 'v' 前缀（如果有）
VERSION_NUM=${VERSION#v}

echo "📦 创建 sckit-cli Release 包: $VERSION_NUM"
echo ""

# 创建临时目录
RELEASE_DIR=".genreleases"
rm -rf "$RELEASE_DIR"
mkdir -p "$RELEASE_DIR"

# 检查 commands 目录
if [ ! -d "commands" ]; then
    echo "❌ 错误: commands/ 目录不存在"
    exit 1
fi

# 统计文件数
FILE_COUNT=$(find commands -name "*.md" | wc -l)
echo "📄 找到 $FILE_COUNT 个提示词文件"
echo ""

# ============================================================================
# T061: 打包 Cursor 版本
# ============================================================================

echo "🔨 打包 Cursor 模板..."

CURSOR_DIR="$RELEASE_DIR/cursor-package"
mkdir -p "$CURSOR_DIR/.cursor/commands"

# 复制所有 markdown 文件到 .cursor/commands/
cp commands/*.md "$CURSOR_DIR/.cursor/commands/" 2>/dev/null || {
    echo "❌ 错误: 无法复制文件到 Cursor 包"
    exit 1
}

# 创建 zip 包
cd "$CURSOR_DIR"
zip -r "../sckit-cursor-${VERSION_NUM}.zip" . > /dev/null
cd ../..

CURSOR_SIZE=$(du -h "$RELEASE_DIR/sckit-cursor-${VERSION_NUM}.zip" | cut -f1)
echo "   ✅ sckit-cursor-${VERSION_NUM}.zip ($CURSOR_SIZE)"

# ============================================================================
# T062: 打包 Claude 版本
# ============================================================================

echo "🔨 打包 Claude 模板..."

CLAUDE_DIR="$RELEASE_DIR/claude-package"
mkdir -p "$CLAUDE_DIR/.claude/commands"

# 复制所有 markdown 文件到 .claude/commands/
cp commands/*.md "$CLAUDE_DIR/.claude/commands/" 2>/dev/null || {
    echo "❌ 错误: 无法复制文件到 Claude 包"
    exit 1
}

# 创建 zip 包
cd "$CLAUDE_DIR"
zip -r "../sckit-claude-${VERSION_NUM}.zip" . > /dev/null
cd ../..

CLAUDE_SIZE=$(du -h "$RELEASE_DIR/sckit-claude-${VERSION_NUM}.zip" | cut -f1)
echo "   ✅ sckit-claude-${VERSION_NUM}.zip ($CLAUDE_SIZE)"

# ============================================================================
# 汇总信息
# ============================================================================

echo ""
echo "✨ Release 包创建完成！"
echo ""
echo "📦 生成的文件:"
ls -lh "$RELEASE_DIR"/*.zip | awk '{print "   - " $9 " (" $5 ")"}'
echo ""
echo "🎯 下一步: 运行 create-github-release.sh 上传到 GitHub"

