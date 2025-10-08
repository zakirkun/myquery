#!/bin/bash
# Build macOS DMG installer for MyQuery

set -e

VERSION="0.1.0"
APP_NAME="MyQuery"
DMG_NAME="myquery-setup-macos.dmg"
VOLUME_NAME="MyQuery Installer"

echo "🍎 Building macOS DMG installer..."

# Create temporary directory structure
TMP_DIR=$(mktemp -d)
APP_DIR="$TMP_DIR/$APP_NAME"

mkdir -p "$APP_DIR/bin"
mkdir -p "$APP_DIR/share/doc"

# Copy binary
cp dist/binary/myquery "$APP_DIR/bin/"
chmod +x "$APP_DIR/bin/myquery"

# Copy documentation
cp README.md "$APP_DIR/share/doc/"
cp LICENSE "$APP_DIR/share/doc/"

# Create install script
cat > "$APP_DIR/install.sh" <<'EOF'
#!/bin/bash
# MyQuery Installer

set -e

echo "🚀 Installing MyQuery..."

# Determine install location
if [ "$EUID" -eq 0 ]; then
    INSTALL_DIR="/usr/local/bin"
else
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
fi

# Copy binary
cp -f "$(dirname "$0")/bin/myquery" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/myquery"

echo "✅ MyQuery installed to $INSTALL_DIR/myquery"

# Add to PATH if needed
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "⚠️  Please add $INSTALL_DIR to your PATH:"
    echo ""
    if [ -f "$HOME/.zshrc" ]; then
        echo "  echo 'export PATH=\"$INSTALL_DIR:\$PATH\"' >> ~/.zshrc"
        echo "  source ~/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        echo "  echo 'export PATH=\"$INSTALL_DIR:\$PATH\"' >> ~/.bashrc"
        echo "  source ~/.bashrc"
    fi
fi

echo ""
echo "🎉 Installation complete! Run 'myquery --help' to get started."
EOF

chmod +x "$APP_DIR/install.sh"

# Create README
cat > "$APP_DIR/README.txt" <<EOF
MyQuery v$VERSION
=================

AI-powered CLI for natural language database interactions.

Installation:
1. Double-click on install.sh
2. Or run in Terminal: ./install.sh

After installation, run:
  myquery --help

For more information, visit:
https://github.com/zakirkun/myquery

EOF

# Create Applications symlink for easy access
ln -s /Applications "$TMP_DIR/Applications"

# Create DMG
echo "📦 Creating DMG..."
hdiutil create -volname "$VOLUME_NAME" \
    -srcfolder "$TMP_DIR" \
    -ov -format UDZO \
    "dist/$DMG_NAME"

# Calculate SHA256
shasum -a 256 "dist/$DMG_NAME" > "dist/$DMG_NAME.sha256"

# Cleanup
rm -rf "$TMP_DIR"

echo "✅ DMG created: dist/$DMG_NAME"
echo "📋 SHA256: $(cat dist/$DMG_NAME.sha256)"

