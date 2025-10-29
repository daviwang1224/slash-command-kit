# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Basic CLI framework with Typer
- Support for Cursor and Claude Code editors
- GitHub Release integration for template distribution
- **Interactive arrow-key selection for editor choice in `init` command** (Feature 002)
  - Visual selection interface using ↑/↓ arrow keys
  - Automatic fallback to default editor in non-interactive environments (CI/CD)
  - ESC to cancel, Ctrl+C to interrupt
  - Cross-platform keyboard support via `readchar`
- Force overwrite mode for updates
- Progress indicators for downloads
- Cross-platform support (Windows, macOS, Linux)
- Comprehensive error handling with friendly messages
- Environment variable configuration support

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- N/A (initial release)

## [0.1.0] - TBD

### Added
- Initial MVP release
- Core functionality for template deployment
- User Story 1: CLI installation from GitHub
- User Story 2: New project initialization
- CI/CD pipeline for automated releases

---

[Unreleased]: https://github.com/daviwang1224/slash-command-kit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/daviwang1224/slash-command-kit/releases/tag/v0.1.0

