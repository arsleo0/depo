# 🎬 After Effects MCP - Kullanım Örnekleri

Pratik, gerçek dünya senaryolarıyla After Effects MCP kullanımı.

---

## 📚 İçindekiler

1. [Temel İşlemler](#-temel-i̇şlemler)
2. [YouTube İçerikleri](#-youtube-i̇çerikleri)
3. [Social Media](#-social-media)
4. [Motion Graphics](#-motion-graphics)
5. [Video Editing](#️-video-editing)
6. [Gelişmiş JSX](#-gelişmiş-jsx)

---

## 🎯 Temel İşlemler

### 1. Bağlantı Testi

```
Claude'a sor:
"After Effects bağlantımı kontrol et"
```

**Çıktı:**
```
✅ After Effects bağlantısı başarılı!
Adobe After Effects 2024 24.0
Platform: Darwin
```

---

### 2. Proje Bilgisi

```
Claude'a sor:
"After Effects projem hakkında bilgi ver"
```

**Çıktı:**
```
🎬 After Effects Proje Bilgileri:

📝 Proje: my_project.aep
🎞️ Composition Sayısı: 3
📁 Footage Sayısı: 5

📺 Aktif Composition:
  - İsim: Main Comp
  - Boyut: 1920 x 1080 piksel
  - Süre: 10.00 saniye
  - Frame Rate: 30 fps
  - Layer Sayısı: 4
```

---

### 3. Yeni Composition Oluşturma

```
Claude'a sor:
"'Intro' adında yeni comp oluştur:
- 1920x1080
- 5 saniye
- 30fps"
```

---

### 4. Composition'ları Listeleme

```
Claude'a sor:
"Tüm composition'ları listele"
```

**Çıktı:**
```
🎞️ Compositions:

1. Intro
   📏 1920x1080 | ⏱️ 5.00s | 🎬 30fps
2. Main Scene
   📏 1920x1080 | ⏱️ 15.00s | 🎬 24fps
3. Outro
   📏 1920x1080 | ⏱️ 3.00s | 🎬 30fps
```

---

### 5. Layer Ekleme

**Solid Layer:**
```
"Aktif comp'a kırmızı solid layer ekle, 'Background' adında"
```

**Text Layer:**
```
"Aktif comp'a 'HELLO WORLD' yazısı ekle, 72pt, beyaz renk"
```

---

### 6. Dosya Import

```
"Desktop/video.mp4 dosyasını projeye import et"
```

```
"Desktop/logo.png'yi import et ve aktif comp'a ekle"
```

---

## 🎥 YouTube İçerikleri

### Örnek 1: Basit Intro

```
Claude'a sor:
"YouTube intro oluştur:
1. 'YouTube Intro' comp oluştur (1920x1080, 5s, 30fps)
2. Mavi solid background ekle (#0066FF)
3. 'TECH CHANNEL' yazısı ekle (96pt, beyaz, ortada)
4. Yazıya fade-in animasyonu ekle (2 saniye)
5. Desktop/intro.mov olarak render et"
```

**Sonuç:** 5 saniyelik intro videosu hazır!

---

### Örnek 2: Subscribe Butonu Animasyonu

```
Claude'a sor:
"Subscribe button animasyonu oluştur:
1. 'Subscribe Anim' comp oluştur (400x400, 3s, 60fps)
2. Kırmızı solid circle ekle (YouTube kırmızısı #FF0000)
3. 'SUBSCRIBE' yazısı ekle (beyaz, bold)
4. Scale animasyonu ekle (pulse effect):
   - 0s: scale 100%
   - 0.5s: scale 110%
   - 1s: scale 100%
5. PNG sequence olarak Desktop/subscribe/ klasörüne render et"
```

---

### Örnek 3: Lower Third (Alt Yazı Bandı)

```
Claude'a sor:
"Lower third oluştur:
- Text: 'Ahmet Yılmaz - Yazılım Geliştirici'
- Konum: Sol alt köşe
- Slide-in animasyon (soldan sağa, 0.5s)
- 3 saniye ekranda kal, sonra slide-out
- Render et: Desktop/lower_third.mov"
```

---

### Örnek 4: End Screen Template

```
Claude'a sor:
"YouTube end screen template oluştur (1920x1080, 20s):
1. Siyah background
2. 'Beğenmeyi Unutmayın!' yazısı (üstte, fade in)
3. İki boş alan (thumbnail placeholder) - sol ve sağda
4. 'ABONE OL' butonu (ortada, pulse animasyon)
5. Render et: Desktop/end_screen.mov"
```

---

## 📱 Social Media

### Örnek 5: Instagram Story

```
Claude'a sor:
"Instagram story oluştur:
1. Comp: 1080x1920 (story format), 15s, 30fps
2. Gradient background (pembe → mor)
3. 'YENİ ÜRÜN!' yazısı (üstte, büyük, fade-in)
4. 'Kaydır' yazısı (altta, küçük, sonsuz pulse)
5. Render: Desktop/story.mp4"
```

---

### Örnek 6: TikTok Intro

```
Claude'a sor:
"TikTok intro hazırla:
- Format: 1080x1920, 3s, 30fps
- Logo ortada (Desktop/logo.png import et)
- Logo reveal animasyonu (rotation + scale)
- Glow effect ekle
- Render: Desktop/tiktok_intro.mov"
```

---

### Örnek 7: Facebook Ad

```
Claude'a sor:
"Facebook ad video oluştur:
1. Comp: 1080x1080 (square), 15s, 30fps
2. Ürün görseli import et (Desktop/product.jpg)
3. '%50 İNDİRİM!' yazısı ekle (kırmızı, büyük, üstte)
4. Yazıya bounce animasyon ekle
5. 'Şimdi Al' butonu ekle (altta, pulse)
6. H.264 render: Desktop/fb_ad.mp4"
```

---

## 🎨 Motion Graphics

### Örnek 8: Logo Reveal

```
Claude'a sor:
"Profesyonel logo reveal oluştur:
1. Comp oluştur: 'Logo Reveal', 1920x1080, 5s, 60fps
2. Logo import et: Desktop/logo.png
3. Animasyon:
   - 0s: scale 0%, rotation 0°, opacity 0%
   - 2s: scale 120%, rotation 360°, opacity 100%
   - 3s: scale 100% (settle down)
4. Glow effect ekle (intensity artan)
5. Render: Desktop/logo_reveal.mov"
```

---

### Örnek 9: Text Kinetic Typography

```
Claude'a sor:
"Kinetic typography animasyonu yap:
- Comp: 1920x1080, 10s, 60fps
- Text: 'CREATE. INSPIRE. INNOVATE.'
- Her kelime ayrı layer
- Kelimeler sırayla gelsin (stagger effect)
- Position, scale, rotation animasyonları
- Drop shadow effect'leri ekle"
```

---

### Örnek 10: Particle Effect (JSX ile)

```
Claude'a sor:
"Şu JSX kodunu çalıştır (particle effect simülasyonu):

var comp = app.project.activeItem;
var particleCount = 50;

for (var i = 0; i < particleCount; i++) {
    var particle = comp.layers.addSolid([1, 1, 1], 'Particle ' + i, 10, 10, 1);

    var startX = comp.width / 2;
    var startY = comp.height / 2;
    var endX = Math.random() * comp.width;
    var endY = Math.random() * comp.height;

    var pos = particle.property('Position');
    pos.setValueAtTime(0, [startX, startY]);
    pos.setValueAtTime(2, [endX, endY]);

    var opacity = particle.property('Opacity');
    opacity.setValueAtTime(0, 100);
    opacity.setValueAtTime(2, 0);
}

'50 particle oluşturuldu ve animate edildi';
"
```

---

## 🎞️ Video Editing

### Örnek 11: Video Montaj

```
Claude'a sor:
"Video montaj oluştur:
1. Desktop/Videos/ klasöründeki tüm MP4'leri import et
2. 'Montage' comp oluştur (1920x1080, 60s, 30fps)
3. Tüm videoları sırayla timeline'a ekle (her biri 5s)
4. Her video arası 0.5s fade transition
5. Background müzik ekle: Desktop/music.mp3
6. H.264 render: Desktop/montage.mp4"
```

---

### Örnek 12: Color Grading

```
Claude'a sor:
"Video'ya color grading uygula:
1. Desktop/raw_footage.mp4'ü import et ve comp'a ekle
2. Brightness & Contrast effect ekle (contrast +20)
3. Hue/Saturation effect ekle (saturation +15)
4. Glow effect ekle (subtle)
5. Render: Desktop/graded_footage.mov"
```

---

### Örnek 13: Slow Motion

```
Claude'a sor:
"Slow motion effect oluştur:
1. Desktop/action_clip.mp4 import et
2. Yeni comp oluştur (video boyutunda, 10s, 60fps)
3. Video'yu comp'a ekle
4. Time remapping uygula (2x slow motion)
5. Render: Desktop/slow_motion.mov"
```

---

## 🎬 Animasyon Şablonları

### Örnek 14: Fade In Animasyonu

```
Claude'a sor:
"'text_fade_in' şablonuyla 'WELCOME' animasyonu oluştur, 3 saniye"
```

**Otomatik olarak:**
- Text layer oluşturulur
- Opacity keyframe'leri eklenir (0% → 100%)

---

### Örnek 15: Logo Reveal Şablonu

```
"'logo_reveal' şablonuyla 'MY BRAND' logo reveal'ı oluştur, 4 saniye"
```

**Otomatik olarak:**
- Scale animasyonu (0% → 100%)

---

### Örnek 16: Lower Third Şablonu

```
"'lower_third' şablonuyla 'John Doe - CEO' alt yazısı oluştur"
```

**Otomatik olarak:**
- Background bar
- Text layer
- Slide-in animasyon

---

## 🚀 Gelişmiş JSX

### Örnek 17: Batch Effect Uygulama

```
Claude'a sor:
"Şu JSX'i çalıştır (tüm layer'lara glow ekle):

var comp = app.project.activeItem;
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    var glow = layer.property('Effects').addProperty('Glow');
    glow.property('Glow Threshold').setValue(50);
    glow.property('Glow Radius').setValue(20);
}
'Tüm layer'lara glow effect eklendi';
"
```

---

### Örnek 18: Random Position Animasyon

```
"Şu JSX'i çalıştır:

var comp = app.project.activeItem;
for (var i = 1; i <= comp.numLayers; i++) {
    var layer = comp.layer(i);
    var pos = layer.property('Position');

    for (var t = 0; t < comp.duration; t += 0.5) {
        var randomX = Math.random() * comp.width;
        var randomY = Math.random() * comp.height;
        pos.setValueAtTime(t, [randomX, randomY]);
    }
}
'Random position animasyonları eklendi';
"
```

---

### Örnek 19: Expression Ekleme

```
"Şu JSX'i çalıştır (wiggle expression ekle):

var comp = app.project.activeItem;
var layer = comp.layer(1);
var pos = layer.property('Position');
pos.expression = 'wiggle(5, 50)';
'Wiggle expression eklendi';
"
```

---

## 🎯 Kompleks Workflow'lar

### Örnek 20: Tam YouTube Video Template

```
Claude'a sor:
"YouTube video template seti oluştur:

1. INTRO (5s):
   - Logo reveal
   - Channel name fade-in
   - Subscribe reminder

2. MAIN CONTENT (30s):
   - Lower third placeholder
   - Text overlay hazır
   - Transition points

3. OUTRO (10s):
   - End screen
   - Subscribe button
   - Social media links

Hepsini ayrı comp'larda oluştur ve master comp'ta birleştir.
Render: Desktop/youtube_template.mov"
```

---

### Örnek 21: Kurumsal Video Paketi

```
"Kurumsal video paketi hazırla:
1. Company intro (10s) - logo + slogan
2. Product showcase template (20s)
3. Testimonial lower thirds (3 adet)
4. Call-to-action end screen (5s)

Tüm comp'ları Desktop/Corporate_Package/ klasörüne H.264 render et"
```

---

### Örnek 22: Instagram Carousel Set

```
"Instagram için 10 slide carousel oluştur:
- Her slide: 1080x1080, 3s
- Arkaplan: Gradient (mavi → yeşil)
- Text: 'İPUCU 1/10', 'İPUCU 2/10', ... 'İPUCU 10/10'
- Her slide fade transition ile
- Tüm carousel'i tek video olarak render et (30s total)"
```

---

## 💡 Pro İpuçları

### Batch Rendering

```
"Tüm composition'ları Desktop/Renders/ klasörüne render et, H.264 format"
```

### Comp Duplicate

```
"'Main Comp' composition'ını duplicate et, 'Main Comp v2' adıyla"
```

### Layer Organizing

```
"Tüm text layer'ları 'TEXTS' klasörüne, solid layer'ları 'BACKGROUNDS' klasörüne organize et"
```

### Preset Uygulama

```
"Tüm layer'lara 'Fade In' animation preset'ini uygula"
```

---

## 🎓 Öğrenme Yolu

### Başlangıç Seviyesi

1. Composition oluşturma
2. Text ve solid layer ekleme
3. Basit animasyonlar (opacity, position)
4. Render etme

### Orta Seviye

5. Effect'ler kullanma
6. Keyframe animasyonları
7. Footage import ve placement
8. Template'leri özelleştirme

### İleri Seviye

9. JSX scriptleri yazma
10. Expression'lar kullanma
11. Karmaşık animasyon zincirleri
12. Batch automation

---

## 🎉 Sonuç

After Effects MCP ile:
- ⚡ Hızlı workflow
- 🤖 Otomasyon
- 🎨 Yaratıcılık odaklı
- 💬 Doğal dil kontrolü

**Harika motion graphics oluşturun! 🎬✨**
