# Godot MCP Server - Claude Desktop & Godot Entegrasyonu

Bu proje, Claude Desktop uygulamasını Godot oyun motoruyla entegre eder. Claude, Godot projelerinizi okuyabilir, düzenleyebilir ve yönetebilir.

## Sorun ve Çözüm

### Hata: `Unexpected token 'S', "[SERVER] Us"... is not valid JSON`

**Sorunun Kaynağı:**
- MCP sunucuları `stdout` üzerinden JSON-RPC mesajları gönderir
- Eğer sunucu `stdout`'a normal log mesajları yazarsa (örn: "[SERVER] Using..."), Claude Desktop bunları JSON olarak parse etmeye çalışır ve hata verir
- **ÇÖZÜMümüz:** Tüm log mesajlarını `stderr`'e yönlendirmek, `stdout`'u sadece JSON mesajları için temiz tutmak

```python
# ❌ YANLIŞ - stdout'a log yazmak
print("[SERVER] Using Godot project...")

# ✅ DOĞRU - stderr'e log yazmak
import logging
logging.basicConfig(stream=sys.stderr)
logger = logging.getLogger(__name__)
logger.info("Using Godot project...")
```

## Özellikler

- 🎮 Godot proje yapısını keşfet
- 📝 GDScript dosyalarını oku/yaz
- 🎬 Sahne dosyalarını (.tscn) görüntüle
- ⚙️ Proje ayarlarını incele
- 🤖 Claude ile doğal dilde Godot geliştirme

## Kurulum

### 1. Gereksinimleri Yükle

```bash
# Python 3.10+ gerekli
python3 --version

# MCP SDK'yı yükle
pip install mcp

# Veya pyproject.toml ile
pip install -e .
```

### 2. Claude Desktop'ı Yapılandır

Claude Desktop yapılandırma dosyasını düzenleyin:

**Linux/Mac:**
```bash
~/.config/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

Aşağıdaki yapılandırmayı ekleyin (PATH'leri kendi sisteminize göre değiştirin):

```json
{
  "mcpServers": {
    "godot": {
      "command": "python3",
      "args": [
        "/TAMAMYOLU/godot_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Önemli:**
- `/TAMAMYOLU/godot_mcp_server.py` kısmını gerçek dosya yolunuzla değiştirin
- Windows'ta şöyle olmalı: `"C:\\Users\\KullaniciAdi\\depo\\godot_mcp_server.py"`
- `PYTHONUNBUFFERED=1` Python'un çıktıyı buffer'lamadan göndermesini sağlar

### 3. Claude Desktop'ı Yeniden Başlat

Yapılandırma değişikliklerinin geçerli olması için Claude Desktop'ı tamamen kapatıp yeniden açın.

## Kullanım

Claude Desktop'ta şunları sorabilirsiniz:

### Proje Ayarlama
```
Godot projem /home/user/MyGame dizininde, bağlan
```

Claude otomatik olarak `set_godot_project` tool'unu kullanacak.

### Dosyaları Keşfetme
```
Projemde hangi sahneler var?
```
```
Tüm GDScript dosyalarını listele
```

### Kod Okuma
```
scripts/player.gd dosyasını oku
```

### Kod Yazma
```
scripts/enemy.gd adında yeni bir enemy script'i oluştur, temel AI hareket kodu ekle
```

### Proje Bilgileri
```
Proje ayarlarımı göster (project.godot)
```

## Mevcut Araçlar (Tools)

| Tool | Açıklama |
|------|----------|
| `set_godot_project` | Godot proje yolunu ayarla |
| `list_godot_scenes` | Tüm .tscn dosyalarını listele |
| `list_godot_scripts` | Tüm .gd dosyalarını listele |
| `read_godot_script` | GDScript dosyasını oku |
| `write_godot_script` | GDScript dosyası oluştur/düzenle |
| `read_godot_scene` | Sahne dosyasını oku |
| `get_project_info` | project.godot bilgilerini al |

## Hata Ayıklama

### MCP server loglarını görme

MCP sunucusu tüm logları `stderr`'e yazar. Claude Desktop Developer Console'da görebilirsiniz:

**Mac:** `Cmd + Option + Shift + i`
**Windows/Linux:** `Ctrl + Shift + i`

Console'da şöyle loglar göreceksiniz:
```
[GODOT-MCP] INFO: Godot MCP Server başlatılıyor...
[GODOT-MCP] INFO: MCP server hazır ve bağlantı bekliyor...
[GODOT-MCP] INFO: Tool çağrıldı: set_godot_project with args: {'path': '/home/user/MyGame'}
```

### Yaygın Hatalar

#### "mcp paketi bulunamadı"
```bash
pip install mcp
```

#### "Godot proje yolunu ayarlayın" hatası
Önce Claude'a proje yolunuzu söyleyin:
```
Godot projem /tam/yol/buraya dizininde
```

#### JSON parse hataları devam ediyor
1. `godot_mcp_server.py` dosyasında `print()` kullanmadığınızdan emin olun
2. Tüm loglar `logger.info()`, `logger.error()` vb. ile yapılmalı
3. `logging.basicConfig(stream=sys.stderr)` satırının olduğundan emin olun

## Genişletme

Yeni özellikler eklemek için:

1. `list_tools()` içinde yeni bir `Tool` tanımlayın
2. `call_tool()` içinde tool handler'ı ekleyin
3. İlgili işlevi implement edin

Örnek:
```python
Tool(
    name="run_godot_scene",
    description="Godot sahnesini çalıştır",
    inputSchema={
        "type": "object",
        "properties": {
            "scene_path": {"type": "string"}
        }
    }
)
```

## Lisans

MIT

## Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır!

## Destek

Sorun yaşıyorsanız:
1. Developer Console'daki logları kontrol edin
2. `godot_mcp_server.py` dosyasını elle çalıştırıp hata olup olmadığını görün:
   ```bash
   python3 godot_mcp_server.py
   ```
3. Issue açın veya yardım isteyin
