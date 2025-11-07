# 📖 3D Print Automation - Kullanım Örnekleri

Bu dokümanda gerçek hayat senaryoları ve Claude Desktop ile nasıl kullanılacağı gösterilmektedir.

---

## 🎯 Senaryo 1: İlk Kez Kullanım - Test Workflow

**Hedef:** Sistemi test etmek ve basit bir model yazdırmak

### Adım 1: MCP Araçlarını Kontrol Et

```
Claude'a: "MCP araçlarımı listele"
```

**Beklenen Sonuç:** ~30+ araç görmelisiniz.

### Adım 2: Blender Kurulumu Kontrol

```
Claude'a: "Blender kurulumunu kontrol et"
```

**Cevap örneği:**
```json
{
  "blender_path": "C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe",
  "blender_found": true,
  "version_output": "Blender 4.0.0"
}
```

### Adım 3: Basit Bir Model Oluştur

```
Claude'a: "5cm yarıçapında, 10cm yüksekliğinde bir silindir model oluştur.
Dosya yolu: C:\Users\Arslan\Desktop\test_cylinder.stl"
```

**Claude şunları yapacak:**
1. `create_parametric_model` aracını kullanacak
2. Blender'da model oluşturacak
3. STL olarak export edecek

**Sonuç:**
```json
{
  "success": true,
  "output_file": "C:\\Users\\Arslan\\Desktop\\test_cylinder.stl",
  "model_type": "cylinder"
}
```

### Adım 4: Slice Et

```
Claude'a: "test_cylinder.stl dosyasını Bambu Lab A1 için slice et.
PLA materyal, standard kalite kullan.
Output: C:\Users\Arslan\Desktop\test_cylinder.gcode"
```

**Sonuç:** G-code dosyası + süre/maliyet tahmini

### Adım 5: Yazıcıya Gönder (Opsiyonel)

```
Claude'a: "Bambu Lab yazıcıma bağlan:
IP: 192.168.1.100
Access Code: XXXXX

Sonra test_cylinder.gcode'u gönder"
```

---

## 🛍️ Senaryo 2: E-ticaret Ürün Araştırması

**Hedef:** Etsy'de satılabilecek karlı bir ürün bulmak

### Adım 1: Trend Keywords Al

```
Claude'a: "3D baskı için trend olan keywords listesini ver"
```

**Cevap:**
```json
{
  "total_keywords": 15,
  "keywords": [
    "plant pot",
    "phone holder",
    "desk organizer",
    "cookie cutter",
    ...
  ]
}
```

### Adım 2: Niş Fırsat Analizi

```
Claude'a: "Bu keywordler arasından en iyi 3 niş fırsatı bul:
- plant pot
- phone holder
- desk organizer
- cookie cutter
- vase"
```

**Claude şunları yapacak:**
1. Her keyword için rekabet analizi
2. Fiyat araştırması
3. Thingiverse'de model sayısı kontrolü
4. Opportunity score hesaplama

**Cevap örneği:**
```json
{
  "top_3": [
    {
      "keyword": "plant pot",
      "opportunity_score": 75,
      "competition_level": "Low",
      "average_price": "$18.50",
      "etsy_results": 15,
      "thingiverse_results": 24
    },
    ...
  ]
}
```

### Adım 3: En İyi Nişte Detaylı Rapor

```
Claude'a: "Plant pot nişi için detaylı pazar raporu oluştur"
```

**Cevap:** Recommendations, pricing strategy, next steps

### Adım 4: Ürün Modeli Oluştur

```
Claude'a: "Plant pot kategorisinde modern, minimalist bir model oluştur:
- Çap: 12cm
- Yükseklik: 12cm
- Drainage hole olsun
- Wall thickness: 2mm

Dosya: C:\Users\Arslan\Desktop\modern_pot.stl"
```

**Sonuç:** Yazdırmaya hazır STL modeli

---

## 🚀 Senaryo 3: Tam Otomatik Production Pipeline

**Hedef:** Fikir → Model → Baskı (tamamen otomatik)

### Single Command Workflow

```
Claude'a: "Phone holder nişinde yeni bir proje başlat.

Adımlar:
1. Pazar araştırması yap
2. En popüler phone holder tipini belirle
3. O tip için 3D model oluştur
4. Bambu Lab A1 için slice et (PLA, standard)
5. Maliyet hesapla
6. Bana her adımı rapor et

Proje adı: MyPhoneHolder_v1"
```

**Claude'ın yapacakları:**

**ADIM 1: Pazar Araştırması**
```
- Etsy'de "phone holder" araştırması
- Popüler tasarımları analiz
- Fiyat aralığı: $8-$15
```

**ADIM 2: Model Belirleme**
```
- En popüler: Ayarlanabilir açılı stand
- Özellikler: Cable slot, non-slip base
```

**ADIM 3: Model Oluşturma**
```
- create_parametric_model veya AI generation
- Output: output/models/MyPhoneHolder_v1.stl
```

**ADIM 4: Slicing**
```
- slice_model ile G-code üret
- Output: output/gcode/MyPhoneHolder_v1.gcode
- Tahmini süre: 2 saat 15 dakika
- Filament: 35g
```

**ADIM 5: Maliyet**
```
- Materyal: $0.70 (35g PLA @ $20/kg)
- Elektrik: $0.11 (2.25h @ 100W)
- Toplam: $0.81
- Önerilen satış fiyatı: $12-15 (15x kar marjı)
```

**ADIM 6: Rapor**
```json
{
  "project_id": 1,
  "project_name": "MyPhoneHolder_v1",
  "niche": "phone holder",
  "status": "ready_to_print",
  "model_path": "output/models/MyPhoneHolder_v1.stl",
  "gcode_path": "output/gcode/MyPhoneHolder_v1.gcode",
  "estimated_cost": "$0.81",
  "recommended_price": "$12-15",
  "profit_margin": "15x"
}
```

---

## 🎨 Senaryo 4: Custom Design ile Özel Üretim

**Hedef:** Müşteriden gelen isteğe göre özel model

### Müşteri İsteği:
"Masama özel bir kalem tutucu istiyorum:
- 3 bölmeli (kalem, silgi, ataş için)
- Minimalist tasarım
- Ahşap masama uygun renk (kahverengi/siyah)
- Boyut: 15cm x 8cm x 6cm"

### Claude ile Üretim:

```
Claude'a: "Müşteri isteği:
3 bölmeli masaüstü organizer oluştur.

Özellikler:
- Bölüm 1: Kalem için (7cm çap, 10cm derinlik)
- Bölüm 2: Silgi/küçük eşya (4cm çap, 5cm derinlik)
- Bölüm 3: Ataş için (5cm x 5cm, 3cm derinlik)
- Genel boyut: 15cm x 8cm
- Modern, minimalist tasarım

Blender'da custom script ile oluştur ve STL export et."
```

**Claude'ın oluşturacağı Blender Script:**
```python
import bpy
import bmesh

# Sahneyi temizle
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Ana base oluştur
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.3))
base = bpy.context.active_object
base.scale = (7.5, 4, 0.3)

# Kalem bölmesi (silindir)
bpy.ops.mesh.primitive_cylinder_add(radius=3.5, depth=10, location=(-3, 0, 5.3))
pencil_section = bpy.context.active_object

# ... (diğer bölümler)

# Export STL
bpy.ops.export_mesh.stl(filepath="C:\\custom_organizer.stl")
```

---

## 🔄 Senaryo 5: Batch Production (Toplu Üretim)

**Hedef:** 10 farklı cookie cutter modeli yazdırmak

### Workflow:

```
Claude'a: "Cookie cutter kategorisinde 10 farklı şekil bul ve hepsi için model oluştur:

1. Pazar araştır, popüler 10 şekli belirle
2. Her biri için parametrik model oluştur
3. Tümünü slice et (aynı ayarlar)
4. Toplam maliyet hesapla
5. Batch print listesi oluştur"
```

**Claude'ın işlem adımları:**

**1. Araştırma:**
- Star, Heart, Christmas Tree, Snowflake, Cat, Dog, Flower, Butterfly, Moon, Sun

**2. Model Oluşturma (loop):**
```python
for shape in shapes:
    create_parametric_model(
        model_type=shape,
        output_path=f"output/models/cookie_{shape}.stl"
    )
```

**3. Slicing (batch):**
```python
for stl_file in stl_files:
    slice_model(
        input_path=stl_file,
        output_path=f"output/gcode/{stl_file.stem}.gcode",
        printer="A1",
        material="PLA"
    )
```

**4. Maliyet Raporu:**
```json
{
  "total_models": 10,
  "total_filament": "120g",
  "total_cost": "$2.40",
  "total_print_time": "4 hours 30 minutes",
  "cost_per_unit": "$0.24",
  "recommended_price_per_unit": "$3-5"
}
```

**5. Print Queue:**
```json
{
  "queue": [
    {"file": "cookie_star.gcode", "priority": 1},
    {"file": "cookie_heart.gcode", "priority": 2},
    ...
  ],
  "estimated_completion": "Tomorrow 2:30 PM"
}
```

---

## 🤖 Senaryo 6: AI-Generated Model

**Hedef:** Hyper3D AI ile text-to-3D model oluşturmak

### Prompt Engineering:

```
Claude'a: "Hyper3D AI kullanarak şu modeli oluştur:

Prompt: 'Modern geometric vase with hexagonal pattern,
20cm tall, watertight, minimalist design, suitable for
3D printing with PLA'

Style: Low Poly
Output: C:\Users\Arslan\Desktop\ai_vase.stl

Sonra yazdırmaya optimize et."
```

**Claude şunları yapacak:**

1. **AI Generation:**
```python
generate_model_with_ai(
    prompt="Modern geometric vase with hexagonal pattern...",
    style="low_poly",
    output_path="C:\\Users\\Arslan\\Desktop\\ai_vase.stl"
)
```

2. **Optimization:**
```python
optimize_for_printing(
    input_path="ai_vase.stl",
    output_path="ai_vase_optimized.stl"
)
```

**Sonuç:** Yazdırmaya hazır, optimize edilmiş AI modeli

---

## 📊 Senaryo 7: Multi-Product Comparison

**Hedef:** 3 farklı nişi karşılaştırmak ve en iyisini seçmek

```
Claude'a: "Şu 3 niş için detaylı analiz yap ve hangisinin
en karlı olduğunu söyle:

1. Plant pots
2. Phone stands
3. Desk organizers

Her biri için:
- Pazar araştırması
- Rekabet analizi
- Ortalama fiyat
- Üretim maliyeti tahmini
- Kar marjı
- Nihai tavsiye"
```

**Claude'ın Çıktısı:**

| Niş | Rekabet | Ort. Fiyat | Üretim Maliyeti | Kar Marjı | Skor |
|-----|---------|-----------|----------------|-----------|------|
| Plant Pots | Düşük | $18 | $1.20 | 15x | ⭐⭐⭐⭐⭐ |
| Phone Stands | Orta | $12 | $0.80 | 15x | ⭐⭐⭐⭐ |
| Desk Organizers | Yüksek | $15 | $1.50 | 10x | ⭐⭐⭐ |

**Tavsiye:**
```
🏆 Plant Pots en iyi fırsat:
- Düşük rekabet
- Yüksek fiyat noktası
- İyi kar marjı
- Sürekli talep

Sonraki adım: Plant pot koleksiyonu oluşturun!
```

---

## 🎯 Senaryo 8: Quality Control & Iteration

**Hedef:** Model iterasyonu ve iyileştirme

### İlk Versiyon:

```
Claude'a: "Phone holder modeli oluştur ve slice et"
```

### Baskı Sonrası:

```
Claude'a: "Phone holder'ı yazdırdım ama şu sorunlar var:
1. Telefon biraz gevşek oturuyor
2. Kablo geçişi çok dar
3. Ağırlık hafif, devrilme riski var

Bu sorunları düzeltmek için yeni versiyon oluştur:
- Phone slot'u 2mm daralt
- Cable hole'u 3mm genişlet
- Base'e 5mm daha kalın yap (ağırlık için)

Dosya: phone_holder_v2.stl"
```

**Claude şunları yapacak:**
1. Önceki modeli analiz eder
2. Parametreleri günceller
3. Yeni versiyon oluşturur
4. Değişiklikleri raporlar

---

## 🌟 Senaryo 9: Seasonal Products (Mevsimsel Ürünler)

**Hedef:** Noel sezonu için ürün koleksiyonu

```
Claude'a: "Noel sezonu için satılabilecek 5 ürün öner ve
hepsinin modelini oluştur:

Kriterler:
- Noel teması
- 3D baskıya uygun
- Etsy'de popüler
- Üretim maliyeti <$2
- Satış fiyatı >$15

Her biri için model + slice + maliyet raporu ver."
```

**Claude'ın Önerileri:**
1. Snowflake ornaments (set of 6)
2. Christmas tree phone stand
3. Santa cookie cutters (set of 4)
4. Reindeer desk organizer
5. Advent calendar small boxes (set of 24)

**Rapor:**
```json
{
  "collection": "Christmas 2024",
  "total_products": 5,
  "total_cost": "$8.50",
  "estimated_revenue": "$75-90",
  "profit_margin": "9-10x",
  "print_time": "2 days",
  "recommendation": "Start with snowflake ornaments - fastest to print, highest margin"
}
```

---

## 💰 Senaryo 10: Profitability Calculator

**Hedef:** Ürün karlılığını hesaplamak

```
Claude'a: "Plant pot modelim için karlılık analizi yap:

Maliyetler:
- Filament: 45g PLA ($20/kg)
- Elektrik: 2.5 saat baskı
- Paketleme: $0.50
- Etsy fees: %6.5
- Shipping: $3.50

Satış fiyatı: $18

Ne kadar kar ederim? Bu fiyat mantıklı mı?"
```

**Claude'ın Hesaplaması:**

```
Maliyetler:
- Filament: $0.90 (45g @ $20/kg)
- Elektrik: $0.13 (2.5h @ 100W @ $0.15/kWh)
- Paketleme: $0.50
- Etsy fees: $1.17 (6.5% of $18)
- Shipping: $3.50
──────────────────
Toplam Maliyet: $6.20

Satış: $18.00
Net Kar: $11.80

ROI: 190%
Kar Marjı: 65%

✅ Çok iyi bir kar marjı!

Tavsiye:
- Bu fiyat çok uygun
- Eğer talep yüksekse $20-22'ye çıkarabilirsiniz
- Veya 2'li set olarak $32'ye satabilirsiniz
```

---

## 🎓 Bonus: Workflow Templates

### Template 1: Hızlı Prototip

```
"[NICHE] için hızlı prototip:
1. Basit parametrik model
2. Draft quality slice
3. Hızlı baskı (0.28mm layer)
4. Maliyet <$1"
```

### Template 2: Kaliteli Ürün

```
"[NICHE] için satış kalitesinde ürün:
1. AI veya custom model
2. Fine quality slice (0.12mm)
3. Optimize supports
4. Detaylı maliyet raporu"
```

### Template 3: Batch Production

```
"[CATEGORY] için toplu üretim:
1. 10+ varyasyon
2. Standart ayarlar
3. Toplam maliyet ve süre
4. Print queue planlama"
```

---

**Bu örneklerle 3D Print Automation Ecosystem'inizi tam performansta kullanabilirsiniz! 🚀**

Daha fazla örnek için projeyi yıldızlayın ⭐ ve katkıda bulunun!
