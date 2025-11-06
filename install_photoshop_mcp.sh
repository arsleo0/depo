#!/bin/bash
# Photoshop MCP Server - Otomatik Kurulum Scripti
# Bu script, Photoshop MCP server'ını otomatik olarak kurar

echo "🎨 Photoshop MCP Server Kurulum Başlatılıyor..."
echo ""

# Platform tespiti
PLATFORM=$(uname -s)
echo "📍 Platform: $PLATFORM"
echo ""

# Python versiyonu kontrolü
echo "🐍 Python versiyonu kontrol ediliyor..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ HATA: Python 3 bulunamadı!"
    echo "   Lütfen Python 3.10+ yükleyin."
    exit 1
fi
echo "✅ Python bulundu!"
echo ""

# MCP SDK kurulumu
echo "📦 MCP SDK kuruluyor..."
pip install -q mcp
if [ $? -eq 0 ]; then
    echo "✅ MCP SDK kuruldu!"
else
    echo "⚠️  MCP SDK kurulumunda sorun olabilir, devam ediyoruz..."
fi
echo ""

# Platform-specific kurulumlar
if [[ "$PLATFORM" == "Darwin" ]]; then
    echo "🍎 macOS tespit edildi"
    echo "   AppleScript desteği varsayılan olarak mevcut."
    CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
elif [[ "$PLATFORM" == "MINGW"* ]] || [[ "$PLATFORM" == "MSYS"* ]] || [[ "$PLATFORM" == "CYGWIN"* ]]; then
    echo "🪟 Windows tespit edildi"
    echo "   pywin32 kuruluyor..."
    pip install -q pywin32
    if [ $? -eq 0 ]; then
        echo "✅ pywin32 kuruldu!"
        python -m pip install --upgrade pip
        python Scripts/pywin32_postinstall.py -install 2>/dev/null || echo "   (postinstall opsiyonel)"
    fi
    CLAUDE_CONFIG_DIR="$APPDATA/Claude"
else
    echo "🐧 Linux tespit edildi"
    echo "⚠️  UYARI: Photoshop Linux'ta doğal olarak çalışmaz."
    echo "   Wine veya başka bir çözüm kullanmanız gerekebilir."
    CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
fi
echo ""

# Proje dizinini tespit et
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_PATH="$SCRIPT_DIR/photoshop_mcp_server.py"

echo "📂 Proje dizini: $SCRIPT_DIR"
echo "🔧 Server yolu: $SERVER_PATH"
echo ""

# Server dosyasını kontrol et
if [ ! -f "$SERVER_PATH" ]; then
    echo "❌ HATA: photoshop_mcp_server.py bulunamadı!"
    echo "   Beklenen konum: $SERVER_PATH"
    exit 1
fi
echo "✅ Server dosyası bulundu!"
echo ""

# Claude Desktop config dizinini oluştur
echo "⚙️  Claude Desktop yapılandırması hazırlanıyor..."
mkdir -p "$CLAUDE_CONFIG_DIR" 2>/dev/null

CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

# Mevcut config'i kontrol et
if [ -f "$CONFIG_FILE" ]; then
    echo "⚠️  Mevcut config dosyası bulundu: $CONFIG_FILE"
    echo "   Yedekleniyor..."
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✅ Yedek oluşturuldu!"

    # JSON dosyasını oku ve photoshop server'ı ekle
    # (Basit ekleme - manuel düzenleme önerilir)
    echo ""
    echo "📝 Config dosyanıza manuel olarak şunu ekleyin:"
else
    echo "📝 Yeni config dosyası oluşturuluyor..."
fi

# Config örneği göster
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Claude Desktop Config ($CONFIG_FILE):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat << EOF
{
  "mcpServers": {
    "photoshop": {
      "command": "python3",
      "args": [
        "$SERVER_PATH"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
EOF
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Eğer mevcut config yoksa, yeni oluştur
if [ ! -f "$CONFIG_FILE" ]; then
    cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "photoshop": {
      "command": "python3",
      "args": [
        "$SERVER_PATH"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
EOF
    echo "✅ Config dosyası oluşturuldu!"
else
    echo "⚠️  Mevcut config dosyanız var. Yukarıdaki JSON'u manuel olarak ekleyin."
fi
echo ""

# Test
echo "🧪 Server testi yapılıyor..."
echo "   (5 saniye bekleyip kapatacağız...)"
echo ""

timeout 5s python3 "$SERVER_PATH" 2>&1 | head -n 5 || true

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ KURULUM TAMAMLANDI!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Sıradaki Adımlar:"
echo ""
echo "1. Adobe Photoshop'u açın"
echo ""
echo "2. Claude Desktop'ı yeniden başlatın:"
if [[ "$PLATFORM" == "Darwin" ]]; then
    echo "   - Cmd+Q ile tamamen kapatın"
else
    echo "   - Sistem tepsisinden tamamen kapatın"
fi
echo "   - Yeniden açın"
echo ""
echo "3. Claude Desktop'ta test edin:"
echo "   Yeni sohbette yazın: 'Photoshop bağlantımı kontrol et'"
echo ""
echo "4. Daha fazla örnek için:"
echo "   cat $SCRIPT_DIR/PHOTOSHOP_EXAMPLES.md"
echo ""
echo "🎉 Harika işler çıkarın!"
echo ""
