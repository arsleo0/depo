# Photoshop MCP Server - Claude Desktop & Adobe Photoshop Entegrasyonu 🎨

Claude Desktop uygulamasını Adobe Photoshop ile entegre eder. Claude, Photoshop'u kontrol edebilir, görüntü düzenlemeleri yapabilir, katmanları yönetebilir ve otomasyonlar çalıştırabilir!

## ✨ Özellikler

- 📂 **Dosya İşlemleri**: PSD, JPG, PNG, TIFF dosyalarını açma/kaydetme
- 🎨 **Katman Yönetimi**: Katman oluşturma, listeleme, düzenleme
- 🖼️ **Görüntü İşleme**: Yeniden boyutlandırma, kırpma, döndürme
- 🎭 **Filtreler**: Blur, Sharpen, Brightness/Contrast, Hue/Saturation
- ✍️ **Metin Ekleme**: Özelleştirilebilir font, boyut, renk
- 🔄 **Batch İşlemler**: Birden fazla dosyayı toplu işleme
- 💻 **Platformlar Arası**: Mac ve Windows desteği
- 🤖 **Doğal Dil Kontrolü**: Claude ile konuşarak Photoshop'u yönetin

## 🛠️ Desteklenen İşlemler

| Kategori | İşlemler |
|----------|----------|
| **Dosya** | Aç, Kaydet, Dışa Aktar (JPG, PNG, PSD, TIFF) |
| **Katman** | Oluştur, Sil, Gizle/Göster, Opacity, Blend Mode |
| **Düzenleme** | Resize, Crop, Rotate, Flip |
| **Filtreler** | Gaussian Blur, Sharpen, Invert, Brightness/Contrast |
| **Metin** | Metin katmanı ekle, font ayarları, renk |
| **Otomasyon** | Batch resize, JSX script çalıştırma |

## 📋 Gereksinimler

### Yazılım
- **Adobe Photoshop**: 2020 veya daha yeni (CC 2020, 2021, 2022, 2023, 2024)
- **Python**: 3.10 veya üzeri
- **Claude Desktop**: En güncel sürüm

### İşletim Sistemi
- ✅ **macOS**: 10.15 (Catalina) veya üzeri
- ✅ **Windows**: 10/11
- ❌ **Linux**: Doğrudan destek yok (Wine ile deneyebilirsiniz)

## 🚀 Kurulum

### 1. Repository'yi İndirin

```bash
cd ~/depo
# Dosyalar zaten mevcut:
# - photoshop_mcp_server.py
# - requirements-photoshop.txt
# - PHOTOSHOP_README.md
```

### 2. Python Bağımlılıklarını Yükleyin

```bash
# MCP SDK'yı yükle
pip install -r requirements-photoshop.txt

# VEYA manuel:
pip install mcp

# Windows kullanıcıları için ek (COM automation):
pip install pywin32  # Sadece Windows'ta
```

### 3. Server'ı Test Edin

Photoshop'u açın, sonra:

```bash
python3 photoshop_mcp_server.py
```

Şu logları görmelisiniz:
```
[PHOTOSHOP-MCP] INFO: Photoshop MCP Server başlatılıyor...
[PHOTOSHOP-MCP] INFO: Platform: Darwin  # (veya Windows)
[PHOTOSHOP-MCP] INFO: MCP server hazır ve bağlantı bekliyor...
```

`Ctrl+C` ile çıkın.

### 4. Claude Desktop'ı Yapılandırın

#### 🍎 **macOS Kullanıcıları:**

Config dosyasını düzenleyin:
```bash
nano ~/.config/Claude/claude_desktop_config.json
```

**VEYA** Godot sunucunuz varsa, mevcut config'e ekleyin:

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
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**ÖNEMLİ:** `/home/user/depo/photoshop_mcp_server.py` yolunu kendi sisteminize göre değiştirin!

```bash
# Tam yolu almak için:
cd ~/depo
pwd
# Çıktı: /home/kullanici/depo
# O zaman: /home/kullanici/depo/photoshop_mcp_server.py
```

#### 🪟 **Windows Kullanıcıları:**

1. Dosya Gezgini'nde şu adrese gidin:
   ```
   %APPDATA%\Claude
   ```

2. `claude_desktop_config.json` dosyasını düzenleyin:

```json
{
  "mcpServers": {
    "photoshop": {
      "command": "python",
      "args": [
        "C:\\Users\\KULLANICI_ADIN\\depo\\photoshop_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Not:** Windows'ta backslash'leri çift yapın: `C:\\Users\\...`

### 5. Claude Desktop'ı Yeniden Başlatın

- Claude Desktop'ı **tamamen kapatın** (sistem tepsisinde de olmamalı)
- Yeniden açın
- Yeni bir sohbet başlatın

### 6. Test Edin! 🎉

Claude'a şunu yazın:

```
MCP araçlarımı listele
```

"photoshop" server'ını ve araçları görmelisiniz:
- ✅ photoshop_check_connection
- ✅ photoshop_get_info
- ✅ photoshop_open_file
- ✅ photoshop_save_file
- ✅ photoshop_create_layer
- ✅ photoshop_list_layers
- ✅ photoshop_apply_filter
- ✅ photoshop_add_text
- ✅ photoshop_resize_image
- ✅ photoshop_crop
- ✅ photoshop_execute_jsx
- ✅ photoshop_batch_resize

## 📖 Kullanım Örnekleri

### 1️⃣ Bağlantıyı Test Etme

```
Photoshop bağlantımı kontrol et
```

Claude otomatik olarak `photoshop_check_connection` aracını kullanacak.

### 2️⃣ Dosya Açma

```
/Users/kullanici/Pictures/photo.jpg dosyasını Photoshop'ta aç
```

```
C:\Users\Kullanici\Desktop\image.psd dosyasını aç
```

### 3️⃣ Aktif Doküman Bilgileri

```
Şu anki Photoshop dokümanı hakkında bilgi ver
```

Çıktı:
```
📄 Aktif Doküman Bilgileri:

📝 İsim: portrait.jpg
📏 Boyut: 1920 x 1080 piksel
🎨 Renk Modu: RGBColorMode
🔍 Çözünürlük: 72 DPI
📚 Katman Sayısı: 3
💾 Yol: /Users/kullanici/portrait.jpg
```

### 4️⃣ Görüntüyü Yeniden Boyutlandırma

```
Bu görüntüyü 800x600 piksel boyutuna küçült
```

### 5️⃣ Filtre Uygulama

```
Aktif katmana 10 piksel Gaussian Blur uygula
```

```
Görüntüyü keskinleştir (sharpen)
```

### 6️⃣ Metin Ekleme

```
Görüntünün üstüne "YARIN ÇIKARIM" yazısını ekle, kırmızı renkte, 48pt boyutunda
```

### 7️⃣ Katman İşlemleri

```
"Yeni Efekt" adında bir katman oluştur
```

```
Tüm katmanları listele
```

Çıktı:
```
📚 Katmanlar:

1. 👁️ Yeni Efekt (Opacity: 100%)
2. 👁️ Background copy (Opacity: 80%)
3. 🚫 Background (Opacity: 100%)
```

### 8️⃣ Batch İşlemler

```
/Users/kullanici/Photos klasöründeki tüm resimleri 1024x768'e resize et ve /Users/kullanici/Output klasörüne JPG olarak kaydet
```

### 9️⃣ Kaydetme ve Dışa Aktarma

```
Bu dosyayı PNG formatında kaydet: /Users/kullanici/Desktop/output.png
```

```
JPEG olarak kaydet, kalite 12
```

### 🔟 Gelişmiş: Özel JSX Script Çalıştırma

```
Şu JSX kodunu çalıştır:

var doc = app.activeDocument;
for (var i = 0; i < doc.layers.length; i++) {
    doc.layers[i].opacity = 50;
}
"Tüm katmanların opacity'si %50 yapıldı";
```

## 🎯 Pratik Kullanım Senaryoları

### Senaryo 1: Logo Batch İşleme

```
Bana yardım et: /Users/kullanici/Logos klasöründeki tüm logoları:
1. 512x512 piksel boyutuna getir
2. PNG olarak dışa aktar
3. /Users/kullanici/Logos_Export klasörüne kaydet
```

### Senaryo 2: Fotoğraf Düzenleme Workflow

```
1. /Users/kullanici/portrait.jpg dosyasını aç
2. 5 piksel Gaussian Blur uygula
3. Brightness/Contrast ayarla
4. Sol üst köşeye "© 2024" watermark ekle
5. JPEG olarak kaydet, maksimum kalite
```

### Senaryo 3: Sosyal Medya İçeriği Oluşturma

```
1. Yeni bir 1080x1080 piksel doküman oluştur
2. Arka plana gradient ekle
3. Ortaya "YENİ ÜRÜN" başlığı ekle (beyaz, 72pt)
4. Alt kısma küçük açıklama metni ekle
5. Instagram için PNG olarak kaydet
```

## 🐛 Sorun Giderme

### ❌ "Photoshop'a bağlanılamadı" Hatası

**Sebep:**
- Photoshop açık değil
- Photoshop scripting desteği kapalı

**Çözüm:**
1. Adobe Photoshop'u açın
2. Preferences → Scripting → "Enable Remote Connections" açık olmalı (bazı versiyonlarda)
3. Server'ı tekrar test edin

### ❌ "pywin32 yüklü değil" (Windows)

```bash
pip install pywin32
```

Kurulumdan sonra:
```bash
python Scripts/pywin32_postinstall.py -install
```

### ❌ JSON Parse Error

**Sebep:** Server stdout'a log yazıyor (yazmamalı)

**Kontrol:**
- `photoshop_mcp_server.py` dosyasında `logging.basicConfig(stream=sys.stderr)` var mı?
- Hiçbir yerde `print()` kullanılmıyor mu?

### ❌ "Unable to execute JSX" (Mac)

**Sebep:** macOS'ta AppleScript izinleri

**Çözüm:**
1. System Preferences → Security & Privacy → Automation
2. Terminal veya Claude Desktop'a Adobe Photoshop'u kontrol etme izni verin

### ❌ Server Başlamıyor

Developer Console'u açın:
- **Mac:** `Cmd + Option + Shift + i`
- **Windows/Linux:** `Ctrl + Shift + i`

Console'da hataları kontrol edin.

Manuel test:
```bash
python3 photoshop_mcp_server.py
# Çıkan hataları okuyun
```

## 🎓 JSX (ExtendScript) Hakkında

Photoshop'un scripting dili JSX (JavaScript Extended) kullanır. İleri düzey kullanıcılar için:

### Örnek JSX Scriptleri

**Tüm katmanları hizala:**
```javascript
var doc = app.activeDocument;
for (var i = 0; i < doc.layers.length; i++) {
    doc.layers[i].translate(0, 100); // 100px aşağı kaydır
}
```

**Smart Object oluştur:**
```javascript
var doc = app.activeDocument;
var layer = doc.activeLayer;
layer.convertToSmartObject();
```

**Batch Watermark:**
```javascript
var folder = new Folder("~/Desktop/Photos");
var files = folder.getFiles(/\.(jpg|png)$/i);

for (var i = 0; i < files.length; i++) {
    var doc = app.open(files[i]);

    var textLayer = doc.artLayers.add();
    textLayer.kind = LayerKind.TEXT;
    textLayer.textItem.contents = "© 2024";
    textLayer.textItem.size = 36;

    doc.flatten();
    doc.save();
    doc.close();
}
```

Claude'a "Bu JSX kodunu çalıştır" diyerek yukarıdaki scriptleri çalıştırabilirsiniz!

## 🚀 İleri Düzey Kullanım

### Çoklu Photoshop Versiyonları

Farklı Photoshop versiyonları için ayrı serverlar:

```json
{
  "mcpServers": {
    "photoshop-2024": {
      "command": "python3",
      "args": ["/path/to/photoshop_mcp_server.py"],
      "env": {
        "PHOTOSHOP_VERSION": "2024"
      }
    },
    "photoshop-2023": {
      "command": "python3",
      "args": ["/path/to/photoshop_mcp_server.py"],
      "env": {
        "PHOTOSHOP_VERSION": "2023"
      }
    }
  }
}
```

### Actions'ları Çalıştırma

```javascript
// Claude'a şunu söyleyin:
// "Şu JSX kodunu çalıştır: "

var actionSet = "My Actions";
var actionName = "Sepia Tone Effect";
app.doAction(actionName, actionSet);
```

### Photoshop + Diğer Adobe Uygulamaları

Illustrator, After Effects, InDesign için benzer serverlar oluşturabilirsiniz!

## 📚 Kaynaklar

- [Adobe Photoshop Scripting Guide](https://www.adobe.com/devnet/photoshop/scripting.html)
- [ExtendScript Toolkit](https://helpx.adobe.com/photoshop/kb/extended-scripting-toolkit.html)
- [MCP Protocol Docs](https://modelcontextprotocol.io/)
- [Godot MCP Server](./README.md) - Bu projedeki örnek

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır!

Eklemek istediğiniz özellikler:
- [ ] Layer effects (drop shadow, glow, vb.)
- [ ] Selection tools (magic wand, lasso)
- [ ] History management (undo/redo)
- [ ] Color adjustments (curves, levels)
- [ ] Channels ve masks
- [ ] 3D features
- [ ] Animation timeline

## 📄 Lisans

MIT

## 💡 İpuçları

1. **Performans:** Batch işlemler için Photoshop'ta "Actions" kullanmak daha hızlıdır
2. **Güvenlik:** JSX scriptleri güçlüdür, trusted kaynaklardan çalıştırın
3. **Backup:** Önemli dosyalarda işlem yapmadan önce backup alın
4. **Memory:** Büyük dosyalarla çalışırken Photoshop'a yeterli RAM ayırın

## 🎉 Başarılar!

Artık Claude Desktop ile Photoshop'u kontrol edebilirsiniz!

Sorularınız için:
- README.md dosyasını okuyun
- Developer Console loglarını kontrol edin
- Issue açın
- Discord/forum'da yardım isteyin

**Harika görüntüler oluşturun! 🎨✨**
