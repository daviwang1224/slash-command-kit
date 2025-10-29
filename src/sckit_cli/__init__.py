"""
sckit-cli - 轻量级提示词管理工具

从GitHub部署AI编辑器（Cursor/Claude Code）的提示词模板到项目中。
"""

from __future__ import annotations

import os
import sys
import signal
import atexit
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Callable
from datetime import datetime

__version__ = "0.2.0"


# ============================================================================
# T009: Editor 枚举
# ============================================================================

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


# ============================================================================
# T010: 异常层次结构
# ============================================================================

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


# ============================================================================
# T011: Config 数据类
# ============================================================================

@dataclass(frozen=True)
class Config:
    """全局配置"""
    # GitHub仓库信息
    GITHUB_OWNER: str = os.getenv("SCKIT_REPO_OWNER", "daviwang1224")
    GITHUB_REPO: str = os.getenv("SCKIT_REPO", "slash-command-kit")
    
    # API配置
    GITHUB_API_BASE: str = "https://api.github.com"
    REQUEST_TIMEOUT: float = float(os.getenv("SCKIT_TIMEOUT", "10.0"))
    DOWNLOAD_CHUNK_SIZE: int = 8192  # 8KB
    
    # 文件大小限制
    MAX_TEMPLATE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # 版本
    CLI_VERSION: str = __version__
    
    @property
    def release_api_url(self) -> str:
        """最新Release的API URL"""
        return (
            f"{self.GITHUB_API_BASE}/repos/"
            f"{self.GITHUB_OWNER}/{self.GITHUB_REPO}/releases/latest"
        )


# 全局配置实例
config = Config()


# ============================================================================
# T012: ReleaseAsset 数据类
# ============================================================================

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


# ============================================================================
# T013: Release 数据类
# ============================================================================

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
    
    def get_template_asset(self, editor: Editor) -> Optional[ReleaseAsset]:
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


# ============================================================================
# T014: InstallConfig 数据类
# ============================================================================

@dataclass
class InstallConfig:
    """安装配置"""
    target_path: Path
    editor: Editor
    force: bool = False
    github_token: Optional[str] = None
    
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


# ============================================================================
# T015: InstallResult 数据类
# ============================================================================

@dataclass
class InstallResult:
    """安装结果"""
    success: bool
    version: str
    files_copied: int
    target_path: Path
    editor: Editor
    files_skipped: int = 0
    files_overwritten: int = 0
    
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


# ============================================================================
# T016: DownloadProgress 数据类
# ============================================================================

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


# 类型别名
ProgressCallback = Callable[[DownloadProgress], None]
FileConflictCallback = Callable[[Path], bool]


# ============================================================================
# T017: is_valid_project_name 验证器函数
# ============================================================================

def is_valid_project_name(name: str) -> bool:
    """验证项目名称合法性
    
    禁止的字符（Windows + Unix）: < > : " / \\ | ? *
    """
    forbidden = r'<>:"/\|?*'
    return not any(c in forbidden for c in name)


# ============================================================================
# T018: error_handler 函数
# ============================================================================

def error_handler(e: Exception, verbose: bool = False) -> None:
    """处理并显示错误消息
    
    Args:
        e: 异常对象
        verbose: 是否显示详细堆栈跟踪
    """
    # 将在后续任务中实现完整的 Rich 格式化
    # 目前提供基础错误处理
    
    if isinstance(e, RateLimitError):
        print(f"❌ 错误: GitHub API速率限制", file=sys.stderr)
        print(f"配额重置时间: {e.reset_time}", file=sys.stderr)
        print(f"💡 建议: 设置GITHUB_TOKEN环境变量", file=sys.stderr)
    elif isinstance(e, TemplateNotFoundError):
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        print(f"💡 建议: 检查仓库Release是否包含正确的模板文件", file=sys.stderr)
    elif isinstance(e, NetworkError):
        print(f"❌ 错误: 网络连接失败", file=sys.stderr)
        print(f"💡 建议: 检查网络连接后重试", file=sys.stderr)
    elif isinstance(e, FileSystemError):
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        print(f"💡 建议: 使用有写入权限的目录", file=sys.stderr)
    elif isinstance(e, ValidationError):
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        print(f"💡 建议: 只使用字母、数字、下划线和连字符", file=sys.stderr)
    elif verbose:
        import traceback
        traceback.print_exc()
    else:
        print(f"❌ 错误: {str(e)}", file=sys.stderr)


# ============================================================================
# T019: 信号处理器
# ============================================================================

# 用于清理的临时路径列表
_cleanup_paths: List[Path] = []


def cleanup() -> None:
    """清理临时文件"""
    import shutil
    for path in _cleanup_paths:
        if path.exists():
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
            except Exception:
                pass  # 静默忽略清理错误


def signal_handler(signum: int, frame) -> None:
    """信号处理器（Ctrl+C等）"""
    print("\n[yellow]操作已取消，正在清理...[/yellow]", file=sys.stderr)
    cleanup()
    sys.exit(2)


def register_cleanup_path(path: Path) -> None:
    """注册需要清理的路径"""
    _cleanup_paths.append(path)


# 注册清理和信号处理
atexit.register(cleanup)
signal.signal(signal.SIGINT, signal_handler)
if hasattr(signal, 'SIGTERM'):
    signal.signal(signal.SIGTERM, signal_handler)


# ============================================================================
# T020-T022: Typer CLI 应用
# ============================================================================

import typer
from rich.console import Console

console = Console()

app = typer.Typer(
    name="sckit",
    help="轻量级提示词管理工具 - 从GitHub部署AI编辑器提示词模板",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """显示版本信息并退出"""
    if value:
        console.print(f"sckit version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="显示版本号并退出",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """
    sckit - 轻量级提示词管理工具
    
    从GitHub部署AI编辑器（Cursor/Claude Code）的提示词模板到项目中。
    """
    pass


# ============================================================================
# T032-T036: 核心函数
# ============================================================================

import httpx
import zipfile
import tempfile
import shutil
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.prompt import Prompt, Confirm
from rich.panel import Panel


def get_latest_release(github_token: Optional[str] = None) -> Release:
    """
    T032: 获取最新 Release
    
    从 GitHub API 获取仓库的最新 Release 信息
    """
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    
    # T044: 支持 GITHUB_TOKEN
    token = github_token or os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        response = httpx.get(
            config.release_api_url,
            headers=headers,
            timeout=config.REQUEST_TIMEOUT,
        )
        
        # 检查速率限制
        if response.status_code == 403:
            reset_time = response.headers.get("X-RateLimit-Reset", "unknown")
            if reset_time != "unknown":
                reset_dt = datetime.fromtimestamp(int(reset_time))
                reset_time = reset_dt.strftime("%Y-%m-%d %H:%M:%S")
            raise RateLimitError(reset_time)
        
        response.raise_for_status()
        return Release.from_api_response(response.json())
        
    except httpx.TimeoutException:
        raise NetworkError("请求超时，请检查网络连接")
    except httpx.HTTPError as e:
        raise NetworkError(f"网络请求失败: {e}")


def download_file(
    url: str,
    dest: Path,
    progress_callback: Optional[ProgressCallback] = None
) -> None:
    """
    T033: 下载文件
    
    使用 httpx 流式下载文件，支持进度回调
    """
    try:
        with httpx.stream("GET", url, timeout=config.REQUEST_TIMEOUT * 3, follow_redirects=True) as response:
            response.raise_for_status()
            total = int(response.headers.get("content-length", 0))
            
            downloaded = 0
            with open(dest, "wb") as f:
                for chunk in response.iter_bytes(chunk_size=config.DOWNLOAD_CHUNK_SIZE):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(DownloadProgress(downloaded, total))
            
            # 验证文件大小
            if total > 0 and dest.stat().st_size != total:
                raise DownloadError("文件下载不完整")
                
    except httpx.HTTPError as e:
        raise DownloadError(f"下载失败: {e}")


def extract_zip(zip_path: Path, extract_to: Path) -> None:
    """
    T034: 解压 ZIP 文件
    
    解压模板 zip 文件到指定目录
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    except zipfile.BadZipFile:
        raise FileSystemError(f"ZIP 文件损坏: {zip_path}")
    except Exception as e:
        raise FileSystemError(f"解压失败: {e}")


def copy_template_files(
    source_dir: Path,
    target_dir: Path,
    force: bool = False,
    conflict_callback: Optional[FileConflictCallback] = None
) -> tuple[int, int, int]:
    """
    T035: 复制模板文件
    
    从源目录复制文件到目标目录，处理文件冲突
    
    Returns:
        (files_copied, files_skipped, files_overwritten)
    """
    files_copied = 0
    files_skipped = 0
    files_overwritten = 0
    
    # 确保目标目录存在
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 遍历源目录中的所有文件
    for source_file in source_dir.rglob("*"):
        if source_file.is_file():
            # 计算相对路径
            rel_path = source_file.relative_to(source_dir)
            target_file = target_dir / rel_path
            
            # 检查文件是否已存在
            if target_file.exists() and not force:
                # 询问是否覆盖
                if conflict_callback and conflict_callback(target_file):
                    # 用户选择覆盖
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, target_file)
                    files_overwritten += 1
                else:
                    # 跳过
                    files_skipped += 1
            else:
                # 复制文件
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_file, target_file)
                if target_file.exists() and not force:
                    files_overwritten += 1
                else:
                    files_copied += 1
    
    return files_copied, files_skipped, files_overwritten


def prompt_editor_choice() -> Editor:
    """
    T036: 交互式编辑器选择
    
    使用 Rich Prompt 让用户选择编辑器
    """
    choice = Prompt.ask(
        "选择 AI 编辑器",
        choices=["Cursor", "Claude"],
        default="Cursor"
    )
    
    if choice.lower() == "cursor":
        return Editor.CURSOR
    else:
        return Editor.CLAUDE


# ============================================================================
# T037: install_template 编排函数
# ============================================================================

def install_template(config_obj: InstallConfig) -> InstallResult:
    """
    T037: 安装模板
    
    编排完整的模板安装流程：下载 → 解压 → 复制
    """
    # 验证配置
    config_obj.validate()
    
    # T042: 获取最新 Release
    console.print("\n[cyan]正在获取最新模板信息...[/cyan]")
    release = get_latest_release(config_obj.github_token)
    
    # 获取对应编辑器的模板资源
    asset = release.get_template_asset(config_obj.editor)
    if not asset:
        raise TemplateNotFoundError(config_obj.editor, release.version)
    
    console.print(f"[green]找到模板: {asset.name} ({asset.size // 1024} KB)[/green]")
    
    # 创建临时目录用于下载和解压
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        zip_file = tmp_path / asset.name
        extract_dir = tmp_path / "extracted"
        
        # 注册清理路径
        register_cleanup_path(tmp_path)
        
        # T033 + T042: 下载文件（带进度）
        console.print("\n[cyan]正在下载模板...[/cyan]")
        with Progress(
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task_id = progress.add_task("[cyan]下载中", total=asset.size)
            
            def update_progress(prog: DownloadProgress):
                progress.update(task_id, completed=prog.downloaded)
            
            download_file(asset.download_url, zip_file, update_progress)
        
        console.print("[green]✓ 下载完成[/green]")
        
        # T034: 解压
        console.print("\n[cyan]正在解压模板...[/cyan]")
        extract_zip(zip_file, extract_dir)
        console.print("[green]✓ 解压完成[/green]")
        
        # T035: 复制文件
        console.print("\n[cyan]正在复制文件...[/cyan]")
        
        # 查找 commands 目录（可能在 .cursor/commands 或 .claude/commands）
        commands_source = None
        for candidate in [
            extract_dir / config_obj.editor.config_dir / "commands",
            extract_dir / "commands",
        ]:
            if candidate.exists() and candidate.is_dir():
                commands_source = candidate
                break
        
        if not commands_source:
            raise FileSystemError("模板包中未找到 commands 目录")
        
        # 定义冲突处理回调
        def handle_conflict(file_path: Path) -> bool:
            """询问用户是否覆盖文件"""
            if config_obj.force:
                return True
            return Confirm.ask(f"文件 '{file_path.name}' 已存在，是否覆盖？", default=False)
        
        # 复制文件
        files_copied, files_skipped, files_overwritten = copy_template_files(
            commands_source,
            config_obj.commands_dir,
            config_obj.force,
            handle_conflict
        )
        
        console.print("[green]✓ 文件复制完成[/green]")
        
        # T043: 显示成功消息
        result = InstallResult(
            success=True,
            version=release.version,
            files_copied=files_copied,
            target_path=config_obj.target_path,
            editor=config_obj.editor,
            files_skipped=files_skipped,
            files_overwritten=files_overwritten,
        )
        
        console.print(Panel(
            result.format_summary(),
            title="[bold green]安装成功[/bold green]",
            border_style="green",
        ))
        
        return result


# ============================================================================
# T038-T041: init 命令
# ============================================================================

@app.command()
def init(
    path: str = typer.Argument(
        ".",
        help="项目路径。使用 '.' 表示当前目录，或指定目录名创建新项目"
    ),
    editor: Optional[str] = typer.Option(
        None,
        "--editor",
        "-e",
        help="指定编辑器（cursor 或 claude），跳过交互式选择"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="强制覆盖已存在的文件，跳过确认"
    ),
) -> None:
    """
    在项目中初始化或更新提示词模板
    
    示例:
        sckit init my-project          # 创建新项目
        sckit init .                   # 在当前目录初始化
        sckit init . --force           # 强制更新
        sckit init my-project -e cursor  # 指定编辑器
    """
    try:
        # T041: 处理路径
        target_path = Path(path).resolve()
        
        # 如果不是当前目录，创建新目录
        if path != "." and not target_path.exists():
            console.print(f"\n[cyan]创建项目目录: {target_path}[/cyan]")
            target_path.mkdir(parents=True, exist_ok=True)
        
        # T039: 选择编辑器
        if editor:
            # 从命令行参数获取
            if editor.lower() in ["cursor", "claude"]:
                selected_editor = Editor.CURSOR if editor.lower() == "cursor" else Editor.CLAUDE
            else:
                console.print("[red]错误: 编辑器必须是 'cursor' 或 'claude'[/red]")
                raise typer.Exit(1)
        else:
            # T036: 交互式选择
            selected_editor = prompt_editor_choice()
        
        # 创建安装配置
        install_config = InstallConfig(
            target_path=target_path,
            editor=selected_editor,
            force=force,
        )
        
        # 执行安装
        install_template(install_config)
        
    except SCKitError as e:
        error_handler(e)
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]操作已取消[/yellow]")
        raise typer.Exit(2)
    except Exception as e:
        console.print(f"\n[red]未预期的错误: {e}[/red]")
        raise typer.Exit(1)


# 主入口点
def cli() -> None:
    """CLI 入口点"""
    app()
