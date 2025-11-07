# 🔷 OpenSCAD MCP - Hızlı Başlangıç Rehberi

Claude Desktop üzerinden OpenSCAD ile parametrik 3D modelleme, geometri üretimi ve CAD işlemleri için kullanım kılavuzu.

## 📦 Kurulum

```bash
# Hızlı kurulum
./install_openscad_mcp.sh

# Veya tüm MCP sunucularını kur
./install_all_mcp.sh openscad
```

### OpenSCAD Kurulumu

#### macOS
```bash
brew install openscad
```

#### Ubuntu/Debian
```bash
sudo apt-get install openscad
```

#### Arch Linux
```bash
sudo pacman -S openscad
```

#### Windows
[https://openscad.org/downloads.html](https://openscad.org/downloads.html) adresinden indir ve PATH'e ekle.

## 🚀 Hızlı Başlangıç

### 1. Çalışma Dizinini Ayarla

```
Claude'a: "OpenSCAD için /home/user/3d-models çalışma dizinini ayarla"
```

### 2. Basit Geometri Oluştur

```
Claude'a: "Bir küp geometrisi oluştur ve cube.scad olarak kaydet"
```

### 3. Geometriyi Render Et

```
Claude'a: "cube.scad dosyasını PNG olarak render et"
```

### 4. 3D Baskı için Export

```
Claude'a: "cube.scad dosyasını STL formatına çevir"
```

## 📋 Temel Komutlar ve Örnekler

### Geometrik Şekiller

#### Küp (Cube)
```
Claude'a: "10 birim kenarlı bir küp oluştur"
```

Oluşturulan kod:
```openscad
// Küp
cube([10, 10, 10], center=true);
```

#### Küre (Sphere)
```
Claude'a: "Yarıçapı 15 olan bir küre oluştur"
```

Oluşturulan kod:
```openscad
// Küre
sphere(r=15, $fn=100);
```

#### Silindir (Cylinder)
```
Claude'a: "Yarıçapı 5, yüksekliği 20 olan bir silindir oluştur"
```

Oluşturulan kod:
```openscad
// Silindir
cylinder(h=20, r=5, center=true, $fn=100);
```

#### Koni (Cone)
```
Claude'a: "Taban yarıçapı 8, yüksekliği 15 olan bir koni oluştur"
```

Oluşturulan kod:
```openscad
// Koni
cylinder(h=15, r1=8, r2=0, center=true, $fn=100);
```

#### Torus
```
Claude'a: "Yarıçapı 10 olan bir torus oluştur"
```

Oluşturulan kod:
```openscad
// Torus
rotate_extrude($fn=100)
translate([20, 0, 0])
circle(r=10, $fn=100);
```

### Gelişmiş Modelleme

#### Boolean İşlemleri

**Union (Birleştirme)**
```
Claude'a: "İki küreyi birleştiren bir geometri oluştur"
```

```openscad
union() {
    sphere(r=10, $fn=100);
    translate([12, 0, 0])
    sphere(r=10, $fn=100);
}
```

**Difference (Çıkarma)**
```
Claude'a: "İçi oyulmuş bir küp oluştur"
```

```openscad
difference() {
    cube([20, 20, 20], center=true);
    cube([16, 16, 16], center=true);
}
```

**Intersection (Kesişim)**
```
Claude'a: "Bir küp ile kürenin kesişimini oluştur"
```

```openscad
intersection() {
    cube([20, 20, 20], center=true);
    sphere(r=14, $fn=100);
}
```

#### Transformasyonlar

**Döndürme (Rotate)**
```openscad
rotate([45, 0, 0])
cube([10, 10, 10], center=true);
```

**Ölçekleme (Scale)**
```openscad
scale([2, 1, 1])
sphere(r=10, $fn=100);
```

**Çevirme (Translate)**
```openscad
translate([10, 5, 0])
cylinder(h=20, r=5, center=true, $fn=100);
```

### Parametrik Modelleme

```
Claude'a: "Parametrik bir vida modeli oluştur"
```

```openscad
// Parametrik Vida
module screw(length=20, diameter=6, pitch=2) {
    difference() {
        cylinder(h=length, d=diameter, $fn=50);

        for (i = [0:pitch:length]) {
            translate([0, 0, i])
            rotate([0, 0, i*360/pitch])
            translate([diameter/2, 0, 0])
            sphere(r=pitch/4, $fn=20);
        }
    }
}

screw(length=30, diameter=8, pitch=2.5);
```

## 🎯 Gerçek Dünya Örnekleri

### Örnek 1: Basit Kutu Tasarımı

```
Claude'a: "Kapağı olan 50x50x30 mm boyutunda bir kutu tasarla"
```

```openscad
// Kutu tabanı
module box_base(width, depth, height, thickness) {
    difference() {
        cube([width, depth, height]);
        translate([thickness, thickness, thickness])
        cube([width-2*thickness, depth-2*thickness, height]);
    }
}

// Kutu kapağı
module box_lid(width, depth, thickness) {
    cube([width, depth, thickness]);
}

// Kutu
box_base(50, 50, 30, 2);

// Kapak (yanında)
translate([55, 0, 0])
box_lid(50, 50, 2);
```

### Örnek 2: Dişli Tasarımı

```
Claude'a: "20 dişli basit bir dişli oluştur"
```

```openscad
// Basit dişli
module gear(teeth=20, radius=20, thickness=5) {
    linear_extrude(height=thickness) {
        circle(r=radius, $fn=teeth*4);

        for (i = [0:teeth-1]) {
            rotate([0, 0, i*360/teeth])
            translate([radius, 0, 0])
            circle(r=radius/10, $fn=20);
        }
    }
}

gear(teeth=20, radius=20, thickness=5);
```

### Örnek 3: Vida Deliği Şablonu

```
Claude'a: "M3 vida delikleri olan bir montaj plakası oluştur"
```

```openscad
// Montaj plakası
module mounting_plate(width, height, thickness, hole_diameter, hole_spacing) {
    difference() {
        // Ana plaka
        cube([width, height, thickness]);

        // Köşe delikleri
        for (x = [hole_spacing, width-hole_spacing]) {
            for (y = [hole_spacing, height-hole_spacing]) {
                translate([x, y, -1])
                cylinder(h=thickness+2, d=hole_diameter, $fn=30);
            }
        }
    }
}

mounting_plate(
    width=100,
    height=80,
    thickness=3,
    hole_diameter=3.2,  // M3 vida için
    hole_spacing=10
);
```

## 🔧 İleri Düzey Özellikler

### Dosya İşlemleri

**Dosya Listele**
```
Claude'a: "Tüm SCAD dosyalarını listele"
```

**Dosya Oku**
```
Claude'a: "gear.scad dosyasını oku"
```

**Dosya Yaz**
```
Claude'a: "Bu kodu custom_part.scad olarak kaydet: [kod]"
```

### Render ve Export

**PNG Render**
```
Claude'a: "model.scad dosyasını 1920x1080 boyutunda render et"
```

**STL Export (3D Baskı)**
```
Claude'a: "final_design.scad dosyasını STL formatına çevir"
```

**Batch İşlem**
```
Claude'a: "models/ dizinindeki tüm SCAD dosyalarını STL'e çevir"
```

## 📐 OpenSCAD İpuçları

### Performans

1. **$fn değeri**: Düşük değer hızlı önizleme, yüksek değer kaliteli render
   ```openscad
   // Önizleme için
   sphere(r=10, $fn=20);

   // Son render için
   sphere(r=10, $fn=100);
   ```

2. **Modüler tasarım**: Tekrar kullanılabilir modüller oluştur
   ```openscad
   module my_part() {
       // Kod
   }

   // Tekrar kullan
   my_part();
   translate([20, 0, 0]) my_part();
   ```

### Debug

**Echo ile değer kontrolü**
```openscad
radius = 10;
echo("Radius:", radius);
```

**# ile vurgulama**
```openscad
#sphere(r=10);  // Kırmızı transparan
```

**% ile hayalet görünüm**
```openscad
%cube([20, 20, 20]);  // Gri transparan
```

## 🎓 Öğrenme Kaynakları

### Resmi Dokümantasyon
- [OpenSCAD Cheat Sheet](https://openscad.org/cheatsheet/)
- [OpenSCAD Manual](https://openscad.org/documentation.html)
- [OpenSCAD Tutorial](https://openscad.org/documentation.html#tutorial)

### Topluluk Kaynakları
- [Thingiverse - OpenSCAD Designs](https://www.thingiverse.com/search?q=openscad)
- [OpenSCAD Forum](https://forum.openscad.org/)
- [r/openscad](https://www.reddit.com/r/openscad/)

## 🐛 Sorun Giderme

### OpenSCAD Bulunamıyor

**Kontrol:**
```bash
openscad --version
```

**macOS çözüm:**
```bash
brew install openscad
```

**Linux çözüm:**
```bash
sudo apt-get install openscad  # Ubuntu/Debian
```

### Render Zaman Aşımı

Karmaşık modeller için timeout süresini artırabilirsiniz:

```python
# openscad_mcp_server.py içinde timeout değerini değiştirin
timeout=300  # 5 dakika
```

### MCP Bağlantı Sorunu

1. Claude Desktop'ı tamamen kapatın
2. Config dosyasını kontrol edin
3. Claude Desktop'ı yeniden başlatın
4. Log dosyalarını inceleyin

## 💡 En İyi Uygulamalar

1. **Parametrik düşün**: Sabit değerler yerine değişkenler kullan
2. **Modüler kod yaz**: Tekrar kullanılabilir modüller oluştur
3. **Yorum ekle**: Karmaşık geometrileri açıkla
4. **Git kullan**: SCAD dosyalarını version control'de tut
5. **Test et**: STL export etmeden önce render kontrol et
6. **Optimize et**: Gereksiz yüksek $fn değerlerinden kaçın

## 🎉 Sonraki Adımlar

1. ✅ OpenSCAD kurulumunu tamamla
2. ✅ Basit şekillerle başla
3. ✅ Boolean işlemlerini öğren
4. ✅ Parametrik modeller oluştur
5. ✅ 3D yazıcı için STL export et
6. ✅ Topluluk ile paylaş

**İyi modellemeler! 🚀**
