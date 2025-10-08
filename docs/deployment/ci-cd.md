# 🔄 CI/CD Pipeline

Dokumentasi lengkap tentang Continuous Integration dan Continuous Deployment setup untuk MyQuery.

## 🏗️ Architecture Overview

MyQuery menggunakan GitHub Actions untuk CI/CD pipeline dengan workflow berikut:

```
┌─────────────┐
│   Push to   │
│    main     │
└──────┬──────┘
       │
       ├──────────────────────────────────────┐
       │                                      │
       ▼                                      ▼
┌─────────────┐                      ┌──────────────┐
│  CI Tests   │                      │   Docker     │
│  & Linting  │                      │    Build     │
└──────┬──────┘                      └──────┬───────┘
       │                                    │
       │                                    ▼
       │                            ┌──────────────┐
       │                            │  Push to     │
       │                            │    GHCR      │
       │                            └──────────────┘
       │
       ▼
┌─────────────┐
│  Tag Push   │
│   (v*.*)    │
└──────┬──────┘
       │
       ├──────────────────────────────────────┬──────────────────┐
       │                                      │                  │
       ▼                                      ▼                  ▼
┌─────────────┐                      ┌──────────────┐   ┌──────────────┐
│   Build     │                      │  Publish to  │   │   Update     │
│  Binaries   │────────────┐         │    PyPI      │   │  Homebrew    │
│  & Install  │            │         └──────────────┘   └──────────────┘
└─────────────┘            │
                           │
                           ▼
                   ┌──────────────┐
                   │   Create     │
                   │   GitHub     │
                   │   Release    │
                   └──────────────┘
```

## 📋 Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)

**Trigger:** Push atau PR ke `main` atau `develop`

**Jobs:**

#### Lint
- Run Black (code formatting)
- Run Ruff (linting)
- Run MyPy (type checking)

#### Test
- Test pada Python 3.9, 3.10, 3.11
- Run pytest dengan coverage
- Upload coverage ke Codecov

#### Security
- Trivy vulnerability scan
- Upload hasil ke GitHub Security

**Example:**
```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: black --check .
      - run: ruff check .
      
  test:
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pytest tests/ --cov
```

### 2. Release Workflow (`.github/workflows/release.yml`)

**Trigger:** Push ke `main` atau tag `v*`

**Jobs:**

#### Test
- Full test suite sebelum build

#### Build Binaries
- Build untuk Linux (x86_64)
- Build untuk macOS (x86_64, arm64)
- Build untuk Windows (x86_64)
- Create tarball/zip packages
- Generate SHA256 checksums

#### Build Installers
- Build Windows installer (Inno Setup)
- Build macOS DMG
- Build Linux DEB package

#### Release
- Create GitHub Release
- Upload semua artifacts
- Generate release notes

#### Publish PyPI
- Build Python package
- Upload ke PyPI

#### Update Homebrew
- Update Homebrew tap formula

### 3. Docker Workflow (`.github/workflows/docker.yml`)

**Trigger:** Push ke `main` atau tag `v*`

**Jobs:**

#### Build and Push
- Build multi-platform (amd64, arm64)
- Push ke GitHub Container Registry
- Tag dengan version dan latest

## 🔐 Secrets Configuration

Setup GitHub secrets yang diperlukan:

### Required Secrets

```bash
# PyPI Token untuk publishing
PYPI_TOKEN=pypi-xxx...

# GitHub Token untuk update Homebrew tap
TAP_GITHUB_TOKEN=ghp_xxx...

# Optional: Codecov token
CODECOV_TOKEN=xxx...
```

### Setup Secrets

1. Buka repository Settings
2. Navigate ke: Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add masing-masing secret

**PyPI Token:**
```bash
# Login ke https://pypi.org
# Account Settings → API tokens → Add API token
# Scope: Project (myquery)
# Copy token dan save sebagai PYPI_TOKEN
```

**Homebrew Tap Token:**
```bash
# Buat personal access token di GitHub
# Settings → Developer settings → Personal access tokens
# Scope: repo
# Save sebagai TAP_GITHUB_TOKEN
```

## 🎯 Build Process

### Binary Build dengan PyInstaller

Script: `scripts/build_binary.py`

**Features:**
- Single executable file
- Include semua dependencies
- Platform-specific optimizations
- Asset bundling

**Command:**
```bash
python scripts/build_binary.py --platform linux
```

**Output:**
- `dist/myquery` (Linux/macOS)
- `dist/myquery.exe` (Windows)

### Installer Build

#### Windows (Inno Setup)
```bash
# Script: scripts/windows-installer.iss
iscc scripts/windows-installer.iss

# Output: dist/myquery-setup-windows.exe
```

**Features:**
- GUI installer
- Auto PATH configuration
- Start menu shortcuts
- Uninstaller

#### macOS (DMG)
```bash
# Script: scripts/build-macos-dmg.sh
bash scripts/build-macos-dmg.sh

# Output: dist/myquery-setup-macos.dmg
```

**Features:**
- Drag-and-drop installer
- Installation script
- README included

#### Linux (DEB)
```bash
# Script: scripts/build-linux-deb.sh
bash scripts/build-linux-deb.sh

# Output: dist/myquery-setup-linux.deb
```

**Features:**
- Debian package
- Auto dependency resolution
- Man page included
- Post-install scripts

## 🐳 Docker Build

### Multi-stage Build

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt
COPY . .
RUN pip install --user -e .

# Stage 2: Runtime
FROM python:3.11-slim
COPY --from=builder /root/.local /home/myquery/.local
USER myquery
ENTRYPOINT ["myquery"]
```

### Multi-platform Support

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ghcr.io/myquery/myquery:latest \
  --push .
```

## 📊 Monitoring & Notifications

### GitHub Actions Status

Check status di:
- Repository → Actions tab
- Commit status checks
- PR checks

### Notifications

Setup notifications untuk:
- Failed workflows
- Successful releases
- Security issues

**Slack Integration:**
```yaml
- name: Slack Notification
  if: failure()
  uses: rtCamp/action-slack-notify@v2
  env:
    SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
```

## 🧪 Testing Pipeline

### Local Testing

Test workflows locally dengan [act](https://github.com/nektos/act):

```bash
# Install act
# macOS
brew install act

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run CI workflow
act -j lint
act -j test

# Run release workflow
act -j build --secret-file .secrets
```

### Test Release Locally

```bash
# Test build process
python scripts/build_binary.py

# Test installer (Linux)
bash scripts/build-linux-deb.sh

# Install dan test
sudo dpkg -i dist/myquery-setup-linux.deb
myquery --version
```

## 🔄 Continuous Deployment

### Auto-deploy Strategy

- **main branch**: Auto-deploy dev version ke GHCR
- **v* tags**: Full release dengan binaries dan installers
- **develop branch**: Test builds only

### Deployment Targets

1. **GitHub Releases** - Binary downloads
2. **PyPI** - Python package
3. **GHCR** - Docker images
4. **Homebrew** - macOS package manager

## 📈 Metrics & Analytics

### Build Metrics

Monitor:
- Build success rate
- Build duration
- Binary sizes
- Test coverage

### Release Metrics

Track:
- Release frequency
- Download counts
- Platform distribution
- Version adoption

## 🔧 Maintenance

### Update Dependencies

```bash
# Update Python dependencies
pip-compile requirements.in > requirements.txt

# Update GitHub Actions
# Dependabot akan create PRs otomatis
```

### Setup Dependabot

`.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## 🆘 Troubleshooting

### Build Failures

**Symptoms:** Binary build fails

**Solutions:**
```bash
# Check PyInstaller logs
cat build/myquery/warn-myquery.txt

# Test locally
python scripts/build_binary.py --platform linux

# Check hidden imports
pyinstaller --debug=imports cli/main.py
```

### Workflow Failures

**Check:**
1. Secrets configured correctly
2. Dependencies versions compatible
3. Platform-specific issues
4. Network/download issues

**Debug:**
```bash
# Enable debug logging
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

### Deployment Issues

**PyPI:**
- Verify token valid
- Check version not already exists
- Test with TestPyPI first

**Docker:**
- Check GHCR permissions
- Verify multi-platform setup
- Test build locally

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller Manual](https://pyinstaller.org/en/stable/)
- [Docker Multi-platform Builds](https://docs.docker.com/build/building/multi-platform/)
- [PyPI Publishing Guide](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)

## 🔗 Related Docs

- [Release Process](release-process.md)
- [Contributing Guide](../../CONTRIBUTING.md)
- [Installation Guide](../installation/binary.md)

