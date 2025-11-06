#!/usr/bin/env python3
"""
Maya MCP Server - Claude Desktop ile Autodesk Maya arasında köprü kurar
3D modelleme, animasyon, rendering ve daha fazlası için MCP entegrasyonu
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
    format='[MAYA-MCP] %(levelname)s: %(message)s',
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

# Maya Python modülünü import et
try:
    import maya.cmds as cmds
    import maya.standalone
    MAYA_AVAILABLE = True
    logger.info("Maya Python API yüklendi")
except ImportError:
    MAYA_AVAILABLE = False
    logger.warning("Maya Python API bulunamadı. Bazı özellikler çalışmayabilir.")
    logger.warning("Maya içinden çalıştırın veya mayapy kullanın: mayapy maya_mcp_server.py")


class MayaMCPServer:
    """Autodesk Maya için MCP sunucusu"""

    def __init__(self):
        self.server = Server("maya-mcp-server")
        self._maya_initialized = False
        self._register_handlers()

    def _initialize_maya(self):
        """Maya standalone'ı başlat"""
        if not MAYA_AVAILABLE:
            return False

        if not self._maya_initialized:
            try:
                maya.standalone.initialize()
                self._maya_initialized = True
                logger.info("Maya standalone başlatıldı")
            except Exception as e:
                logger.error(f"Maya başlatılamadı: {e}")
                return False
        return True

    def _register_handlers(self):
        """MCP handler'ları kaydet"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Kullanılabilir araçları listele"""
            logger.info("Maya araçları listeleniyor...")
            return [
                Tool(
                    name="maya_open_file",
                    description="Maya .ma veya .mb dosyasını aç",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Açılacak Maya dosyasının tam yolu"
                            }
                        },
                        "required": ["filepath"]
                    }
                ),
                Tool(
                    name="maya_save_file",
                    description="Mevcut Maya sahnesini kaydet",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Kaydedilecek dosyanın tam yolu"
                            },
                            "file_type": {
                                "type": "string",
                                "enum": ["mayaAscii", "mayaBinary"],
                                "description": "Dosya tipi (varsayılan: mayaAscii)"
                            }
                        },
                        "required": ["filepath"]
                    }
                ),
                Tool(
                    name="maya_new_scene",
                    description="Yeni bir boş sahne oluştur",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "force": {
                                "type": "boolean",
                                "description": "Kaydetmeden yeni sahne aç (varsayılan: false)"
                            }
                        }
                    }
                ),
                Tool(
                    name="maya_get_scene_info",
                    description="Mevcut sahne hakkında bilgi al (objeler, kameralar, ışıklar)",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="maya_create_polygon",
                    description="Polygon obje oluştur (küp, küre, silindir, vb.)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "object_type": {
                                "type": "string",
                                "enum": ["cube", "sphere", "cylinder", "cone", "plane", "torus"],
                                "description": "Oluşturulacak obje tipi"
                            },
                            "name": {
                                "type": "string",
                                "description": "Obje adı"
                            }
                        },
                        "required": ["object_type"]
                    }
                ),
                Tool(
                    name="maya_create_light",
                    description="Işık oluştur",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "light_type": {
                                "type": "string",
                                "enum": ["directional", "point", "spot", "area"],
                                "description": "Işık tipi"
                            },
                            "name": {
                                "type": "string",
                                "description": "Işık adı"
                            }
                        },
                        "required": ["light_type"]
                    }
                ),
                Tool(
                    name="maya_create_camera",
                    description="Kamera oluştur",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Kamera adı"
                            }
                        }
                    }
                ),
                Tool(
                    name="maya_delete_object",
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
                    name="maya_select",
                    description="Obje(leri) seç",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "objects": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Seçilecek obje adları"
                            }
                        },
                        "required": ["objects"]
                    }
                ),
                Tool(
                    name="maya_transform",
                    description="Obje transformasyonu (move, rotate, scale)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "object_name": {
                                "type": "string",
                                "description": "Transform edilecek obje adı"
                            },
                            "translate": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "Konum [x, y, z]",
                                "minItems": 3,
                                "maxItems": 3
                            },
                            "rotate": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "Rotasyon [x, y, z] (derece)",
                                "minItems": 3,
                                "maxItems": 3
                            },
                            "scale": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "Ölçek [x, y, z]",
                                "minItems": 3,
                                "maxItems": 3
                            }
                        },
                        "required": ["object_name"]
                    }
                ),
                Tool(
                    name="maya_render",
                    description="Sahneyi render et",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "output_path": {
                                "type": "string",
                                "description": "Render çıktısının kaydedileceği yol"
                            },
                            "camera": {
                                "type": "string",
                                "description": "Kullanılacak kamera adı (varsayılan: persp)"
                            },
                            "width": {
                                "type": "integer",
                                "description": "Genişlik (varsayılan: 1920)"
                            },
                            "height": {
                                "type": "integer",
                                "description": "Yükseklik (varsayılan: 1080)"
                            }
                        },
                        "required": ["output_path"]
                    }
                ),
                Tool(
                    name="maya_run_mel",
                    description="MEL komut çalıştır",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "Çalıştırılacak MEL komutu"
                            }
                        },
                        "required": ["command"]
                    }
                ),
                Tool(
                    name="maya_run_python",
                    description="Maya içinde Python kodu çalıştır (maya.cmds kullanarak)",
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
                    name="maya_export",
                    description="Sahneyi farklı formatlarda dışa aktar",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Dışa aktarılacak dosya yolu"
                            },
                            "format": {
                                "type": "string",
                                "enum": ["FBX", "OBJ", "Alembic"],
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

            if not MAYA_AVAILABLE:
                return [TextContent(
                    type="text",
                    text="Hata: Maya Python API bulunamadı. Maya içinden veya mayapy ile çalıştırın:\nmayapy maya_mcp_server.py"
                )]

            # Maya'yı başlat
            if not self._initialize_maya():
                return [TextContent(
                    type="text",
                    text="Hata: Maya başlatılamadı"
                )]

            try:
                if name == "maya_open_file":
                    return await self._open_file(arguments.get("filepath"))
                elif name == "maya_save_file":
                    return await self._save_file(
                        arguments.get("filepath"),
                        arguments.get("file_type", "mayaAscii")
                    )
                elif name == "maya_new_scene":
                    return await self._new_scene(arguments.get("force", False))
                elif name == "maya_get_scene_info":
                    return await self._get_scene_info()
                elif name == "maya_create_polygon":
                    return await self._create_polygon(
                        arguments.get("object_type"),
                        arguments.get("name")
                    )
                elif name == "maya_create_light":
                    return await self._create_light(
                        arguments.get("light_type"),
                        arguments.get("name")
                    )
                elif name == "maya_create_camera":
                    return await self._create_camera(arguments.get("name"))
                elif name == "maya_delete_object":
                    return await self._delete_object(arguments.get("object_name"))
                elif name == "maya_select":
                    return await self._select(arguments.get("objects"))
                elif name == "maya_transform":
                    return await self._transform(
                        arguments.get("object_name"),
                        arguments.get("translate"),
                        arguments.get("rotate"),
                        arguments.get("scale")
                    )
                elif name == "maya_render":
                    return await self._render(
                        arguments.get("output_path"),
                        arguments.get("camera", "persp"),
                        arguments.get("width", 1920),
                        arguments.get("height", 1080)
                    )
                elif name == "maya_run_mel":
                    return await self._run_mel(arguments.get("command"))
                elif name == "maya_run_python":
                    return await self._run_python(arguments.get("code"))
                elif name == "maya_export":
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
        """Maya dosyasını aç"""
        try:
            cmds.file(filepath, open=True, force=True)
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

    async def _save_file(self, filepath: str, file_type: str) -> list[TextContent]:
        """Maya dosyasını kaydet"""
        try:
            cmds.file(rename=filepath)
            cmds.file(save=True, type=file_type)
            logger.info(f"Dosya kaydedildi: {filepath} ({file_type})")
            return [TextContent(
                type="text",
                text=f"Başarılı: {filepath} dosyası kaydedildi (tip: {file_type})"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Dosya kaydedilemedi: {e}"
            )]

    async def _new_scene(self, force: bool) -> list[TextContent]:
        """Yeni sahne oluştur"""
        try:
            cmds.file(new=True, force=force)
            logger.info("Yeni sahne oluşturuldu")
            return [TextContent(
                type="text",
                text="Başarılı: Yeni sahne oluşturuldu"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Yeni sahne oluşturulamadı: {e}"
            )]

    async def _get_scene_info(self) -> list[TextContent]:
        """Sahne bilgilerini al"""
        try:
            info = {
                "scene_name": cmds.file(query=True, sceneName=True) or "Kaydedilmemiş",
                "objects": [],
                "cameras": [],
                "lights": []
            }

            # Tüm transform node'larını al
            all_objects = cmds.ls(type="transform")

            for obj in all_objects:
                obj_type = "transform"
                shapes = cmds.listRelatives(obj, shapes=True) or []

                if shapes:
                    shape_type = cmds.nodeType(shapes[0])
                    if shape_type == "camera":
                        info["cameras"].append(obj)
                        obj_type = "camera"
                    elif "light" in shape_type.lower():
                        info["lights"].append(obj)
                        obj_type = "light"

                # Pozisyon bilgisi
                position = cmds.xform(obj, query=True, worldSpace=True, translation=True)
                rotation = cmds.xform(obj, query=True, worldSpace=True, rotation=True)

                info["objects"].append({
                    "name": obj,
                    "type": obj_type,
                    "position": position,
                    "rotation": rotation
                })

            info_text = json.dumps(info, indent=2, ensure_ascii=False)
            return [TextContent(
                type="text",
                text=f"=== Maya Sahne Bilgileri ===\n{info_text}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Sahne bilgisi alınamadı: {e}"
            )]

    async def _create_polygon(self, object_type: str, name: str = None) -> list[TextContent]:
        """Polygon obje oluştur"""
        try:
            if object_type == "cube":
                obj = cmds.polyCube()[0]
            elif object_type == "sphere":
                obj = cmds.polySphere()[0]
            elif object_type == "cylinder":
                obj = cmds.polyCylinder()[0]
            elif object_type == "cone":
                obj = cmds.polyCone()[0]
            elif object_type == "plane":
                obj = cmds.polyPlane()[0]
            elif object_type == "torus":
                obj = cmds.polyTorus()[0]
            else:
                return [TextContent(
                    type="text",
                    text=f"Hata: Bilinmeyen obje tipi: {object_type}"
                )]

            if name:
                obj = cmds.rename(obj, name)

            logger.info(f"Polygon oluşturuldu: {obj} ({object_type})")
            return [TextContent(
                type="text",
                text=f"Başarılı: {obj} polygon objesi oluşturuldu (tip: {object_type})"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Polygon oluşturulamadı: {e}"
            )]

    async def _create_light(self, light_type: str, name: str = None) -> list[TextContent]:
        """Işık oluştur"""
        try:
            if light_type == "directional":
                light = cmds.directionalLight()
            elif light_type == "point":
                light = cmds.pointLight()
            elif light_type == "spot":
                light = cmds.spotLight()
            elif light_type == "area":
                light = cmds.areaLight()
            else:
                return [TextContent(
                    type="text",
                    text=f"Hata: Bilinmeyen ışık tipi: {light_type}"
                )]

            # Transform node'u al
            light_transform = cmds.listRelatives(light, parent=True)[0]

            if name:
                light_transform = cmds.rename(light_transform, name)

            logger.info(f"Işık oluşturuldu: {light_transform} ({light_type})")
            return [TextContent(
                type="text",
                text=f"Başarılı: {light_transform} ışığı oluşturuldu (tip: {light_type})"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Işık oluşturulamadı: {e}"
            )]

    async def _create_camera(self, name: str = None) -> list[TextContent]:
        """Kamera oluştur"""
        try:
            camera = cmds.camera()[0]

            if name:
                camera = cmds.rename(camera, name)

            logger.info(f"Kamera oluşturuldu: {camera}")
            return [TextContent(
                type="text",
                text=f"Başarılı: {camera} kamerası oluşturuldu"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Kamera oluşturulamadı: {e}"
            )]

    async def _delete_object(self, object_name: str) -> list[TextContent]:
        """Objeyi sil"""
        try:
            if not cmds.objExists(object_name):
                return [TextContent(
                    type="text",
                    text=f"Hata: Obje bulunamadı: {object_name}"
                )]

            cmds.delete(object_name)
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

    async def _select(self, objects: list) -> list[TextContent]:
        """Objeleri seç"""
        try:
            cmds.select(objects)
            logger.info(f"Seçildi: {objects}")
            return [TextContent(
                type="text",
                text=f"Başarılı: {len(objects)} obje seçildi: {', '.join(objects)}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Seçim yapılamadı: {e}"
            )]

    async def _transform(self, object_name: str, translate: list, rotate: list, scale: list) -> list[TextContent]:
        """Obje transformasyonu"""
        try:
            if not cmds.objExists(object_name):
                return [TextContent(
                    type="text",
                    text=f"Hata: Obje bulunamadı: {object_name}"
                )]

            if translate:
                cmds.move(translate[0], translate[1], translate[2], object_name, absolute=True)
            if rotate:
                cmds.rotate(rotate[0], rotate[1], rotate[2], object_name, absolute=True)
            if scale:
                cmds.scale(scale[0], scale[1], scale[2], object_name, absolute=True)

            logger.info(f"Transform uygulandı: {object_name}")
            result = []
            if translate:
                result.append(f"Konum: {translate}")
            if rotate:
                result.append(f"Rotasyon: {rotate}")
            if scale:
                result.append(f"Ölçek: {scale}")

            return [TextContent(
                type="text",
                text=f"Başarılı: {object_name} transform edildi\n" + "\n".join(result)
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Transform uygulanamadı: {e}"
            )]

    async def _render(self, output_path: str, camera: str, width: int, height: int) -> list[TextContent]:
        """Render işlemi"""
        try:
            # Render ayarları
            cmds.setAttr("defaultResolution.width", width)
            cmds.setAttr("defaultResolution.height", height)

            # Render et
            cmds.render(camera, x=width, y=height)

            # Render'ı kaydet
            cmds.renderWindowEditor("renderView", edit=True, writeImage=output_path)

            logger.info(f"Render tamamlandı: {output_path}")
            return [TextContent(
                type="text",
                text=f"Başarılı: Render tamamlandı ve {output_path} konumuna kaydedildi\nKamera: {camera}\nÇözünürlük: {width}x{height}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Render işlemi başarısız: {e}"
            )]

    async def _run_mel(self, command: str) -> list[TextContent]:
        """MEL komut çalıştır"""
        try:
            result = cmds.mel.eval(command)
            logger.info(f"MEL komutu çalıştırıldı: {command}")
            return [TextContent(
                type="text",
                text=f"Başarılı: MEL komutu çalıştırıldı\nKomut: {command}\nSonuç: {result}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: MEL komutu çalıştırılamadı: {e}"
            )]

    async def _run_python(self, code: str) -> list[TextContent]:
        """Python kodu çalıştır"""
        try:
            exec_globals = {"cmds": cmds}
            exec_locals = {}

            exec(code, exec_globals, exec_locals)
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

    async def _export(self, filepath: str, format: str) -> list[TextContent]:
        """Sahneyi dışa aktar"""
        try:
            format_map = {
                "FBX": "FBX export",
                "OBJ": "OBJexport",
                "Alembic": "Alembic"
            }

            file_type = format_map.get(format)
            if not file_type:
                return [TextContent(
                    type="text",
                    text=f"Hata: Desteklenmeyen format: {format}"
                )]

            cmds.file(filepath, force=True, options="", type=file_type, exportAll=True)

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
    logger.info("Maya MCP Server başlatılıyor...")

    if not MAYA_AVAILABLE:
        logger.error("Maya Python API bulunamadı!")
        logger.error("Maya içinden veya mayapy ile çalıştırın:")
        logger.error("  mayapy maya_mcp_server.py")

    maya_server = MayaMCPServer()

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Maya MCP server hazır ve bağlantı bekliyor...")
        await maya_server.server.run(
            read_stream,
            write_stream,
            maya_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
