#!/usr/bin/env python3
"""
Text-generation-webui shared.py Path context manager hatasını düzelten script
"""
import sys
from pathlib import Path

def fix_shared_py(textgen_path: str):
    """
    shared.py dosyasındaki Path context manager hatasını düzelt
    """
    shared_py = Path(textgen_path) / "modules" / "shared.py"

    if not shared_py.exists():
        print(f"❌ Hata: {shared_py} bulunamadı!")
        print(f"   Text-generation-webui yolunun doğru olduğundan emin olun.")
        return False

    print(f"📂 Dosya bulundu: {shared_py}")

    # Dosyayı oku
    try:
        with open(shared_py, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Dosya okunamadı: {e}")
        return False

    # Hatalı kodu bul
    wrong_code = "with Path(f'{args.model_dir}/config.yaml') as p:"

    if wrong_code not in content:
        print("✓ Hata bulunamadı! Dosya zaten düzeltilmiş olabilir.")
        return True

    # Düzelt
    fixed_content = content.replace(
        "with Path(f'{args.model_dir}/config.yaml') as p:\n    if p.exists():",
        "p = Path(f'{args.model_dir}/config.yaml')\nif p.exists():"
    )

    # Yedek al
    backup_path = shared_py.with_suffix('.py.backup')
    try:
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 Yedek oluşturuldu: {backup_path}")
    except Exception as e:
        print(f"⚠️ Yedek oluşturulamadı: {e}")

    # Düzeltilmiş dosyayı kaydet
    try:
        with open(shared_py, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"✅ Dosya başarıyla düzeltildi!")
        print(f"")
        print(f"🚀 Şimdi text-generation-webui'yi başlatabilirsiniz:")
        print(f"   cd {textgen_path}")
        print(f"   python server.py --api")
        return True
    except Exception as e:
        print(f"❌ Dosya yazılamadı: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python fix_textgen_webui.py <text-generation-webui-yolu>")
        print("")
        print("Örnek (Windows):")
        print('  python fix_textgen_webui.py "C:\\Users\\mcgus\\Documents\\text-generation"')
        print("")
        print("Örnek (Linux):")
        print('  python fix_textgen_webui.py "/home/user/text-generation-webui"')
        sys.exit(1)

    textgen_path = sys.argv[1]
    print(f"🔧 Text-generation-webui Path hatası düzeltiliyor...")
    print(f"📁 Yol: {textgen_path}")
    print("")

    success = fix_shared_py(textgen_path)
    sys.exit(0 if success else 1)
