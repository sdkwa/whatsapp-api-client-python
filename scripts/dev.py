"""Makefile-like commands for development."""

import glob
import shutil
import subprocess
import sys
from pathlib import Path

def run_command(command: str) -> int:
    """Run a shell command and return exit code."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True)
    return result.returncode

def install():
    """Install package in development mode."""
    return run_command("pip install -e .")

def format_code():
    """Format code."""
    commands = [
        "black sdkwa examples",
        "isort sdkwa examples"
    ]
    
    for cmd in commands:
        if run_command(cmd) != 0:
            return 1
    return 0

def clean():
    """Clean build artifacts."""
    paths_to_clean = [
        "build",
        "dist", 
        "*.egg-info"
    ]
    
    # Clean specific paths
    for pattern in paths_to_clean:
        if "*" in pattern:
            # Handle glob patterns
            for path in glob.glob(pattern):
                if Path(path).exists():
                    if Path(path).is_dir():
                        shutil.rmtree(path)
                    else:
                        Path(path).unlink()
        else:
            # Handle direct paths
            path = Path(pattern)
            if path.exists():
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
    
    # Clean __pycache__ recursively
    for pycache in Path(".").rglob("__pycache__"):
        shutil.rmtree(pycache)
    
    print("Cleaned build artifacts")
    return 0

def build():
    """Build package."""
    clean()
    return run_command("python -m build")

def publish_test():
    """Publish to test PyPI."""
    return run_command("twine upload --repository testpypi dist/*")

def publish():
    """Publish to PyPI."""
    return run_command("twine upload dist/*")

def help_cmd():
    """Show available commands."""
    print("Available commands:")
    print("  install     - Install package in development mode")
    print("  format      - Format code")
    print("  clean       - Clean build artifacts")
    print("  build       - Build package")
    print("  publish-test - Publish to test PyPI")
    print("  publish     - Publish to PyPI")
    print("  help        - Show this help")

if __name__ == "__main__":
    commands = {
        "install": install,
        "format": format_code,
        "clean": clean,
        "build": build,
        "publish-test": publish_test,
        "publish": publish,
        "help": help_cmd,
    }
    
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        help_cmd()
        sys.exit(1)
    
    command = sys.argv[1]
    exit_code = commands[command]()
    sys.exit(exit_code)
