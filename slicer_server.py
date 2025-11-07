#!/usr/bin/env python3
"""
Bambu Lab Slicer MCP Server
3D Print Ecosystem - Bambu Studio entegrasyonu

Bu sunucu Claude Desktop'ın 3D modelleri slice etmesini ve
G-code üretmesini sağlar.
"""

import asyncio
import json
import os
import sys
import subprocess
from typing import Any, Dict, List, Optional
from pathlib import Path
import logging

# MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("ERROR: MCP SDK not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("slicer-server")

# Server instance
app = Server("3d-print-slicer")


class BambuStudioSlicer:
    """Bambu Studio CLI wrapper"""

    def __init__(self, bambu_path: Optional[str] = None):
        self.bambu_path = bambu_path or self._find_bambu_studio()
        if not self.bambu_path:
            logger.warning("Bambu Studio not found. Slicing may fail.")

        # Default profiles
        self.printer_profiles = {
            'A1': 'Bambu Lab A1',
            'A1_mini': 'Bambu Lab A1 mini',
            'P1P': 'Bambu Lab P1P',
            'X1C': 'Bambu Lab X1-Carbon'
        }

        self.material_profiles = {
            'PLA': 'Generic PLA',
            'PETG': 'Generic PETG',
            'ABS': 'Generic ABS',
            'TPU': 'Generic TPU'
        }

        self.quality_profiles = {
            'draft': '0.28mm Draft',
            'standard': '0.20mm Standard',
            'fine': '0.12mm Fine',
            'ultra_fine': '0.08mm Ultra Fine'
        }

    def _find_bambu_studio(self) -> Optional[str]:
        """Bambu Studio executable bul"""
        common_paths = [
            r"C:\Program Files\BambuStudio\bambu-studio-console.exe",
            r"C:\Program Files\BambuStudio\bambu-studio.exe",
            r"C:\Program Files (x86)\BambuStudio\bambu-studio-console.exe",
        ]

        # PATH'de ara
        try:
            result = subprocess.run(
                ["where", "bambu-studio-console"] if os.name == 'nt' else ["which", "bambu-studio-console"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass

        # Bilinen yollarda ara
        for path in common_paths:
            if os.path.exists(path):
                return path

        return None

    def slice_model(
        self,
        input_path: str,
        output_path: str,
        printer: str = 'A1',
        material: str = 'PLA',
        quality: str = 'standard',
        infill: int = 20,
        supports: bool = True,
        brim: bool = False
    ) -> Dict[str, Any]:
        """Model slice et ve G-code üret"""

        if not self.bambu_path:
            return {
                'success': False,
                'error': 'Bambu Studio not found. Please install or set BAMBU_STUDIO_PATH'
            }

        if not os.path.exists(input_path):
            return {
                'success': False,
                'error': f'Input file not found: {input_path}'
            }

        logger.info(f"Slicing {input_path}...")
        logger.info(f"Printer: {printer}, Material: {material}, Quality: {quality}")

        # Config file oluştur (Bambu Studio config format)
        config = self._create_config(
            printer=printer,
            material=material,
            quality=quality,
            infill=infill,
            supports=supports,
            brim=brim
        )

        # Temporary config dosyası
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            for key, value in config.items():
                f.write(f"{key} = {value}\n")
            config_path = f.name

        try:
            # Bambu Studio console çalıştır
            # Not: Gerçek Bambu Studio CLI parametreleri dokümantasyona göre ayarlanmalı
            cmd = [
                self.bambu_path,
                '--load', config_path,
                '--export-gcode',
                '--output', output_path,
                input_path
            ]

            logger.info(f"Running: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 dakika
            )

            os.unlink(config_path)

            if result.returncode != 0:
                logger.error(f"Slicing error: {result.stderr}")
                return {
                    'success': False,
                    'error': result.stderr,
                    'output': result.stdout
                }

            # G-code dosyası oluşturuldu mu?
            if not os.path.exists(output_path):
                return {
                    'success': False,
                    'error': 'G-code file not created'
                }

            # G-code analizi
            gcode_info = self._analyze_gcode(output_path)

            return {
                'success': True,
                'output_file': output_path,
                'gcode_info': gcode_info,
                'slicer_output': result.stdout
            }

        except subprocess.TimeoutExpired:
            if os.path.exists(config_path):
                os.unlink(config_path)
            return {
                'success': False,
                'error': 'Slicing timeout (5 minutes)'
            }
        except Exception as e:
            if os.path.exists(config_path):
                os.unlink(config_path)
            return {
                'success': False,
                'error': str(e)
            }

    def _create_config(
        self,
        printer: str,
        material: str,
        quality: str,
        infill: int,
        supports: bool,
        brim: bool
    ) -> Dict[str, Any]:
        """Slicer config oluştur"""

        config = {
            'printer_model': self.printer_profiles.get(printer, printer),
            'filament_type': self.material_profiles.get(material, material),
            'layer_height': self._get_layer_height(quality),
            'fill_density': f"{infill}%",
            'support_material': '1' if supports else '0',
            'brim_width': '5' if brim else '0',
            'wall_loops': '3',
            'top_solid_layers': '4',
            'bottom_solid_layers': '4',
            'infill_pattern': 'grid'
        }

        return config

    def _get_layer_height(self, quality: str) -> str:
        """Quality'den layer height'ı al"""
        heights = {
            'draft': '0.28',
            'standard': '0.20',
            'fine': '0.12',
            'ultra_fine': '0.08'
        }
        return heights.get(quality, '0.20')

    def _analyze_gcode(self, gcode_path: str) -> Dict[str, Any]:
        """G-code dosyasını analiz et (süre, materyal, vb.)"""

        info = {
            'file_size': os.path.getsize(gcode_path),
            'estimated_time': 'Unknown',
            'filament_used': 'Unknown',
            'layer_count': 0
        }

        try:
            with open(gcode_path, 'r') as f:
                for line in f:
                    line = line.strip()

                    # Bambu Studio comments içinde bilgiler var
                    if 'estimated printing time' in line.lower():
                        info['estimated_time'] = line.split('=')[-1].strip()
                    elif 'filament used' in line.lower():
                        info['filament_used'] = line.split('=')[-1].strip()
                    elif line.startswith(';LAYER_COUNT:'):
                        info['layer_count'] = int(line.split(':')[-1])

        except Exception as e:
            logger.warning(f"G-code analysis error: {e}")

        return info

    def estimate_cost(
        self,
        filament_weight: float,  # grams
        material: str = 'PLA',
        filament_cost_per_kg: float = 20.0
    ) -> Dict[str, Any]:
        """Baskı maliyeti hesapla"""

        material_cost = (filament_weight / 1000) * filament_cost_per_kg

        # Elektrik maliyeti (örnek)
        # Ortalama 3D yazıcı: ~100W
        # Print time varsayımı: 2 saat
        electricity_kwh = 0.1 * 2  # 100W * 2h
        electricity_cost_per_kwh = 0.15  # $0.15/kWh
        electricity_cost = electricity_kwh * electricity_cost_per_kwh

        total_cost = material_cost + electricity_cost

        return {
            'material_cost': f"${material_cost:.2f}",
            'electricity_cost': f"${electricity_cost:.2f}",
            'total_cost': f"${total_cost:.2f}",
            'filament_weight_g': filament_weight,
            'note': 'Estimate based on default values. Actual may vary.'
        }

    def optimize_supports(
        self,
        input_path: str,
        output_path: str,
        support_type: str = 'auto'
    ) -> Dict[str, Any]:
        """Support yapılarını optimize et"""

        # Bu fonksiyon Bambu Studio'nun support optimizasyon
        # özelliklerini kullanabilir

        logger.info(f"Optimizing supports for {input_path}")

        # Şimdilik basit bir wrapper - gerçek implementasyon
        # Bambu Studio CLI dokümantasyonuna göre yapılmalı

        return self.slice_model(
            input_path=input_path,
            output_path=output_path,
            supports=True
        )


# Global instance
slicer = BambuStudioSlicer()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """MCP araçlarını listele"""
    return [
        Tool(
            name="slice_model",
            description="3D modeli slice et ve G-code üret. Bambu Studio kullanır.",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Input STL dosyası yolu"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output G-code dosyası yolu"
                    },
                    "printer": {
                        "type": "string",
                        "enum": ["A1", "A1_mini", "P1P", "X1C"],
                        "description": "Yazıcı modeli",
                        "default": "A1"
                    },
                    "material": {
                        "type": "string",
                        "enum": ["PLA", "PETG", "ABS", "TPU"],
                        "description": "Materyal tipi",
                        "default": "PLA"
                    },
                    "quality": {
                        "type": "string",
                        "enum": ["draft", "standard", "fine", "ultra_fine"],
                        "description": "Baskı kalitesi",
                        "default": "standard"
                    },
                    "infill": {
                        "type": "integer",
                        "description": "Doluluk yüzdesi (0-100)",
                        "default": 20
                    },
                    "supports": {
                        "type": "boolean",
                        "description": "Support yapıları ekle",
                        "default": True
                    },
                    "brim": {
                        "type": "boolean",
                        "description": "Brim ekle (bed adhesion için)",
                        "default": False
                    }
                },
                "required": ["input_path", "output_path"]
            }
        ),
        Tool(
            name="estimate_cost",
            description="Baskı maliyeti tahmini (materyal + elektrik)",
            inputSchema={
                "type": "object",
                "properties": {
                    "filament_weight": {
                        "type": "number",
                        "description": "Filament ağırlığı (gram)"
                    },
                    "material": {
                        "type": "string",
                        "description": "Materyal tipi",
                        "default": "PLA"
                    },
                    "filament_cost_per_kg": {
                        "type": "number",
                        "description": "Filament maliyeti ($/kg)",
                        "default": 20.0
                    }
                },
                "required": ["filament_weight"]
            }
        ),
        Tool(
            name="analyze_gcode",
            description="G-code dosyasını analiz et (süre, materyal, layer sayısı)",
            inputSchema={
                "type": "object",
                "properties": {
                    "gcode_path": {
                        "type": "string",
                        "description": "G-code dosya yolu"
                    }
                },
                "required": ["gcode_path"]
            }
        ),
        Tool(
            name="optimize_supports",
            description="Support yapılarını optimize et",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Input STL dosyası"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output G-code dosyası"
                    },
                    "support_type": {
                        "type": "string",
                        "enum": ["auto", "tree", "normal"],
                        "description": "Support tipi",
                        "default": "auto"
                    }
                },
                "required": ["input_path", "output_path"]
            }
        ),
        Tool(
            name="get_slicer_info",
            description="Bambu Studio kurulumu ve ayarları hakkında bilgi",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """MCP araç çağrıları"""

    try:
        if name == "slice_model":
            input_path = arguments["input_path"]
            output_path = arguments["output_path"]
            printer = arguments.get("printer", "A1")
            material = arguments.get("material", "PLA")
            quality = arguments.get("quality", "standard")
            infill = arguments.get("infill", 20)
            supports = arguments.get("supports", True)
            brim = arguments.get("brim", False)

            # Dizini oluştur
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            result = slicer.slice_model(
                input_path=input_path,
                output_path=output_path,
                printer=printer,
                material=material,
                quality=quality,
                infill=infill,
                supports=supports,
                brim=brim
            )

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "estimate_cost":
            filament_weight = arguments["filament_weight"]
            material = arguments.get("material", "PLA")
            cost_per_kg = arguments.get("filament_cost_per_kg", 20.0)

            result = slicer.estimate_cost(filament_weight, material, cost_per_kg)

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "analyze_gcode":
            gcode_path = arguments["gcode_path"]

            if not os.path.exists(gcode_path):
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        'success': False,
                        'error': f'G-code file not found: {gcode_path}'
                    })
                )]

            info = slicer._analyze_gcode(gcode_path)

            return [TextContent(
                type="text",
                text=json.dumps(info, indent=2)
            )]

        elif name == "optimize_supports":
            input_path = arguments["input_path"]
            output_path = arguments["output_path"]
            support_type = arguments.get("support_type", "auto")

            result = slicer.optimize_supports(input_path, output_path, support_type)

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "get_slicer_info":
            info = {
                'bambu_studio_path': slicer.bambu_path,
                'bambu_studio_found': slicer.bambu_path is not None,
                'supported_printers': list(slicer.printer_profiles.keys()),
                'supported_materials': list(slicer.material_profiles.keys()),
                'quality_presets': list(slicer.quality_profiles.keys()),
                'note': 'Eğer Bambu Studio bulunamadıysa, config.yaml\'da BAMBU_STUDIO_PATH ayarlayın'
            }

            return [TextContent(
                type="text",
                text=json.dumps(info, indent=2)
            )]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Tool execution error: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=f"ERROR: {str(e)}"
        )]


async def main():
    """MCP server'ı başlat"""
    logger.info("Starting Bambu Lab Slicer MCP Server...")
    logger.info("Bambu Studio path: " + (slicer.bambu_path or "NOT FOUND"))
    logger.info("Tools: slice_model, estimate_cost, analyze_gcode, optimize_supports, get_slicer_info")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
