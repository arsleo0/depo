#!/usr/bin/env python3
"""
3D Model Generator MCP Server
3D Print Ecosystem - Blender ve Hyper3D entegrasyonu

Bu sunucu Claude Desktop'ın 3D model oluşturmasını, düzenlemesini ve
optimize etmesini sağlar.
"""

import asyncio
import json
import os
import sys
import subprocess
import tempfile
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

try:
    import requests
except ImportError:
    print("ERROR: Install requirements: pip install requests", file=sys.stderr)
    sys.exit(1)

# Logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("model-generator-server")

# Server instance
app = Server("3d-print-model-generator")


class BlenderController:
    """Blender Python API controller"""

    def __init__(self, blender_path: Optional[str] = None):
        self.blender_path = blender_path or self._find_blender()
        if not self.blender_path:
            logger.warning("Blender not found in PATH. Model generation may fail.")

    def _find_blender(self) -> Optional[str]:
        """Blender executable bul"""
        # Windows yolları
        common_paths = [
            r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender\blender.exe",
        ]

        # PATH'de ara
        try:
            result = subprocess.run(
                ["where", "blender"] if os.name == 'nt' else ["which", "blender"],
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

    def run_blender_script(self, script: str, background=True) -> Dict[str, Any]:
        """Blender Python scripti çalıştır"""
        if not self.blender_path:
            raise RuntimeError("Blender executable not found")

        logger.info("Running Blender script...")

        # Temporary script file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(script)
            script_path = f.name

        try:
            # Blender'ı background modda çalıştır
            cmd = [self.blender_path]
            if background:
                cmd.extend(['--background', '--python', script_path])
            else:
                cmd.extend(['--python', script_path])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            # Script'i temizle
            os.unlink(script_path)

            if result.returncode != 0:
                logger.error(f"Blender error: {result.stderr}")
                return {
                    'success': False,
                    'error': result.stderr,
                    'output': result.stdout
                }

            return {
                'success': True,
                'output': result.stdout,
                'stderr': result.stderr
            }

        except subprocess.TimeoutExpired:
            os.unlink(script_path)
            return {
                'success': False,
                'error': 'Blender script timeout (60s)'
            }
        except Exception as e:
            if os.path.exists(script_path):
                os.unlink(script_path)
            return {
                'success': False,
                'error': str(e)
            }

    def create_parametric_model(self, model_type: str, parameters: Dict[str, Any], output_path: str) -> Dict[str, Any]:
        """Parametrik model oluştur"""
        logger.info(f"Creating parametric {model_type} model...")

        # Parametrik model şablonları
        if model_type == "cylinder":
            script = self._generate_cylinder_script(parameters, output_path)
        elif model_type == "cube":
            script = self._generate_cube_script(parameters, output_path)
        elif model_type == "sphere":
            script = self._generate_sphere_script(parameters, output_path)
        elif model_type == "torus":
            script = self._generate_torus_script(parameters, output_path)
        elif model_type == "plant_pot":
            script = self._generate_plant_pot_script(parameters, output_path)
        else:
            return {'success': False, 'error': f'Unknown model type: {model_type}'}

        result = self.run_blender_script(script)

        if result['success']:
            result['output_file'] = output_path
            result['model_type'] = model_type

        return result

    def _generate_cylinder_script(self, params: Dict, output: str) -> str:
        radius = params.get('radius', 1.0)
        height = params.get('height', 2.0)
        vertices = params.get('vertices', 32)

        return f'''
import bpy
import math

# Sahneyi temizle
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Cylinder oluştur
bpy.ops.mesh.primitive_cylinder_add(
    vertices={vertices},
    radius={radius},
    depth={height},
    location=(0, 0, 0)
)

# Export STL
bpy.ops.export_mesh.stl(filepath=r"{output}")
print("SUCCESS: Cylinder exported to {output}")
'''

    def _generate_cube_script(self, params: Dict, output: str) -> str:
        size = params.get('size', 2.0)

        return f'''
import bpy

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

bpy.ops.mesh.primitive_cube_add(size={size}, location=(0, 0, 0))

bpy.ops.export_mesh.stl(filepath=r"{output}")
print("SUCCESS: Cube exported")
'''

    def _generate_sphere_script(self, params: Dict, output: str) -> str:
        radius = params.get('radius', 1.0)
        subdivisions = params.get('subdivisions', 2)

        return f'''
import bpy

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

bpy.ops.mesh.primitive_uv_sphere_add(radius={radius}, location=(0, 0, 0))

obj = bpy.context.active_object
modifier = obj.modifiers.new(name='Subsurf', type='SUBSURF')
modifier.levels = {subdivisions}

bpy.ops.export_mesh.stl(filepath=r"{output}")
print("SUCCESS: Sphere exported")
'''

    def _generate_torus_script(self, params: Dict, output: str) -> str:
        major_radius = params.get('major_radius', 1.0)
        minor_radius = params.get('minor_radius', 0.25)

        return f'''
import bpy

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

bpy.ops.mesh.primitive_torus_add(
    major_radius={major_radius},
    minor_radius={minor_radius},
    location=(0, 0, 0)
)

bpy.ops.export_mesh.stl(filepath=r"{output}")
print("SUCCESS: Torus exported")
'''

    def _generate_plant_pot_script(self, params: Dict, output: str) -> str:
        """Plant pot (saksı) oluştur"""
        diameter = params.get('diameter', 10.0)
        height = params.get('height', 10.0)
        wall_thickness = params.get('wall_thickness', 0.2)
        drainage_hole = params.get('drainage_hole', True)

        return f'''
import bpy
import bmesh

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Dış silindir
bpy.ops.mesh.primitive_cylinder_add(
    vertices=64,
    radius={diameter/2},
    depth={height},
    location=(0, 0, {height/2})
)

outer = bpy.context.active_object

# İç silindir (boşluk)
bpy.ops.mesh.primitive_cylinder_add(
    vertices=64,
    radius={diameter/2 - wall_thickness},
    depth={height},
    location=(0, 0, {height/2 + 0.5})
)

inner = bpy.context.active_object

# Boolean modifier ile boşluk oluştur
mod = outer.modifiers.new(name='Boolean', type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = inner

bpy.context.view_layer.objects.active = outer
bpy.ops.object.modifier_apply(modifier='Boolean')

# İç silindiri sil
bpy.ops.object.select_all(action='DESELECT')
inner.select_set(True)
bpy.ops.object.delete()

# Drainage hole
if {str(drainage_hole).lower()}:
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.5,
        depth=1,
        location=(0, 0, 0),
        rotation=(0, 0, 0)
    )

    hole = bpy.context.active_object

    mod = outer.modifiers.new(name='DrainageHole', type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = hole

    bpy.context.view_layer.objects.active = outer
    bpy.ops.object.modifier_apply(modifier='DrainageHole')

    bpy.ops.object.select_all(action='DESELECT')
    hole.select_set(True)
    bpy.ops.object.delete()

# Select outer pot and export
bpy.ops.object.select_all(action='DESELECT')
outer.select_set(True)

bpy.ops.export_mesh.stl(filepath=r"{output}")
print("SUCCESS: Plant pot exported")
'''

    def optimize_for_printing(self, input_path: str, output_path: str) -> Dict[str, Any]:
        """3D baskı için model optimize et"""
        logger.info(f"Optimizing model for printing: {input_path}")

        script = f'''
import bpy

# Mevcut sahneyi temizle
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Model import
bpy.ops.import_mesh.stl(filepath=r"{input_path}")

obj = bpy.context.selected_objects[0]
bpy.context.view_layer.objects.active = obj

# Manifold olup olmadığını kontrol et ve düzelt
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Non-manifold kenarları onar
bpy.ops.mesh.select_non_manifold()
bpy.ops.mesh.fill_holes()

bpy.ops.object.mode_set(mode='OBJECT')

# Normals'ları düzelt
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode='OBJECT')

# Decimate (polygon sayısını azalt - opsiyonel)
# modifier = obj.modifiers.new(name='Decimate', type='DECIMATE')
# modifier.ratio = 0.5
# bpy.ops.object.modifier_apply(modifier='Decimate')

# Export
bpy.ops.export_mesh.stl(filepath=r"{output_path}")
print("SUCCESS: Optimized model exported")
'''

        return self.run_blender_script(script)


class Hyper3DClient:
    """Hyper3D API client - AI ile 3D model generation"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('HYPER3D_API_KEY')
        self.base_url = "https://api.hyper3d.ai/v1"  # Örnek URL

    def generate_model(self, prompt: str, style: str = "default") -> Dict[str, Any]:
        """AI ile 3D model oluştur"""
        if not self.api_key:
            return {
                'success': False,
                'error': 'HYPER3D_API_KEY not set. Set it in environment or config.yaml',
                'note': 'For now, using parametric models instead'
            }

        logger.info(f"Generating 3D model with Hyper3D: {prompt}")

        # Hyper3D API call (örnek)
        # Not: Gerçek API endpoint ve format API dokümantasyonuna göre ayarlanmalı
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'prompt': prompt,
                    'style': style,
                    'format': 'stl'
                },
                timeout=120
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'model_url': data.get('model_url'),
                    'job_id': data.get('job_id')
                }
            else:
                return {
                    'success': False,
                    'error': f'API error: {response.status_code}',
                    'message': response.text
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def download_model(self, model_url: str, output_path: str) -> Dict[str, Any]:
        """Generated modeli indir"""
        try:
            response = requests.get(model_url, stream=True, timeout=60)

            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                return {
                    'success': True,
                    'output_path': output_path
                }
            else:
                return {
                    'success': False,
                    'error': f'Download failed: {response.status_code}'
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Global instances
blender = BlenderController()
hyper3d = Hyper3DClient()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """MCP araçlarını listele"""
    return [
        Tool(
            name="create_parametric_model",
            description="Parametrik 3D model oluştur (cylinder, cube, sphere, torus, plant_pot). Blender kullanır.",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_type": {
                        "type": "string",
                        "enum": ["cylinder", "cube", "sphere", "torus", "plant_pot"],
                        "description": "Model tipi"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Model parametreleri (radius, height, size, vb.)"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output STL dosya yolu (örn: C:\\Users\\Name\\model.stl)"
                    }
                },
                "required": ["model_type", "output_path"]
            }
        ),
        Tool(
            name="generate_model_with_ai",
            description="Hyper3D AI ile text-to-3D model oluştur. Prompt'tan otomatik model üretir.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Model açıklaması (örn: 'modern minimalist vase with geometric patterns')"
                    },
                    "style": {
                        "type": "string",
                        "enum": ["default", "low_poly", "realistic", "stylized"],
                        "description": "Model stili",
                        "default": "default"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output STL dosya yolu"
                    }
                },
                "required": ["prompt", "output_path"]
            }
        ),
        Tool(
            name="optimize_for_printing",
            description="3D modeli baskıya hazırla (manifold check, normals fix, vb.). STL input/output.",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Input STL dosyası"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optimize edilmiş output STL"
                    }
                },
                "required": ["input_path", "output_path"]
            }
        ),
        Tool(
            name="run_custom_blender_script",
            description="Özel Blender Python scripti çalıştır. İleri düzey kullanıcılar için.",
            inputSchema={
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "Blender Python (bpy) scripti"
                    },
                    "background": {
                        "type": "boolean",
                        "description": "Background modda çalıştır (GUI yok)",
                        "default": True
                    }
                },
                "required": ["script"]
            }
        ),
        Tool(
            name="get_blender_info",
            description="Blender kurulumu ve versiyonu hakkında bilgi al",
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
        if name == "create_parametric_model":
            model_type = arguments["model_type"]
            parameters = arguments.get("parameters", {})
            output_path = arguments["output_path"]

            # Dizini oluştur
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            result = blender.create_parametric_model(model_type, parameters, output_path)

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "generate_model_with_ai":
            prompt = arguments["prompt"]
            style = arguments.get("style", "default")
            output_path = arguments["output_path"]

            # AI generation
            gen_result = hyper3d.generate_model(prompt, style)

            if not gen_result['success']:
                return [TextContent(
                    type="text",
                    text=json.dumps(gen_result, indent=2)
                )]

            # Model indir
            download_result = hyper3d.download_model(gen_result['model_url'], output_path)

            output = {
                'generation': gen_result,
                'download': download_result,
                'final_path': output_path if download_result['success'] else None
            }

            return [TextContent(
                type="text",
                text=json.dumps(output, indent=2)
            )]

        elif name == "optimize_for_printing":
            input_path = arguments["input_path"]
            output_path = arguments["output_path"]

            if not os.path.exists(input_path):
                return [TextContent(
                    type="text",
                    text=json.dumps({'success': False, 'error': f'Input file not found: {input_path}'})
                )]

            result = blender.optimize_for_printing(input_path, output_path)

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "run_custom_blender_script":
            script = arguments["script"]
            background = arguments.get("background", True)

            result = blender.run_blender_script(script, background)

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "get_blender_info":
            info = {
                'blender_path': blender.blender_path,
                'blender_found': blender.blender_path is not None,
                'note': 'Eğer Blender bulunamadıysa, config.yaml\'da BLENDER_PATH ayarlayın'
            }

            # Version check
            if blender.blender_path:
                try:
                    result = subprocess.run(
                        [blender.blender_path, '--version'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    info['version_output'] = result.stdout.split('\n')[0]
                except:
                    info['version_output'] = 'Unable to get version'

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
    logger.info("Starting 3D Model Generator MCP Server...")
    logger.info("Blender path: " + (blender.blender_path or "NOT FOUND"))
    logger.info("Tools: create_parametric_model, generate_model_with_ai, optimize_for_printing, run_custom_blender_script, get_blender_info")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
