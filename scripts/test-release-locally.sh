#!/bin/bash
# 本地测试 Release 打包流程（不创建真实 Release）

set -e

echo "🧪 本地测试 Release 打包流程"
echo "================================"
echo ""

# 检查是否在项目根目录
if [ ! -f "pyproject.toml" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 使用测试版本号
TEST_VERSION="v0.1.0-test"
echo "📦 测试版本: $TEST_VERSION"
echo ""

# 运行打包脚本
echo "1️⃣ 运行打包脚本..."
bash .github/workflows/scripts/create-release-packages.sh "$TEST_VERSION"

echo ""
echo "================================"
echo "✅ 本地测试完成！"
echo ""
echo "📋 生成的文件:"
ls -lh .genreleases/*.zip 2>/dev/null || echo "   未找到生成的文件"
echo ""
echo "🔍 验证包内容:"
echo ""

VERSION_NUM=${TEST_VERSION#v}
CURSOR_ZIP=".genreleases/sckit-cursor-${VERSION_NUM}.zip"
CLAUDE_ZIP=".genreleases/sckit-claude-${VERSION_NUM}.zip"

if [ -f "$CURSOR_ZIP" ]; then
    echo "📦 Cursor 包内容:"
    unzip -l "$CURSOR_ZIP"
    echo ""
fi

if [ -f "$CLAUDE_ZIP" ]; then
    echo "📦 Claude 包内容:"
    unzip -l "$CLAUDE_ZIP"
    echo ""
fi

echo "🎯 下一步:"
echo "   1. 如果测试通过，可以创建真实的 Git tag"
echo "   2. 运行: git tag v0.1.0"
echo "   3. 推送: git push origin v0.1.0"
echo "   4. GitHub Actions 会自动创建 Release"
echo ""
echo "💡 提示: 记得先提交所有更改再创建 tag"

