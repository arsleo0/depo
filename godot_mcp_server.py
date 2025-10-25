#!/usr/bin/env python3
"""
Godot MCP Server - Claude Desktop ile Godot arasında köprü kurar
"""
import sys
import os
import asyncio
import json
from typing import Any
from pathlib import Path

# CRITICAL: Tüm logları stderr'e yönlendir
# stdout sadece MCP JSON-RPC mesajları için kullanılmalı
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[GODOT-MCP] %(levelname)s: %(message)s',
    stream=sys.stderr  # stdout DEĞİL, stderr kullan!
)
logger = logging.getLogger(__name__)

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
    import mcp.server.stdio
except ImportError:
    logger.error("mcp paketi bulunamadı. Lütfen yükleyin: pip install mcp")
    sys.exit(1)


class GodotMCPServer:
    """Godot Engine için MCP sunucusu"""

    def __init__(self):
        self.server = Server("godot-mcp-server")
        self.godot_project_path: str | None = None

        # Tool'ları kaydet
        self._register_handlers()

    def _register_handlers(self):
        """MCP handler'ları kaydet"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Kullanılabilir araçları listele"""
            logger.info("Araçlar listeleniyor...")
            return [
                Tool(
                    name="set_godot_project",
                    description="Godot proje yolunu ayarla",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Godot project.godot dosyasının bulunduğu dizin"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="list_godot_scenes",
                    description="Godot projesindeki tüm .tscn dosyalarını listele",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="list_godot_scripts",
                    description="Godot projesindeki tüm .gd (GDScript) dosyalarını listele",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="read_godot_script",
                    description="Bir GDScript dosyasını oku",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "script_path": {
                                "type": "string",
                                "description": "Okunacak .gd dosyasının yolu"
                            }
                        },
                        "required": ["script_path"]
                    }
                ),
                Tool(
                    name="write_godot_script",
                    description="Bir GDScript dosyası yaz veya güncelle",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "script_path": {
                                "type": "string",
                                "description": "Yazılacak .gd dosyasının yolu"
                            },
                            "content": {
                                "type": "string",
                                "description": "Dosya içeriği"
                            }
                        },
                        "required": ["script_path", "content"]
                    }
                ),
                Tool(
                    name="read_godot_scene",
                    description="Bir Godot sahne dosyasını (.tscn) oku",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "scene_path": {
                                "type": "string",
                                "description": "Okunacak .tscn dosyasının yolu"
                            }
                        },
                        "required": ["scene_path"]
                    }
                ),
                Tool(
                    name="get_project_info",
                    description="Godot proje bilgilerini al (project.godot)",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Tool çağrılarını işle"""
            logger.info(f"Tool çağrıldı: {name} with args: {arguments}")

            try:
                if name == "set_godot_project":
                    return await self._set_godot_project(arguments.get("path"))
                elif name == "list_godot_scenes":
                    return await self._list_godot_scenes()
                elif name == "list_godot_scripts":
                    return await self._list_godot_scripts()
                elif name == "read_godot_script":
                    return await self._read_godot_script(arguments.get("script_path"))
                elif name == "write_godot_script":
                    return await self._write_godot_script(
                        arguments.get("script_path"),
                        arguments.get("content")
                    )
                elif name == "read_godot_scene":
                    return await self._read_godot_scene(arguments.get("scene_path"))
                elif name == "get_project_info":
                    return await self._get_project_info()
                else:
                    raise ValueError(f"Bilinmeyen tool: {name}")
            except Exception as e:
                logger.error(f"Tool hatası: {e}", exc_info=True)
                return [TextContent(
                    type="text",
                    text=f"Hata: {str(e)}"
                )]

    async def _set_godot_project(self, path: str) -> list[TextContent]:
        """Godot proje yolunu ayarla"""
        project_path = Path(path).resolve()

        if not project_path.exists():
            return [TextContent(
                type="text",
                text=f"Hata: Dizin bulunamadı: {project_path}"
            )]

        # project.godot dosyasını ara
        project_file = project_path / "project.godot"
        if not project_file.exists():
            return [TextContent(
                type="text",
                text=f"Hata: project.godot bulunamadı: {project_file}"
            )]

        self.godot_project_path = str(project_path)
        logger.info(f"Godot proje yolu ayarlandı: {self.godot_project_path}")

        return [TextContent(
            type="text",
            text=f"Godot proje yolu ayarlandı: {self.godot_project_path}"
        )]

    async def _list_godot_scenes(self) -> list[TextContent]:
        """Tüm sahne dosyalarını listele"""
        if not self.godot_project_path:
            return [TextContent(
                type="text",
                text="Hata: Önce set_godot_project ile proje yolunu ayarlayın"
            )]

        scenes = list(Path(self.godot_project_path).rglob("*.tscn"))
        scenes_text = "\n".join([str(s.relative_to(self.godot_project_path)) for s in scenes])

        return [TextContent(
            type="text",
            text=f"Godot Sahneleri ({len(scenes)} adet):\n{scenes_text}"
        )]

    async def _list_godot_scripts(self) -> list[TextContent]:
        """Tüm script dosyalarını listele"""
        if not self.godot_project_path:
            return [TextContent(
                type="text",
                text="Hata: Önce set_godot_project ile proje yolunu ayarlayın"
            )]

        scripts = list(Path(self.godot_project_path).rglob("*.gd"))
        scripts_text = "\n".join([str(s.relative_to(self.godot_project_path)) for s in scripts])

        return [TextContent(
            type="text",
            text=f"GDScript Dosyaları ({len(scripts)} adet):\n{scripts_text}"
        )]

    async def _read_godot_script(self, script_path: str) -> list[TextContent]:
        """GDScript dosyasını oku"""
        if not self.godot_project_path:
            return [TextContent(
                type="text",
                text="Hata: Önce set_godot_project ile proje yolunu ayarlayın"
            )]

        full_path = Path(self.godot_project_path) / script_path

        if not full_path.exists():
            return [TextContent(
                type="text",
                text=f"Hata: Dosya bulunamadı: {script_path}"
            )]

        try:
            content = full_path.read_text(encoding='utf-8')
            return [TextContent(
                type="text",
                text=f"=== {script_path} ===\n{content}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Dosya okunamadı: {e}"
            )]

    async def _write_godot_script(self, script_path: str, content: str) -> list[TextContent]:
        """GDScript dosyası yaz"""
        if not self.godot_project_path:
            return [TextContent(
                type="text",
                text="Hata: Önce set_godot_project ile proje yolunu ayarlayın"
            )]

        full_path = Path(self.godot_project_path) / script_path

        try:
            # Dizin yoksa oluştur
            full_path.parent.mkdir(parents=True, exist_ok=True)

            full_path.write_text(content, encoding='utf-8')
            logger.info(f"Dosya yazıldı: {script_path}")

            return [TextContent(
                type="text",
                text=f"Başarılı: {script_path} dosyası yazıldı/güncellendi"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Dosya yazılamadı: {e}"
            )]

    async def _read_godot_scene(self, scene_path: str) -> list[TextContent]:
        """Sahne dosyasını oku"""
        if not self.godot_project_path:
            return [TextContent(
                type="text",
                text="Hata: Önce set_godot_project ile proje yolunu ayarlayın"
            )]

        full_path = Path(self.godot_project_path) / scene_path

        if not full_path.exists():
            return [TextContent(
                type="text",
                text=f"Hata: Sahne dosyası bulunamadı: {scene_path}"
            )]

        try:
            content = full_path.read_text(encoding='utf-8')
            return [TextContent(
                type="text",
                text=f"=== {scene_path} ===\n{content}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Sahne dosyası okunamadı: {e}"
            )]

    async def _get_project_info(self) -> list[TextContent]:
        """Proje bilgilerini al"""
        if not self.godot_project_path:
            return [TextContent(
                type="text",
                text="Hata: Önce set_godot_project ile proje yolunu ayarlayın"
            )]

        project_file = Path(self.godot_project_path) / "project.godot"

        try:
            content = project_file.read_text(encoding='utf-8')
            return [TextContent(
                type="text",
                text=f"=== project.godot ===\n{content}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: project.godot okunamadı: {e}"
            )]


async def main():
    """Ana fonksiyon"""
    logger.info("Godot MCP Server başlatılıyor...")

    # Server oluştur
    godot_server = GodotMCPServer()

    # CRITICAL: stdio kullan - stdout sadece JSON, stderr loglar için
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("MCP server hazır ve bağlantı bekliyor...")
        await godot_server.server.run(
            read_stream,
            write_stream,
            godot_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
