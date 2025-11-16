# Neural Network Simülatörü - Windows Kurulum Rehberi

## Adım 1: NumPy'ı Yükleyin

Visual Studio Code terminalinde aşağıdaki komutlardan birini çalıştırın:

### Seçenek A: Virtual Environment Kullanıyorsanız (.venv)

```powershell
# Virtual environment'ı aktifleştirin
.\.venv\Scripts\Activate.ps1

# NumPy'ı yükleyin
pip install numpy

# veya tüm gereksinimleri yükleyin
pip install -r requirements.txt
```

### Seçenek B: Global Python Kullanıyorsanız

```powershell
# NumPy'ı yükleyin
pip install numpy

# veya tüm gereksinimleri yükleyin
pip install -r requirements.txt
```

## Adım 2: Demo'yu Çalıştırın

**ÖNEMLİ:** `neural_network_simulator.py` değil, `neural_network_demo.py` dosyasını çalıştırın!

```powershell
# Virtual environment ile
.\.venv\Scripts\python.exe neural_network_demo.py

# veya global Python ile
python neural_network_demo.py
```

## Hata Çözümleri

### "No module named 'numpy'" Hatası

```powershell
# Virtual environment'ta mısınız kontrol edin
# Terminal başında (.venv) görünüyor mu?

# Yoksa aktifleştirin:
.\.venv\Scripts\Activate.ps1

# NumPy'ı yükleyin:
pip install numpy
```

### PowerShell Script Çalıştırma Hatası

Eğer "cannot be loaded because running scripts is disabled" hatası alırsanız:

```powershell
# Execution policy'yi değiştirin (Yönetici olarak)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### VS Code'da Python Interpreter Seçimi

1. `Ctrl + Shift + P` tuşlarına basın
2. "Python: Select Interpreter" yazın
3. `.venv` içindeki Python'u seçin

## Örnek Çıktı

Başarılı bir çalıştırma şöyle görünecektir:

```
╔==========================================================╗
║              NEURAL NETWORK SİMÜLATÖRÜ DEMO              ║
╚==========================================================╝

============================================================
XOR PROBLEMİ ÇÖZÜMÜ
============================================================

Eğitim Verileri:
Giriş (X):
[[0 0]
 [0 1]
 [1 0]
 [1 1]]

Eğitim Başlıyor...
Epoch 0, Loss: 0.256305
Epoch 1000, Loss: 0.010188
...
Doğruluk: 100.00%
```

## Hızlı Başlangıç (Tek Komut)

```powershell
# Tüm adımları birlikte yapın
.\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; python neural_network_demo.py
```

## Programatik Kullanım

Kendi Python kodunuzda kullanmak için:

```python
from neural_network_simulator import NeuralNetwork
import numpy as np

# Neural network oluştur
nn = NeuralNetwork(input_size=2, hidden_size=4, output_size=1)

# XOR problemi
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# Eğit
nn.train(X, y, epochs=10000)

# Tahmin yap
predictions = nn.predict(X)
print(predictions)
```

## Yardım

Sorun yaşamaya devam ederseniz:

1. Python versiyonunuzu kontrol edin: `python --version` (3.7+ olmalı)
2. Pip versiyonunu kontrol edin: `pip --version`
3. Virtual environment'ın aktif olduğundan emin olun
4. Gerekirse virtual environment'ı yeniden oluşturun:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
