#!/bin/bash
# Quick install script for MyQuery
# Usage: curl -sSL https://install.myquery.dev | bash

set -e

VERSION="latest"
GITHUB_REPO="myquery/myquery"
INSTALL_DIR="$HOME/.local/bin"

echo "🚀 Installing MyQuery..."

# Detect OS and architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

case "$OS" in
    linux*)
        PLATFORM="linux"
        ;;
    darwin*)
        PLATFORM="macos"
        ;;
    *)
        echo "❌ Unsupported operating system: $OS"
        exit 1
        ;;
esac

case "$ARCH" in
    x86_64|amd64)
        ARCH="x86_64"
        ;;
    arm64|aarch64)
        ARCH="arm64"
        ;;
    *)
        echo "❌ Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

echo "📦 Platform: $PLATFORM-$ARCH"

# Get latest version if not specified
if [ "$VERSION" = "latest" ]; then
    echo "🔍 Fetching latest version..."
    VERSION=$(curl -s "https://api.github.com/repos/$GITHUB_REPO/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
    if [ -z "$VERSION" ]; then
        echo "❌ Failed to fetch latest version"
        exit 1
    fi
    echo "✅ Latest version: $VERSION"
fi

# Download URL
ARCHIVE_NAME="myquery-${PLATFORM}-${ARCH}.tar.gz"
DOWNLOAD_URL="https://github.com/$GITHUB_REPO/releases/download/$VERSION/$ARCHIVE_NAME"

echo "⬇️  Downloading from: $DOWNLOAD_URL"

# Create temp directory
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"

# Download binary
if ! curl -L -o "$ARCHIVE_NAME" "$DOWNLOAD_URL"; then
    echo "❌ Failed to download MyQuery"
    rm -rf "$TMP_DIR"
    exit 1
fi

# Extract
echo "📦 Extracting..."
tar -xzf "$ARCHIVE_NAME"

# Create install directory
mkdir -p "$INSTALL_DIR"

# Install binary
echo "📥 Installing to $INSTALL_DIR..."
mv myquery "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/myquery"

# Cleanup
cd - > /dev/null
rm -rf "$TMP_DIR"

echo "✅ MyQuery installed successfully!"
echo ""

# Check if install dir is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "⚠️  $INSTALL_DIR is not in your PATH."
    echo ""
    echo "Add it by running:"
    echo ""
    
    SHELL_RC=""
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.profile"
    fi
    
    echo "  echo 'export PATH=\"$INSTALL_DIR:\$PATH\"' >> $SHELL_RC"
    echo "  source $SHELL_RC"
    echo ""
fi

echo "🎉 Quick Start:"
echo ""
echo "  myquery --help           # Show help"
echo "  myquery connect          # Connect to a database"
echo "  myquery chat             # Start interactive chat"
echo ""
echo "📚 Documentation: https://github.com/$GITHUB_REPO"

