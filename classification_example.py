"""
Basit Sınıflandırma Örneği - Boy ve Kilo ile Kategori Belirleme

Bu örnek, bir kişinin boy ve kilosuna bakarak hangi kategoriye ait olduğunu öğrenir.
Kategoriler:
  0 = Zayıf
  1 = Normal
  2 = Kilolu
"""

from neural_network_simulator import NeuralNetwork
import numpy as np


def boy_kilo_siniflandirma():
    """
    Boy ve kilo verilerine göre kategori belirleme.

    Boy (metre cinsinden) ve Kilo (kg) -> Kategori (0, 1, veya 2)
    """
    print("=" * 70)
    print("BOY-KİLO SINIFLANDIRMA ÖRNEĞİ")
    print("=" * 70)
    print()

    # Eğitim verileri
    # Format: [boy (m), kilo (kg)]
    X_train = np.array([
        [1.60, 45],   # Kısa, hafif
        [1.65, 50],   # Kısa-orta, hafif
        [1.70, 55],   # Orta, hafif
        [1.75, 70],   # Orta-uzun, normal
        [1.80, 75],   # Uzun, normal
        [1.85, 80],   # Uzun, normal
        [1.70, 90],   # Orta, kilolu
        [1.75, 95],   # Orta-uzun, kilolu
        [1.80, 100],  # Uzun, kilolu
    ])

    # Etiketler
    # 0 = Zayıf, 1 = Normal, 2 = Kilolu
    y_train = np.array([
        [1, 0, 0],  # Zayıf
        [1, 0, 0],  # Zayıf
        [1, 0, 0],  # Zayıf
        [0, 1, 0],  # Normal
        [0, 1, 0],  # Normal
        [0, 1, 0],  # Normal
        [0, 0, 1],  # Kilolu
        [0, 0, 1],  # Kilolu
        [0, 0, 1],  # Kilolu
    ])

    print("📊 EĞİTİM VERİLERİ:")
    print("-" * 70)
    kategoriler = ["Zayıf", "Normal", "Kilolu"]
    for i, (x, y) in enumerate(zip(X_train, y_train)):
        kategori = kategoriler[np.argmax(y)]
        print(f"  {i+1}. Boy: {x[0]:.2f}m, Kilo: {x[1]:.0f}kg → {kategori}")
    print()

    # Verileri normalize et (0-1 arası)
    X_normalized = X_train.copy()
    X_normalized[:, 0] = (X_train[:, 0] - 1.5) / 0.5  # Boy: 1.5-2.0m arası
    X_normalized[:, 1] = X_train[:, 1] / 120.0        # Kilo: 0-120kg arası

    # Neural network oluştur
    # 2 giriş (boy, kilo), 6 gizli nöron, 3 çıkış (zayıf, normal, kilolu)
    nn = NeuralNetwork(
        input_size=2,
        hidden_size=6,
        output_size=3,
        learning_rate=0.5
    )

    print("🧠 NEURAL NETWORK OLUŞTURULDU:")
    print("-" * 70)
    info = nn.get_info()
    print(f"  Giriş katmanı: {info['input_size']} nöron (boy, kilo)")
    print(f"  Gizli katman: {info['hidden_size']} nöron")
    print(f"  Çıkış katmanı: {info['output_size']} nöron (zayıf, normal, kilolu)")
    print(f"  Öğrenme oranı: {info['learning_rate']}")
    print()

    # Eğitim
    print("🎓 EĞİTİM BAŞLIYOR...")
    print("-" * 70)
    nn.train(X_normalized, y_train, epochs=15000, verbose=True)
    print()

    # Eğitim verilerini test et
    print("✅ EĞİTİM VERİLERİ KONTROLÜ:")
    print("-" * 70)
    predictions = nn.predict(X_normalized)
    dogru = 0
    for i, (x_orig, pred, expected) in enumerate(zip(X_train, predictions, y_train)):
        pred_kategori = kategoriler[np.argmax(pred)]
        gercek_kategori = kategoriler[np.argmax(expected)]
        dogru_mu = "✓" if np.argmax(pred) == np.argmax(expected) else "✗"
        if dogru_mu == "✓":
            dogru += 1

        print(f"  Boy: {x_orig[0]:.2f}m, Kilo: {x_orig[1]:.0f}kg")
        print(f"    Tahmin: {pred_kategori} {pred} {dogru_mu}")
        print(f"    Gerçek: {gercek_kategori}")
        print()

    accuracy = (dogru / len(X_train)) * 100
    print(f"📈 Eğitim Doğruluğu: {accuracy:.1f}%")
    print()

    # Yeni verilerle test
    print("🔮 YENİ VERİLER İLE TAHMİN:")
    print("=" * 70)

    test_data = np.array([
        [1.68, 52],   # Beklenenden hafif
        [1.75, 72],   # Normal
        [1.82, 88],   # Biraz kilolu
        [1.60, 70],   # Kısa ve kilolu
        [1.90, 78],   # Uzun ve normal
    ])

    for x_test in test_data:
        # Normalize et
        x_normalized = np.array([[
            (x_test[0] - 1.5) / 0.5,
            x_test[1] / 120.0
        ]])

        # Tahmin yap
        pred = nn.predict(x_normalized)[0]
        pred_kategori = kategoriler[np.argmax(pred)]
        confidence = np.max(pred) * 100

        print(f"\n  📍 Boy: {x_test[0]:.2f}m, Kilo: {x_test[1]:.0f}kg")
        print(f"     Tahmin: {pred_kategori} (Güven: %{confidence:.1f})")
        print(f"     Detay: Zayıf=%{pred[0]*100:.1f}, Normal=%{pred[1]*100:.1f}, Kilolu=%{pred[2]*100:.1f}")

    print()
    print("=" * 70)
    print("SINIFLAMA TAMAMLANDI!")
    print("=" * 70)


def meyve_siniflandirma():
    """
    Meyveleri ağırlık ve çaplarına göre sınıflandırma.

    Ağırlık (gram) ve Çap (cm) -> Meyve Türü
    """
    print("\n\n")
    print("=" * 70)
    print("MEYVE SINIFLANDIRMA ÖRNEĞİ")
    print("=" * 70)
    print()

    # Eğitim verileri
    # Format: [ağırlık (g), çap (cm)]
    X_train = np.array([
        [150, 7],    # Elma
        [160, 7.5],  # Elma
        [140, 6.8],  # Elma
        [300, 12],   # Portakal
        [320, 13],   # Portakal
        [290, 11.5], # Portakal
        [50, 4],     # Limon
        [60, 4.5],   # Limon
        [45, 3.8],   # Limon
    ])

    # Etiketler (One-hot encoding)
    # 0 = Elma, 1 = Portakal, 2 = Limon
    y_train = np.array([
        [1, 0, 0],  # Elma
        [1, 0, 0],
        [1, 0, 0],
        [0, 1, 0],  # Portakal
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 1],  # Limon
        [0, 0, 1],
        [0, 0, 1],
    ])

    print("📊 EĞİTİM VERİLERİ:")
    print("-" * 70)
    meyveler = ["🍎 Elma", "🍊 Portakal", "🍋 Limon"]
    for i, (x, y) in enumerate(zip(X_train, y_train)):
        meyve = meyveler[np.argmax(y)]
        print(f"  {i+1}. Ağırlık: {x[0]:.0f}g, Çap: {x[1]:.1f}cm → {meyve}")
    print()

    # Normalize et
    X_normalized = X_train / np.array([400, 15])  # Max değerlere böl

    # Neural network
    nn = NeuralNetwork(input_size=2, hidden_size=5, output_size=3, learning_rate=0.6)

    print("🎓 Eğitim başlıyor...")
    nn.train(X_normalized, y_train, epochs=10000, verbose=False)
    print("✅ Eğitim tamamlandı!")
    print()

    # Test
    print("🔮 YENİ MEYVE TAHMİNLERİ:")
    print("-" * 70)

    test_data = np.array([
        [155, 7.2],   # Elma gibi
        [310, 12.5],  # Portakal gibi
        [55, 4.2],    # Limon gibi
        [200, 9],     # Karışık - muhtemelen portakal
    ])

    for x_test in test_data:
        x_normalized = x_test / np.array([400, 15])
        pred = nn.predict(x_normalized.reshape(1, -1))[0]
        pred_meyve = meyveler[np.argmax(pred)]
        confidence = np.max(pred) * 100

        print(f"\n  📍 Ağırlık: {x_test[0]:.0f}g, Çap: {x_test[1]:.1f}cm")
        print(f"     Tahmin: {pred_meyve} (Güven: %{confidence:.1f})")

    print()
    print("=" * 70)


def main():
    """Ana fonksiyon - tüm sınıflandırma örneklerini çalıştırır."""
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  NEURAL NETWORK - BASİT SINIFLANDIRMA ÖRNEKLERİ  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    # Örnek 1: Boy-Kilo sınıflandırma
    boy_kilo_siniflandirma()

    # Örnek 2: Meyve sınıflandırma
    meyve_siniflandirma()

    print("\n")
    print("=" * 70)
    print("TÜM SINIFLANDIRMA ÖRNEKLERİ TAMAMLANDI!")
    print("=" * 70)
    print()
    print("💡 İPUCU: Kendi verilerinizle denemek için bu dosyayı düzenleyebilirsiniz!")
    print()


if __name__ == "__main__":
    main()
