#!/usr/bin/env python3
"""
Safetensors Model Inspector
LLM modellerinin .safetensors dosyalarını analiz eder ve mimari bilgilerini gösterir.
"""

import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

try:
    from safetensors import safe_open
except ImportError:
    print("❌ 'safetensors' kütüphanesi bulunamadı!")
    print("Lütfen yükleyin: pip install safetensors")
    sys.exit(1)


class SafetensorsInspector:
    """Safetensors dosyalarını analiz eden sınıf"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")

        self.tensors = {}
        self.metadata = {}
        self.load_file()

    def load_file(self):
        """Safetensors dosyasını yükle"""
        with safe_open(self.file_path, framework="pt", device="cpu") as f:
            # Metadata'yı al
            self.metadata = f.metadata() or {}

            # Tüm tensor'ları yükle
            for key in f.keys():
                tensor = f.get_tensor(key)
                self.tensors[key] = {
                    'shape': list(tensor.shape),
                    'dtype': str(tensor.dtype),
                    'numel': tensor.numel()
                }

    def get_layer_statistics(self) -> Dict:
        """Katman istatistiklerini hesapla"""
        layer_types = defaultdict(int)
        layer_names = defaultdict(list)

        for key in self.tensors.keys():
            # Katman tipini belirle
            if 'attention' in key.lower() or 'attn' in key.lower():
                layer_type = 'attention'
            elif 'mlp' in key.lower() or 'ffn' in key.lower() or 'feed_forward' in key.lower():
                layer_type = 'mlp'
            elif 'embed' in key.lower():
                layer_type = 'embedding'
            elif 'norm' in key.lower() or 'ln' in key.lower() or 'layernorm' in key.lower():
                layer_type = 'normalization'
            elif 'output' in key.lower() or 'lm_head' in key.lower():
                layer_type = 'output'
            elif 'conv' in key.lower():
                layer_type = 'convolution'
            else:
                layer_type = 'other'

            layer_types[layer_type] += 1
            layer_names[layer_type].append(key)

        return dict(layer_types), dict(layer_names)

    def detect_model_architecture(self) -> str:
        """Model mimarisini tahmin et"""
        keys = [k.lower() for k in self.tensors.keys()]

        # Transformer tabanlı modeller
        if any('attention' in k or 'attn' in k for k in keys):
            if any('encoder' in k and 'decoder' in k for k in keys):
                return "Encoder-Decoder Transformer"
            elif any('decoder' in k for k in keys):
                return "Decoder-only Transformer (GPT-style)"
            elif any('encoder' in k for k in keys):
                return "Encoder-only Transformer (BERT-style)"
            else:
                return "Transformer-based Model"

        # CNN modeller
        elif any('conv' in k for k in keys):
            return "Convolutional Neural Network (CNN)"

        # RNN modeller
        elif any('rnn' in k or 'lstm' in k or 'gru' in k for k in keys):
            return "Recurrent Neural Network (RNN/LSTM/GRU)"

        return "Unknown Architecture"

    def count_transformer_layers(self) -> int:
        """Transformer katman sayısını say"""
        layer_numbers = set()

        for key in self.tensors.keys():
            # "layers.0", "layer.1", "h.0", "block.0" gibi patternleri ara
            parts = key.split('.')
            for i, part in enumerate(parts):
                if part in ['layers', 'layer', 'h', 'block', 'blocks'] and i + 1 < len(parts):
                    try:
                        layer_num = int(parts[i + 1])
                        layer_numbers.add(layer_num)
                    except ValueError:
                        continue

        return len(layer_numbers) if layer_numbers else 0

    def calculate_total_parameters(self) -> int:
        """Toplam parametre sayısını hesapla"""
        return sum(t['numel'] for t in self.tensors.values())

    def get_model_dimensions(self) -> Dict:
        """Model boyutlarını çıkar (hidden_size, num_heads, vb.)"""
        dims = {}

        # Embedding boyutunu bul
        for key, tensor_info in self.tensors.items():
            if 'embed' in key.lower() and 'weight' in key.lower():
                shape = tensor_info['shape']
                if len(shape) >= 2:
                    dims['vocab_size'] = shape[0]
                    dims['hidden_size'] = shape[1]
                    break

        # Attention head sayısını tahmin et
        for key, tensor_info in self.tensors.items():
            if 'attention' in key.lower() or 'attn' in key.lower():
                if 'q_proj' in key.lower() or 'query' in key.lower():
                    shape = tensor_info['shape']
                    if len(shape) >= 2 and 'hidden_size' in dims:
                        if shape[-1] == dims['hidden_size']:
                            dims['attention_dim'] = shape[0]

        return dims

    def print_summary(self, detailed: bool = False):
        """Model özetini yazdır"""
        print("=" * 80)
        print(f"📊 SAFETENSORS MODEL ANALİZİ")
        print("=" * 80)
        print(f"\n📁 Dosya: {self.file_path.name}")
        print(f"📏 Dosya Boyutu: {self.file_path.stat().st_size / (1024**3):.2f} GB")

        # Model mimarisi
        print(f"\n🏗️  Model Mimarisi: {self.detect_model_architecture()}")

        # Katman sayısı
        num_layers = self.count_transformer_layers()
        if num_layers > 0:
            print(f"📚 Transformer Katman Sayısı: {num_layers}")

        # Toplam parametre
        total_params = self.calculate_total_parameters()
        print(f"🔢 Toplam Parametre: {total_params:,} ({total_params / 1e9:.2f}B)")

        # Model boyutları
        dims = self.get_model_dimensions()
        if dims:
            print(f"\n📐 Model Boyutları:")
            for key, value in dims.items():
                print(f"   • {key}: {value:,}")

        # Katman istatistikleri
        layer_types, layer_names = self.get_layer_statistics()
        print(f"\n🧱 Katman İstatistikleri:")
        for layer_type, count in sorted(layer_types.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {layer_type.capitalize()}: {count} katman")

        # Metadata
        if self.metadata:
            print(f"\n📋 Metadata:")
            for key, value in self.metadata.items():
                print(f"   • {key}: {value}")

        # Detaylı bilgi
        if detailed:
            print(f"\n📝 Detaylı Tensor Bilgileri:")
            print("-" * 80)

            for layer_type in sorted(layer_types.keys()):
                print(f"\n[{layer_type.upper()}]")
                for name in sorted(layer_names[layer_type])[:10]:  # İlk 10'u göster
                    tensor_info = self.tensors[name]
                    params = tensor_info['numel']
                    shape_str = ' × '.join(map(str, tensor_info['shape']))
                    print(f"  {name}")
                    print(f"    Shape: {shape_str}")
                    print(f"    Dtype: {tensor_info['dtype']}")
                    print(f"    Parameters: {params:,}")

                remaining = len(layer_names[layer_type]) - 10
                if remaining > 0:
                    print(f"  ... ve {remaining} tensor daha")

        print("\n" + "=" * 80)

    def export_to_json(self, output_path: str):
        """Analiz sonuçlarını JSON'a aktar"""
        layer_types, layer_names = self.get_layer_statistics()

        data = {
            'file_name': self.file_path.name,
            'file_size_gb': round(self.file_path.stat().st_size / (1024**3), 2),
            'architecture': self.detect_model_architecture(),
            'num_transformer_layers': self.count_transformer_layers(),
            'total_parameters': self.calculate_total_parameters(),
            'model_dimensions': self.get_model_dimensions(),
            'layer_statistics': layer_types,
            'metadata': self.metadata,
            'tensors': self.tensors
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Analiz sonuçları kaydedildi: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Safetensors model dosyalarını analiz eder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  %(prog)s model.safetensors
  %(prog)s model.safetensors --detailed
  %(prog)s model.safetensors --export analysis.json
        """
    )

    parser.add_argument('file', help='Analiz edilecek .safetensors dosyası')
    parser.add_argument('-d', '--detailed', action='store_true',
                        help='Detaylı tensor bilgilerini göster')
    parser.add_argument('-e', '--export', metavar='FILE',
                        help='Analiz sonuçlarını JSON dosyasına aktar')

    args = parser.parse_args()

    try:
        # Dosyayı analiz et
        inspector = SafetensorsInspector(args.file)

        # Özeti yazdır
        inspector.print_summary(detailed=args.detailed)

        # JSON'a aktar
        if args.export:
            inspector.export_to_json(args.export)

    except FileNotFoundError as e:
        print(f"❌ Hata: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
