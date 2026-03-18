# Copilot Instructions for pressEnterLater

## Project Overview

Python application using `uv` package manager that provides a TkInter GUI for scheduling automated key presses. Users can specify which key to press (e.g., Enter), delay before starting, number of presses, frequency, and repeat count.

## Build & Development Commands

```bash
# Install dependencies with uv
uv sync

# Run the application
uv run python main.py

# Run tests (if configured)
uv run pytest

# Run single test file
uv run pytest tests/test_file.py

# Format code
uv run ruff format .

# Lint code
uv run ruff check .
```

## Building Releases

GitHub Actions workflow builds executables using PyInstaller for Windows, macOS, and Linux.

```bash
# Build executable locally
uv run pyinstaller main.py --onefile --windowed --name pressEnterLater
```

## Project Architecture

- **main.py**: Entry point, launches TkInter GUI
- **gui/**: TkInter interface components
- **keyboard/**: Key press automation logic (using `pynput` or similar)
- **scheduler/**: Timing and repeat logic

## Key Conventions

- Use `uv` for all dependency management (not pip directly)
- TkInter for GUI - keep it simple and functional
- Cross-platform key automation library (e.g., `pynput`)
- Configuration stored in simple data structures (no complex config files initially)
- PyInstaller for building standalone executables

## Dependencies

- Python 3.11+
- TkInter (included with Python)
- `pynput` or `keyboard` library for key automation
- `pyinstaller` for building executables
