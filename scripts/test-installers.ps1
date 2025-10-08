# Test script untuk Windows installer
# Usage: .\scripts\test-installers.ps1

$ErrorActionPreference = "Stop"

Write-Host "🧪 MyQuery Installer Test Script (Windows)" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Check if PyInstaller is installed
Write-Host ""
Write-Host "📦 Installing PyInstaller..." -ForegroundColor Yellow
pip install pyinstaller | Out-Null

# Build binary
Write-Host ""
Write-Host "1️⃣ Building binary..." -ForegroundColor Yellow
python scripts/build_binary.py --platform windows

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Binary build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Binary built successfully" -ForegroundColor Green

# Check if Inno Setup is installed
$innoSetupPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

if (-not (Test-Path $innoSetupPath)) {
    Write-Host ""
    Write-Host "⚠️  Inno Setup not found" -ForegroundColor Yellow
    Write-Host "To build Windows installer, please:" -ForegroundColor Yellow
    Write-Host "  1. Install Inno Setup from https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
    Write-Host "  2. Or install via Chocolatey: choco install innosetup" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Binary is ready at: dist\myquery.exe" -ForegroundColor Green
    exit 0
}

# Build installer
Write-Host ""
Write-Host "2️⃣ Building Windows installer..." -ForegroundColor Yellow

# Create binary directory for installer
New-Item -ItemType Directory -Force -Path "dist\binary" | Out-Null
Copy-Item "dist\myquery.exe" "dist\binary\" -Force

# Run Inno Setup
& $innoSetupPath "scripts\windows-installer.iss"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Installer build failed!" -ForegroundColor Red
    exit 1
}

$installerFile = "dist\myquery-setup-windows.exe"

if (Test-Path $installerFile) {
    Write-Host "✅ Installer created: $installerFile" -ForegroundColor Green
    
    $fileSize = (Get-Item $installerFile).Length / 1MB
    Write-Host "📦 Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
    
    # Calculate SHA256
    $hash = Get-FileHash $installerFile -Algorithm SHA256
    $hash.Hash | Out-File -Encoding ASCII "$installerFile.sha256"
    
    Write-Host "📋 SHA256: $($hash.Hash)" -ForegroundColor Cyan
} else {
    Write-Host "❌ Installer not found: $installerFile" -ForegroundColor Red
    exit 1
}

# Test binary
Write-Host ""
Write-Host "3️⃣ Testing binary..." -ForegroundColor Yellow
& "dist\myquery.exe" --version

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Binary test passed!" -ForegroundColor Green
} else {
    Write-Host "❌ Binary test failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ Build complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📦 Binary: dist\myquery.exe" -ForegroundColor Cyan
Write-Host "📦 Installer: $installerFile" -ForegroundColor Cyan
Write-Host ""
Write-Host "To test installer:" -ForegroundColor Yellow
Write-Host "  1. Run $installerFile" -ForegroundColor Yellow
Write-Host "  2. Follow installation wizard" -ForegroundColor Yellow
Write-Host "  3. Test with: myquery --version" -ForegroundColor Yellow

