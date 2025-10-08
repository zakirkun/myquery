#!/usr/bin/env python3
"""Build script for creating standalone executables using PyInstaller."""

import os
import sys
import shutil
import argparse
import platform
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"


def clean_build_dirs():
    """Clean previous build artifacts."""
    print("🧹 Cleaning previous build artifacts...")
    for dir_path in [DIST_DIR, BUILD_DIR]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
    DIST_DIR.mkdir(exist_ok=True)


def get_pyinstaller_args(platform_name: str) -> list:
    """Get PyInstaller arguments for the current platform."""
    
    # Base arguments
    args = [
        "pyinstaller",
        "--name=myquery",
        "--onefile",
        "--clean",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR}",
        f"--specpath={BUILD_DIR}",
    ]
    
    # Add entry point
    args.append(str(PROJECT_ROOT / "cli" / "main.py"))
    
    # Hidden imports (dependencies that PyInstaller might miss)
    hidden_imports = [
        "langchain",
        "langchain_openai",
        "langchain_community",
        "openai",
        "typer",
        "rich",
        "sqlalchemy",
        "psycopg2",
        "pymysql",
        "fastapi",
        "uvicorn",
        "plotly",
        "matplotlib",
        "pandas",
        "websockets",
        "pydantic",
        "pydantic_settings",
        "dotenv",
    ]
    
    for imp in hidden_imports:
        args.append(f"--hidden-import={imp}")
    
    # Data files to include
    data_files = [
        (PROJECT_ROOT / "assets", "assets"),
        (PROJECT_ROOT / "README.md", "."),
        (PROJECT_ROOT / "LICENSE", "."),
    ]
    
    for src, dst in data_files:
        if src.exists():
            args.append(f"--add-data={src}{os.pathsep}{dst}")
    
    # Platform-specific options
    if platform_name == "windows":
        args.extend([
            "--console",
            f"--icon={PROJECT_ROOT / 'assets' / 'myquery-logo.png'}",
            "--version-file=version.txt",  # We'll create this
        ])
    elif platform_name == "macos":
        args.extend([
            "--console",
            f"--icon={PROJECT_ROOT / 'assets' / 'myquery-logo.png'}",
            "--osx-bundle-identifier=dev.myquery.cli",
        ])
    else:  # linux
        args.extend([
            "--console",
        ])
    
    # Optimization
    args.extend([
        "--strip",
        "--optimize=2",
    ])
    
    return args


def create_version_file():
    """Create Windows version file."""
    version_content = """
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(0, 1, 0, 0),
    prodvers=(0, 1, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '040904B0',
        [StringStruct('CompanyName', 'MyQuery Team'),
        StringStruct('FileDescription', 'AI-powered database query assistant'),
        StringStruct('FileVersion', '0.1.0'),
        StringStruct('InternalName', 'myquery'),
        StringStruct('LegalCopyright', 'Copyright (c) 2025 MyQuery Team'),
        StringStruct('OriginalFilename', 'myquery.exe'),
        StringStruct('ProductName', 'MyQuery'),
        StringStruct('ProductVersion', '0.1.0')])
      ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""
    with open(PROJECT_ROOT / "version.txt", "w") as f:
        f.write(version_content)


def build(platform_name: str):
    """Build the executable."""
    print(f"🔨 Building myquery for {platform_name}...")
    
    # Clean previous builds
    clean_build_dirs()
    
    # Create version file for Windows
    if platform_name == "windows":
        create_version_file()
    
    # Get PyInstaller arguments
    args = get_pyinstaller_args(platform_name)
    
    # Run PyInstaller
    import subprocess
    result = subprocess.run(args, cwd=PROJECT_ROOT)
    
    if result.returncode != 0:
        print("❌ Build failed!")
        sys.exit(1)
    
    print(f"✅ Build successful! Binary located at: {DIST_DIR}")
    
    # List files in dist
    print("\n📦 Generated files:")
    for file in DIST_DIR.iterdir():
        size = file.stat().st_size / (1024 * 1024)  # MB
        print(f"  - {file.name} ({size:.2f} MB)")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Build myquery binary")
    parser.add_argument(
        "--platform",
        choices=["linux", "macos", "windows"],
        default=platform.system().lower(),
        help="Target platform (default: current platform)",
    )
    
    args = parser.parse_args()
    
    # Normalize platform name
    platform_map = {
        "darwin": "macos",
        "win32": "windows",
    }
    platform_name = platform_map.get(args.platform, args.platform)
    
    print("=" * 60)
    print("🚀 MyQuery Binary Builder")
    print("=" * 60)
    print(f"Platform: {platform_name}")
    print(f"Python: {sys.version}")
    print(f"Project Root: {PROJECT_ROOT}")
    print("=" * 60)
    print()
    
    build(platform_name)
    
    print("\n" + "=" * 60)
    print("✨ Build complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

