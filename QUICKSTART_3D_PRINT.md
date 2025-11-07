# 🚀 3D Print Automation Ecosystem - Hızlı Başlangıç

## 🎯 5 Dakikada Kurulum

### 1. Repository'yi İndirin

```powershell
# PowerShell (Windows 11)
cd $HOME
git clone <repo-url> 3d-print-ecosystem
cd 3d-print-ecosystem
```

### 2. Python Bağımlılıklarını Yükleyin

```powershell
# Python 3.10+ gerekli
python --version

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 3. Otomatik Kurulum

```powershell
# Kurulum scriptini çalıştır
python install_3d_ecosystem.py
```

Bu script:
- ✅ MCP sunucularını Claude Desktop'a ekler
- ✅ Output dizinlerini oluşturur
- ✅ .env template oluşturur

### 4. Konfigürasyon

#### a) `.env` Dosyasını Düzenleyin

```bash
# .env
HYPER3D_API_KEY=your_api_key_here
BAMBU_PRINTER_IP=192.168.1.100
BAMBU_ACCESS_CODE=your_access_code
BLENDER_PATH=C:\Program Files\Blender Foundation\Blender 4.0\blender.exe
BAMBU_STUDIO_PATH=C:\Program Files\BambuStudio\bambu-studio-console.exe
```

#### b) `config.yaml` Kontrol Edin

Dizinlerin doğru olduğundan emin olun.

### 5. Claude Desktop'ı Yeniden Başlatın

**ÖNEMLİ:** Claude Desktop'ı tamamen kapatıp yeniden açın (Ctrl+Q veya Task Manager'dan kapatın).

### 6. Test Edin!

Claude Desktop'ta yazın:

```
MCP araçlarımı listele
```

**Görmelisiniz:**
- ✅ ~30+ araç
- ✅ 5 MCP sunucu aktif
- ✅ 3d-print-* isimleri

---

## 🎨 İlk Kullanım - Adım Adım

### Senaryo 1: Basit Test (Parametrik Model)

Claude'a sırayla şunları yazın:

```
1. "Blender kurulumu kontrol et"

2. "10cm çapında, 10cm yüksekliğinde bir plant pot modeli oluştur.
    Dosya adı: C:\Users\YourName\Desktop\test_pot.stl"

3. "Bu modeli Bambu Lab A1 için slice et.
    PLA materyal, standard kalite.
    Output: C:\Users\YourName\Desktop\test_pot.gcode"

4. "G-code dosyasını analiz et ve baskı süresini söyle"
```

**Sonuç:** Masaüstünde test_pot.stl ve test_pot.gcode dosyalarınız olacak!

---

### Senaryo 2: Pazar Araştırması + Model

```
1. "Etsy'de 'plant pot' için pazar araştırması yap"

2. "En popüler 5 ürünü listele ve fiyatlarını karşılaştır"

3. "En karlı görünen ürün için benzer bir 3D model oluştur"

4. "Bu modeli yazdırmaya hazırla ve maliyet tahmini ver"
```

**Sonuç:** Veri-destekli ürün kararı + hazır model!

---

### Senaryo 3: Tam Otomatik Workflow

```
"Plant pot nişinde tam otomatik bir ürün geliştir:
1. Pazar araştır
2. Model oluştur
3. Slice et
4. Yazıcıya gönder

Her adımı bana rapor et."
```

Claude şunları yapacak:
- 🔍 Etsy, Thingiverse'de araştırma
- 🎨 3D model oluşturma
- ⚙️ Slicing
- 🖨️ Yazıcıya gönderme
- 📊 Her adımı raporlama

---

## 🛠️ MCP Araçları Referansı

### 📊 Market Research Server

```
search_products           - Ürün araştırması
analyze_competition       - Rekabet analizi
find_niche_opportunities  - Niş fırsat bulma
get_trending_keywords     - Trend keywords
generate_market_report    - Detaylı rapor
```

**Örnek:**
```
"Trend olan 3D baskı ürünlerini araştır ve
en iyi 3 niş fırsatı bul"
```

---

### 🎨 Model Generator Server

```
create_parametric_model   - Parametrik model (cylinder, cube, sphere, torus, plant_pot)
generate_model_with_ai    - AI ile model (Hyper3D)
optimize_for_printing     - Baskıya hazırlama
run_custom_blender_script - Özel Blender scripti
get_blender_info          - Blender bilgisi
```

**Örnek:**
```
"15cm çapında, modern minimal vase oluştur.
Parametrik olsun ve yazdırmaya optimize et."
```

---

### ⚙️ Slicer Server

```
slice_model           - Model slice et
estimate_cost         - Maliyet tahmini
analyze_gcode         - G-code analizi
optimize_supports     - Support optimizasyonu
get_slicer_info       - Slicer bilgisi
```

**Örnek:**
```
"model.stl'yi slice et:
- Printer: Bambu A1
- Material: PLA
- Quality: Fine
- Infill: 30%
- Supports: Evet"
```

---

### 🖨️ Printer Manager Server

```
connect_printer       - Yazıcıya bağlan
get_printer_status    - Durum kontrol
send_job              - İş gönder
get_job_queue         - İş sırası
monitor_progress      - İlerleme takibi
pause_resume_job      - Duraklat/devam
cancel_job            - İptal
get_camera_snapshot   - Kamera görüntüsü
get_statistics        - İstatistikler
```

**Örnek:**
```
"Bambu Lab yazıcıma bağlan (IP: 192.168.1.100)
ve test.gcode dosyasını gönder"
```

---

### 🎯 Workflow Orchestrator Server

```
start_full_workflow      - Tam workflow başlat
market_research_step     - Pazar araştırması adımı
model_generation_step    - Model oluşturma adımı
slicing_step             - Slicing adımı
printing_step            - Printing adımı
get_project_summary      - Proje özeti
list_projects            - Tüm projeler
```

**Örnek:**
```
"'Modern vase' nişinde yeni bir proje başlat
ve tüm adımları otomatik yap"
```

---

## 💡 İleri Düzey Kullanım

### Batch Processing

```
"Phone holder kategorisinde 5 farklı ürün bul,
her biri için model oluştur ve toplu slice et"
```

### Custom Blender Script

```
"Blender'da özel bir script çalıştır:
import bpy
bpy.ops.mesh.primitive_torus_add(major_radius=2, minor_radius=0.5)
bpy.ops.export_mesh.stl(filepath='C:\\torus.stl')"
```

### Trend Tracking

```
"Bu hafta Etsy'de trend olan ürünleri bul,
en popüler 3 tanesi için hemen model oluştur
ve yazdırmaya hazırla"
```

---

## 🐛 Sorun Giderme

### ❌ "MCP araçlarını göremiyorum"

**Çözüm:**
1. Claude Desktop'ı tamamen kapatın (Task Manager)
2. Config dosyasını kontrol edin:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```
3. Yeniden başlatın

---

### ❌ "Blender bulunamadı"

**Çözüm:**
```powershell
# .env dosyasında yolu düzeltin
BLENDER_PATH=C:\Program Files\Blender Foundation\Blender 4.0\blender.exe

# Veya PATH'e ekleyin
$env:PATH += ";C:\Program Files\Blender Foundation\Blender 4.0"
```

---

### ❌ "Bambu Lab yazıcıya bağlanılamadı"

**Kontrol listesi:**
- [ ] Yazıcı ve PC aynı WiFi ağında mı?
- [ ] Yazıcının IP adresi doğru mu?
- [ ] Access code doğru mu?
- [ ] Yazıcıda LAN Mode aktif mi?

**Test:**
```powershell
# Ping testi
ping 192.168.1.100
```

---

### ❌ "Hyper3D API hatası"

**Çözüm:**
1. API key'i .env'de doğru mu?
2. API rate limit aşıldı mı?
3. İnternet bağlantısı var mı?

**Alternatif:** Parametrik modelleri kullanın:
```
"AI yerine parametrik plant pot oluştur"
```

---

## 📚 Ek Kaynaklar

### Dokümantasyon
- [3D_PRINT_ECOSYSTEM_README.md](3D_PRINT_ECOSYSTEM_README.md) - Detaylı mimari
- [config.yaml](config.yaml) - Konfigürasyon ayarları

### Yazılımlar
- **Blender:** https://www.blender.org/download/
- **Bambu Studio:** https://bambulab.com/en/download/studio
- **Claude Desktop:** https://claude.ai/desktop

### API'ler
- **Hyper3D:** (API dokümantasyonu)
- **Bambu Lab:** (API dokümantasyonu)

---

## 🎉 Başarılar!

Artık Claude Desktop ile 3D baskı ekosisteminiz hazır!

**Deneyebilecekleriniz:**
- ✅ Pazar araştırması ile ürün fikirleri bulun
- ✅ Otomatik 3D model oluşturun
- ✅ Optimum baskı ayarlarını bulun
- ✅ Remote yazıcı kontrolü yapın
- ✅ Tam otomasyon ile üretim yapın

**Sonraki seviye:**
- Multi-printer setup
- Cloud entegrasyonu
- AI kalite kontrol
- Etsy/Shopify direkt satış

---

**Sorularınız mı var?**
- GitHub Issues
- Dokümantasyona bakın
- Developer Console (Ctrl+Shift+I) loglarını kontrol edin

**İyi baskılar! 🖨️✨**
