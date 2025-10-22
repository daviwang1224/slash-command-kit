# Research & Technical Decisions

**Feature**: 轻量级提示词管理CLI工具  
**Date**: 2025-10-22  
**Phase**: Phase 0 - Research

本文档记录技术选型、最佳实践研究和关键决策。

## 1. CLI框架选择

### Decision: Typer

**Rationale**:
- **类型安全**: 基于类型注解自动生成CLI接口，减少错误
- **自动文档**: 从docstring和类型注解自动生成帮助信息
- **Rich集成**: 内置支持Rich库，提供美观的终端输出
- **简洁API**: 装饰器风格，代码可读性高
- **Click基础**: 基于成熟的Click框架，稳定可靠

**Alternatives Considered**:
- **argparse** (标准库): 功能完整但代码冗长，缺少现代特性
- **Click**: 成熟但需要更多样板代码，Typer是其改进版
- **Fire**: 过于魔法化，难以控制接口细节

**Implementation Notes**:
```python
import typer
app = typer.Typer(help="轻量级提示词管理工具")

@app.command()
def init(
    path: str = typer.Argument(..., help="项目路径"),
    force: bool = typer.Option(False, "--force", help="强制覆盖")
):
    """在项目中初始化提示词"""
    pass
```

---

## 2. HTTP客户端选择

### Decision: httpx

**Rationale**:
- **异步支持**: 虽然当前不需要，但为未来扩展保留可能
- **现代API**: 类似requests但更现代化
- **进度跟踪**: 支持流式下载和进度回调
- **超时控制**: 更好的超时和重试控制
- **HTTP/2支持**: 更高效的网络通信

**Alternatives Considered**:
- **requests**: 最流行但缺少异步和现代特性
- **urllib3**: 底层API，过于复杂
- **aiohttp**: 强制异步，对于CLI过于复杂

**Implementation Notes**:
```python
import httpx
from rich.progress import Progress

def download_with_progress(url: str, dest: Path) -> None:
    with httpx.stream("GET", url) as response:
        total = int(response.headers.get("content-length", 0))
        with Progress() as progress:
            task = progress.add_task("[cyan]下载中...", total=total)
            with open(dest, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
                    progress.update(task, advance=len(chunk))
```

---

## 3. 终端UI库选择

### Decision: Rich

**Rationale**:
- **美观输出**: 彩色文本、表格、进度条、树形图
- **跨平台**: Windows/macOS/Linux一致体验
- **Typer集成**: 与Typer天然集成
- **交互式提示**: 支持选择菜单（通过questionary或手动实现）
- **错误格式化**: 美化异常和错误消息

**Alternatives Considered**:
- **colorama**: 仅颜色支持，功能有限
- **click.echo**: 基础功能，不够美观
- **termcolor**: 轻量但功能单一

**Implementation Notes**:
```python
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.panel import Panel

console = Console()

# 选择编辑器
editor = Prompt.ask(
    "选择AI编辑器",
    choices=["Cursor", "Claude Code"],
    default="Cursor"
)

# 成功消息
console.print(Panel(
    f"✅ 成功复制 {count} 个文件到 {dest}",
    style="green"
))
```

---

## 4. GitHub Release API集成

### Decision: 直接调用GitHub REST API v3

**Rationale**:
- **简单直接**: 仅需GET /repos/{owner}/{repo}/releases/latest
- **无需认证**: 公开仓库可匿名访问
- **稳定API**: GitHub API v3成熟稳定
- **避免SDK依赖**: PyGithub等SDK过重，增加依赖

**API Endpoints**:
```
GET https://api.github.com/repos/{owner}/{repo}/releases/latest
Response: {
  "tag_name": "v0.1.0",
  "assets": [
    {
      "name": "sckit-cursor-0.1.0.zip",
      "browser_download_url": "https://github.com/.../releases/download/..."
    }
  ]
}
```

**Rate Limiting**:
- 未认证: 60请求/小时/IP
- 认证: 5000请求/小时（通过GITHUB_TOKEN）
- 策略: 提供环境变量支持，显示限流错误

**Implementation Notes**:
```python
def get_latest_release(owner: str, repo: str) -> dict:
    headers = {}
    if token := os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"token {token}"
    
    response = httpx.get(
        f"https://api.github.com/repos/{owner}/{repo}/releases/latest",
        headers=headers,
        timeout=10.0
    )
    
    if response.status_code == 403:
        # Rate limit exceeded
        reset_time = response.headers.get("X-RateLimit-Reset")
        raise RateLimitError(reset_time)
    
    response.raise_for_status()
    return response.json()
```

---

## 5. 文件完整性验证

### Decision: SHA256 checksum (可选)

**Rationale**:
- **检测损坏**: 验证下载完整性
- **标准库支持**: Python hashlib内置
- **性能开销小**: 5MB文件验证 < 100ms
- **可选特性**: Release可选择提供checksum文件

**Implementation Strategy**:
1. **Phase 1**: 基于文件大小验证（Content-Length）
2. **Phase 2**: 如果Release提供.sha256文件，进行校验

**Implementation Notes**:
```python
import hashlib

def verify_checksum(file_path: Path, expected: str) -> bool:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest() == expected

# 简化版：仅验证大小
def verify_size(file_path: Path, expected: int) -> bool:
    return file_path.stat().st_size == expected
```

---

## 6. 跨平台路径处理

### Decision: pathlib.Path

**Rationale**:
- **现代API**: Python 3.4+推荐方式
- **跨平台**: 自动处理Windows/Unix路径差异
- **类型安全**: 路径对象vs字符串，减少错误
- **丰富方法**: exists(), mkdir(), glob()等

**Best Practices**:
```python
from pathlib import Path

# ✅ 正确
target = Path(project_name) / ".cursor" / "commands"
target.mkdir(parents=True, exist_ok=True)

# ❌ 避免
target = os.path.join(project_name, ".cursor", "commands")
os.makedirs(target, exist_ok=True)
```

**Windows特殊处理**:
```python
# 符号链接检测（Windows需要特殊权限）
def is_symlink_safe(path: Path) -> bool:
    try:
        return path.is_symlink()
    except OSError:
        # Windows权限不足
        return False
```

---

## 7. 临时文件管理

### Decision: tempfile.TemporaryDirectory with context manager

**Rationale**:
- **自动清理**: 上下文管理器退出时自动删除
- **异常安全**: 即使出错也会清理
- **跨平台**: 自动选择合适的临时目录
- **线程安全**: 避免并发冲突

**Implementation Notes**:
```python
import tempfile
from pathlib import Path

def install_template(url: str, target: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # 下载到临时目录
        zip_file = tmp_path / "template.zip"
        download(url, zip_file)
        
        # 解压
        extract_dir = tmp_path / "extracted"
        extract_zip(zip_file, extract_dir)
        
        # 复制到目标
        copy_files(extract_dir, target)
        
        # 函数返回时，tmp_dir自动删除
```

---

## 8. 信号处理（Ctrl+C）

### Decision: signal.signal + atexit

**Rationale**:
- **优雅退出**: 捕获SIGINT/SIGTERM清理资源
- **跨平台**: Windows/Unix信号差异由Python处理
- **清理保证**: atexit确保正常和异常退出都清理

**Implementation Notes**:
```python
import signal
import atexit
from pathlib import Path

cleanup_paths: list[Path] = []

def cleanup():
    for path in cleanup_paths:
        if path.exists():
            shutil.rmtree(path)

def signal_handler(signum, frame):
    console.print("\n[yellow]操作已取消，正在清理...[/yellow]")
    cleanup()
    sys.exit(1)

# 注册清理和信号处理
atexit.register(cleanup)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
```

---

## 9. 错误处理策略

### Decision: 自定义异常层次 + Rich格式化

**Rationale**:
- **类型区分**: 网络错误、文件错误、用户错误分类处理
- **友好消息**: Rich格式化，包含建议操作
- **调试信息**: --verbose标志显示详细堆栈

**Exception Hierarchy**:
```python
class SCKitError(Exception):
    """基础异常"""
    pass

class NetworkError(SCKitError):
    """网络相关错误"""
    pass

class RateLimitError(NetworkError):
    """GitHub API限流"""
    def __init__(self, reset_time: str):
        self.reset_time = reset_time

class FileSystemError(SCKitError):
    """文件系统错误"""
    pass

class ValidationError(SCKitError):
    """验证错误"""
    pass
```

**Error Handler**:
```python
def handle_error(e: Exception, verbose: bool = False):
    if isinstance(e, RateLimitError):
        console.print(Panel(
            f"❌ GitHub API速率限制\n"
            f"配额重置时间: {e.reset_time}\n"
            f"💡 建议: 设置GITHUB_TOKEN环境变量",
            title="错误",
            style="red"
        ))
    elif isinstance(e, NetworkError):
        console.print(Panel(
            f"❌ 网络连接失败\n"
            f"💡 建议: 检查网络连接后重试",
            style="red"
        ))
    elif verbose:
        console.print_exception()
    else:
        console.print(f"[red]错误: {e}[/red]")
```

---

## 10. 打包和分发策略

### Decision: pyproject.toml + uv-compatible

**Rationale**:
- **现代标准**: PEP 517/518标准打包
- **uv兼容**: 目标用户使用uv安装
- **依赖锁定**: 明确版本范围
- **入口点**: 定义sckit命令

**pyproject.toml**:
```toml
[project]
name = "sckit-cli"
version = "0.1.0"
description = "轻量级提示词管理工具"
requires-python = ">=3.8"
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "httpx>=0.24.0",
]

[project.scripts]
sckit = "sckit_cli.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Installation Command**:
```bash
uv tool install sckit-cli --from git+https://github.com/username/slash-command-kit.git
```

---

## 11. CI/CD Release流程

### Decision: GitHub Actions单源多目标打包

**Rationale**:
- **单源维护**: `commands/`只存一份Markdown模板（参考spec-kit）
- **多目标打包**: CI/CD脚本生成cursor和claude两种目录结构
- **自动化**: Git tag触发自动构建和Release
- **一致性**: 两个zip内容相同，仅目录结构不同

**Packaging Strategy** (参考spec-kit/create-release-packages.sh):
```bash
# 从单份commands/*.md生成两种结构
build_cursor_package() {
  mkdir -p .genreleases/cursor-package/.cursor/commands
  cp commands/*.md .genreleases/cursor-package/.cursor/commands/
  cd .genreleases/cursor-package
  zip -r ../sckit-cursor-${VERSION}.zip .
}

build_claude_package() {
  mkdir -p .genreleases/claude-package/.claude/commands
  cp commands/*.md .genreleases/claude-package/.claude/commands/
  cd .genreleases/claude-package
  zip -r ../sckit-claude-${VERSION}.zip .
}
```

**Workflow Outline**:
```yaml
name: Release
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Create release packages
        run: |
          chmod +x .github/workflows/scripts/create-release-packages.sh
          .github/workflows/scripts/create-release-packages.sh ${{ github.ref_name }}
      
      - name: Create GitHub Release
        run: |
          chmod +x .github/workflows/scripts/create-github-release.sh
          .github/workflows/scripts/create-github-release.sh ${{ github.ref_name }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Benefits**:
- 提示词维护只需编辑`commands/`中的一份文件
- 避免cursor和claude两份文件同步问题
- 遵循DRY原则（Don't Repeat Yourself）
- 参考spec-kit成熟的打包实践

---

## 12. 交互式编辑器选择

### Decision: Rich Prompt.ask

**Rationale**:
- **简洁API**: 一行代码实现选择
- **验证**: 自动验证choices
- **美观**: Rich样式一致
- **键盘友好**: 上下箭头或数字选择

**Implementation**:
```python
from rich.prompt import Prompt

editor = Prompt.ask(
    "选择AI编辑器",
    choices=["Cursor", "Claude"],
    default="Cursor"
)

# 或使用Confirm进行二选一
use_cursor = Confirm.ask("使用Cursor编辑器？", default=True)
editor = "Cursor" if use_cursor else "Claude"
```

---

## Summary

### 核心技术栈
- **Python**: 3.8+ (兼容性)
- **CLI**: Typer (类型安全、自动文档)
- **UI**: Rich (美观、跨平台)
- **HTTP**: httpx (现代、进度支持)
- **测试**: pytest (标准选择)

### 关键决策
1. **简单架构**: 单一Python包，无复杂抽象
2. **直接API调用**: 避免SDK依赖
3. **临时文件模式**: 下载即删，无本地缓存
4. **友好错误**: 100%提供建议操作
5. **跨平台优先**: pathlib + 信号处理

### 风险与缓解
| 风险 | 缓解策略 |
|------|---------|
| GitHub API限流 | 支持GITHUB_TOKEN，显示友好错误 |
| 网络不稳定 | 超时控制，重试建议 |
| 磁盘空间不足 | 预检查，临时文件小于5MB |
| 跨平台差异 | pathlib统一，信号处理测试 |

### 下一步 (Phase 1)
- 定义数据模型（Editor枚举、Config类）
- 生成CLI接口规范
- 编写quickstart文档

