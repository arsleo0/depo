# Visual Studio Code'da Proje Kurulumu

## 🚀 Hızlı Başlangıç

### 1. Projeyi Aç

**Seçenek A - Komut satırından:**
```bash
cd /home/user/depo/image-to-3d-pipeline
code .
```

**Seçenek B - VS Code içinden:**
1. VS Code'u aç
2. **File → Open Folder** (veya `Ctrl+K Ctrl+O`)
3. `/home/user/depo/image-to-3d-pipeline` klasörünü seç
4. **Select Folder**'a tıkla

### 2. Gerekli Uzantıları Yükle

VS Code açıldığında sol tarafta **Extensions** (`Ctrl+Shift+X`) bölümünden şunları yükle:

✅ **Python** (Microsoft)
✅ **Pylance** (Microsoft)
✅ **YAML** (Red Hat) - config.yaml için

### 3. Python Yorumlayıcısını Seç

1. `Ctrl+Shift+P` tuşuna bas
2. **"Python: Select Interpreter"** yaz
3. **Python 3.8+** sürümünü seç
   - Eğer virtual environment oluşturursanız: `./venv/bin/python`

### 4. Terminal'i Aç

- **Kısayol:** `Ctrl+ö` veya `Ctrl+``
- **Menüden:** Terminal → New Terminal

### 5. Sanal Ortam Oluştur (Önerilen)

Terminal'de:

**Linux/Mac:**
```bash
# Virtual environment oluştur
python3 -m venv venv

# Aktive et
source venv/bin/activate

# Prompt (venv) ile başlamalı
```

**Windows:**
```bash
# Virtual environment oluştur
python -m venv venv

# Aktive et
venv\Scripts\activate
```

### 6. Bağımlılıkları Yükle

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Bu işlem 5-10 dakika sürebilir (PyTorch büyük bir kütüphane).

### 7. Kurulumu Doğrula

```bash
python verify_installation.py
```

Şöyle bir çıktı görmelisiniz:
```
============================================================
Image-to-3D Pipeline - Installation Verification
============================================================

Checking core dependencies...
✓ PyTorch
✓ TorchVision
✓ NumPy
...
```

## 📁 Proje Yapısı (VS Code'da)

VS Code Explorer'da göreceğiniz yapı:

```
📁 image-to-3d-pipeline/
├── 📄 image_to_3d.py          # Ana pipeline scripti
├── 📄 config.yaml              # Tüm ayarlar burada
├── 📄 requirements.txt         # Python bağımlılıkları
├── 📄 README.md               # Detaylı dokümantasyon
├── 📄 QUICKSTART.md           # Hızlı başlangıç
├── 📄 VS_CODE_SETUP.md        # Bu dosya
│
├── 🔧 setup.sh                 # Otomatik kurulum scripti
├── 🔧 examples.sh              # Kullanım örnekleri
├── 🔧 verify_installation.py   # Kurulum doğrulama
│
├── 📁 .vscode/                 # VS Code ayarları
│   ├── settings.json          # Editor ayarları
│   ├── launch.json            # Debug yapılandırmaları
│   └── tasks.json             # Hızlı görevler
│
├── 📁 input/                   # Görselleri buraya koyun
├── 📁 output/                  # Çıktılar burada
│   ├── 📁 stl/                # 3D model dosyaları
│   ├── 📁 previews/           # Önizleme görselleri
│   └── 📁 reports/            # Raporlar ve metadata
├── 📁 logs/                    # İşlem logları
└── 📁 processing/              # Geçici dosyalar
```

## ▶️ VS Code'dan Çalıştırma

### Yöntem 1: Terminal'den Manuel

Terminal'i aç (`Ctrl+ö`) ve:

```bash
# Tek görsel işle
python image_to_3d.py --image input/your-image.jpg --category DECO

# Tüm görselleri toplu işle
python image_to_3d.py --batch
```

### Yöntem 2: Debug Mode (F5)

1. `image_to_3d.py` dosyasını aç
2. **F5** tuşuna bas (veya Run → Start Debugging)
3. Açılan menüden seç:
   - **Python: Pipeline - Single Image** → Tek görsel
   - **Python: Pipeline - Batch** → Toplu işlem
   - **Python: Verify Installation** → Kurulum kontrolü

### Yöntem 3: Tasks (Hızlı Komutlar)

1. `Ctrl+Shift+P` tuşuna bas
2. **"Tasks: Run Task"** yaz
3. Görevi seç:
   - **Verify Installation** → Kurulumu kontrol et
   - **Process Batch** → Toplu işlem başlat
   - **Install Dependencies** → Bağımlılıkları yükle
   - **View Batch Report** → Raporu görüntüle

### Yöntem 4: Sağ Tık Menüsü

1. `image_to_3d.py` dosyasına sağ tıkla
2. **Run Python File in Terminal** seç

## 🎯 İlk Testinizi Yapın

### 1. Test Görseli Ekle

```bash
# Bir ürün fotoğrafı kopyalayın
cp ~/Downloads/product-photo.jpg input/test.jpg
```

Veya VS Code'da:
- `input/` klasörüne sağ tıklayın
- **Upload...** seçin
- Görselinizi seçin

### 2. İşlemi Başlat

Terminal'de:
```bash
python image_to_3d.py --image input/test.jpg --category TEST
```

### 3. Sonuçları İncele

İşlem bittiğinde VS Code Explorer'da:
- `output/stl/` → STL dosyanızı bulun
- `output/previews/` → Önizleme görsellerini açın
- `output/reports/` → JSON metadata'yı inceleyin

## 🔧 Ayarları Düzenle

### config.yaml'ı Aç

1. VS Code Explorer'da `config.yaml` dosyasına tıkla
2. Düzenle:

```yaml
# Görsel kalitesi (512, 1024, 2048)
preprocessing:
  target_resolution: 1024  # Daha hızlı için 512

# Baskı boyutu
printing:
  max_dimension_mm: 100  # İstediğiniz boyut

# Fiyatlandırma
business:
  pricing:
    pla_cost_per_gram: 0.02  # Kendi maliyetiniz
    retail_markup: 5.0        # Kar marjı çarpanı
```

3. Kaydet (`Ctrl+S`)

## 📊 Toplu İşlem Workflow

### Tipik Kullanım Senaryosu:

1. **Görselleri ekle:**
   ```bash
   cp ~/Photos/products/*.jpg input/
   ```

2. **Toplu işlem başlat:**
   ```bash
   python image_to_3d.py --batch
   ```

3. **İlerlemeyi takip et:**
   - Terminal'de progress bar göreceksiniz
   - `logs/pipeline.log` dosyasını açarak detayları izleyebilirsiniz

4. **Raporu incele:**
   ```bash
   cat output/reports/batch_report.csv
   ```

5. **STL dosyalarını kontrol et:**
   - `output/stl/` klasöründeki tüm modeller yazdırmaya hazır
   - PrusaSlicer veya Cura'da açıp doğrulayın

## 🐛 Debug İpuçları

### Breakpoint Ekleme

1. `image_to_3d.py` dosyasını aç
2. Bir satır numarasının soluna tıklayarak kırmızı nokta (breakpoint) ekle
3. **F5** ile debug modunda başlat
4. Program breakpoint'te duracak
5. **Debug Console**'da değişkenleri inceleyebilirsiniz

### Log Dosyasını İzle

VS Code'da `logs/pipeline.log` dosyasını açın. Her işlemde otomatik güncellenir.

### Hata Ayıklama:

Terminal'de daha detaylı çıktı için:
```bash
# Detaylı log seviyesi
python image_to_3d.py --image input/test.jpg --category TEST 2>&1 | tee debug.log
```

## ⌨️ Yararlı VS Code Kısayolları

| Kısayol | Açıklama |
|---------|----------|
| `Ctrl+Shift+P` | Komut Paleti |
| `Ctrl+ö` | Terminal Aç/Kapat |
| `Ctrl+B` | Sidebar Aç/Kapat |
| `Ctrl+P` | Dosya Ara |
| `Ctrl+Shift+F` | Proje İçinde Ara |
| `F5` | Debug Başlat |
| `Ctrl+C` | Terminal'de İşlemi Durdur |
| `Ctrl+K Ctrl+O` | Klasör Aç |
| `Ctrl+,` | Ayarlar |

## 💡 Pratik İpuçları

### 1. Terminal'i Bölme

Birden fazla işlem için:
- Terminal penceresinde **Split Terminal** ikonuna tıklayın
- Veya `Ctrl+Shift+5`

### 2. Çoklu Cursor

Aynı değişikliği birden fazla yerde yapmak için:
- `Alt` + tıklama ile birden fazla cursor ekle
- Veya `Ctrl+D` ile aynı kelimeyi seç

### 3. Git Entegrasyonu

VS Code'un built-in Git desteğini kullanın:
- Sol tarafta **Source Control** (`Ctrl+Shift+G`)
- Değişiklikleri görün, commit yapın

### 4. Settings Sync

VS Code ayarlarınızı GitHub ile senkronize edebilirsiniz:
- Settings → Turn on Settings Sync

## 🚨 Sık Karşılaşılan Sorunlar

### "Python interpreter not found"

**Çözüm:**
1. `Ctrl+Shift+P` → **Python: Select Interpreter**
2. Python 3.8+ seçin
3. Yoksa Python'u yükleyin: https://www.python.org/downloads/

### "Module not found: torch"

**Çözüm:**
```bash
# Virtual environment aktif mi kontrol edin
# Prompt (venv) ile başlamalı

# Bağımlılıkları tekrar yükleyin
pip install -r requirements.txt
```

### "CUDA out of memory"

**Çözüm:**
`config.yaml` dosyasında:
```yaml
preprocessing:
  target_resolution: 512  # 1024'ten düşürün
```

### Terminal'de komut bulunamıyor

**Çözüm:**
```bash
# Doğru dizinde olduğunuzdan emin olun
cd /home/user/depo/image-to-3d-pipeline

# Virtual environment aktif mi?
source venv/bin/activate  # Linux/Mac
```

## 📚 Daha Fazla Bilgi

- **Detaylı dokümantasyon:** `README.md`
- **Hızlı başlangıç:** `QUICKSTART.md`
- **Kullanım örnekleri:** `examples.sh`
- **Log dosyaları:** `logs/pipeline.log`

## ✅ Kontrol Listesi

Kurulum tamamlandığında:

- [ ] VS Code'da proje açık
- [ ] Python uzantısı yüklü
- [ ] Python interpreter seçili
- [ ] Virtual environment oluşturuldu ve aktif
- [ ] Bağımlılıklar yüklendi (`pip install -r requirements.txt`)
- [ ] Kurulum doğrulandı (`python verify_installation.py`)
- [ ] Test görseli işlendi (`python image_to_3d.py --image input/test.jpg`)
- [ ] STL dosyası oluştu (`output/stl/` klasöründe)

## 🎉 Hazırsınız!

Artık VS Code'dan rahatça çalışabilirsiniz. İyi baskılar! 🚀

---

**Yardım gerekirse:**
1. `logs/pipeline.log` dosyasını kontrol edin
2. `python verify_installation.py` çalıştırın
3. README.md'yi inceleyin
