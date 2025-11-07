# 🎨 TripoSR MCP Server - Hızlı Başlangıç

Görüntüden 3D model oluşturmak için TripoSR AI'ı Claude Desktop ile kullanın!

---

## ⚡ Hızlı Kurulum

### Otomatik Kurulum (Önerilen)

```bash
# Tek komutla kur
./install_triposr_mcp.sh
```

### Manuel Kurulum

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements-triposr.txt

# 2. PyTorch yükle (CUDA varsa)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Veya CPU için
pip install torch torchvision

# 3. TripoSR'ı GitHub'dan yükle
git clone https://github.com/VAST-AI-Research/TripoSR.git ~/TripoSR
cd ~/TripoSR
pip install -e .

# 4. Server'ı test et
python3 triposr_mcp_server.py

# Görmek istediğiniz:
# [TRIPOSR-MCP] INFO: TripoSR MCP Server başlatılıyor... (Device: cuda)
# [TRIPOSR-MCP] INFO: TripoSR MCP Server hazır! 🚀
```

---

## ⚙️ Claude Desktop Yapılandırması

### macOS

```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Linux

```bash
nano ~/.config/Claude/claude_desktop_config.json
```

### Windows

```
%APPDATA%\Claude\claude_desktop_config.json
```

**Config içeriği:**

```json
{
  "mcpServers": {
    "triposr": {
      "command": "python3",
      "args": ["/TAM/YOL/triposr_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    }
  }
}
```

**Mevcut server'larınız varsa (Photoshop, Godot, After Effects):**

```json
{
  "mcpServers": {
    "godot": {
      "command": "python3",
      "args": ["/home/user/depo/godot_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    },
    "photoshop": {
      "command": "python3",
      "args": ["/home/user/depo/photoshop_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    },
    "aftereffects": {
      "command": "python3",
      "args": ["/home/user/depo/aftereffects_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    },
    "triposr": {
      "command": "python3",
      "args": ["/home/user/depo/triposr_mcp_server.py"],
      "env": {"PYTHONUNBUFFERED": "1"}
    }
  }
}
```

---

## ✅ İlk Test

1. **Claude Desktop'ı yeniden başlatın** (tamamen kapatıp açın)

2. **Claude'da yazın:**

```
TripoSR durumunu kontrol et
```

**Beklenen çıktı:**

```
✅ TripoSR MCP Server: Çalışıyor
🖥️ Device: cuda (veya cpu)
📦 Model Yüklü: Hayır (ilk kullanımda yüklenecek)
📁 Çıktı Dizini: /Users/name/Desktop/triposr_outputs
🔧 PyTorch: 2.1.0
🎮 CUDA Mevcut: Evet ✅
🎮 GPU: NVIDIA GeForce RTX 3080
💾 GPU Bellek: 10.0 GB
```

---

## 🎨 İlk 3D Modelinizi Oluşturun

### Adım 1: Bir görüntü hazırlayın

Herhangi bir nesne fotoğrafı işe yarar. En iyi sonuçlar için:

- ✅ Tek bir nesne (kupa, sandalye, oyuncak, vb.)
- ✅ Düz veya basit arka plan
- ✅ İyi ışıklandırma
- ✅ Nesne net ve tam görünür
- ❌ Çok karmaşık sahneler
- ❌ Çok sayıda nesne

### Adım 2: 3D model oluşturun

```
Claude'da yazın:
"Desktop/chair.jpg görüntüsünden 3D model oluştur, adı chair_model olsun"
```

**Ne olacak:**

1. TripoSR modeli yüklenecek (ilk kez ~300MB, 2-3 dakika)
2. Görüntü işlenecek
3. Arka plan otomatik kaldırılacak
4. AI 3D model oluşturacak (30-60 saniye)
5. `.obj` ve `.glb` formatlarında kaydedilecek

**Çıktı:**

```
✅ 3D model başarıyla oluşturuldu!

📁 OBJ: /Users/name/Desktop/triposr_outputs/chair_model.obj
📁 GLB: /Users/name/Desktop/triposr_outputs/chair_model.glb

🎨 Kaynak Görüntü: /Users/name/Desktop/chair.jpg
🔧 Device: cuda
🖼️ Arka Plan Kaldırıldı: Evet

💡 İpucu: Bu modeli Blender, Unity, Godot gibi 3D yazılımlarda kullanabilirsiniz!
```

---

## 📚 Kullanım Örnekleri

### Örnek 1: Tek görüntüden model

```
"Desktop/mug.jpg'den 3D model oluştur"
```

### Örnek 2: Arka planı koruyarak

```
"Desktop/statue.png'den 3D model oluştur, arka planı kaldırma"
```

### Örnek 3: Toplu işlem

```
"Desktop/objects klasöründeki tüm jpg görüntülerden 3D modeller oluştur"
```

### Örnek 4: Çıktı dizinini değiştir

```
"3D model çıktı dizinini /Users/name/3D_Models olarak ayarla"
```

### Örnek 5: Oluşturulan modelleri listele

```
"Oluşturduğum 3D modelleri listele"
```

---

## 🎯 Gelişmiş Kullanım

### Python API ile Kullanım

```python
# TripoSR'ı doğrudan Python'da kullanın
from tsr.system import TSR
from tsr.utils import remove_background, resize_foreground
from PIL import Image
import torch

# Model yükle
device = "cuda" if torch.cuda.is_available() else "cpu"
model = TSR.from_pretrained(
    "stabilityai/TripoSR",
    config_name="config.yaml",
    weight_name="model.ckpt",
)
model.to(device)

# Görüntü yükle ve işle
image = Image.open("input.jpg")
image = remove_background(image)
image = resize_foreground(image, 0.85)

# 3D model oluştur
scene_codes = model([image], device=device)
mesh = model.extract_mesh(scene_codes[0])
mesh.export("output.obj")
```

### Batch Processing

```bash
# Birden fazla görüntüyü işle
python3 << EOF
import asyncio
from triposr_mcp_server import TripoSRMCPServer

async def main():
    server = TripoSRMCPServer()
    images = [
        "/path/to/image1.jpg",
        "/path/to/image2.jpg",
        "/path/to/image3.jpg",
    ]
    result = await server._batch_generate_3d(images, remove_bg=True)
    print(result[0].text)

asyncio.run(main())
EOF
```

---

## 🛠️ Performans İpuçları

### GPU Kullanımı

- **NVIDIA GPU önerilen** - 30-60 saniye/model
- CPU ile 3-5 dakika/model
- Minimum 4GB VRAM (8GB+ önerilen)

### Görüntü Kalitesi

- **Çözünürlük:** 512x512 ile 1024x1024 arası ideal
- **Format:** PNG, JPG, WebP desteklenir
- **Arka Plan:** Düz renk en iyi sonucu verir

### Bellek Optimizasyonu

```python
# Düşük VRAM için
import torch
torch.cuda.empty_cache()  # Her model sonrası

# Batch işlerde
# Her 5-10 modelde bir cache temizle
```

---

## 🔧 Sorun Giderme

### ❌ "CUDA out of memory"

**Çözüm:**

```bash
# CPU moduna geç
export CUDA_VISIBLE_DEVICES=""
python3 triposr_mcp_server.py
```

### ❌ "TripoSR bulunamadı"

**Çözüm:**

```bash
# TripoSR'ı GitHub'dan yükle
git clone https://github.com/VAST-AI-Research/TripoSR.git ~/TripoSR
cd ~/TripoSR
pip install -e .
```

### ❌ "Model yüklenemiyor"

**Çözüm:**

```bash
# HuggingFace önbelleğini temizle
rm -rf ~/.cache/huggingface/hub/models--stabilityai--TripoSR
# Tekrar dene
```

### ❌ "Görüntü okunamıyor"

**Çözüm:**

- Dosya yolunun doğru olduğundan emin olun
- Görüntü formatının desteklendiğini kontrol edin (PNG, JPG)
- Dosya izinlerini kontrol edin

---

## 🎨 3D Modelleri Kullanma

### Blender'da Açma

```bash
# Blender'ı aç
File → Import → Wavefront (.obj) veya glTF 2.0 (.glb)
# Modelinizi seçin
```

### Unity'de Kullanma

```bash
# Unity Project'te
Assets klasörüne .glb dosyasını sürükleyin
# Otomatik import edilecek
```

### Godot'ta Kullanma

```bash
# Godot Editor'de
res:// klasörüne .glb dosyasını kopyalayın
# Sahneye ekleyin
```

### Three.js ile Web'de

```javascript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load('model.glb', (gltf) => {
  scene.add(gltf.scene);
});
```

---

## 📊 Kullanım Senaryoları

### 🎮 Oyun Geliştirme

```
1. Gerçek nesne fotoğrafı çek
2. TripoSR ile 3D'ye çevir
3. Blender'da düzenle/optimize et
4. Godot/Unity'e import et
```

### 🛍️ E-Ticaret

```
1. Ürün fotoğraflarını çek
2. Toplu 3D model oluştur
3. AR uygulamasında kullan
```

### 🎨 3D Sanat

```
1. Konsept sketch çiz
2. TripoSR ile hızlı 3D prototip
3. Blender'da detaylandır
```

### 🏛️ Kültürel Koruma

```
1. Tarihi eserler fotoğrafla
2. 3D model oluştur
3. Dijital arşivle
```

---

## 🚀 Workflow Örnekleri

### Photoshop → TripoSR → Godot

```
1. Photoshop'ta nesne tasarla:
   "Yeni doküman oluştur (1024x1024)"
   "Mavi bir robot karakteri çiz"
   "PNG olarak kaydet: Desktop/robot.png"

2. TripoSR ile 3D'ye çevir:
   "Desktop/robot.png'den 3D model oluştur"

3. Godot'a import et:
   "robot_3d.glb'yi Godot projeme kopyala"
```

### After Effects → TripoSR

```
1. After Effects'te render:
   "Karakter animasyonunun frame 100'ünü PNG olarak kaydet"

2. 3D model oluştur:
   "Kaydedilen frame'den 3D model oluştur"

3. Blender'da detaylandır
```

---

## 📈 İstatistikler

| Metrik | Değer |
|--------|-------|
| **Araç Sayısı** | 5 |
| **Ortalama İşlem Süresi** | 30-60 saniye (GPU) |
| **Desteklenen Formatlar** | OBJ, GLB |
| **Model Boyutu** | ~300MB |
| **Çıktı Çözünürlüğü** | Yüksek kalite mesh |

---

## 🎓 Kaynaklar

- **TripoSR GitHub:** https://github.com/VAST-AI-Research/TripoSR
- **TripoSR Paper:** https://stability.ai/research/triposr
- **MCP Protocol:** https://modelcontextprotocol.io/
- **Claude Desktop:** https://claude.ai/desktop

---

## 💡 Pro İpuçları

1. **En İyi Sonuçlar:**
   - Düz arka plan kullanın
   - Nesneyi merkezde tutun
   - İyi ışıklandırma önemli

2. **Hızlı Workflow:**
   - Batch processing kullanın
   - GPU varsa mutlaka kullanın
   - Çıktı dizinini organize edin

3. **Post-Processing:**
   - Blender'da UV mapping yapın
   - Texture ekleyin
   - Polygon sayısını optimize edin

4. **Sorun Çözme:**
   - İlk çalıştırmada model indirilir
   - VRAM doluysa diğer uygulamaları kapatın
   - CPU modunda sabırlı olun

---

## 🎉 Başarılar!

Artık Claude Desktop ile TripoSR kullanarak görüntülerden 3D model oluşturabilirsiniz!

**Hızlı Test:**

```bash
./install_triposr_mcp.sh
# Claude Desktop'ı yeniden başlat
# "TripoSR durumunu kontrol et" yaz
```

**Harika 3D modeller oluşturun! 🚀✨**

---

## 🔗 Diğer MCP Server'lar

Bu repository'de başka neler var:

- **🎮 Godot:** Oyun geliştirme
- **🎨 Photoshop:** Görüntü düzenleme
- **🎬 After Effects:** Video ve animasyon
- **🔷 TripoSR:** 3D model oluşturma (bu dokümantasyon)

**Hepsini birden kullanın ve tam yaratıcılık gücüne ulaşın!**
