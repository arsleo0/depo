#!/bin/bash
# TripoSR MCP Server - Otomatik Kurulum Scripti
# Bu script, TripoSR MCP server'ını otomatik olarak kurar

echo "🎨 TripoSR MCP Server Kurulum Başlatılıyor..."
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
echo "📦 MCP SDK ve gerekli paketler kuruluyor..."
pip install -q mcp
if [ $? -eq 0 ]; then
    echo "✅ MCP SDK kuruldu!"
else
    echo "⚠️  MCP SDK kurulumunda sorun olabilir, devam ediyoruz..."
fi
echo ""

# PyTorch kurulumu (CUDA kontrolü)
echo "🔥 PyTorch kurulumu kontrol ediliyor..."

if command -v nvidia-smi &> /dev/null; then
    echo "🎮 NVIDIA GPU tespit edildi!"
    echo "   PyTorch (CUDA) kuruluyor... (Bu biraz zaman alabilir)"
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
else
    echo "💻 CPU modu - PyTorch kuruluyor..."
    pip install torch torchvision
fi

if [ $? -eq 0 ]; then
    echo "✅ PyTorch kuruldu!"
else
    echo "❌ PyTorch kurulumu başarısız!"
    exit 1
fi
echo ""

# Diğer gerekli paketler
echo "📦 Görüntü işleme ve 3D paketleri kuruluyor..."
pip install -r requirements-triposr.txt

if [ $? -eq 0 ]; then
    echo "✅ Paketler kuruldu!"
else
    echo "⚠️  Bazı paketler kurulamadı olabilir, devam ediyoruz..."
fi
echo ""

# TripoSR GitHub'dan klonlama
echo "📥 TripoSR GitHub'dan indiriliyor..."

TRIPOSR_DIR="$HOME/TripoSR"

if [ -d "$TRIPOSR_DIR" ]; then
    echo "⚠️  TripoSR zaten mevcut: $TRIPOSR_DIR"
    echo "   Güncelleniyor..."
    cd "$TRIPOSR_DIR"
    git pull
else
    echo "   Klonlanıyor: https://github.com/VAST-AI-Research/TripoSR.git"
    git clone https://github.com/VAST-AI-Research/TripoSR.git "$TRIPOSR_DIR"
fi

if [ -d "$TRIPOSR_DIR" ]; then
    echo "✅ TripoSR indirildi: $TRIPOSR_DIR"
    cd "$TRIPOSR_DIR"
    pip install -e .
    echo "✅ TripoSR kuruldu!"
else
    echo "❌ TripoSR indirilemedi!"
    echo "   Manuel olarak indirin:"
    echo "   git clone https://github.com/VAST-AI-Research/TripoSR.git ~/TripoSR"
    echo "   cd ~/TripoSR && pip install -e ."
    exit 1
fi
echo ""

# Claude Desktop config dizinini bul
if [[ "$PLATFORM" == "Darwin" ]]; then
    CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
elif [[ "$PLATFORM" == "MINGW"* ]] || [[ "$PLATFORM" == "MSYS"* ]] || [[ "$PLATFORM" == "CYGWIN"* ]]; then
    CLAUDE_CONFIG_DIR="$APPDATA/Claude"
else
    CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
fi

CLAUDE_CONFIG="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

echo "📝 Claude Desktop config güncelleniyor..."
echo "   Konum: $CLAUDE_CONFIG"

# Config dizinini oluştur
mkdir -p "$CLAUDE_CONFIG_DIR"

# Mevcut scriptin tam yolu
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVER_PATH="$SCRIPT_DIR/triposr_mcp_server.py"

# Config dosyası varsa güncelle, yoksa oluştur
if [ -f "$CLAUDE_CONFIG" ]; then
    echo "   Mevcut config dosyası bulundu, güncelleniyor..."

    # Backup al
    cp "$CLAUDE_CONFIG" "$CLAUDE_CONFIG.backup_$(date +%Y%m%d_%H%M%S)"
    echo "   ✅ Backup oluşturuldu"

    # Python ile JSON güncelle
    python3 << EOF
import json
import sys

try:
    with open("$CLAUDE_CONFIG", "r") as f:
        config = json.load(f)

    if "mcpServers" not in config:
        config["mcpServers"] = {}

    config["mcpServers"]["triposr"] = {
        "command": "python3",
        "args": ["$SERVER_PATH"],
        "env": {"PYTHONUNBUFFERED": "1"}
    }

    with open("$CLAUDE_CONFIG", "w") as f:
        json.dump(config, f, indent=2)

    print("   ✅ Config güncellendi!")
except Exception as e:
    print(f"   ❌ Config güncellenemedi: {e}")
    sys.exit(1)
EOF

else
    echo "   Yeni config dosyası oluşturuluyor..."

    cat > "$CLAUDE_CONFIG" << EOF
{
  "mcpServers": {
    "triposr": {
      "command": "python3",
      "args": ["$SERVER_PATH"],
      "env": {"PYTHONUNBUFFERED": "1"}
    }
  }
}
EOF

    echo "   ✅ Config oluşturuldu!"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ TripoSR MCP Server kurulumu tamamlandı!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Sonraki adımlar:"
echo ""
echo "1. 🔄 Claude Desktop'ı tamamen kapatıp yeniden başlatın"
echo "   (macOS: Cmd+Q, Windows: Görev Yöneticisi'nden kapatın)"
echo ""
echo "2. 🧪 Test edin:"
echo '   Claude Desktop\'ta yazın: "TripoSR durumunu kontrol et"'
echo ""
echo "3. 🎨 İlk 3D modelinizi oluşturun:"
echo '   "Desktop/photo.jpg görüntüsünden 3D model oluştur"'
echo ""
echo "4. 📚 Daha fazla bilgi:"
echo "   cat TRIPOSR_QUICKSTART.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 İpuçları:"
echo "   • GPU kullanımı için NVIDIA CUDA kurulu olmalı"
echo "   • İlk çalıştırmada model indirilecek (~300MB)"
echo "   • Her 3D oluşturma 30-60 saniye sürer"
echo ""
echo "🎉 Harika 3D modeller oluşturun! 🚀"
echo ""
