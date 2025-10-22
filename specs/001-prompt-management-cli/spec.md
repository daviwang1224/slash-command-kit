# Feature Specification: 轻量级提示词管理CLI工具

**Feature Branch**: `001-prompt-management-cli`  
**Created**: 2025-10-22  
**Status**: Draft  
**Input**: 用户描述: "背景：您作为独立开发者，有很多提示词文档分散在电脑各处，希望能够集中管理并方便地在 Cursor 和 Claude Code 中使用。核心目标：创建一个轻量级的提示词管理工具（slash-command-kit），灵感来自 spec-kit，但更加简单专注。"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 从GitHub安装CLI工具 (Priority: P1)

作为独立开发者，我需要能够从GitHub仓库直接安装CLI工具，这样我可以快速开始使用提示词管理功能，而不需要复杂的安装流程。

**Why this priority**: 这是使用整个工具的前提条件，没有安装就无法使用任何功能。这是最基础的MVP功能。

**Independent Test**: 可以通过在全新的环境中执行 `uv tool install` 命令来独立测试，验证工具是否成功安装并可以通过 `sckit --version` 或 `sckit --help` 命令访问。

**Acceptance Scenarios**:

1. **Given** 用户已安装uv包管理器, **When** 用户执行 `uv tool install sckit-cli --from git+https://github.com/用户名/slash-command-kit.git`, **Then** CLI工具成功安装并可通过 `sckit` 命令访问
2. **Given** 用户已安装旧版本的sckit-cli, **When** 用户执行 `uv tool install sckit-cli --force --from git+...`, **Then** 工具更新到最新版本，旧版本被替换
3. **Given** 用户网络正常, **When** 用户执行安装命令, **Then** 在30秒内完成安装过程
4. **Given** CLI工具安装完成, **When** 用户执行 `sckit --version`, **Then** 显示工具版本号但不显示模板版本（模板通过Release独立管理）

---

### User Story 2 - 在新项目中初始化提示词 (Priority: P1)

作为独立开发者，当我创建一个新项目时，我希望能够通过一个简单的命令在新目录中初始化提示词集合，选择我使用的AI编辑器（Cursor或Claude Code），然后自动完成所有提示词文件的复制。

**Why this priority**: 这是工具的核心价值所在，是最常用的使用场景。能够独立提供完整的用户价值。

**Independent Test**: 可以通过在空目录中执行 `sckit init my-project` 来独立测试，验证是否创建了新目录、是否提供了交互式选择、以及是否正确复制了提示词文件到对应位置。

**Acceptance Scenarios**:

1. **Given** 用户在任意目录下, **When** 用户执行 `sckit init my-new-project`, **Then** 创建名为 `my-new-project` 的新目录
2. **Given** 新目录已创建, **When** 用户看到"选择AI编辑器"的提示, **Then** 用户可以通过上下箭头键选择 "Cursor" 或 "Claude Code"
3. **Given** 用户选择了Cursor, **When** 确认选择后, **Then** 工具下载最新的 `sckit-cursor-*.zip` 模板并复制到 `my-new-project/.cursor/commands/` 目录
4. **Given** 用户选择了Claude Code, **When** 确认选择后, **Then** 工具下载最新的 `sckit-claude-*.zip` 模板并复制到 `my-new-project/.claude/commands/` 目录
5. **Given** 初始化完成, **When** 用户查看目标目录, **Then** 显示成功消息，包含已复制的提示词数量、版本号和位置
6. **Given** 下载过程中, **When** 网络正常, **Then** 显示下载进度指示

---

### User Story 3 - 在现有项目中初始化/更新提示词 (Priority: P2)

作为独立开发者，当我在已存在的项目目录中工作时，我希望能够在当前目录直接初始化或更新提示词，无需创建新目录。

**Why this priority**: 这是常见但略次于新项目初始化的场景。用户可能需要在已有项目中添加提示词支持，或更新已安装的提示词到最新版本。

**Independent Test**: 可以通过在已有项目目录中执行 `sckit init .` 来独立测试，验证是否在当前目录创建了对应的 `.cursor/commands/` 或 `.claude/commands/` 目录并复制了文件。

**Acceptance Scenarios**:

1. **Given** 用户在已存在的项目目录中, **When** 用户执行 `sckit init .`, **Then** 提示用户选择AI编辑器而不创建新目录
2. **Given** 用户选择了编辑器, **When** 确认后, **Then** 下载最新模板并在当前目录创建对应的 `.cursor/commands/` 或 `.claude/commands/` 目录
3. **Given** 目标目录已存在提示词文件, **When** 执行初始化且未使用 `--force` 标志, **Then** 询问用户是否覆盖或跳过已存在的文件
4. **Given** 用户执行 `sckit init . --force`, **When** 遇到已存在的文件, **Then** 直接覆盖而不询问，适合更新提示词或自动化场景
5. **Given** 初始化完成, **When** 用户打开Cursor或Claude Code, **Then** 可以通过斜杠命令访问已安装的提示词
6. **Given** 当前目录为非空, **When** 执行 `sckit init .`, **Then** 显示提示消息说明将在现有项目中添加或更新文件

---

### Edge Cases

- **权限问题**: 用户没有写入权限时，显示清晰错误消息并建议解决方案
- **网络错误**: 无法连接网络或下载资源时，提示检查网络连接或稍后重试；API限流时显示重置时间和认证建议
- **资源不可用**: 仓库无Release或模板包损坏时，提示检查仓库状态或重试
- **磁盘空间不足**: 复制前检查空间并显示所需大小
- **目录结构冲突**: 目标路径存在同名文件（非目录）时，提示用户确认删除
- **中途取消**: Ctrl+C取消操作时清理临时文件并优雅退出
- **特殊字符处理**: 项目名包含非法字符时提示使用有效名称
- **符号链接**: 正确解析符号链接并复制到实际位置
- **并发操作**: 多终端同时执行init时避免冲突

## Requirements *(mandatory)*

### Functional Requirements

#### CLI工具
- **FR-001**: 系统必须提供名为 `sckit` 的命令行工具，可通过 `uv tool install sckit-cli --from git+https://github.com/用户名/slash-command-kit.git` 命令安装
- **FR-002**: 系统必须支持通过 `uv tool install sckit-cli --force --from git+...` 命令更新CLI工具到最新版本

#### 模板分发
- **FR-003**: 系统必须通过GitHub Release分发模板文件，每个Release包含不同编辑器的压缩包（命名格式：`sckit-{编辑器名}-{版本号}.zip`）
- **FR-004**: 系统必须在执行init命令时自动获取并下载最新模板
- **FR-005**: 系统必须在下载过程中显示进度指示
- **FR-006**: 系统必须在操作完成后自动删除临时文件

#### 初始化命令
- **FR-007**: 系统必须提供 `sckit init <项目名>` 命令，在新目录中初始化提示词
- **FR-008**: 系统必须提供 `sckit init .` 命令，在当前目录中初始化提示词
- **FR-009**: 系统必须支持 `--force` 标志，跳过覆盖确认直接替换文件（用于更新场景）
- **FR-010**: 系统必须提供交互式界面让用户选择 "Cursor" 或 "Claude Code"
- **FR-011**: 系统必须将模板文件复制到对应的编辑器配置目录（`.cursor/commands/` 或 `.claude/commands/`）

#### 用户反馈
- **FR-012**: 系统必须在操作完成后显示成功消息，包含文件数量、版本号和位置
- **FR-013**: 系统必须在文件已存在时（未使用 `--force`）询问用户是否覆盖或跳过
- **FR-014**: 系统必须在遇到错误时显示清晰的错误消息和解决建议

#### 数据完整性
- **FR-019**: 系统必须保持提示词文件的原始结构和格式，包括文件名、扩展名和内容
- **FR-020**: 系统必须验证下载的zip文件完整性，如发现损坏应删除临时文件并提示用户重试
- **FR-021**: GitHub仓库必须通过CI/CD流程在每次Release时自动打包模板文件为zip格式

#### 跨平台支持
- **FR-022**: 系统必须支持Windows、macOS和Linux操作系统
- **FR-023**: 系统必须允许用户通过Ctrl+C或等效快捷键随时取消操作，并清理临时文件后优雅退出

### Key Entities

- **CLI工具(sckit-cli)**: 命令行工具，提供init命令，是用户与提示词库
交互的主要接口。只包含执行逻辑（Python代码），不包含模板文件
- **模板压缩包**: 通过GitHub Release分发的zip文件（命名格式：`sckit-{编辑器名}-{版本号}.zip`），包含特定编辑器的所有提示词文件
- **提示词文件**: 存储在模板包中的文本文件，包含可在AI编辑器中使用的slash命令定义
- **源仓库(slash-command-kit)**: GitHub中央仓库，包含CLI工具源代码和提示词文件，通过CI/CD自动构建Release
- **目标项目**: 用户希望部署提示词的项目目录
- **编辑器配置目录**: `.cursor/commands/` 或 `.claude/commands/`，AI编辑器加载自定义命令的标准位置

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 用户能够在5分钟内完成从安装CLI工具到在新项目中可用提示词的完整流程
- **SC-002**: 初始化命令在标准网络条件下能够在10秒内完成提示词文件的复制
- **SC-003**: 用户在第一次使用时能够无需查看文档就理解如何选择编辑器和完成初始化（通过清晰的交互式提示实现）
- **SC-004**: 工具在遇到错误时100%的情况下提供明确的错误消息和建议操作，而不是显示技术性堆栈跟踪
- **SC-005**: 用户可以在单个工作站上管理10个以上项目的提示词集合，每个项目独立初始化
- **SC-006**: 提示词文件在复制后能够被Cursor和Claude Code立即识别并可用，无需手动配置或重启编辑器
- **SC-007**: 相比手动复制提示词文件，使用CLI工具能够减少90%的操作步骤和时间
- **SC-008**: 工具支持三大主流操作系统（Windows、macOS、Linux），在每个平台上表现一致

## Assumptions

- 用户已安装Python 3.8或更高版本（uv工具的依赖）
- 用户已安装uv包管理器
- 用户有稳定的互联网连接来访问GitHub API和下载Release资源
- GitHub API和CDN服务可用且响应速度合理（通常在10秒内完成下载）
- 用户使用的是Cursor或Claude Code编辑器（当前版本不支持其他编辑器）
- 提示词文件格式遵循Cursor和Claude Code的slash命令规范（通常是Markdown格式）
- 用户对目标目录和系统临时目录有足够的读写权限
- 用户系统临时目录有足够空间存储下载的模板压缩包（通常小于5MB）
- GitHub仓库保持公开访问，或用户已配置必要的认证凭据（通过环境变量GITHUB_TOKEN）
- 源仓库的Release assets命名遵循约定：`sckit-{编辑器名}-{版本号}.zip`
- 每个Release都包含完整且有效的模板压缩包，已通过CI/CD验证

## Dependencies

- **外部依赖**: uv包管理器必须已安装在用户系统上
- **运行时依赖**: 
  - Python标准库（os, sys, pathlib, shutil, zipfile, tempfile等）用于文件操作
  - `httpx` 库用于HTTP请求和下载（支持进度跟踪）
  - `typer` 库用于CLI框架
  - `rich` 库用于美化终端输出和进度显示
- **网络依赖**: 
  - GitHub API (`api.github.com`) 用于获取Release信息
  - GitHub CDN用于下载Release assets（模板压缩包）
- **CI/CD依赖**: GitHub Actions用于自动构建和发布Release，打包模板文件

## Out of Scope

- 不提供提示词的在线编辑或管理界面（保持简单，只做复制分发）
- 不支持从多个来源仓库安装提示词（只支持单一的slash-command-kit仓库）
- 不包含constitution、plan、tasks等spec-kit的复杂工作流功能
- 不提供提示词的版本控制或回滚功能（用户可以通过Git手动管理）
- 不支持除Cursor和Claude Code之外的编辑器（至少在初始版本）
- 不提供提示词的搜索、过滤或选择性安装功能（安装时复制全部提示词）
- 不处理提示词内容的验证或语法检查（假设源仓库的文件都是有效的）
- 不提供用户认证或权限管理（假设仓库是公开的或用户已配置Git凭据）
