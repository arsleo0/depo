"""
Tahmin (Regresyon) Örnekleri - Sayısal Değer Tahmini

Bu örnekler, neural network ile sayısal değerler tahmin etmeyi gösterir.
Sınıflandırmadan farklı olarak, burada sürekli sayısal çıktılar üretilir.

Örnekler:
  1. Ev Fiyatı Tahmini - Oda sayısı ve metrekareye göre fiyat
  2. Sınav Notu Tahmini - Çalışma saati ve devamsızlığa göre not
  3. Satış Tahmini - Reklam bütçesine göre satış
"""

from neural_network_simulator import NeuralNetwork
import numpy as np


def ev_fiyat_tahmini():
    """
    Ev fiyatı tahmini - Oda sayısı ve metrekare bilgisine göre.

    Girdiler: [oda_sayısı, metrekare]
    Çıktı: Fiyat (bin TL cinsinden)
    """
    print("=" * 70)
    print("EV FİYATI TAHMİNİ")
    print("=" * 70)
    print()

    # Eğitim verileri
    # Format: [oda_sayısı, metrekare]
    X_train = np.array([
        [2, 60],    # 2+1, 60m²
        [2, 75],    # 2+1, 75m²
        [3, 90],    # 3+1, 90m²
        [3, 100],   # 3+1, 100m²
        [4, 120],   # 4+1, 120m²
        [4, 140],   # 4+1, 140m²
        [5, 160],   # 5+1, 160m²
        [5, 180],   # 5+1, 180m²
    ])

    # Fiyatlar (bin TL cinsinden)
    y_train = np.array([
        [800],     # 2+1, 60m² -> 800.000 TL
        [950],     # 2+1, 75m² -> 950.000 TL
        [1200],    # 3+1, 90m² -> 1.200.000 TL
        [1350],    # 3+1, 100m² -> 1.350.000 TL
        [1600],    # 4+1, 120m² -> 1.600.000 TL
        [1850],    # 4+1, 140m² -> 1.850.000 TL
        [2100],    # 5+1, 160m² -> 2.100.000 TL
        [2400],    # 5+1, 180m² -> 2.400.000 TL
    ])

    print("📊 EĞİTİM VERİLERİ:")
    print("-" * 70)
    for i, (x, y) in enumerate(zip(X_train, y_train)):
        print(f"  {i+1}. {int(x[0])+1}+1, {x[1]:.0f}m² → {y[0]:.0f} bin TL ({y[0]/1000:.1f} milyon TL)")
    print()

    # Verileri normalize et (0-1 arası)
    X_normalized = X_train / np.array([6, 200])  # Max: 6 oda, 200 m²
    y_normalized = y_train / 3000  # Max: 3 milyon TL

    # Neural network oluştur
    nn = NeuralNetwork(
        input_size=2,
        hidden_size=8,
        output_size=1,
        learning_rate=0.3
    )

    print("🧠 NEURAL NETWORK BİLGİLERİ:")
    print("-" * 70)
    print(f"  Giriş: {nn.input_size} nöron (oda sayısı, metrekare)")
    print(f"  Gizli katman: {nn.hidden_size} nöron")
    print(f"  Çıkış: {nn.output_size} nöron (fiyat)")
    print()

    # Eğitim
    print("🎓 EĞİTİM BAŞLIYOR...")
    print("-" * 70)
    nn.train(X_normalized, y_normalized, epochs=20000, verbose=True)
    print()

    # Eğitim verilerini kontrol
    print("✅ EĞİTİM VERİLERİ KONTROLÜ:")
    print("-" * 70)
    predictions = nn.predict(X_normalized)
    for i, (x_orig, pred, expected) in enumerate(zip(X_train, predictions, y_train)):
        pred_fiyat = pred[0] * 3000  # Denormalize
        gercek_fiyat = expected[0]
        fark = abs(pred_fiyat - gercek_fiyat)
        fark_yuzde = (fark / gercek_fiyat) * 100

        print(f"  {int(x_orig[0])+1}+1, {x_orig[1]:.0f}m²")
        print(f"    Tahmin: {pred_fiyat:.0f} bin TL ({pred_fiyat/1000:.2f} milyon)")
        print(f"    Gerçek: {gercek_fiyat:.0f} bin TL ({gercek_fiyat/1000:.2f} milyon)")
        print(f"    Fark: {fark:.0f} bin TL (%{fark_yuzde:.1f})")
        print()

    # Yeni evler için tahmin
    print("🔮 YENİ EVLER İÇİN FİYAT TAHMİNİ:")
    print("=" * 70)

    test_data = np.array([
        [2, 70],    # 2+1, 70m²
        [3, 95],    # 3+1, 95m²
        [4, 130],   # 4+1, 130m²
        [5, 200],   # 5+1, 200m² (lüks)
    ])

    for x_test in test_data:
        x_normalized = x_test / np.array([6, 200])
        pred = nn.predict(x_normalized.reshape(1, -1))[0]
        pred_fiyat = pred[0] * 3000

        print(f"\n  🏠 {int(x_test[0])+1}+1 Daire, {x_test[1]:.0f}m²")
        print(f"     Tahmini Fiyat: {pred_fiyat:.0f} bin TL")
        print(f"     ({pred_fiyat/1000:.2f} milyon TL)")

    print()
    print("=" * 70)


def sinav_notu_tahmini():
    """
    Sınav notu tahmini - Çalışma saati ve devamsızlığa göre.

    Girdiler: [haftalık_çalışma_saati, devamsızlık_günü]
    Çıktı: Final notu (0-100)
    """
    print("\n\n")
    print("=" * 70)
    print("SINAV NOTU TAHMİNİ")
    print("=" * 70)
    print()

    # Eğitim verileri
    # Format: [haftalık çalışma saati, devamsızlık günü]
    X_train = np.array([
        [2, 8],     # Az çalışma, çok devamsızlık
        [3, 6],     # Az çalışma, çok devamsızlık
        [5, 5],     # Orta çalışma, orta devamsızlık
        [7, 3],     # İyi çalışma, az devamsızlık
        [10, 2],    # Çok çalışma, çok az devamsızlık
        [12, 1],    # Çok çalışma, çok az devamsızlık
        [15, 0],    # Çok çalışma, hiç devamsızlık
        [18, 0],    # Çok çalışma, hiç devamsızlık
    ])

    # Notlar (0-100)
    y_train = np.array([
        [35],   # Düşük not
        [45],
        [60],
        [72],
        [80],
        [88],
        [93],
        [98],   # Yüksek not
    ])

    print("📊 EĞİTİM VERİLERİ:")
    print("-" * 70)
    for i, (x, y) in enumerate(zip(X_train, y_train)):
        print(f"  {i+1}. Haftalık {x[0]:.0f} saat çalışma, {x[1]:.0f} gün devamsızlık → Not: {y[0]:.0f}")
    print()

    # Normalize
    X_normalized = X_train / np.array([20, 10])
    y_normalized = y_train / 100

    # Neural network
    nn = NeuralNetwork(input_size=2, hidden_size=6, output_size=1, learning_rate=0.4)

    print("🎓 Eğitim başlıyor...")
    nn.train(X_normalized, y_normalized, epochs=15000, verbose=False)
    print("✅ Eğitim tamamlandı!")
    print()

    # Test
    print("🔮 ÖĞRENCİ NOT TAHMİNLERİ:")
    print("-" * 70)

    test_data = np.array([
        [4, 7],     # Az çalışan, çok devamsız
        [8, 4],     # Orta çalışan
        [12, 2],    # İyi çalışan
        [16, 0],    # Çok iyi çalışan
    ])

    for x_test in test_data:
        x_normalized = x_test / np.array([20, 10])
        pred = nn.predict(x_normalized.reshape(1, -1))[0]
        pred_not = pred[0] * 100

        print(f"\n  📚 Haftalık {x_test[0]:.0f} saat çalışma, {x_test[1]:.0f} gün devamsızlık")
        print(f"     Tahmini Not: {pred_not:.1f}")

        # Not durumu
        if pred_not >= 85:
            durum = "🌟 Pekiyi"
        elif pred_not >= 70:
            durum = "👍 İyi"
        elif pred_not >= 60:
            durum = "✓ Orta"
        elif pred_not >= 50:
            durum = "⚠️ Geçer"
        else:
            durum = "❌ Kaldı"
        print(f"     Durum: {durum}")

    print()
    print("=" * 70)


def satis_tahmini():
    """
    Satış tahmini - Reklam bütçesine göre satış miktarı.

    Girdiler: [TV_reklam_bütçesi, sosyal_medya_bütçesi] (bin TL)
    Çıktı: Satış miktarı (bin adet)
    """
    print("\n\n")
    print("=" * 70)
    print("SATIŞ TAHMİNİ (Reklam Bütçesine Göre)")
    print("=" * 70)
    print()

    # Eğitim verileri
    # Format: [TV bütçesi (bin TL), Sosyal medya bütçesi (bin TL)]
    X_train = np.array([
        [50, 10],
        [80, 15],
        [100, 20],
        [150, 25],
        [200, 30],
        [250, 40],
        [300, 50],
        [350, 60],
    ])

    # Satış miktarı (bin adet)
    y_train = np.array([
        [120],
        [180],
        [220],
        [310],
        [390],
        [460],
        [520],
        [580],
    ])

    print("📊 EĞİTİM VERİLERİ (Geçmiş Kampanyalar):")
    print("-" * 70)
    for i, (x, y) in enumerate(zip(X_train, y_train)):
        print(f"  {i+1}. TV: {x[0]:.0f} bin TL, Sosyal Medya: {x[1]:.0f} bin TL → Satış: {y[0]:.0f} bin adet")
    print()

    # Normalize
    X_normalized = X_train / np.array([400, 100])
    y_normalized = y_train / 700

    # Neural network
    nn = NeuralNetwork(input_size=2, hidden_size=7, output_size=1, learning_rate=0.35)

    print("🎓 Eğitim başlıyor...")
    nn.train(X_normalized, y_normalized, epochs=18000, verbose=False)
    print("✅ Eğitim tamamlandı!")
    print()

    # Test
    print("🔮 YENİ KAMPANYA TAHMİNLERİ:")
    print("-" * 70)

    test_data = np.array([
        [120, 22],   # Orta bütçe
        [200, 35],   # İyi bütçe
        [280, 45],   # Yüksek bütçe
        [400, 80],   # Çok yüksek bütçe
    ])

    for x_test in test_data:
        x_normalized = x_test / np.array([400, 100])
        pred = nn.predict(x_normalized.reshape(1, -1))[0]
        pred_satis = pred[0] * 700

        toplam_butce = x_test[0] + x_test[1]
        print(f"\n  💰 TV: {x_test[0]:.0f} bin TL, Sosyal Medya: {x_test[1]:.0f} bin TL")
        print(f"     Toplam Bütçe: {toplam_butce:.0f} bin TL")
        print(f"     Tahmini Satış: {pred_satis:.0f} bin adet")
        print(f"     Satış/Bütçe Oranı: {pred_satis/toplam_butce:.2f}")

    print()
    print("=" * 70)


def main():
    """Ana fonksiyon - tüm tahmin örneklerini çalıştırır."""
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  NEURAL NETWORK - TAHMİN (REGRESYON) ÖRNEKLERİ  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    print("Bu örnekler, neural network ile sayısal değer tahmini yapmayı gösterir.")
    print()

    # Örnek 1: Ev fiyatı tahmini
    ev_fiyat_tahmini()

    # Örnek 2: Sınav notu tahmini
    sinav_notu_tahmini()

    # Örnek 3: Satış tahmini
    satis_tahmini()

    print("\n")
    print("=" * 70)
    print("TÜM TAHMİN ÖRNEKLERİ TAMAMLANDI!")
    print("=" * 70)
    print()
    print("💡 İPUCU:")
    print("  - Tahmin (Regresyon): Sürekli sayısal değer tahmini (fiyat, not, satış)")
    print("  - Sınıflandırma: Kategori belirleme (zayıf/normal/kilolu, elma/portakal)")
    print()
    print("  Kendi verilerinizle denemek için bu dosyayı düzenleyebilirsiniz!")
    print()


if __name__ == "__main__":
    main()
