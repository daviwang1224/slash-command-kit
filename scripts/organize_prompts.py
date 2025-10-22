# -*- coding: utf-8 -*-
import os
import sys

# 设置编码
sys.stdout.reconfigure(encoding='utf-8')

# 文件映射：原文件名 -> (新文件名, 描述)
FILE_MAPPING = {
    '代码鼓励师（猫系女友版）.md': ('sckit.code-cheerleader.md', '代码鼓励师 - 温柔的代码审查与建议（猫系女友版）'),
    '代码审判官.md': ('sckit.code-judge.md', '代码审判官 - 严格的代码审查专家，全方位代码质量评估'),
    '规格驱动开发专家.md': ('sckit.spec-driven.md', '规格驱动开发专家 - 指导基于规格的软件开发流程'),
    '国学大师（傅佩荣版）.md': ('sckit.chinese-classics.md', '国学大师 - 傅佩荣版中华传统文化专家'),
    '接口设计大师.md': ('sckit.api-designer.md', '接口设计大师 - 专业的API接口设计与评审'),
    '精辟怪提示词.md': ('sckit.insight.md', '精辟怪 - 提供独特深刻的见解和分析'),
    '开发平台架构师.md': ('sckit.platform-architect.md', '开发平台架构师 - 设计企业级开发平台架构'),
    '开源组件扫描与分析.md': ('sckit.oss-scanner.md', '开源组件扫描与分析 - 识别和评估开源组件'),
    '提示词分析师.md': ('sckit.prompt-analyzer.md', '提示词分析师 - 分析和优化提示词质量'),
    '文章总结大师提示词.md': ('sckit.article-summary.md', '文章总结大师 - 智能文章摘要与提炼'),
    '需求暴君.md': ('sckit.requirement-tyrant.md', '需求暴君 - PRD终极审判者，严格的需求评审'),
    '需求评审大师.md': ('sckit.requirement-review.md', '需求评审大师 - 专业的产品需求评审与建议'),
    '学习规划大师.md': ('sckit.learning-planner.md', '学习规划大师 - 制定个性化学习路径与计划'),
    '研发主管工作总结助手.md': ('sckit.rd-work-summary.md', '研发主管工作总结助手 - 协助撰写研发管理工作总结'),
    '研发主管AI助理.md': ('sckit.rd-assistant.md', '研发主管AI助理 - 研发管理决策支持与建议'),
    '用户故事助手提示词.md': ('sckit.user-story.md', '用户故事助手 - 编写高质量用户故事'),
    '员工半年工作总结助手.md': ('sckit.work-summary.md', '员工工作总结助手 - 协助撰写半年工作总结'),
    'AI前沿资讯与知识专家.md': ('sckit.ai-news.md', 'AI前沿资讯与知识专家 - 提供最新AI资讯和学习资源'),
    'IPD教练.md': ('sckit.ipd-coach.md', 'IPD教练 - 集成产品开发体系指导与实施'),
    'MOM产品架构师.md': ('sckit.mom-architect.md', 'MOM产品架构师 - 制造运营管理系统架构设计'),
    # 英文文件添加 sckit. 前缀
    'architect-review.md': ('sckit.architect-review.md', '架构评审 - 系统架构设计评审与建议'),
    'code-reviewer.md': ('sckit.code-reviewer.md', '代码审查 - 专业代码审查与质量评估'),
    'docs-architect.md': ('sckit.docs-architect.md', '文档架构师 - 设计和组织项目文档结构'),
    'git-committer.md': ('sckit.git-committer.md', 'Git提交助手 - 生成规范的Git提交信息'),
    'java-pro.md': ('sckit.java-pro.md', 'Java专家 - Java开发最佳实践与问题解决'),
    'mermaid-expert.md': ('sckit.mermaid-expert.md', 'Mermaid专家 - 创建专业的Mermaid图表'),
    'mom-architect.md': ('sckit.mom-arch.md', 'MOM架构 - MOM系统架构设计'),
    'prompt-engineer.md': ('sckit.prompt-engineer.md', '提示词工程师 - 高级提示词技术与LLM优化'),
    'promptExport.md': ('sckit.prompt-export.md', '提示词导出 - 导出和管理提示词'),
    'spec-refactor.md': ('sckit.spec-refactor.md', '规格重构 - 重构和优化技术规格文档'),
    'sql-pro.md': ('sckit.sql-pro.md', 'SQL专家 - SQL开发与优化最佳实践'),
    'test-automator.md': ('sckit.test-automator.md', '测试自动化 - 自动化测试设计与实现'),
    'tutorial-engineer.md': ('sckit.tutorial-engineer.md', '教程工程师 - 创建高质量技术教程'),
}

def add_yaml_metadata(content, name, description):
    """添加YAML元数据"""
    # 检查是否已有元数据
    if content.strip().startswith('---'):
        print(f"  文件已有 YAML 元数据，跳过")
        return content
    
    yaml = f"""---
name: {name.replace('.md', '').replace('sckit.', '')}
description: {description}
author: wq
version: 1.0.0
---

"""
    return yaml + content

def process_files():
    """处理所有文件"""
    source_dir = 'commands/05_prompt'
    target_dir = 'commands'
    
    processed = 0
    skipped = 0
    
    for src_file, (dst_file, description) in FILE_MAPPING.items():
        src_path = os.path.join(source_dir, src_file)
        dst_path = os.path.join(target_dir, dst_file)
        
        if not os.path.exists(src_path):
            print(f"❌ 源文件不存在: {src_file}")
            skipped += 1
            continue
        
        try:
            print(f"处理: {src_file} -> {dst_file}")
            
            # 读取源文件
            with open(src_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 添加元数据
            new_content = add_yaml_metadata(content, dst_file, description)
            
            # 写入目标文件
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  ✓ 已创建: {dst_file}")
            processed += 1
            
        except Exception as e:
            print(f"  ✗ 处理失败: {e}")
            skipped += 1
    
    print()
    print("="*50)
    print(f"整理完成！")
    print(f"已处理: {processed} 个文件")
    print(f"已跳过: {skipped} 个文件")
    print("="*50)

if __name__ == '__main__':
    process_files()

