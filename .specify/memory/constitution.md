# slash-command-kit Constitution

## Core Principles

### I. Simplicity First (NON-NEGOTIABLE)

**原则**: 保持工具的简单性和专注性，避免功能蔓延。

- CLI工具只做一件事：提示词模板的管理和部署
- 不引入复杂架构：无微服务、无抽象层、无ORM
- 最小化外部依赖：仅使用必要的轻量级库
- 直接API调用：避免使用重型SDK
- 无本地缓存：临时文件下载后即删，保持系统干净

**违规示例**:
- ❌ 添加提示词编辑器功能
- ❌ 引入数据库存储配置
- ❌ 实现复杂的插件系统

**合规示例**:
- ✅ 添加新的编辑器支持（Cursor、Claude）
- ✅ 改进下载进度显示
- ✅ 优化错误消息

### II. User Experience First

**原则**: 100%提供明确的错误消息和建议操作，绝不显示技术性堆栈跟踪。

- 所有错误必须包含：错误描述 + 建议解决方案
- 使用Rich库美化终端输出
- 提供交互式选择，降低使用门槛
- 支持非交互模式（`--force`, `--editor`）用于自动化
- 进度反馈：下载、解压、复制都有视觉提示

**必须遵守**:
- 捕获所有异常并转换为友好消息
- 网络错误提示检查连接
- 权限错误提示解决方案
- API限流显示重置时间和token建议

### III. Cross-Platform Consistency (NON-NEGOTIABLE)

**原则**: 在Windows、macOS、Linux上表现一致。

- 使用`pathlib.Path`处理所有路径操作
- 避免平台特定的shell命令
- 信号处理（Ctrl+C）跨平台测试
- 文件权限检查适配不同系统
- 临时目录使用标准库`tempfile`

**测试要求**:
- 每个功能必须在三个平台上验证
- CI/CD包含跨平台测试
- 符号链接在Windows上优雅降级

### IV. Test-Driven Development (TDD)

**原则**: 测试先行，确保代码质量。

**三层测试结构**:
1. **Contract Tests** (`tests/contract/`): 验证外部系统契约
   - GitHub API响应schema
   - 编辑器目录结构约定
   
2. **Integration Tests** (`tests/integration/`): 端到端流程
   - 完整的init工作流
   - 更新场景
   - 错误恢复
   
3. **Unit Tests** (`tests/unit/`): 单元逻辑
   - 数据模型验证
   - 工具函数
   - 异常处理

**强制要求**:
- 新功能必须先写测试
- 测试覆盖率 > 80%
- 所有PR必须通过测试

### V. Minimal Dependencies

**原则**: 只引入必要且轻量的依赖。

**当前依赖**:
- `typer` - CLI框架（基于Click，成熟稳定）
- `rich` - 终端UI（美观输出）
- `httpx` - HTTP客户端（现代、进度支持）
- `pytest` - 测试框架（标准）

**新增依赖审批标准**:
1. 是否有标准库替代？
2. 依赖体积是否合理？
3. 是否有长期维护？
4. 是否增加安装复杂度？

**禁止**:
- 重型框架（Django、Flask等）
- 数据库驱动
- GUI库
- 不必要的包装库

## Development Workflow

### Git Workflow

**分支策略**:
- `main`: 稳定版本，每个commit都可发布
- `001-feature-name`: 功能分支，遵循spec-kit命名
- 无`develop`分支（保持简单）

**Commit规范**:
- 使用清晰的commit message
- 一个commit做一件事
- 关联issue/PR号

### Release Process

**版本号**: 遵循语义化版本（Semantic Versioning）

- **MAJOR.MINOR.PATCH** (例如: 0.1.0)
- **MAJOR**: 不兼容的API变更
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复

**Release流程**:
1. 更新`pyproject.toml`版本号
2. 更新`CHANGELOG.md`
3. 创建Git tag（如`v0.1.0`）
4. GitHub Actions自动：
   - 从`commands/`单源打包生成两种目录结构：
     - `sckit-cursor-{version}.zip` (包含`.cursor/commands/*.md`)
     - `sckit-claude-{version}.zip` (包含`.claude/commands/*.md`)
   - 创建GitHub Release
   - 上传zip文件到Release assets

**打包策略** (参考spec-kit单源多目标):
- 源文件：`commands/` 只存一份Markdown模板
- 打包脚本：`.github/workflows/scripts/create-release-packages.sh`
- 内容相同，仅目录结构不同

### Code Review Standards

**PR必须包含**:
- 测试（覆盖新功能）
- 文档更新（README、契约文档等）
- CHANGELOG条目
- Constitution合规性检查

**审查要点**:
- 是否违反简单性原则？
- 是否增加不必要的依赖？
- 错误处理是否友好？
- 跨平台兼容性？

## Quality Gates

### 代码合并前检查

- [ ] 所有测试通过（unit + integration + contract）
- [ ] 代码覆盖率 ≥ 80%
- [ ] 跨平台测试通过（Windows + macOS + Linux）
- [ ] 文档已更新
- [ ] Constitution合规性检查通过
- [ ] 性能基准测试通过（如适用）

### 性能基准

- CLI启动时间 < 100ms
- 安装命令完成 < 30秒
- 模板下载和部署 < 10秒（标准网络）
- 临时文件清理 < 1秒

## Security Requirements

### 输入验证

- 项目名验证（防止路径遍历）
- URL验证（仅HTTPS）
- 文件大小限制（10MB）

### 网络安全

- 仅使用HTTPS连接
- 验证下载文件完整性（基于Content-Length）
- 支持代理配置
- 超时控制防止挂起

### 敏感信息

- 不存储GitHub token（仅从环境变量读取）
- 不记录敏感数据
- 错误消息不泄露路径信息

## Observability

### 日志策略

**当前**:
- 使用Rich终端输出，无文件日志
- 进度信息直接显示
- 错误通过stderr输出

**未来扩展**（如需要）:
- 可选的`--verbose`标志
- 调试模式显示HTTP请求详情
- 但仍不写入日志文件（保持简单）

### 监控指标（可选）

如果未来需要遥测：
- 安装成功率
- 平均下载时间
- 常见错误类型
- 编辑器使用分布

**必须**:
- 用户可选退出
- 不收集个人信息
- 数据匿名化

## Documentation Standards

### 必需文档

1. **README.md**: 项目概述、快速开始、安装指南
2. **docs/**: 详细文档（参考spec-kit结构）
   - `index.md`: 文档首页
   - `installation.md`: 安装指南
   - `quickstart.md`: 快速开始
3. **specs/**: 功能规格和设计文档
4. **CHANGELOG.md**: 版本变更记录
5. **CONTRACT文档**: CLI接口规范、API契约

### 文档更新时机

- 新功能发布前
- API变更时
- 错误修复影响用户行为时
- 依赖版本更新时

## Governance

**Constitution地位**:
- 本Constitution优先级高于所有其他实践
- 任何违反Constitution的代码不得合并
- Constitution修订需要：
  1. 提案和充分讨论
  2. 更新文档
  3. 迁移计划（如适用）

**复杂度必须证明合理性**:
- 任何引入复杂性的变更必须在PR中说明理由
- 必须证明简单方案不可行
- 需在`plan.md`的Complexity Tracking中记录

**本Constitution适用于**:
- 所有代码变更（src/、tests/）
- 文档更新
- CI/CD配置
- 依赖管理

---

**Version**: 1.0.0  
**Ratified**: 2025-10-22  
**Last Amended**: 2025-10-22
