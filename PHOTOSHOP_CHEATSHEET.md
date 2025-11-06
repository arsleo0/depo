# 🎨 Photoshop MCP - Hızlı Başvuru Kartı

## ⚡ Hızlı Kurulum

```bash
cd ~/depo
./install_photoshop_mcp.sh
```

---

## 🔧 Manuel Kurulum

```bash
# 1. Kurulum
pip install mcp
pip install pywin32  # Sadece Windows

# 2. Config (Mac)
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 2. Config (Linux)
nano ~/.config/Claude/claude_desktop_config.json

# 3. Test
python3 photoshop_mcp_server.py
```

**Config içeriği:**
```json
{
  "mcpServers": {
    "photoshop": {
      "command": "python3",
      "args": ["/TAM/YOL/photoshop_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    }
  }
}
```

---

## 🎯 Temel Komutlar

### Bağlantı Test

```
Photoshop bağlantımı kontrol et
```

### Doküman Bilgisi

```
Aktif doküman hakkında bilgi ver
```

### Dosya İşlemleri

```
/Users/kullanici/Desktop/photo.jpg dosyasını aç
Bu dosyayı PNG olarak Desktop/output.png'ye kaydet
```

---

## 🖼️ Görüntü İşlemleri

### Yeniden Boyutlandırma

```
Bu görüntüyü 800x600 piksel yap
Görüntüyü yarı boyutuna küçült
Instagram için 1080x1080 yap
```

### Kırpma

```
Görüntüyü 100,100 noktasından başlayarak 500x500 piksel kırp
```

### Filtreler

```
5 piksel Gaussian Blur uygula
Görüntüyü keskinleştir
Renkleri ters çevir
```

---

## 📚 Katman İşlemleri

```
Tüm katmanları listele
'Logo' adında katman oluştur
```

---

## ✍️ Metin Ekleme

```
Görüntüye 'HELLO WORLD' yaz
Sağ alt köşeye '© 2024' watermark ekle, beyaz, 18pt
```

---

## 🔄 Batch İşlemler

```
Desktop/Photos/ klasöründeki tüm resimleri 1024x768 yap ve Desktop/Output/'a kaydet
```

---

## 🚀 Gelişmiş - JSX

```
Şu JSX'i çalıştır:

var doc = app.activeDocument;
doc.flatten();
"Katmanlar birleştirildi";
```

---

## 💼 Pratik Senaryolar

### Logo Export (Çoklu Boyut)

```
Desktop/logo.psd'yi şu boyutlarda PNG olarak kaydet:
- 512x512 → logo_512.png
- 256x256 → logo_256.png
- 128x128 → logo_128.png
```

### Fotoğraf Pipeline

```
Desktop/portrait.jpg için:
1. 3px blur uygula
2. '© 2024' watermark ekle
3. JPEG olarak kaydet (kalite 11)
```

### Sosyal Medya Seti

```
Desktop/poster.jpg'yi şu formatlarda hazırla:
- Instagram: 1080x1080
- Story: 1080x1920
- Facebook: 820x312
```

---

## 🐛 Sorun Giderme

### Photoshop'a bağlanılamıyor

```bash
# 1. Photoshop açık mı?
# 2. Mac: System Preferences → Automation izinleri
# 3. Windows: pywin32 yüklü mü?
pip show pywin32
```

### MCP araçları görünmüyor

```bash
# 1. Config dosyası doğru mu?
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 2. Claude'u yeniden başlat (Cmd+Q / tamamen kapat)
```

### JSON parse error

```bash
# Server'ı test et
python3 photoshop_mcp_server.py

# Şu satır görünmeli:
# [PHOTOSHOP-MCP] INFO: Photoshop MCP Server başlatılıyor...
```

---

## 📊 Developer Console

**Açmak için:**
- Mac: `Cmd + Option + Shift + I`
- Windows: `Ctrl + Shift + I`

**Console tab'ında:**
```
[PHOTOSHOP-MCP] INFO: Tool çağrıldı: photoshop_check_connection
```

---

## 🎓 Pro İpuçları

### Hızlı Test

```
MCP araçlarımı listele
Photoshop bağlantımı kontrol et
```

### Workflow Şablonları

Sık kullandığınız işlemleri not edin:

```
"Sabah rutinini çalıştır: RawPhotos klasöründeki resimleri işle"
```

### JSX Scriptleri

Karmaşık işlemler için JSX kullanın:

```javascript
// Tüm katmanları %50 opacity yap
var doc = app.activeDocument;
for (var i = 0; i < doc.layers.length; i++) {
    doc.layers[i].opacity = 50;
}
```

---

## 📚 Daha Fazla Bilgi

- **Detaylı Kurulum:** `PHOTOSHOP_WORKFLOW_TR.md`
- **30+ Örnek:** `PHOTOSHOP_EXAMPLES.md`
- **Full Docs:** `PHOTOSHOP_README.md`

---

## 🎉 Başarılar!

**Unutmayın:**
1. ✅ Photoshop açık olmalı
2. ✅ Claude Desktop yeniden başlatılmış olmalı
3. ✅ Config doğru ayarlanmış olmalı

**Harika işler çıkarın! 🎨✨**
