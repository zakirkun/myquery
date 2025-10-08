# 🚀 Release Process

Panduan lengkap untuk melakukan release MyQuery versi baru.

## 📋 Pre-Release Checklist

Sebelum melakukan release, pastikan:

- [ ] Semua tests passing
- [ ] Documentation sudah diupdate
- [ ] CHANGELOG.md sudah diupdate
- [ ] Version number sudah ditentukan (mengikuti [Semantic Versioning](https://semver.org/))
- [ ] Breaking changes sudah didokumentasikan
- [ ] Examples sudah diupdate jika ada perubahan API

## 🔢 Versioning

MyQuery menggunakan [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backwards compatible
- **PATCH** (0.0.X): Bug fixes, backwards compatible

### Contoh:
- `0.1.0` → `0.1.1`: Bug fix
- `0.1.0` → `0.2.0`: New feature
- `0.1.0` → `1.0.0`: Breaking change atau first stable release

## 📝 Update Version

### 1. Update pyproject.toml

```toml
[project]
name = "myquery"
version = "0.2.0"  # Update version di sini
```

### 2. Update cli/main.py

```python
@app.command()
def version():
    """Show version information."""
    console.print(Panel(
        "[bold cyan]myquery[/bold cyan] [dim]v0.2.0[/dim]\n\n"  # Update di sini
        # ...
    ))
```

### 3. Update CHANGELOG.md

```markdown
## [0.2.0] - 2025-01-15

### Added
- New feature X
- Support for Y

### Changed
- Improved Z

### Fixed
- Bug in component A

### Breaking Changes
- Renamed function B to C
```

## 🏷️ Create Release Tag

```bash
# Pastikan di branch main dan sudah update
git checkout main
git pull origin main

# Create dan push tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

## 🤖 Automated Release Process

Setelah tag di-push, GitHub Actions akan otomatis:

1. ✅ **Run Tests** - Memastikan semua tests passing
2. 🔨 **Build Binaries** - Untuk Linux, macOS, dan Windows
3. 📦 **Create Installers** - DEB, DMG, dan EXE
4. 🐳 **Build Docker Image** - Push ke GHCR
5. 📚 **Publish to PyPI** - Upload package
6. 📋 **Create GitHub Release** - Dengan semua artifacts
7. 🍺 **Update Homebrew** - Update tap formula

### Workflow Files:

- `.github/workflows/release.yml` - Main release workflow
- `.github/workflows/docker.yml` - Docker build dan push
- `.github/workflows/ci.yml` - Continuous integration

## 📦 Manual Release (Jika Diperlukan)

### Build Binaries Locally

```bash
# Install PyInstaller
pip install pyinstaller

# Build untuk platform saat ini
python scripts/build_binary.py

# Build untuk platform spesifik
python scripts/build_binary.py --platform linux
python scripts/build_binary.py --platform macos
python scripts/build_binary.py --platform windows
```

### Create Installers

**Linux (DEB):**
```bash
bash scripts/build-linux-deb.sh
```

**macOS (DMG):**
```bash
bash scripts/build-macos-dmg.sh
```

**Windows (EXE):**
```powershell
# Membutuhkan Inno Setup
iscc scripts\windows-installer.iss
```

### Publish to PyPI

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Upload to PyPI
twine upload dist/*

# Atau upload ke TestPyPI dulu untuk testing
twine upload --repository testpypi dist/*
```

### Create GitHub Release

```bash
# Install GitHub CLI jika belum
# https://cli.github.com/

# Create release dengan artifacts
gh release create v0.2.0 \
  --title "MyQuery v0.2.0" \
  --notes-file RELEASE_NOTES.md \
  dist/*.tar.gz \
  dist/*.zip \
  dist/*.deb \
  dist/*.dmg \
  dist/*.exe
```

## 🐳 Docker Release

### Build dan Push Manual

```bash
# Build untuk multiple platforms
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 \
  -t ghcr.io/myquery/myquery:0.2.0 \
  -t ghcr.io/myquery/myquery:latest \
  --push .
```

### Tag Strategy

- `latest` - Latest stable release
- `v0.2.0` - Specific version
- `v0.2` - Minor version (auto-updated)
- `v0` - Major version (auto-updated)
- `main` - Latest from main branch
- `dev` - Development builds

## 📢 Post-Release Tasks

### 1. Announce Release

- [ ] Update website (jika ada)
- [ ] Post di social media
- [ ] Notify di Discord/Slack community
- [ ] Email mailing list subscribers

### 2. Update Documentation Sites

- [ ] Update docs website
- [ ] Update README.md badges
- [ ] Update installation guides

### 3. Monitor

- [ ] Check GitHub Issues untuk bug reports
- [ ] Monitor download statistics
- [ ] Check CI/CD pipelines
- [ ] Verify installers working di semua platforms

## 🔧 Hotfix Process

Untuk critical bugs yang perlu segera di-fix:

```bash
# Create hotfix branch dari tag
git checkout -b hotfix/0.2.1 v0.2.0

# Fix bug
# ... make changes ...

# Update version ke 0.2.1
# Update CHANGELOG.md

# Commit dan tag
git commit -am "Fix critical bug X"
git tag -a v0.2.1 -m "Hotfix release 0.2.1"

# Push
git push origin hotfix/0.2.1
git push origin v0.2.1

# Merge back to main
git checkout main
git merge hotfix/0.2.1
git push origin main
```

## 📊 Release Checklist Template

Copy ini untuk setiap release:

```markdown
## Release v0.X.Y Checklist

### Pre-Release
- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers updated in code
- [ ] Examples tested and working
- [ ] Breaking changes documented

### Release
- [ ] Tag created and pushed
- [ ] CI/CD pipeline completed successfully
- [ ] GitHub Release created
- [ ] PyPI package published
- [ ] Docker images published
- [ ] Homebrew formula updated

### Post-Release
- [ ] Release announcement posted
- [ ] Documentation sites updated
- [ ] Community notified
- [ ] Download links verified
- [ ] Installers tested on all platforms
- [ ] No critical issues reported

### Rollback Plan (if needed)
- [ ] Previous version tags documented
- [ ] Rollback procedure tested
```

## 🚨 Emergency Rollback

Jika release bermasalah:

```bash
# Hapus tag yang bermasalah
git tag -d v0.2.0
git push origin :refs/tags/v0.2.0

# Hapus release di GitHub
gh release delete v0.2.0

# Unpublish dari PyPI (contact PyPI support)
# PyPI tidak mengizinkan unpublish, hanya yank
# https://pypi.org/help/#yanked

# Revert commits jika perlu
git revert <commit-hash>
git push origin main
```

## 📚 Resources

- [Semantic Versioning](https://semver.org/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [PyPI Publishing](https://packaging.python.org/tutorials/packaging-projects/)
- [Keep a Changelog](https://keepachangelog.com/)

## 🆘 Troubleshooting

### CI/CD Pipeline Failing

1. Check GitHub Actions logs
2. Verify all secrets configured:
   - `PYPI_TOKEN`
   - `TAP_GITHUB_TOKEN`
3. Re-run failed jobs
4. Check for platform-specific issues

### Binary Build Issues

- Ensure all dependencies in requirements.txt
- Check PyInstaller hidden imports
- Verify binary works on target platform
- Test with fresh VM/container

### Publishing Issues

- Verify API tokens valid
- Check version number not already used
- Ensure package builds successfully
- Test with TestPyPI first

## 📞 Support

Butuh bantuan dengan release process?

- Open issue: [GitHub Issues](https://github.com/zakirkun/myquery/issues)
- Discord: [Join our server](#)
- Email: team@myquery.dev

