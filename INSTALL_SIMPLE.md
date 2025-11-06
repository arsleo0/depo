# 🚀 Basit Kurulum Rehberi - Tüm MCP Sunucuları

Script çalışmadıysa, bu adımları **elle** takip edin. Garantili çalışır! ✅

---

## 📋 İHTİYAÇLAR

- Python 3.10+
- Claude Desktop
- Godot / Photoshop / After Effects (hangileri kullanacaksanız)

---

## 🔥 HIZLI KURULUM (Kopyala-Yapıştır)

### 1️⃣ MCP SDK'yı Yükle

Terminal/Command Prompt'u açın:

```bash
pip install mcp
```

**Eğer hata verirse şunu deneyin:**
```bash
pip3 install mcp
```

**Veya:**
```bash
python3 -m pip install mcp
```

**Windows kullanıcıları için ek:**
```bash
pip install pywin32
```

---

### 2️⃣ Proje Dizinine Git

```bash
cd ~/depo
```

**Windows:**
```bash
cd %USERPROFILE%\depo
```

---

### 3️⃣ Server'ları Test Et

**Test 1 - Godot:**
```bash
python3 godot_mcp_server.py
```

Şunu görmelisiniz:
```
[GODOT-MCP] INFO: Godot MCP Server başlatılıyor...
```

`Ctrl+C` ile durdurun.

**Test 2 - Photoshop:**
```bash
python3 photoshop_mcp_server.py
```

Şunu görmelisiniz:
```
[PHOTOSHOP-MCP] INFO: Photoshop MCP Server başlatılıyor...
```

`Ctrl+C` ile durdurun.

**Test 3 - After Effects:**
```bash
python3 aftereffects_mcp_server.py
```

Şunu görmelisiniz:
```
[AE-MCP] INFO: After Effects MCP Server başlatılıyor...
```

`Ctrl+C` ile durdurun.

✅ **Hepsi çalışıyorsa devam edin!**

---

### 4️⃣ Claude Desktop Config'i Oluştur

#### **macOS Kullanıcıları:**

```bash
# Config dizinini oluştur
mkdir -p ~/Library/Application\ Support/Claude

# Config dosyasını oluştur
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

#### **Linux Kullanıcıları:**

```bash
# Config dizinini oluştur
mkdir -p ~/.config/Claude

# Config dosyasını oluştur
nano ~/.config/Claude/claude_desktop_config.json
```

#### **Windows Kullanıcıları:**

1. Dosya Gezgini'ni açın
2. Adres çubuğuna yazın: `%APPDATA%\Claude`
3. `claude_desktop_config.json` dosyası oluşturun (Notepad ile)

---

### 5️⃣ Config İçeriği

**ÖNCE TAM YOLUNUZU ÖĞRENİN:**

```bash
cd ~/depo
pwd
```

Bu size tam yolu verecek, örneğin: `/home/kullanici/depo`

**Sonra bu içeriği config dosyasına yapıştırın (YOLU DEĞİŞTİRİN!):**

```json
{
  "mcpServers": {
    "godot": {
      "command": "python3",
      "args": [
        "/TAM/YOL/BURAYA/depo/godot_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    },
    "photoshop": {
      "command": "python3",
      "args": [
        "/TAM/YOL/BURAYA/depo/photoshop_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    },
    "aftereffects": {
      "command": "python3",
      "args": [
        "/TAM/YOL/BURAYA/depo/aftereffects_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**ÖNEMLİ:** `/TAM/YOL/BURAYA/` yerine `pwd` komutunun verdiği yolu yazın!

**Örnek (macOS/Linux):**
```json
"/home/ahmet/depo/godot_mcp_server.py"
```

**Örnek (Windows):**
```json
"C:\\Users\\Ahmet\\depo\\godot_mcp_server.py"
```

**Not:** Windows'ta `\` karakteri iki kez yazılır: `\\`

Kaydedin ve kapatın (nano'da: `Ctrl+O`, `Enter`, `Ctrl+X`)

---

### 6️⃣ Claude Desktop'ı Yeniden Başlat

**Mac:**
1. `Cmd + Q` (tamamen kapat)
2. Dock'tan çöp kutusunu kontrol edin, arka planda kalmasın
3. Yeniden açın

**Windows:**
1. Sistem tepsisinde (sağ altta, saat yanında) Claude Desktop simgesini bulun
2. Sağ tıklayın
3. "Quit" / "Çıkış"
4. Yeniden açın

**Linux:**
1. Uygulamayı tamamen kapatın
2. `ps aux | grep claude` ile kontrol edin
3. Yeniden açın

---

### 7️⃣ TEST!

Claude Desktop'ta yeni sohbet açın:

```
MCP araçlarımı listele
```

**Göreceğiniz:**
```
📦 godot (7 araç)
  - set_godot_project
  - list_godot_scenes
  - read_godot_script
  - ...

📦 photoshop (12 araç)
  - photoshop_check_connection
  - photoshop_open_file
  - photoshop_save_file
  - ...

📦 aftereffects (15 araç)
  - ae_check_connection
  - ae_create_composition
  - ae_render_composition
  - ...
```

✅ **34 araç görüyorsanız BAŞARILI!** 🎉

---

## 🧪 Bağlantı Testleri

### Photoshop Testi

1. **Photoshop'u açın**
2. Claude'da yazın:

```
Photoshop bağlantımı kontrol et
```

**Başarılı çıktı:**
```
✅ Photoshop bağlantısı başarılı!
Adobe Photoshop 2024 25.0
```

---

### After Effects Testi

1. **After Effects'i açın**
2. Claude'da yazın:

```
After Effects bağlantımı kontrol et
```

**Başarılı çıktı:**
```
✅ After Effects bağlantısı başarılı!
Adobe After Effects 2024 24.0
```

---

### Godot Testi

1. **Godot'u açın**
2. **Bir proje açın**
3. Claude'da yazın:

```
Godot projem /tam/yol/proje/dizinine bağlan
```

**Örnek:**
```
Godot projem /home/ahmet/MyGame dizininde, bağlan
```

---

## 🐛 Sorun Giderme

### ❌ "MCP araçlarını göremiyorum"

**Çözüm 1:** Config dosyasını kontrol edin

```bash
# macOS
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
cat ~/.config/Claude/claude_desktop_config.json
```

JSON syntax'ı doğru mu?
- Virgüller doğru mu?
- Tırnak işaretleri doğru mu?
- Parantezler kapanmış mı?

**Çözüm 2:** Yollar doğru mu?

Config'teki yolları kontrol edin:
```bash
ls -la /tam/yolunuz/depo/godot_mcp_server.py
ls -la /tam/yolunuz/depo/photoshop_mcp_server.py
ls -la /tam/yolunuz/depo/aftereffects_mcp_server.py
```

Hepsi bulunmalı!

**Çözüm 3:** Claude'u gerçekten yeniden başlattınız mı?

Arka planda çalışıyor olabilir:
```bash
# macOS/Linux
ps aux | grep -i claude
```

Görüyorsanız, öldürün ve yeniden başlatın.

---

### ❌ "pip command not found"

**Python'un doğru yüklenmiş olduğundan emin olun:**

```bash
python3 --version
```

**Eğer çalışıyorsa:**
```bash
python3 -m pip install mcp
```

---

### ❌ "Photoshop/After Effects'e bağlanılamadı"

**macOS:**
1. System Preferences → Security & Privacy → Privacy → Automation
2. Terminal veya Claude Desktop'a Adobe Photoshop/After Effects kontrolü için izin verin

**Windows:**
1. pywin32 yüklü mü kontrol edin:
   ```bash
   pip show pywin32
   ```
2. Yoksa yükleyin:
   ```bash
   pip install pywin32
   ```

---

### ❌ Config dosyası nerede?

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

Gerçek yol (Windows):
```
C:\Users\KullaniciAdin\AppData\Roaming\Claude\claude_desktop_config.json
```

---

### 🔍 Developer Console

Detaylı hata mesajları için Developer Console'u açın:

**Mac:** `Cmd + Option + Shift + I`
**Windows/Linux:** `Ctrl + Shift + I`

**Console** tab'ında hataları görebilirsiniz.

---

## ✅ BAŞARILI KURULUM KONTROLLİSTESİ

- [ ] Python 3.10+ yüklü
- [ ] MCP SDK yüklü (`pip list | grep mcp`)
- [ ] pywin32 yüklü (sadece Windows)
- [ ] 3 server dosyası mevcut (godot, photoshop, aftereffects)
- [ ] Config dosyası oluşturuldu
- [ ] Config'teki yollar doğru
- [ ] JSON syntax'ı geçerli
- [ ] Claude Desktop tamamen yeniden başlatıldı
- [ ] Claude'da 34 araç görünüyor
- [ ] İlgili uygulamalar açık
- [ ] Bağlantı testleri başarılı

---

## 🎉 Başarılı Oldunuz!

Artık Claude Desktop ile:
- 🎮 Godot'u kontrol edebilirsiniz
- 🎨 Photoshop'u kontrol edebilirsiniz
- 🎬 After Effects'i kontrol edebilirsiniz

**İlk komutunuzu deneyin:**

```
Desktop/photo.jpg dosyasını Photoshop'ta aç ve 800x600 piksel yap
```

**Veya:**

```
"Test" adında yeni After Effects comp oluştur (1920x1080, 5s, 30fps) ve "HELLO WORLD" yazısı ekle
```

---

## 📚 Daha Fazla Bilgi

- **Hızlı Başvuru:** [QUICKSTART_TR.md](QUICKSTART_TR.md)
- **Photoshop Örnekleri:** [PHOTOSHOP_EXAMPLES.md](PHOTOSHOP_EXAMPLES.md)
- **After Effects Örnekleri:** [AFTEREFFECTS_EXAMPLES.md](AFTEREFFECTS_EXAMPLES.md)

---

## 💬 Yardıma mı İhtiyacınız Var?

Hala sorun yaşıyorsanız, şunu gönderin:

1. İşletim sisteminiz (Mac/Windows/Linux)
2. `python3 --version` çıktısı
3. Config dosyanızın içeriği
4. Developer Console'daki hata mesajları

**Harika projeler oluşturun! 🚀✨**
