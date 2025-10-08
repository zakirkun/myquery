#!/bin/bash
# Build Debian package for MyQuery

set -e

VERSION="0.1.0"
ARCH="amd64"
PACKAGE_NAME="myquery"
DEB_NAME="${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"

echo "🐧 Building Debian package..."

# Create package structure
DEB_DIR="dist/deb"
mkdir -p "$DEB_DIR/DEBIAN"
mkdir -p "$DEB_DIR/usr/local/bin"
mkdir -p "$DEB_DIR/usr/share/doc/$PACKAGE_NAME"
mkdir -p "$DEB_DIR/usr/share/man/man1"

# Copy binary
cp dist/binary/myquery "$DEB_DIR/usr/local/bin/"
chmod 755 "$DEB_DIR/usr/local/bin/myquery"

# Copy documentation
cp README.md "$DEB_DIR/usr/share/doc/$PACKAGE_NAME/"
cp LICENSE "$DEB_DIR/usr/share/doc/$PACKAGE_NAME/copyright"

# Create control file
cat > "$DEB_DIR/DEBIAN/control" <<EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: database
Priority: optional
Architecture: $ARCH
Maintainer: MyQuery Team <team@myquery.dev>
Description: AI-powered CLI for natural language database interactions
 MyQuery is an intelligent command-line tool that allows you to interact
 with databases using natural language. It combines the power of AI with
 traditional database operations to make querying easier and more intuitive.
 .
 Features:
  - Natural language to SQL conversion
  - Support for PostgreSQL, MySQL, and SQLite
  - Data visualization and export
  - Multi-database querying
  - Web UI interface
Depends: libc6 (>= 2.27)
Homepage: https://github.com/zakirkun/myquery
EOF

# Create postinst script
cat > "$DEB_DIR/DEBIAN/postinst" <<'EOF'
#!/bin/bash
set -e

echo "✅ MyQuery installed successfully!"
echo ""
echo "🚀 Quick Start:"
echo "  myquery --help           # Show help"
echo "  myquery connect          # Connect to a database"
echo "  myquery chat             # Start interactive chat"
echo ""
echo "📚 Documentation: https://github.com/zakirkun/myquery"
echo ""

# Check if /usr/local/bin is in PATH
if [[ ":$PATH:" != *":/usr/local/bin:"* ]]; then
    echo "⚠️  /usr/local/bin is not in your PATH."
    echo "   Add it to your PATH by adding this to your ~/.bashrc or ~/.zshrc:"
    echo '   export PATH="/usr/local/bin:$PATH"'
    echo ""
fi

exit 0
EOF

chmod 755 "$DEB_DIR/DEBIAN/postinst"

# Create prerm script
cat > "$DEB_DIR/DEBIAN/prerm" <<'EOF'
#!/bin/bash
set -e
exit 0
EOF

chmod 755 "$DEB_DIR/DEBIAN/prerm"

# Create man page
cat > "$DEB_DIR/usr/share/man/man1/myquery.1" <<'EOF'
.TH MYQUERY 1 "2025" "MyQuery 0.1.0" "User Commands"
.SH NAME
myquery \- AI-powered CLI for natural language database interactions
.SH SYNOPSIS
.B myquery
[\fIOPTION\fR]... [\fICOMMAND\fR]
.SH DESCRIPTION
MyQuery is an intelligent command-line tool that allows you to interact with
databases using natural language. It converts plain English queries into SQL
and provides visualizations and insights.
.SH OPTIONS
.TP
.B \-\-help
Show help message and exit
.TP
.B \-\-version
Show version information
.TP
.B \-\-debug, \-d
Enable debug mode with detailed logging
.SH COMMANDS
.TP
.B connect
Connect to a database
.TP
.B chat
Start interactive chat session
.TP
.B query
Execute a single query
.TP
.B visualize
Generate data visualizations
.TP
.B export
Export query results
.TP
.B server
Manage MCP server
.TP
.B web
Start web UI server
.SH EXAMPLES
.TP
Connect to a PostgreSQL database:
.B myquery connect --db-type postgresql --db-name mydb
.TP
Start interactive chat:
.B myquery chat
.TP
Execute a natural language query:
.B myquery query "Show me the top 10 customers by sales"
.SH FILES
.TP
.I ~/.myquery/config.yaml
User configuration file
.TP
.I ~/.myquery/history.db
Query history database
.SH SEE ALSO
Full documentation at: https://github.com/zakirkun/myquery
.SH AUTHOR
MyQuery Team <team@myquery.dev>
EOF

gzip "$DEB_DIR/usr/share/man/man1/myquery.1"

# Build package
dpkg-deb --build "$DEB_DIR" "dist/$DEB_NAME"

# Rename to standard name
mv "dist/$DEB_NAME" "dist/myquery-setup-linux.deb"

# Calculate SHA256
sha256sum "dist/myquery-setup-linux.deb" > "dist/myquery-setup-linux.deb.sha256"

# Cleanup
rm -rf "$DEB_DIR"

echo "✅ Debian package created: dist/myquery-setup-linux.deb"
echo "📋 SHA256: $(cat dist/myquery-setup-linux.deb.sha256)"

