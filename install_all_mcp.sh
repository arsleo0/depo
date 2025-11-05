#!/bin/bash
# ========================================================================
# TÜM MCP SUNUCULARI - TEK KOMUTLA KURULUM
# ========================================================================
# Bu script, tüm MCP sunucularını (Godot, Photoshop, After Effects)
# tek seferde kurar ve yapılandırır.
#
# Kullanım:
#   ./install_all_mcp.sh              # Hepsini kur
#   ./install_all_mcp.sh photoshop    # Sadece Photoshop
#   ./install_all_mcp.sh ps ae        # Photoshop + After Effects
# ========================================================================

set -e  # Hata durumunda dur

echo "════════════════════════════════════════════════════════════════"
echo "🚀 MCP SUNUCULARI - TOPLU KURULUM"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Platform tespiti
PLATFORM=$(uname -s)
echo "📍 Platform: $PLATFORM"
echo ""

# Proje dizini
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📂 Proje dizini: $SCRIPT_DIR"
echo ""

# Claude Desktop config dizini
if [[ "$PLATFORM" == "Darwin" ]]; then
    CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
elif [[ "$PLATFORM" == "MINGW"* ]] || [[ "$PLATFORM" == "MSYS"* ]] || [[ "$PLATFORM" == "CYGWIN"* ]]; then
    CLAUDE_CONFIG_DIR="$APPDATA/Claude"
else
    CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
fi

CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

# Kurulacak server'ları belirle
INSTALL_GODOT=false
INSTALL_PHOTOSHOP=false
INSTALL_AFTEREFFECTS=false

if [ $# -eq 0 ]; then
    # Argüman yoksa hepsini kur
    echo "📦 Kurulum modu: TÜM SUNUCULAR"
    INSTALL_GODOT=true
    INSTALL_PHOTOSHOP=true
    INSTALL_AFTEREFFECTS=true
else
    # Argümanlara göre seç
    echo "📦 Kurulum modu: SEÇİLİ SUNUCULAR"
    for arg in "$@"; do
        case $arg in
            godot|gd)
                INSTALL_GODOT=true
                echo "   ✓ Godot"
                ;;
            photoshop|ps)
                INSTALL_PHOTOSHOP=true
                echo "   ✓ Photoshop"
                ;;
            aftereffects|ae)
                INSTALL_AFTEREFFECTS=true
                echo "   ✓ After Effects"
                ;;
            all)
                INSTALL_GODOT=true
                INSTALL_PHOTOSHOP=true
                INSTALL_AFTEREFFECTS=true
                echo "   ✓ Hepsi"
                ;;
            *)
                echo "   ⚠️  Bilinmeyen: $arg (godot|photoshop|aftereffects|all)"
                ;;
        esac
    done
fi
echo ""

# ========================================================================
# PYTHON KONTROLÜ
# ========================================================================

echo "════════════════════════════════════════════════════════════════"
echo "🐍 PYTHON KONTROLÜ"
echo "════════════════════════════════════════════════════════════════"
echo ""

python3 --version
if [ $? -ne 0 ]; then
    echo "❌ HATA: Python 3 bulunamadı!"
    echo "   Lütfen Python 3.10+ yükleyin."
    exit 1
fi
echo "✅ Python bulundu!"
echo ""

# ========================================================================
# MCP SDK KURULUMU
# ========================================================================

echo "════════════════════════════════════════════════════════════════"
echo "📦 MCP SDK KURULUMU"
echo "════════════════════════════════════════════════════════════════"
echo ""

pip install -q mcp
if [ $? -eq 0 ]; then
    echo "✅ MCP SDK kuruldu!"
else
    echo "⚠️  MCP SDK kurulumunda sorun olabilir, devam ediyoruz..."
fi
echo ""

# ========================================================================
# PLATFORM-SPECIFIC KURULUMLAR
# ========================================================================

if [[ "$PLATFORM" == "MINGW"* ]] || [[ "$PLATFORM" == "MSYS"* ]] || [[ "$PLATFORM" == "CYGWIN"* ]]; then
    echo "════════════════════════════════════════════════════════════════"
    echo "🪟 WINDOWS - PYWIN32 KURULUMU"
    echo "════════════════════════════════════════════════════════════════"
    echo ""

    pip install -q pywin32
    if [ $? -eq 0 ]; then
        echo "✅ pywin32 kuruldu!"
    fi
    echo ""
fi

# ========================================================================
# SUNUCU DOSYALARINI KONTROL ET
# ========================================================================

echo "════════════════════════════════════════════════════════════════"
echo "🔍 SUNUCU DOSYALARI KONTROLÜ"
echo "════════════════════════════════════════════════════════════════"
echo ""

SERVERS_FOUND=true

if [ "$INSTALL_GODOT" = true ]; then
    if [ -f "$SCRIPT_DIR/godot_mcp_server.py" ]; then
        echo "✅ godot_mcp_server.py bulundu"
    else
        echo "❌ godot_mcp_server.py bulunamadı!"
        SERVERS_FOUND=false
    fi
fi

if [ "$INSTALL_PHOTOSHOP" = true ]; then
    if [ -f "$SCRIPT_DIR/photoshop_mcp_server.py" ]; then
        echo "✅ photoshop_mcp_server.py bulundu"
    else
        echo "❌ photoshop_mcp_server.py bulunamadı!"
        SERVERS_FOUND=false
    fi
fi

if [ "$INSTALL_AFTEREFFECTS" = true ]; then
    if [ -f "$SCRIPT_DIR/aftereffects_mcp_server.py" ]; then
        echo "✅ aftereffects_mcp_server.py bulundu"
    else
        echo "❌ aftereffects_mcp_server.py bulunamadı!"
        SERVERS_FOUND=false
    fi
fi

if [ "$SERVERS_FOUND" = false ]; then
    echo ""
    echo "❌ HATA: Bazı sunucu dosyaları bulunamadı!"
    exit 1
fi
echo ""

# ========================================================================
# CLAUDE DESKTOP CONFIG OLUŞTUR
# ========================================================================

echo "════════════════════════════════════════════════════════════════"
echo "⚙️  CLAUDE DESKTOP YAPILANDIRMASI"
echo "════════════════════════════════════════════════════════════════"
echo ""

mkdir -p "$CLAUDE_CONFIG_DIR" 2>/dev/null

# Mevcut config'i yedekle
if [ -f "$CONFIG_FILE" ]; then
    BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    echo "⚠️  Mevcut config yedekleniyor: $BACKUP_FILE"
    cp "$CONFIG_FILE" "$BACKUP_FILE"
    echo ""
fi

# JSON oluştur
echo "📝 Config dosyası oluşturuluyor..."
echo ""

cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
EOF

# Godot ekle
if [ "$INSTALL_GODOT" = true ]; then
    cat >> "$CONFIG_FILE" << EOF
    "godot": {
      "command": "python3",
      "args": [
        "$SCRIPT_DIR/godot_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
EOF
fi

# Photoshop ekle
if [ "$INSTALL_PHOTOSHOP" = true ]; then
    # Virgül ekle (eğer öncesinde başka server varsa)
    if [ "$INSTALL_GODOT" = true ]; then
        echo "," >> "$CONFIG_FILE"
    fi

    cat >> "$CONFIG_FILE" << EOF
    "photoshop": {
      "command": "python3",
      "args": [
        "$SCRIPT_DIR/photoshop_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
EOF
fi

# After Effects ekle
if [ "$INSTALL_AFTEREFFECTS" = true ]; then
    # Virgül ekle (eğer öncesinde başka server varsa)
    if [ "$INSTALL_GODOT" = true ] || [ "$INSTALL_PHOTOSHOP" = true ]; then
        echo "," >> "$CONFIG_FILE"
    fi

    cat >> "$CONFIG_FILE" << EOF
    "aftereffects": {
      "command": "python3",
      "args": [
        "$SCRIPT_DIR/aftereffects_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
EOF
fi

# JSON'u kapat
cat >> "$CONFIG_FILE" << EOF

  }
}
EOF

echo "✅ Config dosyası oluşturuldu: $CONFIG_FILE"
echo ""

# Config'i göster
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Config içeriği:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat "$CONFIG_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ========================================================================
# TEST (opsiyonel)
# ========================================================================

echo "════════════════════════════════════════════════════════════════"
echo "🧪 HIZLI TEST (5 saniye)"
echo "════════════════════════════════════════════════════════════════"
echo ""

test_server() {
    local server_name=$1
    local server_path=$2

    echo "Testing $server_name..."
    timeout 3s python3 "$server_path" 2>&1 | head -n 3 || true
    echo ""
}

if [ "$INSTALL_GODOT" = true ]; then
    test_server "Godot" "$SCRIPT_DIR/godot_mcp_server.py"
fi

if [ "$INSTALL_PHOTOSHOP" = true ]; then
    test_server "Photoshop" "$SCRIPT_DIR/photoshop_mcp_server.py"
fi

if [ "$INSTALL_AFTEREFFECTS" = true ]; then
    test_server "After Effects" "$SCRIPT_DIR/aftereffects_mcp_server.py"
fi

# ========================================================================
# TAMAMLANDI!
# ========================================================================

echo "════════════════════════════════════════════════════════════════"
echo "✅ KURULUM TAMAMLANDI!"
echo "════════════════════════════════════════════════════════════════"
echo ""

echo "📋 Kurulan sunucular:"
[ "$INSTALL_GODOT" = true ] && echo "   ✅ Godot MCP Server"
[ "$INSTALL_PHOTOSHOP" = true ] && echo "   ✅ Photoshop MCP Server"
[ "$INSTALL_AFTEREFFECTS" = true ] && echo "   ✅ After Effects MCP Server"
echo ""

echo "📋 Sıradaki adımlar:"
echo ""
echo "1️⃣  İlgili uygulamaları açın:"
[ "$INSTALL_GODOT" = true ] && echo "   - Godot (ve bir proje açın)"
[ "$INSTALL_PHOTOSHOP" = true ] && echo "   - Adobe Photoshop"
[ "$INSTALL_AFTEREFFECTS" = true ] && echo "   - Adobe After Effects"
echo ""

echo "2️⃣  Claude Desktop'ı yeniden başlatın:"
if [[ "$PLATFORM" == "Darwin" ]]; then
    echo "   - Cmd+Q ile tamamen kapatın"
else
    echo "   - Sistem tepsisinden tamamen kapatın"
fi
echo "   - Yeniden açın"
echo ""

echo "3️⃣  Claude Desktop'ta test edin:"
echo '   Yeni sohbette yazın: "MCP araçlarımı listele"'
echo ""

echo "4️⃣  Bağlantıları test edin:"
[ "$INSTALL_GODOT" = true ] && echo '   "Godot projem hakkında bilgi ver"'
[ "$INSTALL_PHOTOSHOP" = true ] && echo '   "Photoshop bağlantımı kontrol et"'
[ "$INSTALL_AFTEREFFECTS" = true ] && echo '   "After Effects bağlantımı kontrol et"'
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 Dokümantasyon:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
[ "$INSTALL_GODOT" = true ] && echo "Godot:          cat $SCRIPT_DIR/README.md"
[ "$INSTALL_PHOTOSHOP" = true ] && echo "Photoshop:      cat $SCRIPT_DIR/PHOTOSHOP_WORKFLOW_TR.md"
[ "$INSTALL_AFTEREFFECTS" = true ] && echo "After Effects:  cat $SCRIPT_DIR/AFTEREFFECTS_QUICKSTART.md"
echo ""

echo "🎉 Başarılar! Harika projeler oluşturun!"
echo ""
