#!/bin/bash
# Test script untuk installers
# Usage: ./scripts/test-installers.sh

set -e

echo "🧪 MyQuery Installer Test Script"
echo "================================="
echo ""

# Detect platform
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
case "$OS" in
    linux*)
        PLATFORM="linux"
        INSTALLER="deb"
        ;;
    darwin*)
        PLATFORM="macos"
        INSTALLER="dmg"
        ;;
    *)
        echo "❌ Unsupported OS for this script: $OS"
        echo "For Windows, run test-installers.ps1"
        exit 1
        ;;
esac

echo "📦 Platform: $PLATFORM"
echo "📦 Installer type: $INSTALLER"
echo ""

# First build binary
echo "1️⃣ Building binary..."
bash scripts/local-build.sh

# Build installer
echo ""
echo "2️⃣ Building installer..."

if [ "$PLATFORM" = "linux" ]; then
    bash scripts/build-linux-deb.sh
    INSTALLER_FILE="dist/myquery-setup-linux.deb"
elif [ "$PLATFORM" = "macos" ]; then
    bash scripts/build-macos-dmg.sh
    INSTALLER_FILE="dist/myquery-setup-macos.dmg"
fi

# Check if installer was created
if [ -f "$INSTALLER_FILE" ]; then
    echo "✅ Installer created: $INSTALLER_FILE"
    ls -lh "$INSTALLER_FILE"
else
    echo "❌ Installer not found: $INSTALLER_FILE"
    exit 1
fi

# Test installation (requires sudo for real install)
echo ""
echo "3️⃣ Testing installer..."

if [ "$PLATFORM" = "linux" ]; then
    echo ""
    echo "To test DEB package installation, run:"
    echo "  sudo dpkg -i $INSTALLER_FILE"
    echo ""
    echo "To verify:"
    echo "  myquery --version"
    echo ""
    echo "To uninstall:"
    echo "  sudo apt remove myquery"
    
elif [ "$PLATFORM" = "macos" ]; then
    echo ""
    echo "To test DMG installation:"
    echo "  1. Open $INSTALLER_FILE"
    echo "  2. Run install.sh"
    echo "  3. Test with: myquery --version"
fi

echo ""
echo "================================="
echo "Installer build complete!"
echo ""
echo "📦 Installer: $INSTALLER_FILE"
echo "📋 SHA256: $(cat ${INSTALLER_FILE}.sha256 2>/dev/null || echo 'Not generated')"

