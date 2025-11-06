# 🚀 Script'i Nasıl Çalıştırırım?

## 🍎 macOS Kullanıcıları

### 1. Terminal'i Açın
- **Yöntem 1:** `Cmd + Space` → "Terminal" yazın → Enter
- **Yöntem 2:** Applications → Utilities → Terminal

### 2. Proje Klasörüne Gidin
```bash
cd ~/depo
```

### 3. Script'i Çalıştırın
```bash
./install_manual.sh
```

**Eğer "Permission denied" hatası alırsanız:**
```bash
chmod +x install_manual.sh
./install_manual.sh
```

---

## 🪟 Windows Kullanıcıları

### Seçenek 1: Git Bash (Önerilen)

1. **Git Bash'i açın**
   - Git yüklüyse: Start → "Git Bash" yazın → Enter
   - Git yoksa: https://git-scm.com/downloads

2. **Proje klasörüne gidin:**
   ```bash
   cd ~/depo
   # VEYA tam yol:
   cd /c/Users/KullaniciAdiniz/depo
   ```

3. **Script'i çalıştırın:**
   ```bash
   ./install_manual.sh
   ```

---

### Seçenek 2: PowerShell

1. **PowerShell'i açın**
   - `Win + X` → "Windows PowerShell"
   - VEYA Start → "PowerShell" yazın

2. **Proje klasörüne gidin:**
   ```powershell
   cd $HOME\depo
   ```

3. **Script'i çalıştırın:**
   ```powershell
   bash install_manual.sh
   ```

**Not:** Bu yöntem için Git Bash yüklü olmalı.

---

### Seçenek 3: Elle Kurulum (Windows için En Kolay!)

PowerShell veya Command Prompt'ta:

```powershell
cd %USERPROFILE%\depo

# 1. MCP SDK kur
pip install mcp
pip install pywin32

# 2. Tam yolunuzu öğrenin
cd

# 3. Config dosyası oluşturun
# Dosya Gezgini → Adres çubuğuna: %APPDATA%\Claude
# claude_desktop_config.json oluşturun (Notepad ile)
```

**Config içeriği (Windows için):**
```json
{
  "mcpServers": {
    "godot": {
      "command": "python",
      "args": ["C:\\Users\\KULLANICI_ADIN\\depo\\godot_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    },
    "photoshop": {
      "command": "python",
      "args": ["C:\\Users\\KULLANICI_ADIN\\depo\\photoshop_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    },
    "aftereffects": {
      "command": "python",
      "args": ["C:\\Users\\KULLANICI_ADIN\\depo\\aftereffects_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    }
  }
}
```

**ÖNEMLİ:**
- `KULLANICI_ADIN` yerine kendi kullanıcı adınızı yazın
- `\\` (iki backslash) kullanın

---

## 🐧 Linux Kullanıcıları

### 1. Terminal'i Açın
- `Ctrl + Alt + T`
- VEYA Applications → Terminal

### 2. Proje Klasörüne Gidin
```bash
cd ~/depo
```

### 3. Script'i Çalıştırın
```bash
./install_manual.sh
```

**Eğer "Permission denied" hatası alırsanız:**
```bash
chmod +x install_manual.sh
./install_manual.sh
```

---

## 🎯 Hangi Yöntem Size Uygun?

### macOS → Terminal
### Windows (Git var) → Git Bash
### Windows (Git yok) → Elle Kurulum (yukarıda)
### Linux → Terminal

---

## 📺 Ekran Görüntüsü ile Anlatım

### macOS - Terminal'i Açma

1. **Spotlight açın:** `Cmd + Space`
2. **"Terminal" yazın**
3. **Enter'a basın**
4. **Şu komutları yazın:**
   ```bash
   cd ~/depo
   ./install_manual.sh
   ```

---

### Windows - Git Bash Açma

1. **Start menüsüne tıklayın**
2. **"Git Bash" yazın**
3. **Git Bash'e tıklayın**
4. **Şu komutları yazın:**
   ```bash
   cd ~/depo
   ./install_manual.sh
   ```

---

## ❓ Git Bash Yüklü mü Kontrol Etme

Terminal/PowerShell'de yazın:
```bash
bash --version
```

**Eğer çalışıyorsa:** Git Bash var, scripti çalıştırabilirsiniz!

**Eğer hata veriyorsa:** Git Bash yok, elle kurulum yapın (yukarıda).

---

## 🚀 Hemen Başlayın!

Sisteminize göre yukarıdaki talimatları takip edin. Her adımda ne yapacağınız açıkça yazılı!

**Sorun mu yaşıyorsunuz?** Bana şunu söyleyin:
- İşletim sisteminiz (Mac/Windows/Linux)
- Hangi adımda takıldınız
- Gördüğünüz hata mesajı

Birlikte çözeriz! 💪
