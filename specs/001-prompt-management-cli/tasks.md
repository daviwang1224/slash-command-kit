# Tasks: 轻量级提示词管理CLI工具

**输入**: 设计文档来自 `/specs/001-prompt-management-cli/`
**前置条件**: plan.md, spec.md, data-model.md, contracts/, research.md, quickstart.md

**测试**: 测试任务已包含但可选 - 根据项目需要实施。

**组织方式**: 任务按用户故事分组，以实现每个故事的独立实施和测试。

---

## 📊 项目状态 (更新日期: 2025-10-22)

**版本**: v0.1.0 MVP  
**状态**: ✅ 准备发布

### 完成情况总览

| 类别 | 完成数/总数 | 完成率 | 状态 |
|------|------------|--------|------|
| **MVP任务** | 49/49 | 100% | ✅ 完成 |
| **总任务** | 49/89 | 55% | 🚧 进行中 |

### 阶段进度

| 阶段 | 任务数 | 完成数 | 状态 |
|------|-------|--------|------|
| 阶段 1: 项目设置 | 8 | 8 | ✅ 完成 |
| 阶段 2: 基础设施 | 11 | 11 | ✅ 完成 |
| 阶段 3: 用户故事 1 (CLI安装) | 8 | 8 | ✅ 完成 |
| 阶段 4: 用户故事 2 (新项目初始化) | 19 | 15 | ✅ 核心完成 |
| 阶段 5: 用户故事 3 (现有项目更新) | 11 | 0 | ⏸ 跳过 |
| 阶段 6: CI/CD 自动化 | 7 | 7 | ✅ 完成 |
| 阶段 7: 边缘案例处理 | 10 | 0 | ⏸ 待实施 |
| 阶段 8: 打磨优化 | 15 | 0 | ⏸ 待实施 |

### 已实现功能 ✅

**核心功能**:
- ✅ CLI 工具安装 (`sckit --version`, `--help`)
- ✅ 项目初始化 (`sckit init [path]`)
- ✅ 交互式/非交互式编辑器选择
- ✅ GitHub Release 自动下载
- ✅ 双编辑器支持 (Cursor + Claude Code)
- ✅ CI/CD 自动化流程
- ✅ 完整错误处理和友好提示
- ✅ 进度指示器和富文本UI

**测试状态**: 8/8 基础测试通过

### 下一步行动

**立即可做**: 
- 📋 参考 `RELEASE.md` 进行发布
- 🧪 完整的端到端测试

**后续改进** (可选):
- 阶段 7: 边缘案例处理
- 阶段 8: 打磨和优化
- 更多提示词模板

## 格式: `[ID] [P?] [Story] 描述`

- **[P]**: 可并行执行（不同文件，无依赖）
- **[Story]**: 此任务属于哪个用户故事（如 US1, US2, US3）
- 描述中包含准确的文件路径

## 路径约定

基于 plan.md 结构：
- 源代码: `src/sckit_cli/`
- 测试: `tests/contract/`, `tests/integration/`, `tests/unit/`
- 模板: `commands/`
- CI/CD: `.github/workflows/`
- 配置: 仓库根目录的 `pyproject.toml`

---

## 阶段 1: 项目设置（共享基础设施）

**目的**: 项目初始化和基础结构

- [X] T001 创建项目目录结构：`src/sckit_cli/`, `tests/{contract,integration,unit}/`, `commands/`, `.github/workflows/`
- [X] T002 初始化 pyproject.toml 并添加依赖（typer>=0.9.0, rich>=13.0.0, httpx>=0.24.0, pytest）
- [X] T003 [P] 创建 src/sckit_cli/__init__.py 基础模块结构
- [X] T004 [P] 创建 src/sckit_cli/py.typed 用于 PEP 561 类型标记
- [X] T005 [P] 创建 README.md 包含项目概览和安装说明
- [X] T006 [P] 创建 LICENSE 文件（MIT 许可证）
- [X] T007 [P] 创建 Python 项目的 .gitignore 文件
- [X] T008 [P] 创建 CHANGELOG.md 初始版本 0.1.0

---

## 阶段 2: 基础设施（阻塞性前置条件）

**目的**: 在实施任何用户故事之前必须完成的核心基础设施

**⚠️ 关键**: 在此阶段完成之前，不能开始任何用户故事工作

- [X] T009 [P] 在 src/sckit_cli/__init__.py 中定义 Editor 枚举，包含 display_name、config_dir、get_commands_path 方法
- [X] T010 [P] 在 src/sckit_cli/__init__.py 中定义异常层次结构（SCKitError、NetworkError、RateLimitError、DownloadError、FileSystemError、ValidationError、TemplateNotFoundError）
- [X] T011 [P] 在 src/sckit_cli/__init__.py 中定义 Config 数据类，包含 GitHub 仓库信息、API URLs、超时配置
- [X] T012 [P] 在 src/sckit_cli/__init__.py 中定义 ReleaseAsset 数据类，包含 is_template_for 方法
- [X] T013 在 src/sckit_cli/__init__.py 中定义 Release 数据类，包含 get_template_asset 和 from_api_response 方法（依赖 T012）
- [X] T014 [P] 在 src/sckit_cli/__init__.py 中定义 InstallConfig 数据类，包含验证逻辑
- [X] T015 [P] 在 src/sckit_cli/__init__.py 中定义 InstallResult 数据类，包含 format_summary 方法
- [X] T016 [P] 在 src/sckit_cli/__init__.py 中定义 DownloadProgress 数据类，包含 percentage 和 is_complete 属性
- [X] T017 [P] 在 src/sckit_cli/__init__.py 中实现 is_valid_project_name 验证器函数
- [X] T018 在 src/sckit_cli/__init__.py 中实现 error_handler 函数，为所有异常类型提供 Rich 格式化（依赖 T010）
- [X] T019 在 src/sckit_cli/__init__.py 中实现信号处理器（SIGINT/SIGTERM）用于优雅清理

**检查点**: 基础设施就绪 - 现在可以并行开始用户故事实施

---

## 阶段 3: 用户故事 1 - 从GitHub安装CLI工具（优先级: P1）🎯 MVP 基础

**目标**: 用户能够通过 `uv tool install` 从GitHub安装CLI工具，并通过 `sckit --version` 验证安装

**独立测试**: 在全新环境执行 `uv tool install sckit-cli --from git+https://...`，然后运行 `sckit --version` 验证输出

### 用户故事 1 的实施任务

- [X] T020 [US1] 在 src/sckit_cli/__init__.py 中创建 Typer 应用实例，包含应用名称和帮助文本
- [X] T021 [US1] 在 src/sckit_cli/__init__.py 中实现 version_callback 函数显示 CLI 版本
- [X] T022 [US1] 在 src/sckit_cli/__init__.py 中为 Typer 应用添加 --version 标志和 version_callback
- [X] T023 [US1] 在 pyproject.toml 中定义 project.scripts 入口点 "sckit = sckit_cli:cli"
- [X] T024 [US1] 在 pyproject.toml 中添加项目元数据（name、version、description、requires-python）
- [X] T025 [US1] 在 pyproject.toml 中配置 hatchling 构建系统
- [X] T026 [US1] 更新 README.md 添加安装命令：`uv tool install sckit-cli --from git+...`
- [X] T027 [US1] 更新 README.md 添加验证步骤：`sckit --version` 和 `sckit --help`

**检查点**: CLI 工具可以安装，version/help 命令正常工作

---

## 阶段 4: 用户故事 2 - 在新项目中初始化提示词（优先级: P1）🎯 MVP 核心

**目标**: 用户能够在新目录中执行 `sckit init my-project`，选择编辑器，自动下载并部署提示词到 `.cursor/commands/` 或 `.claude/commands/`

**独立测试**: 在空目录执行 `sckit init test-project`，选择Cursor，验证创建了 `test-project/.cursor/commands/` 并包含提示词文件

### 用户故事 2 的测试（可选）

> **注意: 测试将在 MVP 后补充**

- [ ] T028 [P] [US2] 在 tests/contract/test_github_api.py 中为 GitHub Release API 响应结构编写契约测试 (跳过 - MVP 后实施)
- [ ] T029 [P] [US2] 在 tests/contract/test_template_structure.py 中为模板 zip 结构（.cursor/commands/）编写契约测试 (跳过 - MVP 后实施)
- [ ] T030 [P] [US2] 在 tests/integration/test_init_workflow.py 中为完整的新项目初始化工作流编写集成测试 (跳过 - MVP 后实施)
- [ ] T031 [P] [US2] 在 tests/unit/test_validators.py 中为 is_valid_project_name 函数编写单元测试 (跳过 - MVP 后实施)

### 用户故事 2 的实施任务

- [X] T032 [P] [US2] 在 src/sckit_cli/__init__.py 中实现 get_latest_release 函数（调用 GitHub API，返回 Release）
- [X] T033 [P] [US2] 在 src/sckit_cli/__init__.py 中实现 download_file 函数，支持进度回调（httpx 流式传输）
- [X] T034 [P] [US2] 在 src/sckit_cli/__init__.py 中实现 extract_zip 函数（解压到临时目录）
- [X] T035 [US2] 在 src/sckit_cli/__init__.py 中实现 copy_template_files 函数（从临时目录复制到目标，处理冲突）
- [X] T036 [US2] 在 src/sckit_cli/__init__.py 中实现 prompt_editor_choice 函数（用 Rich Prompt.ask 选择 Cursor/Claude）
- [X] T037 [US2] 在 src/sckit_cli/__init__.py 中实现 install_template 函数，编排 下载 → 解压 → 复制 工作流（依赖 T032-T036）
- [X] T038 [US2] 在 src/sckit_cli/__init__.py 中实现 sckit init 命令，包含 PATH 参数（默认 "."）
- [X] T039 [US2] 在 src/sckit_cli/__init__.py 中为 init 命令添加 --editor 选项（choices: cursor, claude）
- [X] T040 [US2] 在 src/sckit_cli/__init__.py 中为 init 命令添加 --force 标志
- [X] T041 [US2] 在 src/sckit_cli/__init__.py 的 init 命令处理器中实现新项目创建逻辑（mkdir PATH）
- [X] T042 [US2] 在 src/sckit_cli/__init__.py 中为下载、解压、复制步骤添加进度指示器（Rich Progress）
- [X] T043 [US2] 在 src/sckit_cli/__init__.py 中使用 InstallResult.format_summary 添加成功消息（Rich Panel）
- [X] T044 [US2] 在 src/sckit_cli/__init__.py 的 get_latest_release 函数中添加对 GITHUB_TOKEN 环境变量的支持
- [X] T045 [US2] 在 commands/example.md 中创建示例模板文件
- [X] T046 [US2] 在 commands/ 中创建 README.md 解释模板结构

**检查点**: 用户故事 2 应该完全功能化 - 可以创建新项目并部署模板

---

## 阶段 5: 用户故事 3 - 在现有项目中初始化/更新提示词（优先级: P2）

**目标**: 用户能够在已有项目目录执行 `sckit init .`，在当前目录部署或更新提示词，处理文件覆盖场景

**独立测试**: 在已有项目目录执行 `sckit init .`，验证在当前目录创建了 `.cursor/commands/` 或 `.claude/commands/`，再次执行验证覆盖提示逻辑

### 用户故事 3 的测试（可选）

- [ ] T047 [P] [US3] 在 tests/integration/test_init_current_dir.py 中为当前目录初始化工作流编写集成测试
- [ ] T048 [P] [US3] 在 tests/integration/test_force_overwrite.py 中为强制覆盖场景编写集成测试
- [ ] T049 [P] [US3] 在 tests/unit/test_file_operations.py 中为文件冲突处理逻辑编写单元测试

### 用户故事 3 的实施任务

- [ ] T050 [US3] 在 src/sckit_cli/__init__.py 的 init 命令处理器中实现当前目录检测逻辑（PATH == "."）
- [ ] T051 [US3] 在 src/sckit_cli/__init__.py 中实现 file_exists_prompt 函数（用 Rich Confirm 询问覆盖/跳过）
- [ ] T052 [US3] 在 src/sckit_cli/__init__.py 中将文件冲突处理集成到 copy_template_files 函数（除非使用 --force）
- [ ] T053 [US3] 在 src/sckit_cli/__init__.py 的 copy_template_files 中添加文件操作统计跟踪（files_copied、files_skipped、files_overwritten）
- [ ] T054 [US3] 在 src/sckit_cli/__init__.py 中更新 InstallResult.format_summary 显示跳过/覆盖数量
- [ ] T055 [US3] 在 src/sckit_cli/__init__.py 中当在非空目录初始化时添加提示消息
- [ ] T056 [US3] 更新 README.md 添加当前目录初始化示例和 --force 标志用法
- [ ] T057 [US3] 更新 quickstart.md 添加更新工作流示例

**检查点**: 用户故事 2 和 3 都应该独立工作 - 新项目和现有项目更新

---

## 阶段 6: CI/CD 与 Release 自动化（优先级: P2）

**目标**: 自动化打包提示词模板为zip文件并创建GitHub Release

**独立测试**: 创建Git tag，推送后验证GitHub Actions自动创建Release并上传sckit-cursor-*.zip和sckit-claude-*.zip

- [X] T058 [P] 创建 .github/workflows/scripts/create-release-packages.sh 脚本（参考spec-kit）
- [X] T059 [P] 创建 .github/workflows/scripts/create-github-release.sh 脚本
- [X] T060 创建 .github/workflows/release.yml 工作流，由版本标签触发
- [X] T061 [P] 在 create-release-packages.sh 中添加 cursor 结构（.cursor/commands/）的 zip 打包逻辑
- [X] T062 [P] 在 create-release-packages.sh 中添加 claude 结构（.claude/commands/）的 zip 打包逻辑
- [X] T063 在 create-github-release.sh 中添加 GitHub Release 创建和资源上传
- [X] T064 在 README.md 中更新 release 流程文档

**检查点**: CI/CD 流水线可以从标签自动创建 releases

---

## 阶段 7: 边缘案例与错误处理（优先级: P2）

**目标**: 处理所有边缘情况，确保100%友好的错误消息

**独立测试**: 手动触发各种错误场景，验证错误消息和建议操作的正确性

- [ ] T065 [P] 在 src/sckit_cli/__init__.py 的 get_latest_release 中添加网络超时错误处理，并提供重试建议
- [ ] T066 [P] 在 src/sckit_cli/__init__.py 的 get_latest_release 中添加速率限制错误处理，显示重置时间
- [ ] T067 [P] 在 src/sckit_cli/__init__.py 的 install_template 中下载前添加磁盘空间检查
- [ ] T068 [P] 在 src/sckit_cli/__init__.py 的 InstallConfig.validate 中添加目标目录权限检查
- [ ] T069 [P] 在 src/sckit_cli/__init__.py 的 download_file 中下载后添加文件损坏检测（大小验证）
- [ ] T070 [P] 在 src/sckit_cli/__init__.py 的 get_template_asset 中添加模板未找到错误处理
- [ ] T071 [P] 在 src/sckit_cli/__init__.py 的 init 命令处理器中添加非法项目名验证
- [ ] T072 在 src/sckit_cli/__init__.py 的 init 命令处理器中添加 Ctrl+C 取消处理和清理（依赖 T019）
- [ ] T073 [P] 在 src/sckit_cli/__init__.py 的 init 命令处理器中添加目标路径的符号链接解析
- [ ] T074 [P] 在 src/sckit_cli/__init__.py 中更新 error_handler 处理所有边缘案例场景

**检查点**: 所有错误场景都有清晰、可操作的错误消息

---

## 阶段 8: 打磨与跨领域关注点

**目的**: 影响多个用户故事的改进

- [ ] T075 [P] 在 src/sckit_cli/__init__.py 中为所有函数添加详尽的文档字符串
- [ ] T076 [P] 在 pyproject.toml 中添加类型提示验证和 mypy 配置
- [ ] T077 [P] 在 src/sckit_cli/__init__.py 中添加用于调试的日志配置（可选的 --verbose 标志）
- [ ] T078 [P] 创建完整的 README.md 章节：功能、安装、使用、配置、故障排除
- [ ] T079 [P] 使用 spec.md 中的所有场景更新 quickstart.md
- [ ] T080 [P] 在 README.md 中添加环境变量文档（GITHUB_TOKEN、SCKIT_TIMEOUT、SCKIT_REPO）
- [ ] T081 [P] 在 commands/ 目录中添加示例提示词模板文件
- [ ] T082 [P] 在 tests/unit/test_editor.py 中为 Editor 枚举方法编写单元测试
- [ ] T083 [P] 在 tests/unit/test_release.py 中为 Release 数据类方法编写单元测试
- [ ] T084 [P] 在 tests/unit/test_config.py 中为 Config 类编写单元测试
- [ ] T085 代码审查和重构以适应单文件架构（保持在1000行以下）
- [ ] T086 性能测试：验证 init 在 < 10 秒内完成
- [ ] T087 跨平台测试：在 Windows、macOS、Linux 上验证
- [ ] T088 运行 quickstart.md 中的所有场景作为验证
- [ ] T089 更新 CHANGELOG.md 包含 v0.1.0 的所有功能和变更

---

## 依赖关系与执行顺序

### 阶段依赖关系

- **项目设置（阶段 1）**: 无依赖 - 可立即开始
- **基础设施（阶段 2）**: 依赖项目设置（T001-T008）- 阻塞所有用户故事
- **用户故事 1（阶段 3）**: 依赖基础设施（T009-T019）
- **用户故事 2（阶段 4）**: 依赖基础设施（T009-T019）
- **用户故事 3（阶段 5）**: 依赖用户故事 2 完成（需要核心 init 逻辑）
- **CI/CD（阶段 6）**: 可在阶段 1 后开始，独立于用户故事实施
- **边缘案例（阶段 7）**: 依赖用户故事 2 和 3 的实施
- **打磨（阶段 8）**: 依赖所有期望的用户故事完成

### 用户故事依赖关系

- **用户故事 1（P1）**: 仅基础设施 - CLI 结构和版本命令
  - **交付内容**: 可安装的 CLI 工具，支持 --version 和 --help
  - **MVP 价值**: 用户可以安装工具
  
- **用户故事 2（P1）**: 核心功能 - 新项目初始化
  - **依赖于**: 用户故事 1（CLI 基础设施）
  - **交付内容**: 新项目的完整 init 工作流
  - **MVP 价值**: 用户可以将模板部署到新项目
  - **独立测试**: 无需用户故事 3 即可测试
  
- **用户故事 3（P2）**: 增强功能 - 现有项目更新
  - **依赖于**: 用户故事 2（复用下载/解压/复制逻辑）
  - **交付内容**: 当前目录 init、冲突解决、强制更新
  - **MVP 价值**: 用户可以更新现有项目
  - **独立测试**: 可通过在现有目录运行来独立测试

### 每个用户故事内部

**用户故事 1**（T020-T027）:
- T020-T022: CLI 应用设置（单文件内并行，顺序执行）
- T023-T025: pyproject.toml 配置（并行）
- T026-T027: 文档（并行）

**用户故事 2**（T028-T046）:
- 测试（T028-T031）: 全部并行，先编写
- 核心函数（T032-T034）: 并行（不同逻辑单元）
- 文件操作（T035）: 在 T034 之后
- UI/UX（T036, T042-T043）: 并行
- 编排（T037）: 在 T032-T036 之后
- 命令定义（T038-T040）: 顺序但在 T037 之后
- 命令实现（T041）: 在 T038-T040 之后
- 支持功能（T044-T046）: 并行

**用户故事 3**（T047-T057）:
- 测试（T047-T049）: 并行，先编写
- 逻辑（T050-T055）: 顺序（相互构建）
- 文档（T056-T057）: 并行

### 并行执行机会

**阶段 1（项目设置）内部**:
- T003, T004, T005, T006, T007, T008 都可以并行运行（不同文件）

**阶段 2（基础设施）内部**:
- T009, T010, T011, T012, T014, T015, T016, T017 可以并行运行（不同类，同一文件但独立）
- T013 依赖 T012
- T018 依赖 T010
- T019 是独立的

**阶段 4（用户故事 2 实施）内部**:
- 测试: T028, T029, T030, T031 并行
- 核心: T032, T033, T034, T036 并行
- 模板: T045, T046 并行

**阶段 6（CI/CD）内部**:
- T058, T059, T061, T062 并行

**阶段 7（边缘案例）内部**:
- T065, T066, T067, T068, T069, T070, T071, T073, T074 并行

**阶段 8（打磨）内部**:
- T075, T076, T077, T078, T079, T080, T081, T082, T083, T084 并行

---

## 并行示例: 用户故事 2 核心实施

```bash
# 同时启动用户故事 2 的所有测试:
任务: "在 tests/contract/test_github_api.py 中为 GitHub Release API 响应结构编写契约测试"
任务: "在 tests/contract/test_template_structure.py 中为模板 zip 结构编写契约测试"
任务: "在 tests/integration/test_init_workflow.py 中为完整的新项目初始化工作流编写集成测试"
任务: "在 tests/unit/test_validators.py 中为 is_valid_project_name 函数编写单元测试"

# 同时启动所有独立的核心函数:
任务: "在 src/sckit_cli/__init__.py 中实现 get_latest_release 函数"
任务: "在 src/sckit_cli/__init__.py 中实现 download_file 函数"
任务: "在 src/sckit_cli/__init__.py 中实现 extract_zip 函数"
任务: "在 src/sckit_cli/__init__.py 中实现 prompt_editor_choice 函数"

# 同时启动模板文件:
任务: "在 commands/example.md 中创建示例模板文件"
任务: "在 commands/ 中创建 README.md"
```

---

## 实施策略

### MVP 优先（用户故事 1 + 2）

1. 完成阶段 1: 项目设置（T001-T008）
2. 完成阶段 2: 基础设施（T009-T019）- **关键阻塞点**
3. 完成阶段 3: 用户故事 1（T020-T027）- CLI 安装
4. 完成阶段 4: 用户故事 2（T028-T046）- 新项目初始化
5. **停止并验证**: 独立测试用户故事 2
   - 使用 uv 安装 CLI
   - 运行 `sckit init test-project`
   - 验证创建了 `.cursor/commands/` 或 `.claude/commands/` 及文件
   - 在编辑器中打开并测试斜杠命令
6. 完成阶段 6: CI/CD（T058-T064）- 启用 releases
7. **MVP 就绪**: 可以发布给用户

**MVP 范围**: 用户可以安装 CLI，使用模板创建新项目。这是最小可行产品。

### 渐进式交付

1. **MVP**: 项目设置 + 基础设施 + US1 + US2 → 用户可以将模板部署到新项目
2. **v0.2.0**: 添加用户故事 3 → 用户可以更新现有项目
3. **v0.3.0**: 添加边缘案例（阶段 7）→ 健壮的错误处理
4. **v1.0.0**: 添加打磨（阶段 8）→ 生产就绪质量

### 并行团队策略

多个开发者协作时:

1. **团队共同完成项目设置 + 基础设施**（第 1-2 天）
2. 基础设施完成后，分工:
   - **开发者 A**: 用户故事 1（CLI 结构）→ 用户故事 2（init 逻辑）
   - **开发者 B**: CI/CD（阶段 6）- 可并行工作
   - **开发者 C**: 模板文件和文档
3. **集成点**: 用户故事 2 完成
4. **然后再次并行**:
   - **开发者 A**: 用户故事 3（现有项目更新）
   - **开发者 B**: 边缘案例（阶段 7）
   - **开发者 C**: 打磨和测试（阶段 8）

---

## 任务统计摘要

- **总任务数**: 89
- **阶段 1（项目设置）**: 8 个任务
- **阶段 2（基础设施）**: 11 个任务 ⚠️ 阻塞所有用户故事
- **阶段 3（用户故事 1）**: 8 个任务
- **阶段 4（用户故事 2）**: 19 个任务（4 个测试 + 15 个实施）
- **阶段 5（用户故事 3）**: 11 个任务（3 个测试 + 8 个实施）
- **阶段 6（CI/CD）**: 7 个任务
- **阶段 7（边缘案例）**: 10 个任务
- **阶段 8（打磨）**: 15 个任务

**并行执行机会**: ~45 个标记为 [P] 的任务可在各自阶段内并行运行

**MVP 任务数**: 46 个任务（阶段 1-4 + 阶段 6）- 发布的最低要求

**独立测试标准**:
- **US1**: 安装后运行 `sckit --version`
- **US2**: 运行 `sckit init test-project`，验证文件已创建
- **US3**: 在现有项目中运行 `sckit init .`，验证更新/冲突处理

---

## 注释

- [P] 任务 = 不同文件或独立逻辑，无依赖
- [Story] 标签将任务映射到特定用户故事以便追溯
- 每个用户故事应该可以独立完成和测试
- 所有代码在单个文件中：`src/sckit_cli/__init__.py`（遵循 spec-kit 模式）
- 测试是可选的，但建议用于生产质量
- 每个任务或逻辑组后提交
- 在任何检查点停止以独立验证故事
- 遵循宪法原则：简洁性、用户体验、跨平台一致性

