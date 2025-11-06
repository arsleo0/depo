# Creative Software MCP - Windows 11 Otomatik Kurulum Scripti
# Bu scripti PowerShell'de Yönetici olarak çalıştırın

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Creative Software MCP - Windows Kurulum" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Gerekli değişkenler
$userName = $env:USERNAME
$documentsPath = [Environment]::GetFolderPath("MyDocuments")
$targetFolder = Join-Path $documentsPath "creative-mcp"
$claudeConfigPath = Join-Path $env:APPDATA "Claude"
$claudeConfigFile = Join-Path $claudeConfigPath "claude_desktop_config.json"

Write-Host "[1/7] Kullanıcı bilgileri" -ForegroundColor Green
Write-Host "  Kullanıcı: $userName"
Write-Host "  Hedef klasör: $targetFolder"
Write-Host "  Claude config: $claudeConfigFile"
Write-Host ""

# 2. Hedef klasörü oluştur
Write-Host "[2/7] Hedef klasör oluşturuluyor..." -ForegroundColor Green
if (-not (Test-Path $targetFolder)) {
    New-Item -ItemType Directory -Path $targetFolder -Force | Out-Null
    Write-Host "  ✓ Klasör oluşturuldu: $targetFolder" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ Klasör zaten mevcut" -ForegroundColor Yellow
}
Write-Host ""

# 3. Python dosyalarını kopyala
Write-Host "[3/7] MCP server dosyaları kopyalanıyor..." -ForegroundColor Green
$pythonFiles = @(
    "godot_mcp_server.py",
    "blender_mcp_server.py",
    "maya_mcp_server.py",
    "photoshop_mcp_server.py",
    "photoshop_client.jsx",
    "requirements.txt",
    "CREATIVE_SOFTWARE_MCP_SETUP.md"
)

$currentDir = Split-Path -Parent $MyInvocation.MyCommand.Path
foreach ($file in $pythonFiles) {
    $sourcePath = Join-Path $currentDir $file
    $destPath = Join-Path $targetFolder $file

    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $destPath -Force
        Write-Host "  ✓ Kopyalandı: $file" -ForegroundColor Yellow
    } else {
        Write-Host "  ✗ Bulunamadı: $file" -ForegroundColor Red
    }
}
Write-Host ""

# 4. MCP SDK'yı yükle
Write-Host "[4/7] MCP SDK yükleniyor..." -ForegroundColor Green
try {
    pip install mcp 2>&1 | Out-Null
    Write-Host "  ✓ MCP SDK yüklendi" -ForegroundColor Yellow
} catch {
    Write-Host "  ⚠ MCP SDK yüklenemedi. Manuel olarak yükleyin: pip install mcp" -ForegroundColor Red
}
Write-Host ""

# 5. Yazılım yollarını bul
Write-Host "[5/7] Yazılımlar aranıyor..." -ForegroundColor Green

# Python
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($pythonPath) {
    Write-Host "  ✓ Python bulundu: $pythonPath" -ForegroundColor Yellow
} else {
    $pythonPath = "python"
    Write-Host "  ⚠ Python yolu bulunamadı, varsayılan kullanılacak: python" -ForegroundColor Yellow
}

# Blender
$blenderPaths = @(
    "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
    "C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
    "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
    "C:\Program Files\Blender Foundation\Blender 3.6\blender.exe"
)
$blenderPath = $null
foreach ($path in $blenderPaths) {
    if (Test-Path $path) {
        $blenderPath = $path
        break
    }
}
if ($blenderPath) {
    Write-Host "  ✓ Blender bulundu: $blenderPath" -ForegroundColor Yellow
} else {
    Write-Host "  ⚠ Blender bulunamadı. Blender kurulu değilse, MCP server çalışmayacak." -ForegroundColor Yellow
}

# Maya
$mayaPaths = @(
    "C:\Program Files\Autodesk\Maya2024\bin\mayapy.exe",
    "C:\Program Files\Autodesk\Maya2025\bin\mayapy.exe",
    "C:\Program Files\Autodesk\Maya2023\bin\mayapy.exe"
)
$mayaPath = $null
foreach ($path in $mayaPaths) {
    if (Test-Path $path) {
        $mayaPath = $path
        break
    }
}
if ($mayaPath) {
    Write-Host "  ✓ Maya bulundu: $mayaPath" -ForegroundColor Yellow
} else {
    Write-Host "  ⚠ Maya bulunamadı. Maya kurulu değilse, MCP server çalışmayacak." -ForegroundColor Yellow
}

Write-Host ""

# 6. Claude config oluştur
Write-Host "[6/7] Claude Desktop config dosyası oluşturuluyor..." -ForegroundColor Green

# Claude config klasörünü oluştur
if (-not (Test-Path $claudeConfigPath)) {
    New-Item -ItemType Directory -Path $claudeConfigPath -Force | Out-Null
}

# PowerShell hashtable kullanarak config oluştur
$mcpServers = @{}

# Godot ekle
$mcpServers["godot"] = @{
    command = $pythonPath
    args = @(
        (Join-Path $targetFolder "godot_mcp_server.py")
    )
    env = @{
        PYTHONUNBUFFERED = "1"
    }
}

# Blender varsa ekle
if ($blenderPath) {
    $mcpServers["blender"] = @{
        command = $blenderPath
        args = @(
            "--background",
            "--python",
            (Join-Path $targetFolder "blender_mcp_server.py")
        )
        env = @{
            PYTHONUNBUFFERED = "1"
        }
    }
}

# Maya varsa ekle
if ($mayaPath) {
    $mcpServers["maya"] = @{
        command = $mayaPath
        args = @(
            (Join-Path $targetFolder "maya_mcp_server.py")
        )
        env = @{
            PYTHONUNBUFFERED = "1"
        }
    }
}

# Photoshop ekle
$mcpServers["photoshop"] = @{
    command = $pythonPath
    args = @(
        (Join-Path $targetFolder "photoshop_mcp_server.py")
    )
    env = @{
        PYTHONUNBUFFERED = "1"
    }
}

# Config objesi oluştur
$config = @{
    mcpServers = $mcpServers
}

# JSON'a çevir ve kaydet
$configJson = $config | ConvertTo-Json -Depth 10
$configJson | Out-File -FilePath $claudeConfigFile -Encoding UTF8 -Force

Write-Host "  ✓ Config dosyası oluşturuldu: $claudeConfigFile" -ForegroundColor Yellow
Write-Host ""

# 7. Photoshop JSX kopyalama (opsiyonel)
Write-Host "[7/7] Photoshop JSX scripti..." -ForegroundColor Green

$photoshopScriptsPaths = @(
    "C:\Program Files\Adobe\Adobe Photoshop 2024\Presets\Scripts",
    "C:\Program Files\Adobe\Adobe Photoshop 2025\Presets\Scripts",
    "C:\Program Files\Adobe\Adobe Photoshop 2023\Presets\Scripts"
)

$photoshopScriptsPath = $null
foreach ($path in $photoshopScriptsPaths) {
    if (Test-Path $path) {
        $photoshopScriptsPath = $path
        break
    }
}

$jsxSource = Join-Path $targetFolder "photoshop_client.jsx"
if ($photoshopScriptsPath -and (Test-Path $jsxSource)) {
    try {
        Copy-Item -Path $jsxSource -Destination $photoshopScriptsPath -Force
        Write-Host "  ✓ JSX scripti Photoshop'a kopyalandı: $photoshopScriptsPath" -ForegroundColor Yellow
        Write-Host "  → Photoshop'ta: File > Scripts > photoshop_client" -ForegroundColor Cyan
    } catch {
        Write-Host "  ⚠ JSX scripti kopyalanamadı. Manuel olarak kopyalayın:" -ForegroundColor Yellow
        Write-Host "    Kaynak: $jsxSource" -ForegroundColor Gray
        Write-Host "    Hedef: $photoshopScriptsPath" -ForegroundColor Gray
    }
} else {
    Write-Host "  ⚠ Photoshop Scripts klasörü bulunamadı." -ForegroundColor Yellow
    Write-Host "    JSX scriptini manuel olarak çalıştırın:" -ForegroundColor Gray
    Write-Host "    $jsxSource" -ForegroundColor Gray
    Write-Host "    Photoshop: File > Scripts > Browse... > photoshop_client.jsx" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ KURULUM TAMAMLANDI!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Sonraki Adımlar:" -ForegroundColor Yellow
Write-Host "  1. Claude Desktop'ı TAMAMEN KAPATIN" -ForegroundColor White
Write-Host "  2. Claude Desktop'ı yeniden başlatın" -ForegroundColor White
Write-Host "  3. Test edin: 'Blender'da yeni bir küp oluştur'" -ForegroundColor White
Write-Host ""
Write-Host "Dosyalar:" -ForegroundColor Yellow
Write-Host "  MCP Sunucular: $targetFolder" -ForegroundColor Gray
Write-Host "  Config dosyası: $claudeConfigFile" -ForegroundColor Gray
Write-Host "  Dokümantasyon: $targetFolder\CREATIVE_SOFTWARE_MCP_SETUP.md" -ForegroundColor Gray
Write-Host ""
Write-Host "Sorun yaşarsanız:" -ForegroundColor Yellow
Write-Host "  • Claude Desktop Developer Console: Ctrl+Shift+I" -ForegroundColor Gray
Write-Host "  • Dokümantasyonu okuyun: $targetFolder\CREATIVE_SOFTWARE_MCP_SETUP.md" -ForegroundColor Gray
Write-Host ""

# Kullanıcıya bilgi ver
Write-Host "Kurulu MCP Sunucular:" -ForegroundColor Yellow
Write-Host "  ✓ Godot" -ForegroundColor Green
if ($blenderPath) { Write-Host "  ✓ Blender" -ForegroundColor Green } else { Write-Host "  ✗ Blender (kurulu değil)" -ForegroundColor Red }
if ($mayaPath) { Write-Host "  ✓ Maya" -ForegroundColor Green } else { Write-Host "  ✗ Maya (kurulu değil)" -ForegroundColor Red }
Write-Host "  ✓ Photoshop (JSX scripti gerekli)" -ForegroundColor Yellow

Write-Host ""
Write-Host "Devam etmek için herhangi bir tuşa basın..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
