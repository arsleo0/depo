# 🎬 After Effects MCP Server - Hızlı Başlangıç

Adobe After Effects'i Claude Desktop ile kontrol edin!

---

## ⚡ Hızlı Kurulum

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements-aftereffects.txt

# 2. Server'ı test et (After Effects'i önce açın!)
python3 aftereffects_mcp_server.py

# Görmek istediğiniz:
# [AE-MCP] INFO: After Effects MCP Server başlatılıyor...
# [AE-MCP] INFO: MCP server hazır ve bağlantı bekliyor...
```

---

## ⚙️ Claude Desktop Yapılandırması

### Mac

```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Linux

```bash
nano ~/.config/Claude/claude_desktop_config.json
```

**Config içeriği:**

```json
{
  "mcpServers": {
    "aftereffects": {
      "command": "python3",
      "args": ["/TAM/YOL/aftereffects_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    }
  }
}
```

**Mevcut server'larınız varsa (Photoshop, Godot):**

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

## ✅ İlk Test

1. **After Effects'i açın**

2. **Claude Desktop'ı yeniden başlatın** (Cmd+Q / tamamen kapat)

3. **Claude'a yazın:**

```
After Effects bağlantımı kontrol et
```

**Başarılı çıktı:**
```
✅ After Effects bağlantısı başarılı!
Adobe After Effects 2024 24.0
Platform: Darwin
```

---

## 🎯 Temel Kullanım

### 1. Proje Bilgisi

```
After Effects projem hakkında bilgi ver
```

### 2. Composition Oluşturma

```
"Intro" adında yeni bir composition oluştur:
- Boyut: 1920x1080
- Süre: 5 saniye
- Frame rate: 30fps
```

### 3. Text Animasyonu

```
Aktif composition'a "MERHABA DÜNYA" yazısı ekle ve fade-in animasyonu yap
```

### 4. Katman Ekleme

```
Aktif composition'a kırmızı bir solid layer ekle, "Background" adında
```

### 5. Effect Uygulama

```
"Background" layer'ına Gaussian Blur effect'i uygula
```

### 6. Keyframe Animasyonu

```
"MERHABA DÜNYA" layer'ına şu animasyonu ekle:
- 0 saniyede opacity %0
- 2 saniyede opacity %100
```

### 7. Render

```
"Intro" composition'ını render et:
- Output: Desktop/intro.mov
- Format: H.264
```

---

## 🎨 Desteklenen İşlemler

| Kategori | Özellikler |
|----------|-----------|
| **Composition** | Oluşturma, listeleme, aktif comp bilgisi |
| **Layers** | Solid, text, footage ekleme, listeleme |
| **Import** | Video, image, audio dosyalarını projeye ekleme |
| **Effects** | Blur, Glow, Drop Shadow, Brightness, Hue/Saturation |
| **Animation** | Keyframe (position, scale, rotation, opacity) |
| **Render** | H.264, ProRes, PNG Sequence export |
| **Templates** | Fade in, logo reveal, lower third, slide in |
| **JSX** | Özel script çalıştırma |

---

## 💡 Pratik Örnekler

### Örnek 1: YouTube Intro

```
Bana yardım et, YouTube intro oluştur:
1. "YouTube Intro" adında 1920x1080, 5 saniye comp oluştur
2. Mavi solid background ekle
3. "KANAL ADI" yazısı ekle (büyük, beyaz, ortada)
4. Yazıya scale animasyonu ekle (0'dan 100'e)
5. Desktop/intro.mov olarak render et
```

### Örnek 2: Lower Third (Alt Yazı)

```
Lower third animasyonu oluştur:
- Text: "John Doe - CEO"
- Sol alttan slide-in animasyon
- 3 saniye süreli
```

### Örnek 3: Logo Reveal

```
Desktop/logo.png dosyasını import et ve logo reveal animasyonu oluştur:
- Scale 0'dan 100'e
- Rotation 360 derece
- 2 saniye sürede
```

### Örnek 4: Video Montaj

```
Desktop/Videos/ klasöründeki tüm MP4 dosyalarını import et ve sırayla timeline'a ekle
```

### Örnek 5: Batch Render

```
Tüm composition'ları Desktop/Renders/ klasörüne H.264 formatında render et
```

---

## 🛠️ 15 Araç (Tools)

1. **ae_check_connection** - Bağlantı testi
2. **ae_get_project_info** - Proje bilgisi
3. **ae_create_composition** - Comp oluşturma
4. **ae_list_compositions** - Comp listeleme
5. **ae_add_solid_layer** - Solid katman
6. **ae_add_text_layer** - Text katman
7. **ae_import_file** - Dosya import
8. **ae_add_footage_to_comp** - Footage placement
9. **ae_list_layers** - Layer listeleme
10. **ae_apply_effect** - Effect uygulama
11. **ae_set_keyframe** - Keyframe animasyon
12. **ae_render_composition** - Render
13. **ae_save_project** - Proje kaydet
14. **ae_execute_jsx** - Özel JSX
15. **ae_create_simple_animation** - Animasyon şablonları

---

## 🎬 Animasyon Şablonları

### Text Fade In

```
"text_fade_in" şablonuyla "HELLO WORLD" animasyonu oluştur, 3 saniye
```

### Logo Reveal

```
"logo_reveal" şablonuyla logo animasyonu oluştur
```

### Lower Third

```
"lower_third" şablonuyla "John Doe - CEO" alt yazısı oluştur
```

### Slide In

```
"slide_in" şablonuyla slide animasyonu oluştur
```

---

## 🚀 Gelişmiş - JSX

After Effects'in tüm gücüne JSX ile erişin:

```
Şu JSX kodunu çalıştır:

var comp = app.project.activeItem;
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    layer.property("Opacity").setValue(50);
}
"Tüm layer'ların opacity'si %50 yapıldı";
```

---

## 🎯 Kullanım Senaryoları

### Content Creator (YouTube, TikTok)

- **Intro/outro oluşturma**
- **Lower third'ler**
- **Subscribe animasyonları**
- **Transition'lar**

### Video Editor

- **Text animasyonları**
- **Color correction batch**
- **Render otomasyonu**
- **Template oluşturma**

### Motion Designer

- **Karmaşık animasyonlar**
- **Keyframe workflow**
- **Effect chain'leri**
- **Expression'lar (JSX ile)**

### Social Media Manager

- **Instagram stories**
- **Facebook ads**
- **TikTok effects**
- **Batch content creation**

---

## 🐛 Sorun Giderme

### ❌ "After Effects'e bağlanılamadı"

**Çözüm:**
1. After Effects açık mı?
2. (Mac) System Preferences → Automation izinleri
3. (Windows) `pip install pywin32`

### ❌ "Aktif composition yok"

After Effects'te bir composition oluşturun veya mevcut comp'u açın.

### ❌ MCP araçları görünmüyor

1. Config dosyasını kontrol edin
2. PATH'ler doğru mu?
3. Claude'u tamamen kapatıp yeniden açın

---

## 📚 Daha Fazla Bilgi

**JSX Scripting Guide:**
- https://ae-scripting.docsforadobe.dev/

**After Effects API:**
- https://helpx.adobe.com/after-effects/using/scripts.html

**MCP Protocol:**
- https://modelcontextprotocol.io/

---

## 🎉 Başarılar!

Artık After Effects'i Claude ile kontrol edebilirsiniz!

**Unutmayın:**
- ✅ After Effects açık olmalı
- ✅ Claude Desktop yeniden başlatılmış olmalı
- ✅ Config doğru ayarlanmış olmalı

**Harika videolar oluşturun! 🎬✨**
