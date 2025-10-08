#!/bin/bash
# Local build script untuk testing binary builds
# Usage: ./scripts/local-build.sh

set -e

echo "🔨 MyQuery Local Build Script"
echo "=============================="
echo ""

# Detect platform
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
case "$OS" in
    linux*)
        PLATFORM="linux"
        ;;
    darwin*)
        PLATFORM="macos"
        ;;
    mingw*|msys*|cygwin*)
        PLATFORM="windows"
        ;;
    *)
        echo "❌ Unsupported OS: $OS"
        exit 1
        ;;
esac

echo "📦 Platform: $PLATFORM"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
if [ "$PLATFORM" = "windows" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q pyinstaller

# Build binary
echo ""
echo "🔨 Building binary for $PLATFORM..."
python scripts/build_binary.py --platform "$PLATFORM"

# Check if build successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📦 Binary location:"
    ls -lh dist/
    
    # Test binary
    echo ""
    echo "🧪 Testing binary..."
    
    if [ "$PLATFORM" = "windows" ]; then
        dist/myquery.exe --version
    else
        dist/myquery --version
    fi
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Binary test passed!"
        echo ""
        echo "🎉 Build complete! You can find the binary in: ./dist/"
    else
        echo ""
        echo "❌ Binary test failed!"
        exit 1
    fi
else
    echo ""
    echo "❌ Build failed!"
    exit 1
fi

# Deactivate virtual environment
deactivate

echo ""
echo "=============================="
echo "Build completed successfully!"

