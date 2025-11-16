"""
Neural Network Simülatörü Demo

Bu demo, XOR problemi gibi basit problemleri çözmek için
neural network simülatörünü kullanır.
"""

import numpy as np
from neural_network_simulator import NeuralNetwork


def xor_problem():
    """
    XOR problemi çözümü.

    XOR (exclusive OR) mantıksal kapısını öğrenmek için neural network kullanır.
    """
    print("=" * 60)
    print("XOR PROBLEMİ ÇÖZÜMÜ")
    print("=" * 60)
    print()

    # XOR veri seti
    X = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]])

    y = np.array([[0],
                  [1],
                  [1],
                  [0]])

    print("Eğitim Verileri:")
    print("Giriş (X):")
    print(X)
    print("\nBeklenen Çıkış (y):")
    print(y)
    print()

    # Neural network oluştur
    # 2 giriş, 4 gizli nöron, 1 çıkış
    nn = NeuralNetwork(input_size=2, hidden_size=4, output_size=1, learning_rate=0.5)

    print("Neural Network Bilgileri:")
    info = nn.get_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()

    # Eğitim öncesi tahminler
    print("Eğitim Öncesi Tahminler:")
    predictions = nn.predict(X)
    for i, (input_val, pred, expected) in enumerate(zip(X, predictions, y)):
        print(f"  {input_val} -> Tahmin: {pred[0]:.4f}, Beklenen: {expected[0]}")
    print()

    # Neural network'ü eğit
    print("Eğitim Başlıyor...")
    print("-" * 60)
    nn.train(X, y, epochs=10000, verbose=True)
    print("-" * 60)
    print()

    # Eğitim sonrası tahminler
    print("Eğitim Sonrası Tahminler:")
    predictions = nn.predict(X)
    for i, (input_val, pred, expected) in enumerate(zip(X, predictions, y)):
        rounded_pred = round(pred[0])
        status = "✓" if rounded_pred == expected[0] else "✗"
        print(f"  {input_val} -> Tahmin: {pred[0]:.4f} (~{rounded_pred}), Beklenen: {expected[0]} {status}")
    print()

    # Doğruluk hesapla
    predictions_rounded = np.round(predictions)
    accuracy = np.mean(predictions_rounded == y) * 100
    print(f"Doğruluk: {accuracy:.2f}%")
    print()


def simple_classification():
    """
    Basit sınıflandırma problemi.

    Sayıların 0.5'ten büyük mü küçük mü olduğunu öğrenir.
    """
    print("=" * 60)
    print("BASİT SINIFLANDIRMA PROBLEMİ")
    print("=" * 60)
    print()

    # Veri seti: Sayı 0.5'ten büyükse 1, değilse 0
    X = np.array([[0.1],
                  [0.3],
                  [0.7],
                  [0.9]])

    y = np.array([[0],
                  [0],
                  [1],
                  [1]])

    print("Eğitim Verileri:")
    print("Giriş (X):", X.flatten())
    print("Beklenen Çıkış (y):", y.flatten())
    print()

    # Neural network oluştur
    nn = NeuralNetwork(input_size=1, hidden_size=3, output_size=1, learning_rate=0.8)

    print("Eğitim Başlıyor...")
    nn.train(X, y, epochs=5000, verbose=False)
    print("Eğitim Tamamlandı!")
    print()

    # Tahminler
    print("Tahminler:")
    test_inputs = np.array([[0.2], [0.4], [0.6], [0.8]])
    predictions = nn.predict(test_inputs)
    for input_val, pred in zip(test_inputs, predictions):
        rounded_pred = round(pred[0])
        print(f"  {input_val[0]:.1f} -> {pred[0]:.4f} (~{rounded_pred})")
    print()


def main():
    """Ana fonksiyon - tüm demoları çalıştırır."""
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  NEURAL NETWORK SİMÜLATÖRÜ DEMO  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    # XOR problemi
    xor_problem()

    print("\n" + "=" * 60 + "\n")

    # Basit sınıflandırma
    simple_classification()

    print("=" * 60)
    print("TÜM DEMOLAR TAMAMLANDI!")
    print("=" * 60)


if __name__ == "__main__":
    main()
