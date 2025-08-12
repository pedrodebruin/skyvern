# Skyvern Windows Test Script
# Run this script in PowerShell to test Skyvern setup on Windows

Write-Host "🧪 Skyvern Windows Setup Test" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Test Python installation
Write-Host "`n🐍 Testing Python Installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Python installed: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Python not found" -ForegroundColor Red
        Write-Host "  💡 Please install Python 3.11+ from https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "  ❌ Python test failed: $_" -ForegroundColor Red
    exit 1
}

# Test pip installation
Write-Host "`n📦 Testing pip Installation..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ pip installed: $pipVersion" -ForegroundColor Green
    } else {
        Write-Host "  ❌ pip not found" -ForegroundColor Red
        Write-Host "  💡 Please install pip or upgrade Python" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "  ❌ pip test failed: $_" -ForegroundColor Red
    exit 1
}

# Test Docker installation
Write-Host "`n🐳 Testing Docker Installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Docker installed: $dockerVersion" -ForegroundColor Green
        
        # Test if Docker is running
        $dockerInfo = docker info 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ Docker is running" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  Docker is not running" -ForegroundColor Yellow
            Write-Host "  💡 Please start Docker Desktop" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ❌ Docker not found" -ForegroundColor Red
        Write-Host "  💡 Please install Docker Desktop from https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ Docker test failed: $_" -ForegroundColor Red
}

# Test Chrome installation
Write-Host "`n🌐 Testing Chrome Installation..." -ForegroundColor Yellow
$chromePaths = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)

$chromeFound = $false
foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        Write-Host "  ✅ Chrome found at: $path" -ForegroundColor Green
        $chromeFound = $true
        break
    }
}

if (-not $chromeFound) {
    Write-Host "  ⚠️  Chrome not found in common locations" -ForegroundColor Yellow
    Write-Host "  💡 Please install Google Chrome or verify the installation" -ForegroundColor Yellow
}

# Test Skyvern installation
Write-Host "`n🚀 Testing Skyvern Installation..." -ForegroundColor Yellow
try {
    $skyvernHelp = skyvern --help 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Skyvern CLI installed" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Skyvern CLI not found" -ForegroundColor Red
        Write-Host "  💡 Please install Skyvern: pip install skyvern" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "  ❌ Skyvern test failed: $_" -ForegroundColor Red
    Write-Host "  💡 Please install Skyvern: pip install skyvern" -ForegroundColor Yellow
    exit 1
}

# Test Python test script
Write-Host "`n🧪 Running Python Test Script..." -ForegroundColor Yellow
try {
    if (Test-Path "scripts\test_windows_support.py") {
        $testResult = python scripts\test_windows_support.py 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ Python test script passed" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  Python test script had issues" -ForegroundColor Yellow
            Write-Host $testResult -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ℹ️  Python test script not found" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ❌ Python test script failed: $_" -ForegroundColor Red
}

Write-Host "`n" + "=" * 50 -ForegroundColor Cyan
Write-Host "🎉 Windows Setup Test Complete!" -ForegroundColor Green
Write-Host "`n💡 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Run: skyvern init" -ForegroundColor White
Write-Host "2. Run: skyvern quickstart" -ForegroundColor White
Write-Host "3. Open http://localhost:8080 in your browser" -ForegroundColor White

Write-Host "`n📚 For more information, see:" -ForegroundColor Cyan
Write-Host "  - Windows Development Setup Guide: WINDOWS_DEVELOPMENT_SETUP.md" -ForegroundColor White
Write-Host "  - Skyvern Documentation: https://docs.skyvern.com" -ForegroundColor White 