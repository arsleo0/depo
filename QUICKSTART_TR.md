# 🚀 MCP Sunucuları - Hızlı Başlangıç

Claude Desktop ile Godot, Photoshop ve After Effects'i kontrol edin!

---

## 🎯 İki Seçenek

### ✅ Seçenek 1: **Hepsini Birden Kur** (Önerilen!)

Tek komutla tüm MCP sunucularını kurun:

```bash
cd ~/depo
./install_all_mcp.sh
```

**Bu komut:**
- ✅ Tüm bağımlılıkları yükler (MCP SDK, pywin32)
- ✅ Godot, Photoshop, After Effects sunucularını kurar
- ✅ Claude Desktop config'ini otomatik oluşturur
- ✅ Hepsini test eder

**Süre:** 2-3 dakika

---

### ✅ Seçenek 2: **Sadece İstediğini Kur**

Sadece belirli sunucuları kurun:

```bash
# Sadece Photoshop
./install_all_mcp.sh photoshop

# Photoshop + After Effects
./install_all_mcp.sh photoshop aftereffects

# Godot + Photoshop
./install_all_mcp.sh godot photoshop

# Hepsini kur (uzun yol)
./install_all_mcp.sh all
```

**Kısaltmalar:**
- `godot` veya `gd`
- `photoshop` veya `ps`
- `aftereffects` veya `ae`

---

## 📦 Kurulum Sonrası

### 1️⃣ Uygulamaları Açın

Kurduğunuz sunuculara göre:

```bash
# Godot kullanıyorsanız
- Godot'u açın
- Bir proje açın veya oluşturun

# Photoshop kullanıyorsanız
- Adobe Photoshop'u açın

# After Effects kullanıyorsanız
- Adobe After Effects'i açın
```

---

### 2️⃣ Claude Desktop'ı Yeniden Başlatın

**Önemli:** Sadece pencereyi kapatmak yetmez!

**Mac:**
```
Cmd + Q (tamamen kapat)
Yeniden aç
```

**Windows:**
```
Sistem tepsisi → Sağ tık → Quit
Yeniden aç
```

---

### 3️⃣ Test Edin!

Claude Desktop'ta yeni sohbet açın:

```
MCP araçlarımı listele
```

**Göreceğiniz:**
```
📦 Mevcut MCP sunucuları:

godot (7 araç)
  - set_godot_project
  - list_godot_scenes
  - ...

photoshop (12 araç)
  - photoshop_check_connection
  - photoshop_open_file
  - ...

aftereffects (15 araç)
  - ae_create_composition
  - ae_render_composition
  - ...
```

✅ **Araçları görüyorsanız kurulum başarılı!**

---

## ✅ İlk Testler

### Godot

```
Godot projem /home/user/MyGame dizininde, bağlan
```

```
Projemde hangi sahneler var?
```

---

### Photoshop

```
Photoshop bağlantımı kontrol et
```

```
Aktif doküman hakkında bilgi ver
```

```
Bu görüntüyü 800x600 piksel yap
```

---

### After Effects

```
After Effects bağlantımı kontrol et
```

```
"Test" adında yeni comp oluştur (1920x1080, 5s, 30fps)
```

```
"HELLO WORLD" yazısı ekle ve fade-in animasyon yap
```

---

## 🎨 Birlikte Kullanım

Tüm araçları aynı anda kullanabilirsiniz!

### Örnek Workflow:

```
Tam bir video production workflow oluştur:

1. TASARIM (Photoshop):
   "Desktop/banner.psd dosyasını aç"
   "Yeni bir layer oluştur, 'Title' adında"
   "Title layer'a 'YENİ ÜRÜN' yazısı ekle, kırmızı, 96pt"
   "PNG olarak Desktop/title.png'ye kaydet"

2. ANİMASYON (After Effects):
   "Desktop/title.png'yi After Effects'e import et"
   "'Product Intro' comp oluştur (1920x1080, 5s, 30fps)"
   "Title'ı comp'a ekle"
   "Scale animasyonu ekle (0s: 0%, 2s: 100%)"
   "Glow effect ekle"
   "Desktop/intro.mov olarak render et"

3. OYUN ENTEGRASYONu (Godot - opsiyonel):
   "Godot projemde 'ui/intro_video.tres' resource'u oluştur"
   "intro.mov'u Godot'a import et"
```

**Sonuç:** Photoshop → After Effects → Godot, hepsi Claude üzerinden! 🚀

---

## 🛠️ Config Dosyanız

Kurulum sonrası config dosyanız şöyle görünecek:

**Konum:**
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**İçerik:**
```json
{
  "mcpServers": {
    "godot": {
      "command": "python3",
      "args": ["/home/user/depo/godot_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    },
    "photoshop": {
      "command": "python3",
      "args": ["/home/user/depo/photoshop_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    },
    "aftereffects": {
      "command": "python3",
      "args": ["/home/user/depo/aftereffects_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    }
  }
}
```

---

## 🐛 Sorun Giderme

### ❌ "MCP araçlarını göremiyorum"

**Çözüm:**
1. Claude Desktop'ı **tamamen** kapattınız mı? (Cmd+Q / Quit)
2. Config dosyası doğru konumda mı?
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```
3. JSON syntax'ı doğru mu? (virgüller, parantezler)

---

### ❌ "Photoshop/After Effects'e bağlanılamadı"

**Çözüm:**
1. İlgili uygulama açık mı?
2. (Mac) System Preferences → Automation izinleri verildi mi?
3. (Windows) pywin32 yüklü mü?
   ```bash
   pip show pywin32
   ```

---

### ❌ "Godot project not set"

**Çözüm:**
1. Godot açık mı?
2. Bir proje açık mı?
3. Claude'a proje yolunu söyleyin:
   ```
   Godot projem /tam/yol/buraya dizininde
   ```

---

### ❌ Script çalışmıyor

```bash
# Executable olduğundan emin olun
chmod +x install_all_mcp.sh

# Çalıştırın
./install_all_mcp.sh
```

---

## 📚 Daha Fazla Bilgi

Her sunucu için detaylı dokümantasyon:

| Sunucu | Hızlı Başvuru | Detaylı Rehber | Örnekler |
|--------|---------------|----------------|----------|
| **Godot** | `README.md` | `SETUP_TR.md` | README içinde |
| **Photoshop** | `PHOTOSHOP_CHEATSHEET.md` | `PHOTOSHOP_WORKFLOW_TR.md` | `PHOTOSHOP_EXAMPLES.md` (30+) |
| **After Effects** | `AFTEREFFECTS_QUICKSTART.md` | - | `AFTEREFFECTS_EXAMPLES.md` (22+) |

---

## 🎯 Toplam Yetenekleriniz

Artık Claude Desktop ile:

### 🎮 Godot (7 araç)
- Proje keşfi
- Sahne ve script yönetimi
- Kod okuma/yazma

### 🎨 Photoshop (12 araç)
- Görüntü düzenleme
- Layer yönetimi
- Batch işlemler
- Filtreler

### 🎬 After Effects (15 araç)
- Composition oluşturma
- Text ve solid layer'lar
- Animasyonlar (keyframe)
- Video rendering

**TOPLAM: 34 araç, tek bir Claude arayüzünden!** 🚀

---

## 💡 Pratik Senaryolar

### Video Game Developer

```
1. Godot'ta oyun sahnesini düzenle
2. Photoshop'ta UI elementlerini tasarla
3. After Effects'te intro animasyonu oluştur
4. Hepsini Godot'a import et
```

---

### Content Creator

```
1. Photoshop'ta thumbnail tasarla
2. After Effects'te intro/outro oluştur
3. Hepsini render et ve yükle
```

---

### Graphic Designer

```
1. Photoshop'ta grafik tasarla
2. After Effects'te animasyon ekle
3. Müşteriye sunum yap
```

---

## 🎉 Hazırsınız!

**Tek komut:**
```bash
./install_all_mcp.sh
```

**Sonuç:**
- ✅ 3 sunucu kurulu
- ✅ 34 araç hazır
- ✅ Claude Desktop entegre
- ✅ Otomatik workflow'lar

**Harika projeler oluşturun! 🚀✨**
