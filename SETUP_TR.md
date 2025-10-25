# Kurulum Talimatları (Türkçe)

## Adım Adım Kurulum

### 1. Repoyu Klonla veya İndir

```bash
cd ~
git clone <bu-repo-url> godot-mcp
cd godot-mcp
```

### 2. Python Bağımlılıklarını Yükle

```bash
# Python 3.10+ olduğundan emin olun
python3 --version

# Bağımlılıkları yükle
pip install -r requirements.txt

# VEYA editable mode ile
pip install -e .
```

### 3. Server'ı Test Et

Server'ın çalıştığından emin olun:

```bash
python3 godot_mcp_server.py
```

Şu şekilde loglar görmelisiniz:
```
[GODOT-MCP] INFO: Godot MCP Server başlatılıyor...
[GODOT-MCP] INFO: MCP server hazır ve bağlantı bekliyor...
```

**Not:** Server stdin/stdout bekler, bu normal. `Ctrl+C` ile çıkabilirsiniz.

### 4. Claude Desktop Yapılandırması

#### Linux Kullanıcıları:

```bash
# Config dizinini oluştur
mkdir -p ~/.config/Claude

# Config dosyasını düzenle
nano ~/.config/Claude/claude_desktop_config.json
```

Şu içeriği yapıştır (PATH'i düzenle):

```json
{
  "mcpServers": {
    "godot": {
      "command": "python3",
      "args": [
        "/home/KULLANICI_ADIN/godot-mcp/godot_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**ÖNEMLİ:** `/home/KULLANICI_ADIN/godot-mcp/godot_mcp_server.py` kısmını gerçek yolunuzla değiştir:

```bash
# Tam yolu almak için:
pwd
# Çıktı: /home/arsleo/godot-mcp
# O zaman: /home/arsleo/godot-mcp/godot_mcp_server.py kullanın
```

#### Mac Kullanıcıları:

```bash
# Config dizinini oluştur
mkdir -p ~/Library/Application\ Support/Claude

# Config dosyasını düzenle
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Aynı JSON içeriği, ama PATH'i Mac stilinde:
```json
{
  "mcpServers": {
    "godot": {
      "command": "python3",
      "args": [
        "/Users/KULLANICI_ADIN/godot-mcp/godot_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

#### Windows Kullanıcıları:

1. Dosya Gezgini'nde şu dizine git:
   ```
   %APPDATA%\Claude
   ```
   (Adres çubuğuna yapıştır)

2. `claude_desktop_config.json` dosyası oluştur/düzenle

3. Şu içeriği ekle (PATH'i düzenle):

```json
{
  "mcpServers": {
    "godot": {
      "command": "python",
      "args": [
        "C:\\Users\\KULLANICI_ADIN\\godot-mcp\\godot_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Not:** Windows'ta backslash'leri double yapın: `C:\\Users\\...`

### 5. Claude Desktop'ı Yeniden Başlat

- Claude Desktop'ı **tamamen kapat** (sistem tepsisinde de)
- Yeniden aç
- Yeni sohbet başlat

### 6. Test Et!

Claude'a şunu yaz:

```
MCP araçlarımı göster
```

"godot" server'ını ve tool'ları (set_godot_project, list_godot_scenes, vb.) görmelisin.

Sonra bir Godot projen varsa:

```
Godot projem /tam/yol/buraya dizininde, bağlan
```

Claude yanıt verirse, tebrikler! Çalışıyor! 🎉

## Sorun Giderme

### "JSON parse error" hatası

Bu hatayı alıyorsan:
```
Unexpected token 'S', "[SERVER] Us"... is not valid JSON
```

**Sebep:** Server stdout'a log yazıyor (yazmamalı!)

**Çözüm:**
1. `godot_mcp_server.py` dosyasını kontrol et
2. `logging.basicConfig(stream=sys.stderr)` satırı olmalı
3. HİÇBİR YERde `print()` kullanma, sadece `logger.info()` kullan

### Server bağlanmıyor

1. Developer Console aç (Claude Desktop'ta):
   - **Mac:** Cmd + Option + Shift + i
   - **Win/Linux:** Ctrl + Shift + i

2. Console tab'ında hataları kontrol et

3. Terminal'de manual test:
   ```bash
   python3 godot_mcp_server.py
   ```

   Hata varsa göreceksin.

### "mcp module not found"

```bash
pip install mcp

# Veya Python'unuzun doğru versiyonunu kullanın:
python3 -m pip install mcp
```

### Claude tool'ları görmüyor

1. Config dosyası doğru yerde mi?
2. JSON formatı doğru mu? (virgüller, parantezler)
3. PATH'ler doğru mu?
4. Claude'u yeniden başlattın mı?

### Godot proje yolu hatası

```
Hata: project.godot bulunamadı
```

Godot proje dizini şöyle görünmelidir:
```
MyGodotGame/
├── project.godot      <- Bu dosya olmalı!
├── scenes/
├── scripts/
└── ...
```

Claude'a ROOT dizini söyle:
```
Godot projem /home/user/MyGodotGame dizininde
```

## İleri Seviye

### Virtual Environment Kullanımı (önerilen)

```bash
cd ~/godot-mcp

# Venv oluştur
python3 -m venv venv

# Aktifleştir
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Yükle
pip install -r requirements.txt
```

Config'de command'ı değiştir:
```json
{
  "mcpServers": {
    "godot": {
      "command": "/home/KULLANICI/godot-mcp/venv/bin/python3",
      "args": ["/home/KULLANICI/godot-mcp/godot_mcp_server.py"]
    }
  }
}
```

### Çoklu Godot Projeler

Her proje için ayrı server ekleyebilirsin:

```json
{
  "mcpServers": {
    "godot-project1": {
      "command": "python3",
      "args": ["/path/to/godot_mcp_server.py"],
      "env": {
        "DEFAULT_PROJECT": "/path/to/project1"
      }
    },
    "godot-project2": {
      "command": "python3",
      "args": ["/path/to/godot_mcp_server.py"],
      "env": {
        "DEFAULT_PROJECT": "/path/to/project2"
      }
    }
  }
}
```

(Not: DEFAULT_PROJECT özelliği eklemek için kod modifikasyonu gerekir)

## Yardım

Sorun mu var?

1. README.md dosyasını oku
2. Developer Console loglarını kontrol et
3. Issue aç
4. Discord/forum'da yardım iste

Başarılar! 🚀
