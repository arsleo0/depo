#!/usr/bin/env python3
"""
Blender MCP Server - Claude Desktop ile Blender arasında köprü kurar
Blender 3D modelleme, animasyon, rendering ve daha fazlası için MCP entegrasyonu
"""
import sys
import os
import asyncio
import json
from typing import Any
from pathlib import Path

# CRITICAL: Tüm logları stderr'e yönlendir
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[BLENDER-MCP] %(levelname)s: %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
except ImportError:
    logger.error("mcp paketi bulunamadı. Lütfen yükleyin: pip install mcp")
    sys.exit(1)

# Blender Python modülünü import et
try:
    import bpy
    BLENDER_AVAILABLE = True
    logger.info("Blender Python API yüklendi")
except ImportError:
    BLENDER_AVAILABLE = False
    logger.warning("Blender Python API bulunamadı. Bazı özellikler çalışmayabilir.")
    logger.warning("Blender içinden çalıştırın: blender --background --python blender_mcp_server.py")


class BlenderMCPServer:
    """Blender için MCP sunucusu"""

    def __init__(self):
        self.server = Server("blender-mcp-server")
        self._register_handlers()

    def _register_handlers(self):
        """MCP handler'ları kaydet"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Kullanılabilir araçları listele"""
            logger.info("Blender araçları listeleniyor...")
            return [
                Tool(
                    name="blender_open_file",
                    description="Blender .blend dosyasını aç",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Açılacak .blend dosyasının tam yolu"
                            }
                        },
                        "required": ["filepath"]
                    }
                ),
                Tool(
                    name="blender_save_file",
                    description="Mevcut Blender sahnesini kaydet",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Kaydedilecek .blend dosyasının tam yolu"
                            }
                        },
                        "required": ["filepath"]
                    }
                ),
                Tool(
                    name="blender_get_scene_info",
                    description="Mevcut sahne hakkında bilgi al (objeler, kameralar, ışıklar)",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="blender_create_object",
                    description="Yeni bir 3D obje oluştur (cube, sphere, plane, vb.)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "object_type": {
                                "type": "string",
                                "enum": ["CUBE", "SPHERE", "CYLINDER", "CONE", "PLANE", "TORUS", "MONKEY"],
                                "description": "Oluşturulacak obje tipi"
                            },
                            "name": {
                                "type": "string",
                                "description": "Obje adı"
                            },
                            "location": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "Konum [x, y, z]",
                                "minItems": 3,
                                "maxItems": 3
                            }
                        },
                        "required": ["object_type"]
                    }
                ),
                Tool(
                    name="blender_delete_object",
                    description="Bir objeyi sil",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "object_name": {
                                "type": "string",
                                "description": "Silinecek objenin adı"
                            }
                        },
                        "required": ["object_name"]
                    }
                ),
                Tool(
                    name="blender_render",
                    description="Sahneyi render et ve kaydet",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "output_path": {
                                "type": "string",
                                "description": "Render çıktısının kaydedileceği yol"
                            },
                            "resolution_x": {
                                "type": "integer",
                                "description": "Genişlik (varsayılan: 1920)"
                            },
                            "resolution_y": {
                                "type": "integer",
                                "description": "Yükseklik (varsayılan: 1080)"
                            }
                        },
                        "required": ["output_path"]
                    }
                ),
                Tool(
                    name="blender_run_python",
                    description="Blender içinde Python kodu çalıştır (bpy API kullanarak)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Çalıştırılacak Python kodu"
                            }
                        },
                        "required": ["code"]
                    }
                ),
                Tool(
                    name="blender_add_material",
                    description="Bir objeye material ekle",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "object_name": {
                                "type": "string",
                                "description": "Material eklenecek obje adı"
                            },
                            "material_name": {
                                "type": "string",
                                "description": "Oluşturulacak material adı"
                            },
                            "color": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "RGBA renk değerleri [r, g, b, a] (0-1 arası)",
                                "minItems": 4,
                                "maxItems": 4
                            }
                        },
                        "required": ["object_name", "material_name"]
                    }
                ),
                Tool(
                    name="blender_export",
                    description="Sahneyi farklı formatlarda dışa aktar (FBX, OBJ, GLTF, vb.)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Dışa aktarılacak dosya yolu (uzantısı ile)"
                            },
                            "format": {
                                "type": "string",
                                "enum": ["FBX", "OBJ", "GLTF", "STL", "PLY"],
                                "description": "Dışa aktarma formatı"
                            }
                        },
                        "required": ["filepath", "format"]
                    }
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Tool çağrılarını işle"""
            logger.info(f"Tool çağrıldı: {name} with args: {arguments}")

            if not BLENDER_AVAILABLE:
                return [TextContent(
                    type="text",
                    text="Hata: Blender Python API bulunamadı. Bu scripti Blender içinden çalıştırın:\nblender --background --python blender_mcp_server.py"
                )]

            try:
                if name == "blender_open_file":
                    return await self._open_file(arguments.get("filepath"))
                elif name == "blender_save_file":
                    return await self._save_file(arguments.get("filepath"))
                elif name == "blender_get_scene_info":
                    return await self._get_scene_info()
                elif name == "blender_create_object":
                    return await self._create_object(
                        arguments.get("object_type"),
                        arguments.get("name"),
                        arguments.get("location")
                    )
                elif name == "blender_delete_object":
                    return await self._delete_object(arguments.get("object_name"))
                elif name == "blender_render":
                    return await self._render(
                        arguments.get("output_path"),
                        arguments.get("resolution_x", 1920),
                        arguments.get("resolution_y", 1080)
                    )
                elif name == "blender_run_python":
                    return await self._run_python(arguments.get("code"))
                elif name == "blender_add_material":
                    return await self._add_material(
                        arguments.get("object_name"),
                        arguments.get("material_name"),
                        arguments.get("color")
                    )
                elif name == "blender_export":
                    return await self._export(
                        arguments.get("filepath"),
                        arguments.get("format")
                    )
                else:
                    raise ValueError(f"Bilinmeyen tool: {name}")
            except Exception as e:
                logger.error(f"Tool hatası: {e}", exc_info=True)
                return [TextContent(
                    type="text",
                    text=f"Hata: {str(e)}"
                )]

    async def _open_file(self, filepath: str) -> list[TextContent]:
        """Blender dosyasını aç"""
        try:
            bpy.ops.wm.open_mainfile(filepath=filepath)
            logger.info(f"Dosya açıldı: {filepath}")
            return [TextContent(
                type="text",
                text=f"Başarılı: {filepath} dosyası açıldı"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Dosya açılamadı: {e}"
            )]

    async def _save_file(self, filepath: str) -> list[TextContent]:
        """Blender dosyasını kaydet"""
        try:
            bpy.ops.wm.save_as_mainfile(filepath=filepath)
            logger.info(f"Dosya kaydedildi: {filepath}")
            return [TextContent(
                type="text",
                text=f"Başarılı: {filepath} dosyası kaydedildi"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Dosya kaydedilemedi: {e}"
            )]

    async def _get_scene_info(self) -> list[TextContent]:
        """Sahne bilgilerini al"""
        try:
            scene = bpy.context.scene
            info = {
                "scene_name": scene.name,
                "frame_current": scene.frame_current,
                "frame_start": scene.frame_start,
                "frame_end": scene.frame_end,
                "objects": [],
                "cameras": [],
                "lights": []
            }

            for obj in bpy.data.objects:
                obj_info = {
                    "name": obj.name,
                    "type": obj.type,
                    "location": list(obj.location),
                    "rotation": list(obj.rotation_euler),
                    "scale": list(obj.scale)
                }

                info["objects"].append(obj_info)

                if obj.type == 'CAMERA':
                    info["cameras"].append(obj.name)
                elif obj.type == 'LIGHT':
                    info["lights"].append(obj.name)

            info_text = json.dumps(info, indent=2, ensure_ascii=False)
            return [TextContent(
                type="text",
                text=f"=== Sahne Bilgileri ===\n{info_text}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Sahne bilgisi alınamadı: {e}"
            )]

    async def _create_object(self, object_type: str, name: str = None, location: list = None) -> list[TextContent]:
        """Yeni obje oluştur"""
        try:
            object_type = object_type.upper()

            if object_type == "CUBE":
                bpy.ops.mesh.primitive_cube_add()
            elif object_type == "SPHERE":
                bpy.ops.mesh.primitive_uv_sphere_add()
            elif object_type == "CYLINDER":
                bpy.ops.mesh.primitive_cylinder_add()
            elif object_type == "CONE":
                bpy.ops.mesh.primitive_cone_add()
            elif object_type == "PLANE":
                bpy.ops.mesh.primitive_plane_add()
            elif object_type == "TORUS":
                bpy.ops.mesh.primitive_torus_add()
            elif object_type == "MONKEY":
                bpy.ops.mesh.primitive_monkey_add()
            else:
                return [TextContent(
                    type="text",
                    text=f"Hata: Bilinmeyen obje tipi: {object_type}"
                )]

            obj = bpy.context.active_object

            if name:
                obj.name = name

            if location:
                obj.location = location

            logger.info(f"Obje oluşturuldu: {obj.name} ({object_type})")
            return [TextContent(
                type="text",
                text=f"Başarılı: {obj.name} objesi oluşturuldu (tip: {object_type})"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Obje oluşturulamadı: {e}"
            )]

    async def _delete_object(self, object_name: str) -> list[TextContent]:
        """Objeyi sil"""
        try:
            obj = bpy.data.objects.get(object_name)
            if not obj:
                return [TextContent(
                    type="text",
                    text=f"Hata: Obje bulunamadı: {object_name}"
                )]

            bpy.data.objects.remove(obj, do_unlink=True)
            logger.info(f"Obje silindi: {object_name}")
            return [TextContent(
                type="text",
                text=f"Başarılı: {object_name} objesi silindi"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Obje silinemedi: {e}"
            )]

    async def _render(self, output_path: str, resolution_x: int, resolution_y: int) -> list[TextContent]:
        """Sahneyi render et"""
        try:
            scene = bpy.context.scene
            scene.render.filepath = output_path
            scene.render.resolution_x = resolution_x
            scene.render.resolution_y = resolution_y

            bpy.ops.render.render(write_still=True)
            logger.info(f"Render tamamlandı: {output_path}")
            return [TextContent(
                type="text",
                text=f"Başarılı: Render tamamlandı ve {output_path} konumuna kaydedildi\nÇözünürlük: {resolution_x}x{resolution_y}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Render işlemi başarısız: {e}"
            )]

    async def _run_python(self, code: str) -> list[TextContent]:
        """Python kodu çalıştır"""
        try:
            # Global namespace'e bpy ekle
            exec_globals = {"bpy": bpy}
            exec_locals = {}

            exec(code, exec_globals, exec_locals)

            # Eğer return değeri varsa göster
            result = exec_locals.get("result", "Kod başarıyla çalıştırıldı (output yok)")

            logger.info("Python kodu çalıştırıldı")
            return [TextContent(
                type="text",
                text=f"Başarılı: Python kodu çalıştırıldı\nSonuç: {result}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Python kodu çalıştırılamadı: {e}"
            )]

    async def _add_material(self, object_name: str, material_name: str, color: list = None) -> list[TextContent]:
        """Objeye material ekle"""
        try:
            obj = bpy.data.objects.get(object_name)
            if not obj:
                return [TextContent(
                    type="text",
                    text=f"Hata: Obje bulunamadı: {object_name}"
                )]

            # Material oluştur
            mat = bpy.data.materials.new(name=material_name)
            mat.use_nodes = True

            # Eğer renk verilmişse ayarla
            if color and len(color) == 4:
                bsdf = mat.node_tree.nodes.get("Principled BSDF")
                if bsdf:
                    bsdf.inputs["Base Color"].default_value = color

            # Objeye material ekle
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)

            logger.info(f"Material eklendi: {material_name} -> {object_name}")
            return [TextContent(
                type="text",
                text=f"Başarılı: {material_name} materiali {object_name} objesine eklendi"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Material eklenemedi: {e}"
            )]

    async def _export(self, filepath: str, format: str) -> list[TextContent]:
        """Sahneyi dışa aktar"""
        try:
            format = format.upper()

            if format == "FBX":
                bpy.ops.export_scene.fbx(filepath=filepath)
            elif format == "OBJ":
                bpy.ops.export_scene.obj(filepath=filepath)
            elif format == "GLTF":
                bpy.ops.export_scene.gltf(filepath=filepath)
            elif format == "STL":
                bpy.ops.export_mesh.stl(filepath=filepath)
            elif format == "PLY":
                bpy.ops.export_mesh.ply(filepath=filepath)
            else:
                return [TextContent(
                    type="text",
                    text=f"Hata: Desteklenmeyen format: {format}"
                )]

            logger.info(f"Export tamamlandı: {filepath} ({format})")
            return [TextContent(
                type="text",
                text=f"Başarılı: Sahne {format} formatında dışa aktarıldı: {filepath}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Dışa aktarma başarısız: {e}"
            )]


async def main():
    """Ana fonksiyon"""
    logger.info("Blender MCP Server başlatılıyor...")

    if not BLENDER_AVAILABLE:
        logger.error("Blender Python API bulunamadı!")
        logger.error("Bu scripti Blender içinden çalıştırın:")
        logger.error("  blender --background --python blender_mcp_server.py")

    blender_server = BlenderMCPServer()

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Blender MCP server hazır ve bağlantı bekliyor...")
        await blender_server.server.run(
            read_stream,
            write_stream,
            blender_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
