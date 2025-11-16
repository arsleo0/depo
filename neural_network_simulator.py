"""
Basit Neural Network Simülatörü

Bu modül, feedforward neural network'ün temel işlevlerini simüle eder.
Sigmoid aktivasyon fonksiyonu ve backpropagation kullanır.
"""

import numpy as np


class NeuralNetwork:
    """
    Basit bir feedforward neural network implementasyonu.

    Attributes:
        input_size (int): Giriş katmanı nöron sayısı
        hidden_size (int): Gizli katman nöron sayısı
        output_size (int): Çıkış katmanı nöron sayısı
        learning_rate (float): Öğrenme oranı
    """

    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.5):
        """
        Neural network'ü başlatır.

        Args:
            input_size (int): Giriş katmanı nöron sayısı
            hidden_size (int): Gizli katman nöron sayısı
            output_size (int): Çıkış katmanı nöron sayısı
            learning_rate (float): Öğrenme oranı (varsayılan: 0.5)
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate

        # Ağırlıkları rastgele başlat (-1 ile 1 arası)
        self.weights_input_hidden = np.random.uniform(-1, 1, (input_size, hidden_size))
        self.weights_hidden_output = np.random.uniform(-1, 1, (hidden_size, output_size))

        # Bias'ları sıfırla başlat
        self.bias_hidden = np.zeros((1, hidden_size))
        self.bias_output = np.zeros((1, output_size))

    def sigmoid(self, x):
        """
        Sigmoid aktivasyon fonksiyonu.

        Args:
            x (np.ndarray): Giriş değerleri

        Returns:
            np.ndarray: Sigmoid çıkışı
        """
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))  # Overflow önleme

    def sigmoid_derivative(self, x):
        """
        Sigmoid fonksiyonunun türevi.

        Args:
            x (np.ndarray): Sigmoid çıkış değerleri

        Returns:
            np.ndarray: Sigmoid türevi
        """
        return x * (1 - x)

    def forward(self, X):
        """
        Forward propagation işlemi.

        Args:
            X (np.ndarray): Giriş verileri (shape: [samples, input_size])

        Returns:
            np.ndarray: Network çıkışı
        """
        # Gizli katman hesaplaması
        self.hidden_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        self.hidden_output = self.sigmoid(self.hidden_input)

        # Çıkış katmanı hesaplaması
        self.output_input = np.dot(self.hidden_output, self.weights_hidden_output) + self.bias_output
        self.output = self.sigmoid(self.output_input)

        return self.output

    def backward(self, X, y, output):
        """
        Backpropagation işlemi.

        Args:
            X (np.ndarray): Giriş verileri
            y (np.ndarray): Gerçek etiketler
            output (np.ndarray): Network çıkışı
        """
        # Çıkış katmanı hatası
        output_error = y - output
        output_delta = output_error * self.sigmoid_derivative(output)

        # Gizli katman hatası
        hidden_error = output_delta.dot(self.weights_hidden_output.T)
        hidden_delta = hidden_error * self.sigmoid_derivative(self.hidden_output)

        # Ağırlıkları güncelle
        self.weights_hidden_output += self.hidden_output.T.dot(output_delta) * self.learning_rate
        self.weights_input_hidden += X.T.dot(hidden_delta) * self.learning_rate

        # Bias'ları güncelle
        self.bias_output += np.sum(output_delta, axis=0, keepdims=True) * self.learning_rate
        self.bias_hidden += np.sum(hidden_delta, axis=0, keepdims=True) * self.learning_rate

    def train(self, X, y, epochs=10000, verbose=True):
        """
        Neural network'ü eğitir.

        Args:
            X (np.ndarray): Eğitim giriş verileri
            y (np.ndarray): Eğitim etiketleri
            epochs (int): Epoch sayısı (varsayılan: 10000)
            verbose (bool): İlerleme göster (varsayılan: True)
        """
        for epoch in range(epochs):
            # Forward propagation
            output = self.forward(X)

            # Backward propagation
            self.backward(X, y, output)

            # Her 1000 epoch'ta bir loss göster
            if verbose and epoch % 1000 == 0:
                loss = np.mean(np.square(y - output))
                print(f"Epoch {epoch}, Loss: {loss:.6f}")

    def predict(self, X):
        """
        Tahmin yapar.

        Args:
            X (np.ndarray): Giriş verileri

        Returns:
            np.ndarray: Tahmin sonuçları
        """
        return self.forward(X)

    def get_info(self):
        """
        Network hakkında bilgi döndürür.

        Returns:
            dict: Network bilgileri
        """
        return {
            'input_size': self.input_size,
            'hidden_size': self.hidden_size,
            'output_size': self.output_size,
            'learning_rate': self.learning_rate,
            'weights_input_hidden_shape': self.weights_input_hidden.shape,
            'weights_hidden_output_shape': self.weights_hidden_output.shape
        }
