#!/bin/bash
# ========================================================================
# MANUEL KURULUM - ADIM ADIM
# ========================================================================
# Bu script her adımı ayrı ayrı gösterir ve doğrulama ister.

echo "════════════════════════════════════════════════════════════════"
echo "📦 MCP SUNUCULARI - MANUEL KURULUM"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Proje dizini
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📂 Proje dizini: $SCRIPT_DIR"
echo ""

# ========================================================================
# ADIM 1: Python Kontrolü
# ========================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ADIM 1: Python Kontrolü"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 bulunamadı!"
    echo "   Lütfen Python 3.10+ yükleyin: https://www.python.org/downloads/"
    exit 1
fi

echo ""
echo "✅ Python hazır!"
echo ""
read -p "Devam etmek için ENTER'a basın..."
echo ""

# ========================================================================
# ADIM 2: MCP SDK Kurulumu
# ========================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ADIM 2: MCP SDK Kurulumu"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "MCP SDK kuruluyor..."
pip install mcp

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ MCP SDK kuruldu!"
else
    echo ""
    echo "⚠️ MCP SDK kurulumunda sorun var. Alternatif deneyin:"
    echo "   pip3 install mcp"
    echo "   veya"
    echo "   python3 -m pip install mcp"
fi

echo ""
read -p "Devam etmek için ENTER'a basın..."
echo ""

# ========================================================================
# ADIM 3: Platform-Specific (Windows için pywin32)
# ========================================================================

if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "ADIM 3: Windows - pywin32 Kurulumu"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    echo "pywin32 kuruluyor (Adobe yazılımları için gerekli)..."
    pip install pywin32

    echo ""
    echo "✅ pywin32 kuruldu!"
    echo ""
    read -p "Devam etmek için ENTER'a basın..."
    echo ""
fi

# ========================================================================
# ADIM 4: Server Dosyalarını Kontrol Et
# ========================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ADIM 4: Server Dosyalarını Kontrol"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

MISSING_FILES=0

if [ -f "$SCRIPT_DIR/godot_mcp_server.py" ]; then
    echo "✅ godot_mcp_server.py"
else
    echo "❌ godot_mcp_server.py bulunamadı!"
    MISSING_FILES=$((MISSING_FILES + 1))
fi

if [ -f "$SCRIPT_DIR/photoshop_mcp_server.py" ]; then
    echo "✅ photoshop_mcp_server.py"
else
    echo "❌ photoshop_mcp_server.py bulunamadı!"
    MISSING_FILES=$((MISSING_FILES + 1))
fi

if [ -f "$SCRIPT_DIR/aftereffects_mcp_server.py" ]; then
    echo "✅ aftereffects_mcp_server.py"
else
    echo "❌ aftereffects_mcp_server.py bulunamadı!"
    MISSING_FILES=$((MISSING_FILES + 1))
fi

if [ $MISSING_FILES -gt 0 ]; then
    echo ""
    echo "❌ $MISSING_FILES dosya eksik!"
    echo "   Lütfen tüm dosyaların $SCRIPT_DIR dizininde olduğundan emin olun."
    exit 1
fi

echo ""
echo "✅ Tüm server dosyaları mevcut!"
echo ""
read -p "Devam etmek için ENTER'a basın..."
echo ""

# ========================================================================
# ADIM 5: Claude Desktop Config Yolu
# ========================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ADIM 5: Claude Desktop Config Yolu"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Platform tespiti
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    CONFIG_DIR="$APPDATA/Claude"
else
    CONFIG_DIR="$HOME/.config/Claude"
fi

echo "Config dizini: $CONFIG_DIR"
echo ""

mkdir -p "$CONFIG_DIR"

CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

if [ -f "$CONFIG_FILE" ]; then
    BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    echo "⚠️  Mevcut config yedekleniyor..."
    cp "$CONFIG_FILE" "$BACKUP_FILE"
    echo "✅ Yedek: $BACKUP_FILE"
    echo ""
fi

echo "✅ Config dizini hazır!"
echo ""
read -p "Devam etmek için ENTER'a basın..."
echo ""

# ========================================================================
# ADIM 6: Config Dosyası Oluştur
# ========================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ADIM 6: Config Dosyası Oluşturuluyor"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "godot": {
      "command": "python3",
      "args": [
        "$SCRIPT_DIR/godot_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    },
    "photoshop": {
      "command": "python3",
      "args": [
        "$SCRIPT_DIR/photoshop_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    },
    "aftereffects": {
      "command": "python3",
      "args": [
        "$SCRIPT_DIR/aftereffects_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
EOF

echo "✅ Config dosyası oluşturuldu!"
echo ""
echo "Dosya konumu: $CONFIG_FILE"
echo ""
echo "İçeriği:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat "$CONFIG_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

read -p "Devam etmek için ENTER'a basın..."
echo ""

# ========================================================================
# ADIM 7: Test
# ========================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ADIM 7: Server Testleri (Kısa)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "1. Godot Server testi..."
timeout 2s python3 "$SCRIPT_DIR/godot_mcp_server.py" 2>&1 | head -n 3 || true
echo ""

echo "2. Photoshop Server testi..."
timeout 2s python3 "$SCRIPT_DIR/photoshop_mcp_server.py" 2>&1 | head -n 3 || true
echo ""

echo "3. After Effects Server testi..."
timeout 2s python3 "$SCRIPT_DIR/aftereffects_mcp_server.py" 2>&1 | head -n 3 || true
echo ""

echo "✅ Testler tamamlandı!"
echo ""

# ========================================================================
# BİTTİ!
# ========================================================================

echo "════════════════════════════════════════════════════════════════"
echo "🎉 KURULUM TAMAMLANDI!"
echo "════════════════════════════════════════════════════════════════"
echo ""

echo "📋 Sıradaki adımlar:"
echo ""
echo "1️⃣  İlgili uygulamaları açın:"
echo "   - Godot (ve bir proje açın)"
echo "   - Adobe Photoshop"
echo "   - Adobe After Effects"
echo ""
echo "2️⃣  Claude Desktop'ı TAMAMEN kapatın ve yeniden açın:"
echo "   Mac: Cmd+Q"
echo "   Windows: Sistem tepsisi → Quit"
echo ""
echo "3️⃣  Claude Desktop'ta test edin:"
echo '   "MCP araçlarımı listele"'
echo ""
echo "4️⃣  Bağlantıları test edin:"
echo '   "Photoshop bağlantımı kontrol et"'
echo '   "After Effects bağlantımı kontrol et"'
echo ""

echo "📚 Dokümantasyon:"
echo "   cat $SCRIPT_DIR/QUICKSTART_TR.md"
echo ""

echo "🎉 Başarılar!"
echo ""
