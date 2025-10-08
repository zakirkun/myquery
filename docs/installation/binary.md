# 📦 Instalasi Binary

Panduan lengkap untuk instalasi MyQuery menggunakan pre-built binary.

## 📥 Download Binary

### Otomatis (Recommended)

**Linux & macOS:**
```bash
curl -sSL https://install.myquery.dev | bash
```

atau dari GitHub:
```bash
curl -sSL https://raw.githubusercontent.com/myquery/myquery/main/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
# Coming soon
iwr -useb https://install.myquery.dev/windows | iex
```

### Manual

1. Kunjungi [GitHub Releases](https://github.com/zakirkun/myquery/releases)
2. Download binary untuk platform Anda:
   - **Linux**: `myquery-linux-x86_64.tar.gz`
   - **macOS (Intel)**: `myquery-macos-x86_64.tar.gz`
   - **macOS (Apple Silicon)**: `myquery-macos-arm64.tar.gz`
   - **Windows**: `myquery-windows-x86_64.zip`

## 🔧 Instalasi Manual

### Linux

```bash
# Download
wget https://github.com/zakirkun/myquery/releases/latest/download/myquery-linux-x86_64.tar.gz

# Verify checksum (optional)
wget https://github.com/zakirkun/myquery/releases/latest/download/myquery-linux-x86_64.tar.gz.sha256
sha256sum -c myquery-linux-x86_64.tar.gz.sha256

# Extract
tar -xzf myquery-linux-x86_64.tar.gz

# Move to bin directory
sudo mv myquery /usr/local/bin/

# Or for user-only install
mkdir -p ~/.local/bin
mv myquery ~/.local/bin/

# Make executable
chmod +x ~/.local/bin/myquery

# Add to PATH (if using ~/.local/bin)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### macOS

```bash
# Download
curl -L -o myquery-macos.tar.gz \
  https://github.com/zakirkun/myquery/releases/latest/download/myquery-macos-x86_64.tar.gz

# For Apple Silicon, use:
# curl -L -o myquery-macos.tar.gz \
#   https://github.com/zakirkun/myquery/releases/latest/download/myquery-macos-arm64.tar.gz

# Verify checksum (optional)
curl -L -o myquery-macos.tar.gz.sha256 \
  https://github.com/zakirkun/myquery/releases/latest/download/myquery-macos-x86_64.tar.gz.sha256
shasum -a 256 -c myquery-macos.tar.gz.sha256

# Extract
tar -xzf myquery-macos.tar.gz

# Move to bin directory
sudo mv myquery /usr/local/bin/

# Or for user-only install
mkdir -p ~/.local/bin
mv myquery ~/.local/bin/

# Make executable
chmod +x ~/.local/bin/myquery

# Add to PATH (if using ~/.local/bin)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### macOS Security Note

Saat pertama kali menjalankan, macOS mungkin memblokir binary karena tidak di-sign:

```bash
# Izinkan binary untuk dijalankan
xattr -d com.apple.quarantine ~/.local/bin/myquery
```

Atau melalui System Preferences:
1. Buka System Preferences → Security & Privacy
2. Klik "Open Anyway" untuk myquery

### Windows

**PowerShell:**
```powershell
# Download
Invoke-WebRequest -Uri "https://github.com/zakirkun/myquery/releases/latest/download/myquery-windows-x86_64.zip" -OutFile "myquery.zip"

# Extract
Expand-Archive -Path myquery.zip -DestinationPath $env:USERPROFILE\myquery

# Add to PATH (User level)
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
[Environment]::SetEnvironmentVariable("Path", "$userPath;$env:USERPROFILE\myquery", "User")

# Reload PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

**Command Prompt:**
```cmd
# Restart terminal setelah mengubah PATH, kemudian test:
myquery --version
```

## ✅ Verifikasi Instalasi

```bash
# Cek versi
myquery --version

# Output yang diharapkan:
# myquery v0.1.0
# AI-powered CLI for natural language database interactions
# Built with ❤️ using LangChain, OpenAI, and Typer

# Cek command help
myquery --help

# Cek system info
myquery info
```

## 🔄 Update Binary

### Otomatis

```bash
# Jalankan ulang install script
curl -sSL https://install.myquery.dev | bash
```

### Manual

1. Download versi terbaru dari [Releases](https://github.com/zakirkun/myquery/releases)
2. Replace binary lama dengan yang baru
3. Verifikasi versi baru:
   ```bash
   myquery --version
   ```

## 🗑️ Uninstall

### Linux & macOS

```bash
# Jika installed di /usr/local/bin
sudo rm /usr/local/bin/myquery

# Jika installed di ~/.local/bin
rm ~/.local/bin/myquery

# Hapus konfigurasi (optional)
rm -rf ~/.myquery
```

### Windows

```powershell
# Hapus binary
Remove-Item -Path "$env:USERPROFILE\myquery" -Recurse

# Hapus dari PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$newPath = ($userPath.Split(';') | Where-Object { $_ -ne "$env:USERPROFILE\myquery" }) -join ';'
[Environment]::SetEnvironmentVariable("Path", $newPath, "User")

# Hapus konfigurasi (optional)
Remove-Item -Path "$env:USERPROFILE\.myquery" -Recurse
```

## 🆘 Troubleshooting

### Command not found

**Masalah:** `myquery: command not found`

**Solusi:**
```bash
# Pastikan binary ada
ls -la ~/.local/bin/myquery

# Pastikan PATH sudah benar
echo $PATH | grep -o '.local/bin'

# Jika tidak ada, tambahkan ke PATH
export PATH="$HOME/.local/bin:$PATH"

# Tambahkan ke shell config agar permanen
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # atau ~/.zshrc
source ~/.bashrc  # atau ~/.zshrc
```

### Permission denied

**Masalah:** `permission denied: myquery`

**Solusi:**
```bash
chmod +x ~/.local/bin/myquery
```

### Library errors (Linux)

**Masalah:** `error while loading shared libraries`

**Solusi:**
```bash
# Ubuntu/Debian
sudo apt-get install -y libc6 libpq5

# Fedora/RHEL
sudo dnf install -y glibc postgresql-libs

# Arch
sudo pacman -S glibc postgresql-libs
```

### macOS Security Warning

**Masalah:** "myquery cannot be opened because the developer cannot be verified"

**Solusi:**
```bash
# Opsi 1: Command line
xattr -d com.apple.quarantine ~/.local/bin/myquery

# Opsi 2: GUI
# System Preferences → Security & Privacy → General → "Open Anyway"
```

### Windows Antivirus

**Masalah:** Antivirus memblokir myquery.exe

**Solusi:**
1. Tambahkan exception untuk `myquery.exe`
2. Atau download dari source terpercaya dan verifikasi checksum

## 📊 Perbandingan dengan Instalasi Lain

| Metode | Pros | Cons |
|--------|------|------|
| **Binary** | ✅ Cepat<br>✅ Tidak butuh Python<br>✅ Portable | ❌ Manual update<br>❌ Binary size besar |
| **PyPI** | ✅ Easy update<br>✅ Python ecosystem | ❌ Butuh Python<br>❌ Dependency conflicts |
| **Installer** | ✅ User-friendly<br>✅ Auto PATH setup | ❌ Platform-specific |
| **Source** | ✅ Latest features<br>✅ Customizable | ❌ Butuh build tools<br>❌ Kompleks |

## 🔗 Langkah Selanjutnya

- [Konfigurasi Awal](../getting-started.md#konfigurasi)
- [Quick Start Guide](../../QUICKSTART.md)
- [Troubleshooting](../troubleshooting.md)

