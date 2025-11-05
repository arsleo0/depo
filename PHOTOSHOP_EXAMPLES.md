# Photoshop MCP Server - Örnek Kullanım Senaryoları

Bu dosya, Claude Desktop ile Photoshop'u kullanırken yapabileceğiniz pratik örnekleri içerir.

## 🎯 Temel İşlemler

### 1. Başlangıç Kontrolü

```
Claude'a sor:
"Photoshop bağlantımı kontrol et"
```

**Beklenen Çıktı:**
```
✅ Photoshop bağlantısı başarılı!

Adobe Photoshop 2024 25.0

Platform: Darwin
```

---

### 2. Dosya Açma

```
Claude'a sor:
"/Users/kullanici/Desktop/photo.jpg dosyasını aç"
```

**Windows'ta:**
```
"C:\Users\Kullanici\Desktop\photo.jpg dosyasını Photoshop'ta aç"
```

---

### 3. Doküman Bilgisi

```
Claude'a sor:
"Aktif Photoshop dokümanı hakkında bilgi ver"
```

**Çıktı:**
```
📄 Aktif Doküman Bilgileri:

📝 İsim: portrait.jpg
📏 Boyut: 1920 x 1080 piksel
🎨 Renk Modu: RGBColorMode
🔍 Çözünürlük: 72 DPI
📚 Katman Sayısı: 3
💾 Yol: /Users/kullanici/portrait.jpg
```

---

## 🖼️ Görüntü Düzenleme

### 4. Yeniden Boyutlandırma

```
Claude'a sor:
"Bu görüntüyü 800x600 piksel yap"
```

```
"Görüntüyü yarı boyutuna küçült"
```

```
"Görüntüyü Instagram square format için 1080x1080 yap"
```

---

### 5. Kırpma (Crop)

```
Claude'a sor:
"Görüntüyü sol üst köşeden başlayarak 500x500 piksel kırp"
```

**Detaylı:**
```
"Görüntüyü şu koordinatlardan kırp:
- X: 100
- Y: 100
- Genişlik: 800
- Yükseklik: 600"
```

---

### 6. Filtre Uygulama

**Gaussian Blur:**
```
Claude'a sor:
"Aktif katmana 5 piksel Gaussian Blur uygula"
```

```
"Background'u 10 piksel bulanıklaştır"
```

**Sharpen:**
```
"Görüntüyü keskinleştir"
```

**Invert:**
```
"Renkleri tersine çevir (invert)"
```

---

## 📚 Katman İşlemleri

### 7. Yeni Katman Oluşturma

```
Claude'a sor:
"'Logo' adında yeni bir katman oluştur"
```

```
"'Background Copy' katmanı ekle"
```

---

### 8. Katmanları Listeleme

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
```

---

## ✍️ Metin İşlemleri

### 9. Basit Metin Ekleme

```
Claude'a sor:
"Görüntünün üstüne 'HELLO WORLD' yaz"
```

---

### 10. Özelleştirilmiş Metin

```
Claude'a sor:
"Görüntüye şu özelliklerde metin ekle:
- Metin: 'YENİ ÜRÜN'
- Konum: X=100, Y=100
- Font boyutu: 72pt
- Renk: Kırmızı (#FF0000)"
```

---

### 11. Watermark Ekleme

```
Claude'a sor:
"Sol alt köşeye '© 2024 Şirket Adı' watermark ekle, küçük font, beyaz renk"
```

---

## 💾 Kaydetme ve Dışa Aktarma

### 12. Mevcut Dosyayı Kaydetme

```
Claude'a sor:
"Dosyayı kaydet"
```

---

### 13. Farklı Kaydet (PSD)

```
Claude'a sor:
"Bu dosyayı /Users/kullanici/Desktop/edited.psd olarak kaydet"
```

---

### 14. JPEG Dışa Aktarma

```
Claude'a sor:
"Bu dosyayı JPEG olarak dışa aktar, maksimum kalite"
```

**Detaylı:**
```
"Dosyayı JPG formatında kaydet:
- Yol: /Users/kullanici/Desktop/output.jpg
- Kalite: 12"
```

---

### 15. PNG Dışa Aktarma

```
Claude'a sor:
"PNG formatında kaydet: /Users/kullanici/Desktop/transparent.png"
```

---

## 🔄 Batch İşlemler

### 16. Toplu Yeniden Boyutlandırma

```
Claude'a sor:
"/Users/kullanici/Photos klasöründeki tüm resimleri 1024x768 boyutuna getir ve /Users/kullanici/Photos_Resized klasörüne JPG olarak kaydet"
```

**Windows'ta:**
```
"C:\Users\Kullanici\Photos klasöründeki resimleri 800x600 yap ve C:\Users\Kullanici\Output'a kaydet"
```

---

### 17. Toplu Format Dönüştürme

```
Claude'a sor:
"Desktop/RawPhotos klasöründeki tüm PSD dosyalarını PNG'ye çevir ve Desktop/PNGs'e kaydet"
```

---

## 🎨 Yaratıcı Workflow'lar

### 18. Logo Hazırlama

```
Claude'a sor:
"Bana yardım et:
1. Desktop/logo.psd dosyasını aç
2. 512x512 piksel boyutuna getir
3. PNG olarak Desktop/logo_512.png'ye kaydet
4. 256x256 boyutuna küçült
5. PNG olarak Desktop/logo_256.png'ye kaydet"
```

---

### 19. Sosyal Medya Paketi

```
Claude'a sor:
"Desktop/poster.jpg dosyasını kullanarak şunları oluştur:
1. Instagram post: 1080x1080
2. Instagram story: 1080x1920
3. Facebook cover: 820x312
4. Twitter header: 1500x500
Hepsini Desktop/SocialMedia/ klasörüne kaydet"
```

---

### 20. Fotoğraf Düzenleme Pipeline

```
Claude'a sor:
"Desktop/portrait.jpg için şu işlemleri yap:
1. Dosyayı aç
2. 3 piksel Gaussian Blur uygula (soft look)
3. Brightness'ı %10 artır
4. Sağ alt köşeye '© 2024' watermark ekle (küçük, beyaz)
5. JPEG olarak kaydet, kalite 11
6. Instagram için 1080x1080'e küçült ve ayrı kaydet"
```

---

### 21. Ürün Fotoğrafı Hazırlama

```
Claude'a sor:
"E-ticaret sitesi için ürün fotoğrafı hazırla:
1. Desktop/product.jpg'yi aç
2. Beyaz arka plan ekle
3. 2000x2000 piksel boyutuna getir (ürün ortada)
4. Hafif sharpen uygula
5. PNG olarak kaydet (şeffaf arka plan)
6. 800x800 thumbnail versiyonu oluştur"
```

---

### 22. Thumbnail Batch Oluşturma

```
Claude'a sor:
"YouTube thumbnail'leri oluştur:
- Kaynak: Desktop/Videos/screenshots/
- Her resmi 1280x720 yap
- Sol üst köşeye 'EP 01', 'EP 02' vb. numara ekle (72pt, bold, beyaz)
- Hedef: Desktop/Thumbnails/
- Format: JPG, yüksek kalite"
```

---

## 🚀 Gelişmiş JSX Scriptleri

### 23. Özel Script: Tüm Katmanları Hizala

```
Claude'a sor:
"Şu JSX kodunu çalıştır:

var doc = app.activeDocument;
for (var i = 0; i < doc.layers.length; i++) {
    doc.layers[i].translate(0, 50);
}
'Tüm katmanlar 50px aşağı taşındı';"
```

---

### 24. Özel Script: Opacity Animasyonu

```
Claude'a sor:
"Şu JSX'i çalıştır:

var doc = app.activeDocument;
for (var i = 0; i < doc.layers.length; i++) {
    doc.layers[i].opacity = (i + 1) * 20;
}
'Katmanlara gradient opacity uygulandı';"
```

---

### 25. Özel Script: Smart Object'e Çevir

```
Claude'a sor:
"Aktif katmanı Smart Object'e çevir:

var layer = app.activeDocument.activeLayer;
layer.convertToSmartObject();
'Smart Object oluşturuldu';"
```

---

### 26. Özel Script: Tüm Katmanları Görünür Yap

```
Claude'a sor:
"Tüm gizli katmanları göster:

var doc = app.activeDocument;
for (var i = 0; i < doc.layers.length; i++) {
    doc.layers[i].visible = true;
}
'Tüm katmanlar görünür yapıldı';"
```

---

## 🎓 Karmaşık Senaryolar

### 27. Profesyonel Fotoğraf Post-Processing

```
Claude'a sor:
"Profesyonel düzenleme yap:
1. Desktop/raw_photo.jpg'yi aç
2. Duplicate layer oluştur
3. Alt katmana 8 piksel Gaussian Blur
4. Üst katmanı %50 opacity yap (glow effect)
5. Flatten image
6. Slight sharpen uygula
7. JPEG olarak kaydet (kalite 12)"
```

---

### 28. Batch Watermark Ekleme

```
Claude'a sor:
"Desktop/Portfolio/ klasöründeki tüm JPG dosyalarına:
- Sağ alt köşeye 'www.sitename.com' watermark ekle
- Font: 24pt, beyaz, %50 opacity
- Aynı dosyanın üzerine kaydet"
```

---

### 29. E-ticaret Ürün Seti

```
Claude'a sor:
"Ürün fotoğrafları için tam set oluştur:
1. Desktop/product_raw.jpg'yi aç
2. White background ekle
3. Şu boyutları oluştur ve kaydet:
   - 2000x2000 (ana görsel)
   - 1000x1000 (detay)
   - 500x500 (thumbnail)
   - 300x300 (mini)
4. Tümünü Desktop/Product_Set/ klasörüne kaydet"
```

---

### 30. Instagram Carousel Hazırlama

```
Claude'a sor:
"Instagram carousel için 10 slide hazırla:
1. Her slide 1080x1080
2. Her slide'a 'Slide 1/10', 'Slide 2/10' vb. ekle (sağ üst)
3. Arkaplan rengi gradient (mavi → mor)
4. Desktop/Carousel/ klasörüne PNG olarak kaydet"
```

---

## 💡 Pro İpuçları

### Kısayollar

```
"Undo yap" → History'de geri git
"Flatten image" → Tüm katmanları birleştir
"Duplicate layer" → Katmanı kopyala
"Merge visible" → Görünür katmanları birleştir
```

### Batch İşlemlerde Dikkat

```
✅ DOĞRU: "Photos klasöründeki JPG dosyalarını işle"
❌ YANLIŞ: Tüm klasörü tek seferde seçmek (hata riski)
```

### Performans

```
🚀 Büyük dosyalarla çalışırken:
- Önce küçük bir test dosyasıyla dene
- History'yi temizle (memory için)
- Gereksiz katmanları flatten et
```

---

## 🎉 Sonuç

Bu örnekler, Claude + Photoshop entegrasyonuyla neler yapabileceğinizi gösterir.

**Kendi senaryolarınızı oluşturun:**
- Workflow'unuzu analiz edin
- Tekrar eden işlemleri belirleyin
- Claude'a doğal dille anlatın
- Otomasyonun keyfini çıkarın!

**Daha fazla fikir:**
- Instagram filter effects
- Product mockup hazırlama
- Certificate/diploma tasarımları
- Batch color correction
- Logo variations
- Social media templates

**Harika işler çıkarın! 🎨✨**
