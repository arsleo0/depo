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
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Dosya okunamadı: {e}")
        return False

    # Hatalı satırı bul
    found_error = False
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Hatalı satırı bul: "with Path(f'{args.model_dir}/config.yaml') as p:"
        if "with Path(f'{args.model_dir}/config.yaml') as p:" in line:
            found_error = True
            print(f"🔍 Hata bulundu: Satır {i+1}")

            # with satırını p = ... ile değiştir
            indent = len(line) - len(line.lstrip())
            fixed_lines.append(' ' * indent + f"p = Path(f'{{args.model_dir}}/config.yaml')\n")

            # Sonraki satırları kontrol et ve girintilerini düzelt
            i += 1
            while i < len(lines):
                next_line = lines[i]
                next_indent = len(next_line) - len(next_line.lstrip())

                # Eğer bir sonraki satır orijinal girintileme + 4 space ise, 4 space azalt
                if next_indent > indent and next_line.strip():
                    # 4 space azalt
                    fixed_lines.append(' ' * (next_indent - 4) + next_line.lstrip())
                elif next_indent <= indent and next_line.strip():
                    # Bu satır bloğun dışında, geri dön
                    i -= 1
                    break
                else:
                    # Boş satır
                    fixed_lines.append(next_line)
                i += 1
        else:
            fixed_lines.append(line)

        i += 1

    if not found_error:
        print("✓ Hata bulunamadı! Dosya zaten düzeltilmiş olabilir.")
        # İndentation hatası varsa düzeltmeye çalış
        if "    else:" in ''.join(lines) and "if p.exists():" in ''.join(lines):
            print("⚠️  Ancak indentation hatası tespit edildi, düzeltiliyor...")
            # Tüm dosyayı tekrar oku
            content = ''.join(lines)
            # else bloğunu düzelt
            if "if p.exists():\n        model_config" in content:
                fixed_content = content.replace(
                    "if p.exists():\n        model_config",
                    "if p.exists():\n    model_config"
                )
                fixed_content = fixed_content.replace(
                    "    else:\n        model_config = {}",
                    "else:\n    model_config = {}"
                )
                fixed_lines = fixed_content.split('\n')
                fixed_lines = [line + '\n' for line in fixed_lines[:-1]] + [fixed_lines[-1]]
                found_error = True
            else:
                return True

    # Yedek al
    backup_path = shared_py.with_suffix('.py.backup')
    try:
        with open(shared_py, 'r', encoding='utf-8') as f:
            original_content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"💾 Yedek oluşturuldu: {backup_path}")
    except Exception as e:
        print(f"⚠️ Yedek oluşturulamadı: {e}")

    # Düzeltilmiş dosyayı kaydet
    try:
        with open(shared_py, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
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
