# 提示词文件整理脚本
# 将 05_prompt 目录中的文件复制到 commands/ 根目录，统一命名和格式

$sourceDir = "commands/05_prompt"
$targetDir = "commands"

# 命名映射表（中文 -> 英文）
$nameMapping = @{
    "代码分析大师.md" = "sckit.code-analyzer.md"
    "代码鼓励师（猫系女友版）.md" = "sckit.code-cheerleader.md"
    "代码审判官.md" = "sckit.code-judge.md"
    "规格驱动开发专家.md" = "sckit.spec-driven.md"
    "国学大师（傅佩荣版）.md" = "sckit.chinese-classics.md"
    "接口设计大师.md" = "sckit.api-designer.md"
    "精辟怪提示词.md" = "sckit.insight.md"
    "开发平台架构师.md" = "sckit.platform-architect.md"
    "开源组件扫描与分析.md" = "sckit.oss-scanner.md"
    "提示词分析师.md" = "sckit.prompt-analyzer.md"
    "文章总结大师提示词.md" = "sckit.article-summary.md"
    "需求暴君.md" = "sckit.requirement-tyrant.md"
    "需求评审大师.md" = "sckit.requirement-review.md"
    "学习规划大师.md" = "sckit.learning-planner.md"
    "研发主管工作总结助手.md" = "sckit.rd-work-summary.md"
    "研发主管AI助理.md" = "sckit.rd-assistant.md"
    "用户故事助手提示词.md" = "sckit.user-story.md"
    "员工半年工作总结助手.md" = "sckit.work-summary.md"
    "AI前沿资讯与知识专家.md" = "sckit.ai-news.md"
    "IPD教练.md" = "sckit.ipd-coach.md"
    "MOM产品架构师.md" = "sckit.mom-architect.md"
    # 英文文件添加 sckit. 前缀
    "architect-review.md" = "sckit.architect-review.md"
    "code-reviewer.md" = "sckit.code-reviewer.md"
    "docs-architect.md" = "sckit.docs-architect.md"
    "git-committer.md" = "sckit.git-committer.md"
    "java-pro.md" = "sckit.java-pro.md"
    "mermaid-expert.md" = "sckit.mermaid-expert.md"
    "mom-architect.md" = "sckit.mom-arch.md"
    "prompt-engineer.md" = "sckit.prompt-engineer.md"
    "promptExport.md" = "sckit.prompt-export.md"
    "spec-refactor.md" = "sckit.spec-refactor.md"
    "sql-pro.md" = "sckit.sql-pro.md"
    "test-automator.md" = "sckit.test-automator.md"
    "tutorial-engineer.md" = "sckit.tutorial-engineer.md"
}

# 描述映射表
$descMapping = @{
    "sckit.code-analyzer.md" = "代码分析大师 - 深度分析代码质量、性能和架构"
    "sckit.code-cheerleader.md" = "代码鼓励师 - 温柔的代码审查与建议（猫系女友版）"
    "sckit.code-judge.md" = "代码审判官 - 严格的代码审查专家，全方位代码质量评估"
    "sckit.spec-driven.md" = "规格驱动开发专家 - 指导基于规格的软件开发流程"
    "sckit.chinese-classics.md" = "国学大师 - 傅佩荣版中华传统文化专家"
    "sckit.api-designer.md" = "接口设计大师 - 专业的API接口设计与评审"
    "sckit.insight.md" = "精辟怪 - 提供独特深刻的见解和分析"
    "sckit.platform-architect.md" = "开发平台架构师 - 设计企业级开发平台架构"
    "sckit.oss-scanner.md" = "开源组件扫描与分析 - 识别和评估开源组件"
    "sckit.prompt-analyzer.md" = "提示词分析师 - 分析和优化提示词质量"
    "sckit.article-summary.md" = "文章总结大师 - 智能文章摘要与提炼"
    "sckit.requirement-tyrant.md" = "需求暴君 - PRD终极审判者，严格的需求评审"
    "sckit.requirement-review.md" = "需求评审大师 - 专业的产品需求评审与建议"
    "sckit.learning-planner.md" = "学习规划大师 - 制定个性化学习路径与计划"
    "sckit.rd-work-summary.md" = "研发主管工作总结助手 - 协助撰写研发管理工作总结"
    "sckit.rd-assistant.md" = "研发主管AI助理 - 研发管理决策支持与建议"
    "sckit.user-story.md" = "用户故事助手 - 编写高质量用户故事"
    "sckit.work-summary.md" = "员工工作总结助手 - 协助撰写半年工作总结"
    "sckit.ai-news.md" = "AI前沿资讯与知识专家 - 提供最新AI资讯和学习资源"
    "sckit.ipd-coach.md" = "IPD教练 - 集成产品开发体系指导与实施"
    "sckit.mom-architect.md" = "MOM产品架构师 - 制造运营管理系统架构设计"
    "sckit.architect-review.md" = "架构评审 - 系统架构设计评审与建议"
    "sckit.code-reviewer.md" = "代码审查 - 专业代码审查与质量评估"
    "sckit.docs-architect.md" = "文档架构师 - 设计和组织项目文档结构"
    "sckit.git-committer.md" = "Git提交助手 - 生成规范的Git提交信息"
    "sckit.java-pro.md" = "Java专家 - Java开发最佳实践与问题解决"
    "sckit.mermaid-expert.md" = "Mermaid专家 - 创建专业的Mermaid图表"
    "sckit.mom-arch.md" = "MOM架构 - MOM系统架构设计"
    "sckit.prompt-engineer.md" = "提示词工程师 - 高级提示词技术与LLM优化"
    "sckit.prompt-export.md" = "提示词导出 - 导出和管理提示词"
    "sckit.spec-refactor.md" = "规格重构 - 重构和优化技术规格文档"
    "sckit.sql-pro.md" = "SQL专家 - SQL开发与优化最佳实践"
    "sckit.test-automator.md" = "测试自动化 - 自动化测试设计与实现"
    "sckit.tutorial-engineer.md" = "教程工程师 - 创建高质量技术教程"
}

function Add-YAMLMetadata {
    param (
        [string]$content,
        [string]$name,
        [string]$description
    )
    
    # 检查是否已有 YAML 元数据
    if ($content -match "^---\s*\n") {
        Write-Host "  文件已有 YAML 元数据，跳过添加"
        return $content
    }
    
    # 添加 YAML 元数据
    $yaml = @"
---
name: $($name.Replace('.md', '').Replace('sckit.', ''))
description: $description
author: wq
version: 1.0.0
---

"@
    
    return $yaml + $content
}

Write-Host "开始整理提示词文件..." -ForegroundColor Green
Write-Host ""

$processedCount = 0
$skippedCount = 0

foreach ($item in $nameMapping.GetEnumerator()) {
    $sourceFile = Join-Path $sourceDir $item.Key
    $targetFile = Join-Path $targetDir $item.Value
    
    if (Test-Path $sourceFile) {
        Write-Host "处理: $($item.Key) -> $($item.Value)" -ForegroundColor Cyan
        
        # 读取原文件内容
        $content = Get-Content -Path $sourceFile -Raw -Encoding UTF8
        
        # 添加 YAML 元数据
        $description = $descMapping[$item.Value]
        if (-not $description) {
            $description = "专业提示词助手"
        }
        
        $newContent = Add-YAMLMetadata -content $content -name $item.Value -description $description
        
        # 写入新文件
        $newContent | Set-Content -Path $targetFile -Encoding UTF8 -NoNewline
        
        Write-Host "  ✓ 已复制到: $targetFile" -ForegroundColor Green
        $processedCount++
    }
    else {
        Write-Host "  ✗ 源文件不存在: $sourceFile" -ForegroundColor Yellow
        $skippedCount++
    }
    
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Green
Write-Host "整理完成!" -ForegroundColor Green
Write-Host "已处理: $processedCount 个文件" -ForegroundColor Cyan
Write-Host "已跳过: $skippedCount 个文件" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "注意: 05_prompt 目录中的原文件未被删除，请手动检查后删除" -ForegroundColor Magenta

