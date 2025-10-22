# Data Model

**Feature**: 轻量级提示词管理CLI工具  
**Date**: 2025-10-22  
**Phase**: Phase 1 - Design

本文档定义系统中的核心数据结构和类型。

## 1. Editor (编辑器枚举)

代表支持的AI编辑器类型。

```python
from enum import Enum

class Editor(str, Enum):
    """支持的AI编辑器"""
    CURSOR = "cursor"
    CLAUDE = "claude"
    
    @property
    def display_name(self) -> str:
        """显示名称"""
        return {
            Editor.CURSOR: "Cursor",
            Editor.CLAUDE: "Claude Code"
        }[self]
    
    @property
    def config_dir(self) -> str:
        """配置目录名"""
        return {
            Editor.CURSOR: ".cursor",
            Editor.CLAUDE: ".claude"
        }[self]
    
    def get_commands_path(self, project_root: Path) -> Path:
        """获取commands目录的完整路径"""
        return project_root / self.config_dir / "commands"
```

**Validation Rules**:
- 必须是预定义的编辑器之一
- 不可为空

**Usage**:
```python
editor = Editor.CURSOR
target = editor.get_commands_path(Path("/my-project"))
# -> Path("/my-project/.cursor/commands")
```

---

## 2. Release (Release信息)

GitHub Release的数据模型。

```python
from dataclasses import dataclass
from typing import List

@dataclass
class ReleaseAsset:
    """Release资源文件"""
    name: str
    download_url: str
    size: int  # 字节
    
    def is_template_for(self, editor: Editor) -> bool:
        """判断是否是指定编辑器的模板"""
        # 期望格式: sckit-{editor}-{version}.zip
        return self.name.startswith(f"sckit-{editor.value}-")

@dataclass
class Release:
    """GitHub Release信息"""
    tag_name: str  # e.g., "v0.1.0"
    name: str
    assets: List[ReleaseAsset]
    
    @property
    def version(self) -> str:
        """版本号（去掉v前缀）"""
        return self.tag_name.lstrip("v")
    
    def get_template_asset(self, editor: Editor) -> ReleaseAsset | None:
        """获取指定编辑器的模板资源"""
        for asset in self.assets:
            if asset.is_template_for(editor):
                return asset
        return None

    @classmethod
    def from_api_response(cls, data: dict) -> "Release":
        """从GitHub API响应构造"""
        assets = [
            ReleaseAsset(
                name=a["name"],
                download_url=a["browser_download_url"],
                size=a["size"]
            )
            for a in data.get("assets", [])
        ]
        return cls(
            tag_name=data["tag_name"],
            name=data.get("name", data["tag_name"]),
            assets=assets
        )
```

**Validation Rules**:
- `tag_name` 必须存在且非空
- `assets` 必须包含至少一个editor的模板
- 资源名必须符合 `sckit-{editor}-{version}.zip` 格式

**State Transitions**: N/A (只读数据)

---

## 3. InstallConfig (安装配置)

初始化操作的配置参数。

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class InstallConfig:
    """安装配置"""
    target_path: Path          # 目标项目路径
    editor: Editor             # 选择的编辑器
    force: bool = False        # 是否强制覆盖
    github_token: str | None = None  # GitHub认证token
    
    @property
    def is_current_dir(self) -> bool:
        """是否在当前目录初始化"""
        return self.target_path.resolve() == Path.cwd().resolve()
    
    @property
    def commands_dir(self) -> Path:
        """目标commands目录"""
        return self.editor.get_commands_path(self.target_path)
    
    def validate(self) -> None:
        """验证配置"""
        # 检查项目名是否合法
        if not self.is_current_dir:
            if not is_valid_project_name(self.target_path.name):
                raise ValidationError(
                    f"项目名 '{self.target_path.name}' 包含非法字符"
                )
        
        # 检查父目录是否可写
        parent = self.target_path.parent
        if not parent.exists() or not os.access(parent, os.W_OK):
            raise FileSystemError(f"无法写入目录: {parent}")

def is_valid_project_name(name: str) -> bool:
    """验证项目名称合法性"""
    # 禁止的字符（Windows + Unix）
    forbidden = r'<>:"/\|?*'
    return not any(c in forbidden for c in name)
```

**Validation Rules**:
- `target_path` 的父目录必须存在且可写
- `editor` 必须是有效的Editor枚举值
- 项目名不能包含非法字符：`< > : " / \ | ? *`

---

## 4. InstallResult (安装结果)

初始化操作的结果信息。

```python
from dataclasses import dataclass
from typing import List

@dataclass
class InstallResult:
    """安装结果"""
    success: bool
    version: str                    # Release版本号
    files_copied: int               # 复制的文件数
    files_skipped: int = 0          # 跳过的文件数
    files_overwritten: int = 0      # 覆盖的文件数
    target_path: Path               # 目标路径
    editor: Editor                  # 编辑器类型
    
    @property
    def total_files(self) -> int:
        """总文件数"""
        return self.files_copied + self.files_skipped
    
    def format_summary(self) -> str:
        """格式化摘要信息"""
        lines = [
            f"✅ 安装完成",
            f"版本: v{self.version}",
            f"编辑器: {self.editor.display_name}",
            f"位置: {self.target_path / self.editor.config_dir / 'commands'}",
            f"文件: {self.files_copied} 个已复制",
        ]
        
        if self.files_skipped > 0:
            lines.append(f"      {self.files_skipped} 个已跳过")
        if self.files_overwritten > 0:
            lines.append(f"      {self.files_overwritten} 个已覆盖")
        
        return "\n".join(lines)
```

---

## 5. DownloadProgress (下载进度)

用于跟踪下载进度的回调数据。

```python
from dataclasses import dataclass

@dataclass
class DownloadProgress:
    """下载进度信息"""
    downloaded: int  # 已下载字节
    total: int       # 总字节数
    
    @property
    def percentage(self) -> float:
        """百分比 (0-100)"""
        if self.total == 0:
            return 0.0
        return (self.downloaded / self.total) * 100
    
    @property
    def is_complete(self) -> bool:
        """是否完成"""
        return self.downloaded >= self.total

# 进度回调类型
ProgressCallback = Callable[[DownloadProgress], None]
```

**Usage**:
```python
def on_progress(progress: DownloadProgress):
    print(f"进度: {progress.percentage:.1f}%")

download_file(url, dest, progress_callback=on_progress)
```

---

## 6. Config (全局配置)

应用程序全局配置和常量。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    """全局配置"""
    # GitHub仓库信息
    GITHUB_OWNER: str = "username"  # TODO: 替换为实际用户名
    GITHUB_REPO: str = "slash-command-kit"
    
    # API配置
    GITHUB_API_BASE: str = "https://api.github.com"
    REQUEST_TIMEOUT: float = 10.0
    DOWNLOAD_CHUNK_SIZE: int = 8192  # 8KB
    
    # 文件大小限制
    MAX_TEMPLATE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # 版本
    CLI_VERSION: str = "0.1.0"
    
    @property
    def release_api_url(self) -> str:
        """最新Release的API URL"""
        return (
            f"{self.GITHUB_API_BASE}/repos/"
            f"{self.GITHUB_OWNER}/{self.GITHUB_REPO}/releases/latest"
        )

# 全局配置实例
config = Config()
```

---

## 7. 异常类型

```python
class SCKitError(Exception):
    """基础异常"""
    pass

class NetworkError(SCKitError):
    """网络错误"""
    pass

class RateLimitError(NetworkError):
    """API限流"""
    def __init__(self, reset_time: str):
        self.reset_time = reset_time
        super().__init__(f"API速率限制，重置时间: {reset_time}")

class DownloadError(NetworkError):
    """下载失败"""
    pass

class FileSystemError(SCKitError):
    """文件系统错误"""
    pass

class ValidationError(SCKitError):
    """验证错误"""
    pass

class TemplateNotFoundError(SCKitError):
    """模板未找到"""
    def __init__(self, editor: Editor, version: str):
        super().__init__(
            f"未找到 {editor.display_name} 的模板包 "
            f"(期望: sckit-{editor.value}-{version}.zip)"
        )
```

---

## Entity Relationships

```
┌─────────────────┐
│  InstallConfig  │
│                 │
│ - target_path   │
│ - editor        │───┐
│ - force         │   │
│ - github_token  │   │
└─────────────────┘   │
                      │
                      ▼
                ┌──────────┐
                │  Editor  │
                │          │
                │ - CURSOR │
                │ - CLAUDE │
                └──────────┘
                      │
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
┌─────────────┐            ┌───────────────┐
│   Release   │            │ InstallResult │
│             │            │               │
│ - tag_name  │            │ - version     │
│ - assets    │────────────│ - files_*     │
└─────────────┘            │ - editor      │
        │                  └───────────────┘
        │
        ▼
┌──────────────────┐
│  ReleaseAsset    │
│                  │
│ - name           │
│ - download_url   │
│ - size           │
└──────────────────┘
```

---

## Validation Summary

### InstallConfig Validation
- ✅ 目标路径父目录存在且可写
- ✅ 编辑器类型有效
- ✅ 项目名不含非法字符

### Release Validation  
- ✅ tag_name非空
- ✅ 至少包含一个editor的模板asset
- ✅ Asset名称符合格式规范

### ReleaseAsset Validation
- ✅ 名称符合 `sckit-{editor}-{version}.zip` 格式
- ✅ 大小 < MAX_TEMPLATE_SIZE (10MB)
- ✅ download_url是有效的HTTPS URL

---

## Type Aliases

```python
from typing import Callable
from pathlib import Path

# 进度回调
ProgressCallback = Callable[[DownloadProgress], None]

# 文件复制回调（用于询问覆盖）
FileConflictCallback = Callable[[Path], bool]  # 返回True表示覆盖
```

