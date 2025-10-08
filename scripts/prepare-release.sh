#!/bin/bash
# Script untuk mempersiapkan release
# Usage: ./scripts/prepare-release.sh [patch|minor|major]

set -e

VERSION_TYPE=${1:-patch}

echo "🚀 Preparing MyQuery Release"
echo "=============================="
echo ""
echo "Version type: $VERSION_TYPE"
echo ""

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes"
    echo ""
    git status --short
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Get current version
CURRENT_VERSION=$(grep -Po '(?<=version = ")[^"]*' pyproject.toml)
echo "Current version: $CURRENT_VERSION"

# Calculate new version
IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

case "$VERSION_TYPE" in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
    *)
        echo "❌ Invalid version type: $VERSION_TYPE"
        echo "Use: patch, minor, or major"
        exit 1
        ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "New version: $NEW_VERSION"
echo ""

# Confirm
read -p "Proceed with release v$NEW_VERSION? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "📝 Updating version numbers..."

# Update pyproject.toml
sed -i.bak "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
rm pyproject.toml.bak

# Update cli/main.py
sed -i.bak "s/v$CURRENT_VERSION/v$NEW_VERSION/" cli/main.py
rm cli/main.py.bak

echo "✅ Version numbers updated"

# Update CHANGELOG
echo ""
echo "📝 Updating CHANGELOG.md..."

TODAY=$(date +%Y-%m-%d)
CHANGELOG_ENTRY="## [$NEW_VERSION] - $TODAY

### Added

### Changed

### Fixed

### Deprecated

### Removed

### Security

"

# Insert after first line
sed -i.bak "1 a\\
$CHANGELOG_ENTRY" CHANGELOG.md
rm CHANGELOG.md.bak

echo "✅ CHANGELOG.md updated"

# Run tests
echo ""
echo "🧪 Running tests..."

if command -v pytest &> /dev/null; then
    pytest tests/ -v
    echo "✅ Tests passed"
else
    echo "⚠️  pytest not found, skipping tests"
fi

# Show summary
echo ""
echo "=============================="
echo "✅ Release preparation complete!"
echo ""
echo "Changes made:"
echo "  - Version updated: $CURRENT_VERSION → $NEW_VERSION"
echo "  - CHANGELOG.md updated"
echo ""
echo "Next steps:"
echo "  1. Review and update CHANGELOG.md with actual changes"
echo "  2. Review changes: git diff"
echo "  3. Commit: git commit -am 'chore: bump version to $NEW_VERSION'"
echo "  4. Tag: git tag -a v$NEW_VERSION -m 'Release v$NEW_VERSION'"
echo "  5. Push: git push && git push --tags"
echo ""
echo "Or run:"
echo "  git add ."
echo "  git commit -m 'chore: bump version to $NEW_VERSION'"
echo "  git tag -a v$NEW_VERSION -m 'Release v$NEW_VERSION'"
echo "  git push origin main --tags"

