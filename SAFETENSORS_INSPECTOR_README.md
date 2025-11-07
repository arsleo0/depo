# 🔍 Safetensors Model Inspector

LLM modellerinin `.safetensors` dosyalarını analiz eden Python aracı. Model mimarisini, katman sayısını, parametre sayısını ve diğer detaylı bilgileri görüntüler.

## ✨ Özellikler

- 📊 Model mimarisini otomatik algılama (GPT-style, BERT-style, CNN, RNN vb.)
- 📚 Transformer katman sayısını belirleme
- 🔢 Toplam parametre sayısını hesaplama
- 📐 Model boyutlarını gösterme (hidden_size, vocab_size vb.)
- 🧱 Katman istatistiklerini çıkarma (attention, MLP, embedding vb.)
- 📋 Metadata bilgilerini görüntüleme
- 💾 Analiz sonuçlarını JSON'a aktarma
- 🎨 Renkli ve düzenli terminal çıktısı

## 📦 Kurulum

### Gereksinimler

Python 3.7 veya üzeri gereklidir.

### Bağımlılıkları Yükleme

```bash
pip install -r requirements-safetensors.txt
```

veya manuel olarak:

```bash
pip install safetensors torch
```

## 🚀 Kullanım

### Temel Kullanım

Model dosyanızı analiz etmek için:

```bash
python safetensors_inspector.py model.safetensors
```

### Detaylı Analiz

Tüm tensor bilgilerini görmek için:

```bash
python safetensors_inspector.py model.safetensors --detailed
```

veya kısa hali:

```bash
python safetensors_inspector.py model.safetensors -d
```

### JSON'a Aktarma

Analiz sonuçlarını JSON dosyasına kaydetmek için:

```bash
python safetensors_inspector.py model.safetensors --export analysis.json
```

veya kısa hali:

```bash
python safetensors_inspector.py model.safetensors -e analysis.json
```

### Kombine Kullanım

```bash
python safetensors_inspector.py model.safetensors -d -e analysis.json
```

## 📊 Örnek Çıktı

```
================================================================================
📊 SAFETENSORS MODEL ANALİZİ
================================================================================

📁 Dosya: llama-2-7b.safetensors
📏 Dosya Boyutu: 13.48 GB

🏗️  Model Mimarisi: Decoder-only Transformer (GPT-style)
📚 Transformer Katman Sayısı: 32
🔢 Toplam Parametre: 6,738,415,616 (6.74B)

📐 Model Boyutları:
   • vocab_size: 32,000
   • hidden_size: 4,096

🧱 Katman İstatistikleri:
   • attention: 96 katman
   • mlp: 64 katman
   • normalization: 33 katman
   • embedding: 1 katman
   • output: 1 katman

📋 Metadata:
   • format: pt
   • model_type: llama
```

## 🔧 Komut Satırı Seçenekleri

| Parametre | Kısa | Açıklama |
|-----------|------|----------|
| `file` | - | Analiz edilecek `.safetensors` dosyası (zorunlu) |
| `--detailed` | `-d` | Detaylı tensor bilgilerini göster |
| `--export FILE` | `-e FILE` | Analiz sonuçlarını JSON dosyasına aktar |

## 📝 Algılanan Model Mimarileri

Araç aşağıdaki model mimarilerini otomatik olarak algılayabilir:

- **Decoder-only Transformer (GPT-style)**: GPT, LLaMA, Mistral gibi modeller
- **Encoder-only Transformer (BERT-style)**: BERT, RoBERTa gibi modeller
- **Encoder-Decoder Transformer**: T5, BART gibi modeller
- **Convolutional Neural Network (CNN)**: ResNet, VGG gibi modeller
- **Recurrent Neural Network**: LSTM, GRU gibi modeller

## 🎯 Kullanım Senaryoları

### 1. Model Bilgilerini Öğrenme

İndirdiğiniz bir modelin özelliklerini öğrenmek için:

```bash
python safetensors_inspector.py ~/models/llama-2-7b.safetensors
```

### 2. Farklı Modelleri Karşılaştırma

Birden fazla modeli analiz edip JSON'a aktararak karşılaştırın:

```bash
python safetensors_inspector.py model1.safetensors -e model1.json
python safetensors_inspector.py model2.safetensors -e model2.json
```

### 3. Model Dökümantasyonu Oluşturma

Detaylı analiz çıktısını bir dosyaya kaydedin:

```bash
python safetensors_inspector.py model.safetensors -d > model_analysis.txt
```

## 🛠️ Teknik Detaylar

### Katman Tipleri

Araç tensor isimlerine bakarak aşağıdaki katman tiplerini tanır:

- **attention**: Attention mekanizması katmanları
- **mlp**: Multi-Layer Perceptron (Feed-Forward) katmanları
- **embedding**: Token ve pozisyon embedding'leri
- **normalization**: LayerNorm, RMSNorm vb. normalleştime katmanları
- **output**: Çıktı katmanları (lm_head vb.)
- **convolution**: Konvolüsyon katmanları

### Parametre Hesaplama

Toplam parametre sayısı, modeldeki tüm tensor'ların eleman sayılarının toplamıdır. Bu, modelin hafıza gereksinimleri ve hesaplama karmaşıklığı hakkında bilgi verir.

### Katman Sayısı Tespiti

Transformer katman sayısı, tensor isimlerindeki `layers.N`, `layer.N`, `h.N`, `block.N` gibi patternlere bakılarak belirlenir.

## 🐛 Sorun Giderme

### "safetensors kütüphanesi bulunamadı" Hatası

```bash
pip install safetensors
```

### "Dosya bulunamadı" Hatası

Dosya yolunun doğru olduğundan emin olun. Mutlak veya göreceli yol kullanabilirsiniz:

```bash
python safetensors_inspector.py /tam/yol/model.safetensors
python safetensors_inspector.py ./models/model.safetensors
```

### Büyük Modeller İçin Hafıza Sorunu

Araç tensörlerin sadece metadata'sını yükler, tüm ağırlıkları bellege almaz. Bu nedenle büyük modeller bile düşük RAM ile analiz edilebilir.

## 📚 Desteklenen Dosya Formatları

- `.safetensors` - Safetensors formatındaki model dosyaları
- Tek dosya veya sharded (parçalı) modeller desteklenir

## 🤝 Katkıda Bulunma

Önerileriniz ve katkılarınız için pull request açabilirsiniz.

## 📄 Lisans

MIT License

## 🔗 İlgili Projeler

- [Safetensors](https://github.com/huggingface/safetensors) - Resmi Safetensors kütüphanesi
- [Hugging Face Hub](https://huggingface.co/models) - LLM modellerini indirin

## 💡 İpuçları

1. **Büyük modeller için**: Detaylı mod çok fazla çıktı üretebilir, önce normal modda deneyin
2. **JSON çıktısı**: Programatik analiz için JSON çıktısını kullanın
3. **Wildcard kullanımı**: Birden fazla model dosyası için shell script yazabilirsiniz

```bash
#!/bin/bash
for model in models/*.safetensors; do
    echo "Analyzing: $model"
    python safetensors_inspector.py "$model" -e "${model%.safetensors}.json"
done
```

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

---

**Not**: Bu araç sadece model yapısını analiz eder, model ağırlıklarını değiştirmez veya modeli çalıştırmaz.
