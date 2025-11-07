# Neural Network Simülatörü

Basit bir feedforward neural network simülatörü. Sigmoid aktivasyon fonksiyonu ve backpropagation algoritması kullanır.

## Özellikler

- ✅ Feedforward neural network
- ✅ Sigmoid aktivasyon fonksiyonu
- ✅ Backpropagation ile öğrenme
- ✅ Özelleştirilebilir katman boyutları
- ✅ Ayarlanabilir öğrenme oranı
- ✅ XOR problemi ve sınıflandırma örnekleri

## Kullanım

### Temel Kullanım

```python
from neural_network_simulator import NeuralNetwork
import numpy as np

# Neural network oluştur
# 2 giriş nöronu, 4 gizli nöron, 1 çıkış nöronu
nn = NeuralNetwork(input_size=2, hidden_size=4, output_size=1, learning_rate=0.5)

# Eğitim verileri (XOR problemi)
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# Eğitim
nn.train(X, y, epochs=10000)

# Tahmin
predictions = nn.predict(X)
print(predictions)
```

### Demo Çalıştırma

```bash
python neural_network_demo.py
```

Demo programı iki örnek içerir:
1. **XOR Problemi**: Klasik XOR mantıksal kapısını öğrenir
2. **Basit Sınıflandırma**: Sayıların 0.5'ten büyük mü küçük mü olduğunu öğrenir

## API Referansı

### NeuralNetwork Sınıfı

#### `__init__(input_size, hidden_size, output_size, learning_rate=0.5)`
Neural network oluşturur.

**Parametreler:**
- `input_size` (int): Giriş katmanı nöron sayısı
- `hidden_size` (int): Gizli katman nöron sayısı
- `output_size` (int): Çıkış katmanı nöron sayısı
- `learning_rate` (float): Öğrenme oranı (varsayılan: 0.5)

#### `train(X, y, epochs=10000, verbose=True)`
Neural network'ü eğitir.

**Parametreler:**
- `X` (np.ndarray): Eğitim giriş verileri
- `y` (np.ndarray): Eğitim etiketleri
- `epochs` (int): Epoch sayısı
- `verbose` (bool): İlerleme göster

#### `predict(X)`
Tahmin yapar.

**Parametreler:**
- `X` (np.ndarray): Giriş verileri

**Döndürür:**
- np.ndarray: Tahmin sonuçları

#### `get_info()`
Network hakkında bilgi döndürür.

**Döndürür:**
- dict: Network bilgileri (katman boyutları, ağırlık şekilleri, vb.)

## Örnek Çıktı

```
==============================================================
XOR PROBLEMİ ÇÖZÜMÜ
==============================================================

Eğitim Verileri:
Giriş (X):
[[0 0]
 [0 1]
 [1 0]
 [1 1]]

Beklenen Çıkış (y):
[[0]
 [1]
 [1]
 [0]]

Eğitim Başlıyor...
------------------------------------------------------------
Epoch 0, Loss: 0.263949
Epoch 1000, Loss: 0.004623
Epoch 2000, Loss: 0.002143
Epoch 3000, Loss: 0.001315
Epoch 4000, Loss: 0.000936
Epoch 5000, Loss: 0.000719
Epoch 6000, Loss: 0.000579
Epoch 7000, Loss: 0.000483
Epoch 8000, Loss: 0.000413
Epoch 9000, Loss: 0.000361
------------------------------------------------------------

Eğitim Sonrası Tahminler:
  [0 0] -> Tahmin: 0.0183 (~0), Beklenen: 0 ✓
  [0 1] -> Tahmin: 0.9812 (~1), Beklenen: 1 ✓
  [1 0] -> Tahmin: 0.9813 (~1), Beklenen: 1 ✓
  [1 1] -> Tahmin: 0.0199 (~0), Beklenen: 0 ✓

Doğruluk: 100.00%
```

## Gereksinimler

```
numpy>=1.19.0
```

## Kurulum

1. NumPy'ı yükleyin:
```bash
pip install numpy
```

2. Simülatörü kullanmaya başlayın:
```bash
python neural_network_demo.py
```

## Mimari

```
Giriş Katmanı → Gizli Katman → Çıkış Katmanı
    (input)       (hidden)        (output)
                     ↓
              Sigmoid Aktivasyon
                     ↓
              Backpropagation
```

## Limitasyonlar

- Şu anda sadece bir gizli katman desteklenir
- Sadece sigmoid aktivasyon fonksiyonu mevcuttur
- Batch processing desteklenmez (tüm veri tek seferde işlenir)
- Sadece tam bağlantılı (fully connected) katmanlar vardır

## Gelecek Geliştirmeler

- [ ] Çoklu gizli katman desteği
- [ ] ReLU, Tanh gibi farklı aktivasyon fonksiyonları
- [ ] Mini-batch gradient descent
- [ ] Dropout regularizasyonu
- [ ] Farklı optimizasyon algoritmaları (Adam, RMSprop)
- [ ] Model kaydetme/yükleme

## Lisans

Bu proje MIT lisansı altında dağıtılmaktadır.
