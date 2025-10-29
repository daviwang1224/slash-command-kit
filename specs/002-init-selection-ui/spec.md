# Feature Specification: Init 命令交互式选择界面

**Feature Branch**: `002-init-selection-ui`  
**Created**: 2025-10-29  
**Status**: Draft  
**Input**: User description: "请将sckit.init 命令安装的终端界面，将Cursor和Claude选择的界面，换成选择，而非人工输入。方便我使用 sckit init 命令时，操作更加流畅。"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 快速选择编辑器 (Priority: P1)

开发者在执行 `sckit init` 命令时，需要选择目标编辑器（Cursor 或 Claude）。当前需要手动输入编辑器名称，容易出现拼写错误或需要回忆准确的名称，影响操作流畅度。改进后，开发者可以使用键盘方向键（↑↓）在可视化选项列表中快速选择，按回车确认，无需输入任何文本。

**Why this priority**: 这是唯一的核心功能，直接影响用户体验。提供可视化选择界面可减少输入错误，提升操作效率，让新手用户无需记忆编辑器名称。

**Independent Test**: 运行 `sckit init` 命令（不带 `--editor` 参数），验证是否出现箭头选择界面，使用方向键选择不同选项，按回车确认是否正确执行后续安装流程。

**Acceptance Scenarios**:

1. **Given** 用户在终端执行 `sckit init .` 且未使用 `--editor` 参数, **When** 系统需要选择编辑器, **Then** 系统显示可视化选择列表，包含 "Cursor" 和 "Claude" 两个选项，高亮第一个选项
2. **Given** 选择界面已显示, **When** 用户按下方向键 ↓, **Then** 高亮光标移动到下一个选项
3. **Given** 选择界面已显示, **When** 用户按下方向键 ↑, **Then** 高亮光标移动到上一个选项（循环至末尾）
4. **Given** 用户已高亮某个选项, **When** 用户按下回车键, **Then** 系统选择该编辑器并继续执行安装流程
5. **Given** 选择界面已显示, **When** 用户按下 Ctrl+C, **Then** 系统取消操作并退出（退出码 2）

---

### Edge Cases

- **键盘兼容性**: 在不同操作系统（Windows PowerShell、macOS/Linux Shell）中，方向键是否能正常响应？
- **终端不支持交互**: 在 CI/CD 管道或非交互式终端中运行 `sckit init` 时（未指定 `--editor`），系统应如何处理？是否应自动使用默认值或报错？
- **用户误操作**: 用户在选择界面按下其他非控制键（如字母、数字）时，系统应如何响应？
- **并发冲突**: 当用户在选择过程中，终端窗口大小改变或输出被中断时，界面是否能正确恢复？

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 当 `sckit init` 命令未使用 `--editor` 参数时，系统必须显示交互式选择界面，而非文本输入提示
- **FR-002**: 选择界面必须采用上下箭头键（↑↓）控制的可视化列表，包含 "Cursor" 和 "Claude" 两个选项
- **FR-003**: 系统必须在列表中高亮当前选中的选项，默认高亮第一个选项（Cursor）
- **FR-004**: 用户按下回车键时，系统必须确认当前高亮的选项并继续执行后续安装流程
- **FR-005**: 用户按下 Ctrl+C 时，系统必须取消操作并以退出码 2 退出程序
- **FR-006**: 系统必须支持方向键循环导航（在最后一项按 ↓ 返回第一项，在第一项按 ↑ 跳转到最后一项）
- **FR-007**: 当使用 `--editor` 参数时，系统必须保持当前行为（跳过交互选择，直接使用指定编辑器）
- **FR-008**: 在非交互式终端环境（如 CI/CD）中，若未指定 `--editor` 参数，系统必须使用默认编辑器（Cursor）并显示提示信息，不应报错退出

### Key Entities *(not applicable for this feature)*

此功能不涉及新的数据实体，仅改进用户交互方式。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 用户可在 3 秒内完成编辑器选择（从界面出现到按回车确认）
- **SC-002**: 新手用户无需查看文档即可理解如何选择编辑器（界面提供视觉引导）
- **SC-003**: 选择过程中用户输入错误率降为 0%（不再需要输入文本）
- **SC-004**: 选择界面在所有支持的操作系统（Windows、macOS、Linux）上正常工作
- **SC-005**: 用户满意度提升：通过用户反馈或测试，90% 的用户认为新界面比旧界面更易用
