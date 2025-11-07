#!/usr/bin/env python3
"""
3D Print Automation Ecosystem - Otomatik Kurulum Scripti
Windows 11 için

Bu script Claude Desktop'a MCP sunucularını otomatik olarak kurar.
"""

import os
import sys
import json
import shutil
from pathlib import Path
import platform

def get_claude_config_path():
    """Claude Desktop config dosyası yolunu bul"""
    if platform.system() == "Windows":
        appdata = os.getenv('APPDATA')
        return Path(appdata) / "Claude" / "claude_desktop_config.json"
    elif platform.system() == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:  # Linux
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"

def load_config():
    """Mevcut config'i yükle veya yeni oluştur"""
    config_path = get_claude_config_path()

    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {"mcpServers": {}}

def save_config(config):
    """Config'i kaydet"""
    config_path = get_claude_config_path()

    # Dizini oluştur
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

    print(f"✅ Config saved to: {config_path}")

def get_project_path():
    """Bu projenin yolunu al"""
    return Path(__file__).parent.absolute()

def setup_mcp_servers():
    """MCP sunucularını config'e ekle"""
    config = load_config()

    if "mcpServers" not in config:
        config["mcpServers"] = {}

    project_path = get_project_path()

    # Python executable
    python_exe = sys.executable

    # MCP sunucuları
    servers = {
        "3d-print-market-research": {
            "command": python_exe,
            "args": [str(project_path / "market_research_server.py")],
            "env": {"PYTHONUNBUFFERED": "1"}
        },
        "3d-print-model-generator": {
            "command": python_exe,
            "args": [str(project_path / "model_generator_server.py")],
            "env": {
                "PYTHONUNBUFFERED": "1",
                "BLENDER_PATH": ""  # config.yaml'dan okunacak
            }
        },
        "3d-print-slicer": {
            "command": python_exe,
            "args": [str(project_path / "slicer_server.py")],
            "env": {
                "PYTHONUNBUFFERED": "1",
                "BAMBU_STUDIO_PATH": ""  # config.yaml'dan okunacak
            }
        },
        "3d-print-printer-manager": {
            "command": python_exe,
            "args": [str(project_path / "printer_manager_server.py")],
            "env": {"PYTHONUNBUFFERED": "1"}
        },
        "3d-print-workflow-orchestrator": {
            "command": python_exe,
            "args": [str(project_path / "workflow_orchestrator_server.py")],
            "env": {"PYTHONUNBUFFERED": "1"}
        }
    }

    # Sunucuları ekle/güncelle
    for name, server_config in servers.items():
        config["mcpServers"][name] = server_config
        print(f"✅ Added MCP server: {name}")

    save_config(config)

def create_output_directories():
    """Output dizinlerini oluştur"""
    project_path = get_project_path()

    dirs = [
        project_path / "output",
        project_path / "output" / "models",
        project_path / "output" / "gcode",
        project_path / "data",
        project_path / "data" / "cache",
        project_path / "logs"
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")

def create_env_file():
    """Example .env dosyası oluştur"""
    project_path = get_project_path()
    env_path = project_path / ".env"

    if not env_path.exists():
        env_content = """# 3D Print Automation Ecosystem - Environment Variables

# Hyper3D API
HYPER3D_API_KEY=your_api_key_here

# Etsy API (opsiyonel)
ETSY_API_KEY=your_etsy_api_key_here

# Bambu Lab Printer
BAMBU_PRINTER_IP=192.168.1.100
BAMBU_ACCESS_CODE=your_access_code

# Paths (Windows)
BLENDER_PATH=C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe
BAMBU_STUDIO_PATH=C:\\Program Files\\BambuStudio\\bambu-studio-console.exe
"""

        with open(env_path, 'w') as f:
            f.write(env_content)

        print(f"✅ Created .env template: {env_path}")
        print("⚠️  Please edit .env file with your actual API keys and paths!")
    else:
        print(f"ℹ️  .env file already exists: {env_path}")

def verify_installation():
    """Kurulumu doğrula"""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)

    # Check MCP servers
    project_path = get_project_path()
    servers = [
        "market_research_server.py",
        "model_generator_server.py",
        "slicer_server.py",
        "printer_manager_server.py",
        "workflow_orchestrator_server.py"
    ]

    all_found = True
    for server in servers:
        path = project_path / server
        if path.exists():
            print(f"✅ Found: {server}")
        else:
            print(f"❌ Missing: {server}")
            all_found = False

    # Check config
    config_path = get_claude_config_path()
    if config_path.exists():
        print(f"✅ Config file: {config_path}")
    else:
        print(f"❌ Config file not found: {config_path}")
        all_found = False

    return all_found

def main():
    """Ana kurulum fonksiyonu"""
    print("="*60)
    print("3D PRINT AUTOMATION ECOSYSTEM - KURULUM")
    print("="*60)
    print()

    # Platform check
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")
    print()

    # Adımlar
    print("🔧 Step 1: Creating output directories...")
    create_output_directories()
    print()

    print("🔧 Step 2: Creating .env template...")
    create_env_file()
    print()

    print("🔧 Step 3: Setting up MCP servers in Claude Desktop...")
    setup_mcp_servers()
    print()

    print("🔧 Step 4: Verifying installation...")
    success = verify_installation()
    print()

    if success:
        print("="*60)
        print("✅ KURULUM BAŞARILI!")
        print("="*60)
        print()
        print("Sonraki Adımlar:")
        print("1. Claude Desktop'ı yeniden başlatın (tamamen kapatıp açın)")
        print("2. .env dosyasını düzenleyin (API keys, paths)")
        print("3. config.yaml dosyasını kontrol edin")
        print("4. Claude Desktop'ta 'MCP araçlarımı listele' yazın")
        print("5. ~30+ araç görmelisiniz!")
        print()
        print("Test için Claude'a şunu yazın:")
        print('  "3D baskı ekosistemimi test et"')
        print()
    else:
        print("="*60)
        print("⚠️  KURULUM TAMAMLANAMADI")
        print("="*60)
        print("Lütfen eksik dosyaları kontrol edin.")

if __name__ == "__main__":
    main()
