# 🎨 Photoshop MCP Server - İş Akışı Rehberi (Türkçe)

Bu rehber, Photoshop MCP Server'ı sıfırdan kurup kullanmaya başlamanız için adım adım yol gösterir.

---

## 📚 İçindekiler

1. [Hızlı Başlangıç](#-hızlı-başlangıç)
2. [Manuel Kurulum](#️-manuel-kurulum-adım-adım)
3. [İlk Test](#-ilk-test)
4. [Pratik Örnekler](#-pratik-iş-akışı-örnekleri)
5. [Sorun Giderme](#-sorun-giderme)

---

## 🚀 Hızlı Başlangıç

### Otomatik Kurulum (Önerilen)

```bash
# 1. Depo klasörüne git
cd ~/depo

# 2. Kurulum scriptini çalıştır
./install_photoshop_mcp.sh

# 3. Talimatları takip et
```

Script şunları yapar:
- ✅ Python kontrolü
- ✅ MCP SDK kurulumu
- ✅ Platform tespiti (Mac/Windows)
- ✅ Gerekli kütüphaneleri yükler
- ✅ Claude Desktop config'i hazırlar

---

## 🛠️ Manuel Kurulum (Adım Adım)

### Adım 1: Python Bağımlılıklarını Yükle

```bash
# MCP SDK'yı yükle
pip install mcp

# Windows kullanıcıları için ek:
pip install pywin32  # Sadece Windows'ta gerekli
```

**Kontrol:**
```bash
python3 -c "import mcp; print('MCP SDK hazır!')"
```

Çıktı: `MCP SDK hazır!` görmelisiniz.

---

### Adım 2: Server'ı Test Et

Photoshop'u açın, sonra:

```bash
cd ~/depo
python3 photoshop_mcp_server.py
```

**Beklenen çıktı:**
```
[PHOTOSHOP-MCP] INFO: Photoshop MCP Server başlatılıyor...
[PHOTOSHOP-MCP] INFO: Platform: Darwin
[PHOTOSHOP-MCP] INFO: MCP server hazır ve bağlantı bekliyor...
```

✅ Bu logları görüyorsanız, server çalışıyor!

`Ctrl+C` ile kapatın.

---

### Adım 3: Claude Desktop Yapılandırması

#### 🍎 macOS

```bash
# 1. Config dizinini oluştur (yoksa)
mkdir -p ~/Library/Application\ Support/Claude

# 2. Config dosyasını düzenle
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Şu içeriği ekleyin:**

```json
{
  "mcpServers": {
    "photoshop": {
      "command": "python3",
      "args": [
        "/Users/KULLANICI_ADIN/depo/photoshop_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**ÖNEMLİ:** `/Users/KULLANICI_ADIN/depo/` kısmını kendi yolunuzla değiştirin!

```bash
# Tam yolu almak için:
cd ~/depo
pwd
# Çıktı: /Users/ahmet/depo
# O zaman: /Users/ahmet/depo/photoshop_mcp_server.py
```

**Mevcut server'larınız varsa (örn: Godot):**

```json
{
  "mcpServers": {
    "godot": {
      "command": "python3",
      "args": ["/Users/kullanici/depo/godot_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    },
    "photoshop": {
      "command": "python3",
      "args": ["/Users/kullanici/depo/photoshop_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    }
  }
}
```

---

#### 🪟 Windows

1. **Dosya Gezgini**'nde şu adrese gidin (adres çubuğuna yapıştırın):
   ```
   %APPDATA%\Claude
   ```

2. `claude_desktop_config.json` dosyasını **Not Defteri** ile açın (yoksa oluşturun)

3. Şu içeriği ekleyin:

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

**ÖNEMLİ:**
- Windows'ta backslash'leri **iki kez** yazın: `C:\\Users\\...`
- Kendi kullanıcı adınızı ve yolunuzu kullanın

**Yolunuzu bulmak için (PowerShell):**
```powershell
cd ~\depo
pwd
# Çıktı: C:\Users\Ahmet\depo
# Config'de: C:\\Users\\Ahmet\\depo\\photoshop_mcp_server.py
```

---

#### 🐧 Linux

```bash
# 1. Config dizinini oluştur
mkdir -p ~/.config/Claude

# 2. Config dosyasını düzenle
nano ~/.config/Claude/claude_desktop_config.json
```

**Not:** Photoshop Linux'ta doğal olarak çalışmaz. Wine veya VM kullanmanız gerekebilir.

---

### Adım 4: Claude Desktop'ı Yeniden Başlat

**Çok Önemli:** Sadece pencereyi kapatmak yetmez!

#### macOS:
1. Claude Desktop'ta `Cmd + Q` (tamamen kapat)
2. Sistem tepsisinde/dock'ta olmadığından emin olun
3. Yeniden açın

#### Windows:
1. Claude Desktop'ı kapatın
2. Sistem tepsisine (saat yanı) sağ tıklayın
3. "Quit" / "Çıkış" yapın (tamamen kapanmalı)
4. Yeniden açın

---

## ✅ İlk Test

### 1. MCP Server'larını Kontrol Et

Claude Desktop'ta yeni bir sohbet açın ve yazın:

```
MCP araçlarımı listele
```

**veya**

```
Hangi MCP server'ları bağlı?
```

**Beklenen çıktı:**

Claude şöyle bir şey gösterecek:
```
Şu MCP server'ları bağlı:

📦 photoshop
  - photoshop_check_connection
  - photoshop_get_info
  - photoshop_open_file
  - photoshop_save_file
  - photoshop_create_layer
  - photoshop_list_layers
  - photoshop_apply_filter
  - photoshop_add_text
  - photoshop_resize_image
  - photoshop_crop
  - photoshop_execute_jsx
  - photoshop_batch_resize
```

✅ Bu araçları görüyorsanız, kurulum başarılı!

---

### 2. Photoshop Bağlantısını Test Et

**ÖNCE Photoshop'u açın!**

Sonra Claude'a yazın:

```
Photoshop bağlantımı kontrol et
```

**Başarılı çıktı:**
```
✅ Photoshop bağlantısı başarılı!

Adobe Photoshop 2024 25.0

Platform: Darwin
```

**Eğer hata alırsanız:**
```
❌ Photoshop'a bağlanılamadı:
execution error: Adobe Photoshop got an error: Connection is invalid. (-609)

Lütfen Photoshop'un açık olduğundan emin olun.
```

**Çözüm:** Photoshop'u açın ve tekrar deneyin.

---

### 3. İlk İşleminizi Yapın

#### Test 1: Doküman Bilgisi

Photoshop'ta **herhangi bir dosya açın** (PSD, JPG, PNG, ne olursa).

Claude'a yazın:
```
Aktif Photoshop dokümanı hakkında bilgi ver
```

**Çıktı:**
```
📄 Aktif Doküman Bilgileri:

📝 İsim: photo.jpg
📏 Boyut: 1920 x 1080 piksel
🎨 Renk Modu: RGBColorMode
🔍 Çözünürlük: 72 DPI
📚 Katman Sayısı: 1
💾 Yol: /Users/ahmet/Desktop/photo.jpg
```

#### Test 2: Basit Düzenleme

```
Bu görüntüyü 800x600 piksel yap
```

Claude, Photoshop'ta dokümanı resize edecek!

#### Test 3: Filtre Uygulama

```
Aktif katmana 5 piksel Gaussian Blur uygula
```

Photoshop'ta bulanıklık efekti uygulanacak.

---

## 💼 Pratik İş Akışı Örnekleri

### Örnek 1: Logo Hazırlama (Batch)

**Senaryo:** Bir logo dosyanız var, farklı boyutlarda export etmek istiyorsunuz.

```
Claude'a sor:
"Desktop/logo.psd dosyasını aç, şu boyutlarda PNG olarak kaydet:
- 512x512 → logo_512.png
- 256x256 → logo_256.png
- 128x128 → logo_128.png
- 64x64 → logo_64.png
Hepsini Desktop/LogoExports/ klasörüne kaydet"
```

**Claude'un yapacakları:**
1. `photoshop_open_file` - logo.psd'yi açar
2. `photoshop_resize_image` - 512x512 yapar
3. `photoshop_save_file` - PNG olarak kaydeder
4. Adım 2-3'ü her boyut için tekrarlar

---

### Örnek 2: Fotoğraf Düzenleme Pipeline

**Senaryo:** Ham fotoğrafı düzenleyip watermark eklemek istiyorsunuz.

```
Claude'a sor:
"Desktop/portrait.jpg için şu işlemleri yap:
1. Dosyayı aç
2. 3 piksel Gaussian Blur uygula
3. Sağ alt köşeye '© 2024 Adım' watermark ekle (beyaz, 18pt)
4. JPEG olarak kaydet, kalite 11, Desktop/edited_portrait.jpg"
```

**İş akışı:**
```
Photoshop'ta açıldı → Blur uygulandı → Metin eklendi → Kaydedildi
```

Tüm işlem 2-3 saniyede tamamlanır!

---

### Örnek 3: Sosyal Medya İçeriği

**Senaryo:** Instagram post hazırlamak istiyorsunuz.

```
Claude'a sor:
"Desktop/photo.jpg dosyasını Instagram için hazırla:
1. 1080x1080 piksel yap (square format)
2. Üste 'YENİ ÜRÜN' yaz (72pt, beyaz, bold)
3. Alt kısma 'www.sitem.com' yaz (24pt, beyaz)
4. PNG olarak Desktop/instagram_post.png'ye kaydet"
```

---

### Örnek 4: Batch Resize (Toplu İşlem)

**Senaryo:** Bir klasör dolusu fotoğrafı küçültmek istiyorsunuz.

```
Claude'a sor:
"Desktop/VacationPhotos/ klasöründeki tüm JPG dosyalarını 1024x768 boyutuna getir ve Desktop/ResizedPhotos/ klasörüne kaydet"
```

**Claude otomatik olarak:**
- Tüm JPG dosyalarını bulur
- Her birini ayrı ayrı açar
- Resize eder
- Yeni klasöre kaydeder

---

### Örnek 5: Katman Yönetimi

**Senaryo:** Karmaşık PSD dosyasında katmanları organize etmek istiyorsunuz.

```
Claude'a sor:
"Tüm katmanları listele"
```

**Çıktı:**
```
📚 Katmanlar:

1. 👁️ Logo (Opacity: 100%)
2. 👁️ Text Layer (Opacity: 80%)
3. 🚫 Background (Opacity: 100%)
4. 👁️ Effects (Opacity: 50%)
```

Sonra:
```
"'Effects' katmanını %100 opacity yap"
"'Background' katmanını gizle"
"'New Layer' adında bir katman oluştur"
```

---

### Örnek 6: Gelişmiş - JSX Script

**Senaryo:** Tüm katmanların opacity'sini aynı anda değiştirmek istiyorsunuz.

```
Claude'a sor:
"Şu JSX kodunu çalıştır:

var doc = app.activeDocument;
for (var i = 0; i < doc.layers.length; i++) {
    doc.layers[i].opacity = 75;
}
'Tüm katmanlar %75 opacity yapıldı';"
```

Bu, saniyeler içinde tüm katmanları değiştirir!

---

## 🎯 İş Akışı Senaryoları

### Freelance Grafik Tasarımcı

**Sabah rutini:**
```
"Desktop/ClientWork/ klasöründeki PSD dosyalarını PNG'ye çevir ve Desktop/Deliverables/'a kaydet"
```

**Hızlı düzeltmeler:**
```
"Bu logoya 2 piksel sharpen uygula"
"Bu posteri 300 DPI yap (baskı için)"
```

---

### E-ticaret Ürün Fotoğrafçısı

**Ürün seti hazırlama:**
```
"Desktop/product_raw.jpg'yi şu formatlarda hazırla:
- Ana görsel: 2000x2000 (beyaz arka plan)
- Thumbnail: 500x500
- Zoom: 3000x3000
Hepsini Desktop/ProductImages/ klasörüne kaydet"
```

**Watermark ekleme:**
```
"Desktop/Products/ klasöründeki tüm resimlere sağ alt köşeye 'www.magaza.com' watermark ekle"
```

---

### YouTube Content Creator

**Thumbnail oluşturma:**
```
"Desktop/screenshot.jpg'yi YouTube thumbnail yap:
- 1280x720 piksel
- Sol üst köşeye 'BÖLÜM 5' yaz (96pt, bold, kırmızı)
- Slight sharpen uygula
- JPEG olarak kaydet, yüksek kalite"
```

---

### Kurumsal Pazarlama

**Marka materyalleri:**
```
"Desktop/campaign_photo.jpg'yi şu platformlar için hazırla:
- Instagram Post: 1080x1080
- Instagram Story: 1080x1920
- Facebook Cover: 820x312
- LinkedIn Banner: 1584x396
Hepsine sol alt köşeye logo ekle (Desktop/logo.png)
Desktop/SocialMedia/ klasörüne kaydet"
```

---

## 🐛 Sorun Giderme

### ❌ "photoshop araçlarını göremiyorum"

**Sebep:** Config dosyası yanlış veya Claude yeniden başlatılmamış.

**Çözüm:**
1. Config dosyasını kontrol edin:
   ```bash
   # Mac
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

   # Linux
   cat ~/.config/Claude/claude_desktop_config.json
   ```

2. JSON syntax'ı doğru mu kontrol edin (virgüller, parantezler)
3. PATH'ler doğru mu kontrol edin
4. Claude'u **tamamen** kapatıp yeniden açın

---

### ❌ "Photoshop'a bağlanılamadı"

**Sebep:** Photoshop açık değil veya scripting izinleri kapalı.

**Çözüm:**

1. **Photoshop'u açın**

2. **Mac kullanıcıları:**
   - System Preferences → Security & Privacy → Privacy → Automation
   - Terminal'e (veya Claude Desktop'a) Adobe Photoshop kontrolü için izin verin

3. **Windows kullanıcıları:**
   - pywin32 yüklü mü kontrol edin:
     ```bash
     pip show pywin32
     ```
   - Yoksa yükleyin:
     ```bash
     pip install pywin32
     python Scripts/pywin32_postinstall.py -install
     ```

4. Photoshop'u yeniden başlatın

---

### ❌ "JSON parse error"

**Sebep:** Server stdout'a log yazıyor.

**Kontrol:**
```bash
# Server'ı manuel çalıştırın
python3 ~/depo/photoshop_mcp_server.py
```

**Doğru çıktı:**
```
[PHOTOSHOP-MCP] INFO: Photoshop MCP Server başlatılıyor...
```

**Yanlış çıktı:**
```
Photoshop MCP Server başlatılıyor...  # ← [PHOTOSHOP-MCP] INFO yok!
```

Eğer yanlış formattaysa, `photoshop_mcp_server.py` dosyasında:
- `logging.basicConfig(stream=sys.stderr)` var mı?
- Hiçbir yerde `print()` kullanılmıyor mu?

---

### ❌ "Unexpected token" hatası

Developer Console'u açın (Cmd+Option+Shift+I / Ctrl+Shift+I) ve hataları inceleyin.

Genelde:
- PATH yanlış (dosya bulunamıyor)
- Python versiyonu uyumsuz
- MCP SDK yüklü değil

---

### ❌ Server başlamıyor

**Debug için:**

```bash
# 1. Python versiyonu
python3 --version  # 3.10+ olmalı

# 2. MCP SDK
python3 -c "import mcp; print('OK')"

# 3. Server'ı verbose modda çalıştır
python3 ~/depo/photoshop_mcp_server.py 2>&1 | head -n 20
```

Hataları buradan görebilirsiniz.

---

## 📊 Developer Console (İleri Düzey Debug)

Claude Desktop Developer Console'u açın:

**Mac:** `Cmd + Option + Shift + I`
**Windows/Linux:** `Ctrl + Shift + I`

**Console** tab'ında şunları göreceksiniz:

```
[PHOTOSHOP-MCP] INFO: Photoshop MCP Server başlatılıyor...
[PHOTOSHOP-MCP] INFO: Platform: Darwin
[PHOTOSHOP-MCP] INFO: MCP server hazır ve bağlantı bekliyor...
[PHOTOSHOP-MCP] INFO: Tool çağrıldı: photoshop_check_connection with args: {}
[PHOTOSHOP-MCP] INFO: JSX script çalıştırılıyor (Platform: Darwin)
```

Bu loglar, sorun giderme için çok değerlidir!

---

## 🎓 Pro İpuçları

### 1. Workflow Otomasyonu

Sık tekrar ettiğiniz işlemleri not edin, sonra Claude'a tek komutla yaptırın:

```
"Desktop/morning_routine.txt dosyasındaki talimatları uygula"
```

**morning_routine.txt:**
```
1. Desktop/RawPhotos/'daki tüm JPG'leri 1920x1080 yap
2. Her birine '© 2024' watermark ekle
3. Desktop/ProcessedPhotos/'a kaydet
```

### 2. Batch Processing'de Dikkat

Büyük klasörlerle çalışırken:
- İlk 2-3 dosyayla test edin
- Sonra tüm klasörü işletin
- Orijinal dosyaları yedekleyin

### 3. JSX Scriptleri Kaydedin

Sık kullandığınız JSX scriptlerini ayrı dosyalara kaydedin:

```bash
# blur_all_layers.jsx
var doc = app.activeDocument;
for (var i = 0; i < doc.layers.length; i++) {
    doc.layers[i].applyGaussianBlur(5);
}
```

Claude'a:
```
"Desktop/scripts/blur_all_layers.jsx dosyasını çalıştır"
```

### 4. Hız Artırma

- Photoshop'ta gereksiz history'yi temizleyin (Edit → Purge → All)
- Büyük dosyalarla çalışırken RAM'i artırın (Preferences → Performance)
- Batch işlemlerde flatten image yapın (hız artar)

---

## 🎉 Başarılar!

Artık Photoshop'u Claude Desktop ile kontrol edebilirsiniz!

**Hatırlatma:**
- Photoshop açık olmalı
- Claude Desktop yeniden başlatılmış olmalı
- Config doğru ayarlanmış olmalı

**Daha fazla örnek için:**
```bash
cat ~/depo/PHOTOSHOP_EXAMPLES.md
```

**Yardım için:**
- PHOTOSHOP_README.md
- Developer Console logları
- GitHub issues

**Keyifli çalışmalar! 🎨✨**
