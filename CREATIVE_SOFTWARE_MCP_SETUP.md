# Yaratıcı Yazılımlar MCP Entegrasyonu

Bu proje, lisanslı yaratıcı yazılımlarınızı Claude Desktop ile entegre eder. Claude Desktop üzerinden Blender, Maya, Photoshop ve diğer Adobe uygulamalarını kontrol edebilirsiniz.

## 📦 Desteklenen Yazılımlar

✅ **Tamamlanan MCP Sunucuları:**
- 🎨 **Blender** - 3D modelleme, animasyon, rendering
- 🎬 **Autodesk Maya** - Profesyonel 3D animasyon ve VFX
- 🖼️ **Adobe Photoshop** - Görsel düzenleme ve fotoğraf manipülasyonu

🔄 **Planlanan (Benzer Yapıyla Eklenebilir):**
- Adobe Illustrator - Vektör grafik
- Adobe After Effects - Video compositing ve efektler
- Adobe InDesign - Sayfa düzeni
- Adobe Premiere Pro - Video düzenleme

---

## 🚀 Kurulum

### Gereksinimler

```bash
# Python 3.10+
python3 --version

# MCP SDK
pip install mcp

# Her yazılım için gerekli Python modülleri
pip install -e .
```

### 1. Blender MCP Sunucusu

#### Kurulum
Blender'ı sisteminize kurun:
- **Linux**: `sudo apt install blender` veya https://www.blender.org/download/
- **Windows**: https://www.blender.org/download/
- **macOS**: `brew install --cask blender`

#### Özellikler
- ✅ Blender dosyalarını aç/kaydet (.blend)
- ✅ Sahne bilgilerini al (objeler, kameralar, ışıklar)
- ✅ 3D objeler oluştur (küp, küre, silindir, vb.)
- ✅ Objeler üzerinde transform işlemleri (move, rotate, scale)
- ✅ Material ve shader oluştur
- ✅ Render işlemleri (PNG, JPEG)
- ✅ Python kodu çalıştır (bpy API)
- ✅ Dışa aktarma (FBX, OBJ, GLTF, STL, PLY)

#### Kullanım Örnekleri

```
# Claude Desktop'ta şunları deneyin:

"Blender'da yeni bir küp oluştur"
"Sahnemdeki tüm objeleri listele"
"Kırmızı bir material oluştur ve küpe uygula"
"Sahneyi 1920x1080 çözünürlükte render et, /tmp/output.png olarak kaydet"
"Sahneyi FBX formatında dışa aktar"
```

---

### 2. Maya MCP Sunucusu

#### Kurulum
Autodesk Maya kurulu olmalı. Maya'nın Python API'sine erişmek için `mayapy` kullanılır.

**Maya Python Yolu Ayarlama:**
```bash
# Linux/Mac
export PATH=$PATH:/usr/autodesk/maya2024/bin

# Windows
# Maya kurulum klasörünü PATH'e ekleyin (örn: C:\Program Files\Autodesk\Maya2024\bin)
```

#### Özellikler
- ✅ Maya dosyalarını aç/kaydet (.ma, .mb)
- ✅ Yeni sahne oluştur
- ✅ Sahne bilgilerini al (objeler, kameralar, ışıklar)
- ✅ Polygon objeler oluştur (küp, küre, silindir, koni, düzlem, torus)
- ✅ Işık oluştur (directional, point, spot, area)
- ✅ Kamera oluştur
- ✅ Objeler üzerinde transform işlemleri
- ✅ Render işlemleri
- ✅ MEL komutları çalıştır
- ✅ Python kodu çalıştır (maya.cmds API)
- ✅ Dışa aktarma (FBX, OBJ, Alembic)

#### Kullanım Örnekleri

```
# Claude Desktop'ta:

"Maya'da yeni bir sahne oluştur"
"Bir küre ve bir ışık ekle"
"Küreyi (5, 0, 0) konumuna taşı"
"Sahneyi render et ve /tmp/maya_render.jpg olarak kaydet"
"Sahneyi FBX formatında dışa aktar"
```

---

### 3. Photoshop MCP Sunucusu

#### Kurulum
Adobe Photoshop kurulu olmalı. Photoshop ile iletişim için iki bileşen gerekir:

1. **Python MCP Sunucusu** - Claude Desktop ile haberleşir
2. **JSX Client Script** - Photoshop içinde çalışır

#### JSX Script'i Yükleme

**Yöntem 1: Manuel Çalıştırma**
1. Photoshop'u açın
2. `File > Scripts > Browse...`
3. `photoshop_client.jsx` dosyasını seçin

**Yöntem 2: Scripts Klasörüne Kopyalama** (Önerilen)
```bash
# Windows
cp photoshop_client.jsx "C:\Program Files\Adobe\Adobe Photoshop 2024\Presets\Scripts\"

# Mac
cp photoshop_client.jsx "/Applications/Adobe Photoshop 2024/Presets/Scripts/"

# Linux (Wine ile)
cp photoshop_client.jsx "~/.wine/drive_c/Program Files/Adobe/Adobe Photoshop/Presets/Scripts/"
```

Sonra Photoshop'ta: `File > Scripts > photoshop_client`

#### Özellikler
- ✅ Photoshop dosyalarını aç (.psd, .jpg, .png, vb.)
- ✅ Dokümanları kaydet
- ✅ Doküman bilgilerini al
- ✅ Katman (layer) oluştur/sil
- ✅ Tüm katmanları listele
- ✅ Görsel boyutlandır
- ✅ Filtre uygula (blur, sharpen, gaussian blur)
- ✅ ExtendScript (JSX) kodu çalıştır
- ✅ Dışa aktarma (PNG, JPEG, TIFF, PDF)

#### Kullanım Örnekleri

```
# Claude Desktop'ta:

"Photoshop'ta /home/user/photo.jpg dosyasını aç"
"Doküman bilgilerini göster"
"Yeni bir katman oluştur, 'Düzenleme' adını ver"
"Görseli 1920x1080 boyutuna getir"
"Gaussian blur filtresi uygula"
"PNG formatında /tmp/output.png olarak kaydet"
```

---

## ⚙️ Claude Desktop Yapılandırması

Claude Desktop yapılandırma dosyasını düzenleyin:

**Linux/Mac:**
```bash
~/.config/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

### Yapılandırma Dosyası

Aşağıdaki config'i kendi sistem yollarınıza göre düzenleyin:

```json
{
  "mcpServers": {
    "blender": {
      "command": "blender",
      "args": [
        "--background",
        "--python",
        "/TAM/YOL/blender_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    },
    "maya": {
      "command": "mayapy",
      "args": [
        "/TAM/YOL/maya_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    },
    "photoshop": {
      "command": "python3",
      "args": [
        "/TAM/YOL/photoshop_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Önemli Notlar:**
- `/TAM/YOL/` kısımlarını gerçek dosya yollarınızla değiştirin
- Windows'ta ters slash kullanın: `"C:\\Users\\KullaniciAdi\\depo\\blender_mcp_server.py"`
- Linux'ta: `"/home/user/depo/blender_mcp_server.py"`
- macOS'ta: `"/Users/username/depo/blender_mcp_server.py"`

---

## 🎯 Kullanım

### Claude Desktop'ı Başlatma

1. Yapılandırma dosyasını kaydedin
2. Claude Desktop'ı **tamamen kapatın**
3. Claude Desktop'ı yeniden açın

MCP sunucuları otomatik olarak başlayacak.

### Bağlantıları Kontrol Etme

Claude Desktop'ta şunları yazın:

```
"Blender bağlantısını kontrol et"
"Maya sahne bilgilerini al"
"Photoshop bağlantısını kontrol et"
```

### Developer Console

Hata ayıklama için Developer Console'u açın:
- **Mac**: `Cmd + Option + Shift + i`
- **Windows/Linux**: `Ctrl + Shift + i`

Console'da MCP sunucu loglarını görebilirsiniz:
```
[BLENDER-MCP] INFO: Blender MCP Server başlatılıyor...
[MAYA-MCP] INFO: Maya MCP Server başlatılıyor...
[PHOTOSHOP-MCP] INFO: Photoshop MCP Server başlatılıyor...
```

---

## 🛠️ Sorun Giderme

### "mcp paketi bulunamadı" Hatası
```bash
pip install mcp
```

### "Blender Python API bulunamadı" Hatası
Blender MCP sunucusu, Blender'ın kendi Python yorumlayıcısı ile çalışmalıdır:
```bash
blender --background --python blender_mcp_server.py
```

Claude Desktop config'de komut zaten doğru ayarlıdır.

### "mayapy bulunamadı" Hatası
Maya'nın kurulum dizinini PATH'e ekleyin:
```bash
# Linux/Mac - .bashrc veya .zshrc'ye ekleyin
export PATH=$PATH:/usr/autodesk/maya2024/bin

# Windows - System Environment Variables'a ekleyin
```

### Photoshop Bağlantı Sorunu
1. Photoshop'un açık olduğundan emin olun
2. `photoshop_client.jsx` script'ini Photoshop içinde çalıştırın
3. Python MCP sunucusunun çalıştığını kontrol edin

### JSON Parse Hataları
Tüm log mesajları `stderr`'e yönlendirilmiş durumda. Eğer hala JSON parse hatası alıyorsanız:
1. Sunucu script'lerinde `print()` kullanmayın
2. Sadece `logger.info()`, `logger.error()` kullanın
3. `logging.basicConfig(stream=sys.stderr)` satırının mevcut olduğundan emin olun

---

## 🔧 Genişletme

### Yeni Özellik Ekleme

Her MCP sunucusu benzer yapıdadır:

1. **Tool tanımlama** - `list_tools()` içinde
2. **Handler ekleme** - `call_tool()` içinde
3. **Fonksiyon implement etme**

Örnek (Blender):
```python
Tool(
    name="blender_new_feature",
    description="Yeni bir özellik",
    inputSchema={
        "type": "object",
        "properties": {
            "param": {"type": "string"}
        }
    }
)
```

### Diğer Adobe Yazılımları İçin MCP Sunucuları

Photoshop MCP sunucusu temel alınarak diğer Adobe uygulamaları için benzer sunucular oluşturabilirsiniz:

- **Illustrator**: Vektör operasyonları, path editing
- **After Effects**: Composition oluşturma, animasyon, rendering
- **InDesign**: Sayfa düzeni, text formatting
- **Premiere Pro**: Video editing, clip management

Her biri için benzer JSX client script'leri oluşturulmalıdır.

---

## 📚 API Referansları

### Blender Python API
https://docs.blender.org/api/current/

### Maya Python API
https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=__CommandsPython_index_html

### Adobe ExtendScript
https://extendscript.docsforadobe.dev/

---

## 📝 Lisans

MIT License

---

## 🤝 Katkıda Bulunma

Pull request'ler ve issue'lar memnuniyetle karşılanır!

---

## 💡 İpuçları

1. **Batch İşlemler**: Claude'a birden fazla işlemi sırayla yapmasını söyleyebilirsiniz
   ```
   "Blender'da bir küre oluştur, kırmızı material ekle, render et"
   ```

2. **Karmaşık İşlemler**: Python/MEL/JSX kodu çalıştırarak karmaşık işlemler yapabilirsiniz
   ```
   "Blender'da şu Python kodunu çalıştır: [bpy kodu]"
   ```

3. **Workflow Otomasyonu**: Tekrarlayan görevleri otomatikleştirin
   ```
   "Maya'da 10 küre oluştur, her birini farklı konuma yerleştir"
   ```

4. **Dosya İşlemleri**: Tam dosya yollarını kullanın
   ```
   "/home/user/projects/model.blend" (Linux/Mac)
   "C:\\Users\\User\\projects\\model.blend" (Windows)
   ```

---

## 🎓 Öğrenme Kaynakları

### Blender
- [Blender Manual](https://docs.blender.org/manual/en/latest/)
- [Blender Python API Quickstart](https://docs.blender.org/api/current/info_quickstart.html)

### Maya
- [Maya Help](https://help.autodesk.com/view/MAYAUL/2024/ENU/)
- [Maya Python for Beginners](https://knowledge.autodesk.com/support/maya/learn)

### Photoshop Scripting
- [Photoshop Scripting Guide](https://helpx.adobe.com/photoshop/using/scripting.html)
- [ExtendScript Toolkit](https://extendscript.docsforadobe.dev/)

---

## 📞 Destek

Sorun yaşıyorsanız:
1. Developer Console'daki logları kontrol edin
2. MCP sunucu script'lerini manuel olarak çalıştırıp test edin
3. GitHub'da issue açın

---

**Başarılı entegrasyonlar! 🎉**
