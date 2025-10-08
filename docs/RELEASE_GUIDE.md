# 🚀 Panduan Release Cepat

Panduan singkat untuk melakukan release MyQuery.

## 📝 Quick Release Checklist

1. ✅ Semua tests passing
2. ✅ Documentation updated
3. ✅ CHANGELOG updated
4. ✅ Version bump ready

## 🎯 Cara Melakukan Release

### Opsi 1: Otomatis dengan GitHub Actions (Recommended)

1. **Buka GitHub Actions di repository**
2. **Pilih workflow "Version Bump"**
3. **Click "Run workflow"**
4. **Pilih version type:**
   - `patch` - Bug fixes (0.1.0 → 0.1.1)
   - `minor` - New features (0.1.0 → 0.2.0)
   - `major` - Breaking changes (0.1.0 → 1.0.0)
5. **Click "Run workflow"**

GitHub Actions akan otomatis:
- Update version di semua file
- Update CHANGELOG
- Create git tag
- Build binaries untuk semua platform
- Create installers (DEB, DMG, EXE)
- Build Docker images
- Publish ke PyPI
- Update Homebrew tap
- Create GitHub Release dengan semua artifacts

### Opsi 2: Manual

```bash
# 1. Update version manually
# Edit pyproject.toml, cli/main.py, CHANGELOG.md

# 2. Commit changes
git add .
git commit -m "chore: bump version to 0.2.0"
git push

# 3. Create and push tag
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0

# GitHub Actions akan otomatis build dan release
```

## 🔍 Monitoring Release

### Cek Status Build

1. **Buka tab "Actions" di GitHub**
2. **Lihat workflow "Build and Release"**
3. **Monitor progress:**
   - ✅ Tests
   - 🔨 Build binaries
   - 📦 Create installers
   - 🚀 Create release

### Verify Release

Setelah release selesai, verifikasi:

```bash
# Cek GitHub Releases
https://github.com/myquery/myquery/releases

# Verify downloads tersedia:
- myquery-linux-x86_64.tar.gz
- myquery-macos-x86_64.tar.gz
- myquery-macos-arm64.tar.gz
- myquery-windows-x86_64.zip
- myquery-setup-linux.deb
- myquery-setup-macos.dmg
- myquery-setup-windows.exe
```

## 🐛 Hotfix Release

Untuk critical bugs:

```bash
# 1. Create hotfix branch
git checkout -b hotfix/0.2.1 v0.2.0

# 2. Fix bug dan commit
git commit -am "fix: critical bug X"

# 3. Update version ke 0.2.1
# Edit pyproject.toml, cli/main.py, CHANGELOG.md

# 4. Create tag
git tag -a v0.2.1 -m "Hotfix v0.2.1"

# 5. Push
git push origin hotfix/0.2.1
git push origin v0.2.1

# 6. Merge back to main
git checkout main
git merge hotfix/0.2.1
git push
```

## 📊 Download Statistics

Cek download statistics di:
- GitHub Releases page
- PyPI stats: https://pypistats.org/packages/myquery
- Docker Hub insights

## 🆘 Troubleshooting

### Build gagal?

1. Cek logs di GitHub Actions
2. Verify semua secrets configured
3. Re-run failed jobs

### Release tidak muncul?

1. Cek apakah tag sudah di-push
2. Verify GitHub Actions completed
3. Check permissions

## 📚 Dokumentasi Lengkap

- [Release Process](deployment/release-process.md) - Panduan detail
- [CI/CD Pipeline](deployment/ci-cd.md) - Technical docs
- [Installation Guide](../INSTALL.md) - Untuk end users

## 🎯 Quick Commands

```bash
# Lihat current version
grep version pyproject.toml

# Lihat semua tags
git tag -l

# Delete tag (jika salah)
git tag -d v0.2.0
git push origin :refs/tags/v0.2.0

# Force re-run release
git tag -f v0.2.0
git push -f origin v0.2.0
```

