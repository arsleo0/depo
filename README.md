# 🚀 MCP Sunucuları - Claude Desktop Entegrasyonları

Claude Desktop ile **Godot, Photoshop, After Effects ve TripoSR**'ı kontrol edin!

Bu proje, Claude Desktop'ın MCP (Model Context Protocol) üzerinden lokal yazılımlarla konuşmasını sağlayan tam özellikli sunucular içerir.

---

## ✨ Özellikler

### 🎮 Godot MCP Server
- Proje keşfi ve sahne yönetimi
- GDScript okuma/yazma
- Proje ayarlarını inceleme
- **7 araç**

### 🎨 Photoshop MCP Server
- Görüntü düzenleme ve layer yönetimi
- Filtreler (Blur, Sharpen, Brightness)
- Batch işlemler
- JSX script desteği
- **12 araç**

### 🎬 After Effects MCP Server
- Composition oluşturma
- Text ve solid layer'lar
- Keyframe animasyonları
- Video rendering (H.264, ProRes)
- Hazır animasyon şablonları
- **15 araç**

### 🔷 TripoSR MCP Server
- Görüntüden 3D model oluşturma
- Otomatik arka plan kaldırma
- Toplu işlem (batch processing)
- OBJ ve GLB format desteği
- GPU/CUDA hızlandırma
- **5 araç**

**TOPLAM: 39 araç, tek bir Claude arayüzünden!**

---

## 🚀 Hızlı Kurulum (5 Dakika!)

### Seçenek 1: Hepsini Birden Kur (Önerilen)

```bash
# 1. Repository'yi klonlayın
git clone <repo-url> ~/depo
cd ~/depo

# 2. Tek komutla tüm sunucuları kurun
./install_all_mcp.sh

# 3. İlgili uygulamaları açın (Godot, Photoshop, After Effects)
#    TripoSR için uygulama açmanıza gerek yok (arka planda çalışır)

# 4. Claude Desktop'ı yeniden başlatın (Cmd+Q / tamamen kapat)

# 5. Test edin!
```

Claude'da yazın:
```
MCP araçlarımı listele
```

✅ **39 araç görüyorsanız, kurulum başarılı!**

---

### Seçenek 2: Sadece İstediğini Kur

```bash
# Sadece Photoshop
./install_all_mcp.sh photoshop

# Photoshop + After Effects
./install_all_mcp.sh photoshop aftereffects

# Godot + Photoshop
./install_all_mcp.sh godot photoshop

# Sadece TripoSR (3D model oluşturma)
./install_triposr_mcp.sh

# Hepsi + TripoSR
./install_all_mcp.sh && ./install_triposr_mcp.sh
```

---

## 📚 Detaylı Dokümantasyon

| Sunucu | Hızlı Başlangıç | Rehber | Örnekler |
|--------|-----------------|--------|----------|
| **🎮 Godot** | [GODOT_README.md](GODOT_README.md) | [SETUP_TR.md](SETUP_TR.md) | GODOT_README.md |
| **🎨 Photoshop** | [PHOTOSHOP_CHEATSHEET.md](PHOTOSHOP_CHEATSHEET.md) | [PHOTOSHOP_WORKFLOW_TR.md](PHOTOSHOP_WORKFLOW_TR.md) | [PHOTOSHOP_EXAMPLES.md](PHOTOSHOP_EXAMPLES.md) (30+) |
| **🎬 After Effects** | [AFTEREFFECTS_QUICKSTART.md](AFTEREFFECTS_QUICKSTART.md) | - | [AFTEREFFECTS_EXAMPLES.md](AFTEREFFECTS_EXAMPLES.md) (22+) |
| **🔷 TripoSR** | [TRIPOSR_QUICKSTART.md](TRIPOSR_QUICKSTART.md) | - | TRIPOSR_QUICKSTART.md (10+) |
| **🚀 Hepsi** | **[QUICKSTART_TR.md](QUICKSTART_TR.md)** ⭐ | - | - |

---

## 🎯 Kullanım Örnekleri

### 🎮 Godot

```
Claude'a sor:
"Godot projem /home/user/MyGame dizininde, bağlan"
"Projemde hangi sahneler var?"
"scripts/player.gd dosyasını oku"
"Yeni bir enemy.gd scripti oluştur"
```

---

### 🎨 Photoshop

```
Claude'a sor:
"Photoshop bağlantımı kontrol et"
"Desktop/photo.jpg dosyasını aç"
"Bu görüntüyü 800x600 piksel yap"
"5 piksel Gaussian Blur uygula"
"PNG olarak Desktop/output.png'ye kaydet"
```

---

### 🎬 After Effects

```
Claude'a sor:
"After Effects bağlantımı kontrol et"
"'Intro' comp oluştur (1920x1080, 5s, 30fps)"
"'HELLO WORLD' yazısı ekle ve fade-in animasyon yap"
"Desktop/intro.mov olarak render et"
```

---

### 🔷 TripoSR (3D Model Oluşturma)

```
Claude'a sor:
"TripoSR durumunu kontrol et"
"Desktop/mug.jpg görüntüsünden 3D model oluştur"
"Oluşturulan modeli mug_3d olarak kaydet"
"Oluşturduğum 3D modelleri listele"
```

---

### 🔥 Birlikte Kullanım!

```
Tam video production workflow:

1. Photoshop'ta banner tasarla:
   "Desktop/banner.psd'yi aç"
   "Yeni layer oluştur, 'YENİ ÜRÜN' yaz (kırmızı, 96pt)"
   "PNG olarak kaydet: Desktop/title.png"

2. After Effects'te animasyon yap:
   "Desktop/title.png'yi import et"
   "'Product Intro' comp oluştur (1920x1080, 5s)"
   "Scale animasyonu ekle (0→100%)"
   "Glow effect ekle"
   "Render: Desktop/intro.mov"

3. Godot'ta entegre et (opsiyonel):
   "intro.mov'u Godot projeme import et"
```

**Sonuç:** Photoshop → After Effects → Godot, hepsi Claude üzerinden! 🎉

---

```
3D oyun asset pipeline:

1. TripoSR ile gerçek nesneyi 3D'ye çevir:
   "Desktop/chair.jpg'den 3D model oluştur"

2. Blender'da düzenle (manuel):
   - Modeli temizle
   - UV unwrap yap
   - Texture ekle

3. Photoshop'ta texture oluştur:
   "1024x1024 yeni doküman"
   "Ahşap texture uygula"
   "Kaydet: Desktop/chair_texture.png"

4. Godot'a import et:
   "chair_3d.glb'yi Godot projeme kopyala"
   "Texture'ı chair_texture.png olarak ata"
```

**Sonuç:** Gerçek Dünya → TripoSR → Blender → Photoshop → Godot, tam 3D pipeline! 🎮

---

## 🛠️ Nasıl Çalışır?

```
┌─────────────────┐
│ Claude Desktop  │  "Bu görüntüyü 800x600 yap"
└────────┬────────┘
         │ MCP Protocol
         ▼
┌─────────────────────────┐
│ MCP Sunucuları (Python) │
│  - Godot Server         │
│  - Photoshop Server     │
│  - After Effects Server │
│  - TripoSR Server       │
└────────┬────────────────┘
         │
         │ Mac: AppleScript
         │ Windows: COM/Win32
         │ JSX/ExtendScript
         │ PyTorch + TripoSR AI
         ▼
┌─────────────────┐
│ Lokal Yazılımlar│
│  - Godot        │
│  - Photoshop    │
│  - After Effects│
│  - TripoSR AI   │
└─────────────────┘
```

**Avantajlar:**
- ⚡ **Anlık** - gerçek zamanlı kontrol
- 💰 **Ücretsiz** - API key gerekmez
- 🔒 **Offline** - internet gerekmez
- 🎨 **Tam özellikli** - tüm yazılım özellikleri
- 🤖 **Doğal dil** - konuşarak kontrol

---

## 📋 Gereksinimler

### Yazılım
- **Python 3.10+**
- **Claude Desktop** (en güncel sürüm)
- **MCP SDK** (`pip install mcp`)
- **pywin32** (sadece Windows için)

### Uygulamalar (İsteğe Bağlı)
- **Godot Engine** (3.x veya 4.x)
- **Adobe Photoshop** (2020+)
- **Adobe After Effects** (2020+)

### İşletim Sistemi
- ✅ **macOS** (10.15+)
- ✅ **Windows** (10/11)
- ✅ **Linux** (Adobe uygulamaları Wine ile)

---

## 🎓 Kullanım Senaryoları

### 🎮 Game Developer
```
- Godot'ta oyun geliştir
- Photoshop'ta UI/asset oluştur
- After Effects'te intro/cutscene yap
```

### 🎥 Content Creator (YouTube, TikTok)
```
- Photoshop'ta thumbnail tasarla
- After Effects'te intro/outro oluştur
- Batch rendering ve automation
```

### 🎨 Graphic/Motion Designer
```
- Photoshop'ta grafik tasarla
- After Effects'te animasyon ekle
- Müşteriye hızlı sunum
```

### 💼 Digital Agency
```
- Tüm asset pipeline'ı otomatize et
- Batch işlemler (logo variations)
- Brand guidelines uygula
```

### 🏗️ 3D Modelleme & AR/VR
```
- Gerçek nesnelerin 3D dijital kopyalarını oluştur
- E-ticaret için AR uygulamaları
- Oyun ve simülasyon için asset üret
- Müze ve kültürel miras dijitalleştirme
```

---

## 🔧 Yapılandırma

Kurulum sonrası Claude Desktop config dosyanız:

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
    },
    "triposr": {
      "command": "python3",
      "args": ["/home/user/depo/triposr_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    }
  }
}
```

---

## 🐛 Sorun Giderme

### ❌ "MCP araçlarını göremiyorum"

**Çözüm:**
1. Claude Desktop'ı **tamamen** kapatıp yeniden açın (Cmd+Q)
2. Config dosyası doğru konumda mı kontrol edin
3. JSON syntax'ı doğru mu kontrol edin

---

### ❌ "Photoshop/After Effects'e bağlanılamadı"

**Çözüm:**
1. İlgili uygulama açık mı?
2. (Mac) System Preferences → Security → Automation izinleri
3. (Windows) `pip install pywin32` yüklü mü?

---

### ❌ "Godot project not set"

**Çözüm:**
```
Godot projem /tam/yol/buraya dizininde
```

---

### 🔍 Developer Console

Detaylı debug için:
- **Mac:** `Cmd + Option + Shift + I`
- **Windows:** `Ctrl + Shift + I`

Console'da server loglarını görebilirsiniz.

---

## 🎨 Örnek Projeler

### 1. YouTube İçerik Pipeline

```python
# Photoshop: Thumbnail tasarla
"Desktop/video_screenshot.jpg'yi aç"
"'BÖLÜM 5' yazısı ekle, büyük, kırmızı"
"Desktop/thumbnail.png olarak kaydet"

# After Effects: Intro oluştur
"'Intro' comp oluştur (1920x1080, 5s)"
"Logo reveal animasyonu yap"
"Desktop/intro.mov render et"

# Sonuç: Hazır YouTube içeriği!
```

---

### 2. Oyun Asset Pipeline

```python
# Photoshop: UI elementi tasarla
"1920x1080 yeni doküman oluştur"
"Button tasarla (mavi gradient, rounded)"
"PNG sequence olarak kaydet (normal, hover, pressed)"

# Godot: Import ve setup
"Desktop/ui_button_*.png'leri Godot'a import et"
"Button sahnesini oluştur"
```

---

### 3. Kurumsal Brand Video

```python
# Photoshop: Logo ve grafik hazırla
"Desktop/raw_logo.psd'yi aç"
"Farklı boyutlarda export et (512, 256, 128)"

# After Effects: Corporate video
"'Brand Video' comp oluştur (1920x1080, 30s)"
"Logo'yu import et"
"Professional animation template uygula"
"Lower third'ler ekle"
"H.264 render et"
```

---

## 📊 İstatistikler

| Metrik | Değer |
|--------|-------|
| **Toplam Araç** | 39 |
| **Sunucu Sayısı** | 4 |
| **Desteklenen Yazılım** | 4 (Godot, Photoshop, After Effects, TripoSR) |
| **Toplam Kod Satırı** | ~5500 |
| **Dokümantasyon Dosyası** | 15 |
| **Örnek Sayısı** | 60+ |

---

## 🚀 Gelecek Özellikler

Planlanan ek entegrasyonlar:

- [x] **TripoSR** - AI ile görüntüden 3D model oluşturma ✅
- [ ] **Illustrator** - Vektör grafik düzenleme
- [ ] **InDesign** - Sayfa düzeni
- [ ] **Premiere Pro** - Video editing
- [ ] **Lightroom** - Fotoğraf düzenleme
- [ ] **Blender** - 3D modelleme ve düzenleme
- [ ] **Maya** - 3D animasyon
- [ ] **Unity** - Oyun motoru
- [ ] **Unreal Engine** - Oyun motoru
- [ ] **Stable Diffusion** - AI görüntü oluşturma

**Hangisini istersiniz?** Issue açın veya PR gönderin!

---

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır!

**Eklenebilecek özellikler:**
- Yeni Adobe yazılım entegrasyonları
- Daha fazla Godot fonksiyonu
- Batch processing iyileştirmeleri
- Yeni animasyon şablonları
- Daha fazla örnek ve tutorial

---

## 📄 Lisans

MIT

---

## 💡 İpuçları

1. **Performans:** Büyük dosyalarla çalışırken uygulamalara yeterli RAM ayırın
2. **Güvenlik:** JSX scriptleri güçlüdür, trusted kaynaklardan çalıştırın
3. **Backup:** Önemli dosyalarda işlem yapmadan önce backup alın
4. **Workflow:** Sık tekrar eden işlemleri not edin, Claude'a tek komutla yaptırın

---

## 📞 Destek

Sorun yaşıyorsanız:

1. **Dokümantasyonu okuyun:**
   - [QUICKSTART_TR.md](QUICKSTART_TR.md) - Hızlı başlangıç
   - İlgili sunucu dokümantasyonu

2. **Developer Console'u kontrol edin:**
   - Cmd+Option+Shift+I (Mac)
   - Ctrl+Shift+I (Windows)

3. **Server'ı manuel test edin:**
   ```bash
   python3 godot_mcp_server.py
   python3 photoshop_mcp_server.py
   python3 aftereffects_mcp_server.py
   ```

4. **Issue açın:**
   - GitHub Issues
   - Detaylı hata mesajları ekleyin
   - Platform ve versiyon belirtin

---

## 🎉 Başarılar!

Artık Claude Desktop ile Godot, Photoshop ve After Effects'i kontrol edebilirsiniz!

**Tek komut:**
```bash
./install_all_mcp.sh
```

**Sonuç:**
- ✅ 4 sunucu çalışıyor
- ✅ 39 araç kullanıma hazır
- ✅ Sınırsız yaratıcılık potansiyeli
- ✅ AI destekli 3D model oluşturma

**Harika projeler oluşturun! 🚀✨**

---

## 🔗 Bağlantılar

- [MCP Protocol Docs](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/desktop)
- [Godot Engine](https://godotengine.org/)
- [Adobe Creative Cloud](https://www.adobe.com/creativecloud.html)
- [ExtendScript Guide](https://www.adobe.com/devnet/scripting.html)

---

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!**
