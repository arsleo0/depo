#!/usr/bin/env python3
"""
Photoshop MCP Server - Claude Desktop ile Adobe Photoshop arasında köprü kurar
Socket-based iletişim ile Photoshop otomasyonu
"""
import sys
import os
import asyncio
import json
import socket
import subprocess
from typing import Any
from pathlib import Path

# CRITICAL: Tüm logları stderr'e yönlendir
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[PHOTOSHOP-MCP] %(levelname)s: %(message)s',
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


class PhotoshopMCPServer:
    """Adobe Photoshop için MCP sunucusu"""

    def __init__(self):
        self.server = Server("photoshop-mcp-server")
        self.socket_port = 49494
        self.socket_server = None
        self.photoshop_connected = False
        self._register_handlers()

    def _register_handlers(self):
        """MCP handler'ları kaydet"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Kullanılabilir araçları listele"""
            logger.info("Photoshop araçları listeleniyor...")
            return [
                Tool(
                    name="photoshop_check_connection",
                    description="Photoshop bağlantısını kontrol et",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="photoshop_open_file",
                    description="Photoshop dosyasını (.psd, .jpg, .png, vb.) aç",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Açılacak dosyanın tam yolu"
                            }
                        },
                        "required": ["filepath"]
                    }
                ),
                Tool(
                    name="photoshop_save_file",
                    description="Aktif dokümanı kaydet",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Kaydedilecek dosya yolu (opsiyonel, belirtilmezse mevcut yola kaydeder)"
                            }
                        }
                    }
                ),
                Tool(
                    name="photoshop_get_document_info",
                    description="Aktif doküman hakkında bilgi al",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="photoshop_create_layer",
                    description="Yeni katman (layer) oluştur",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Katman adı"
                            },
                            "type": {
                                "type": "string",
                                "enum": ["normal", "text", "shape"],
                                "description": "Katman tipi (varsayılan: normal)"
                            }
                        }
                    }
                ),
                Tool(
                    name="photoshop_delete_layer",
                    description="Katman sil",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "layer_name": {
                                "type": "string",
                                "description": "Silinecek katman adı (belirtilmezse aktif katman)"
                            }
                        }
                    }
                ),
                Tool(
                    name="photoshop_list_layers",
                    description="Tüm katmanları listele",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="photoshop_resize_image",
                    description="Görsel boyutunu değiştir",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "width": {
                                "type": "integer",
                                "description": "Yeni genişlik (piksel)"
                            },
                            "height": {
                                "type": "integer",
                                "description": "Yeni yükseklik (piksel)"
                            }
                        },
                        "required": ["width", "height"]
                    }
                ),
                Tool(
                    name="photoshop_apply_filter",
                    description="Filtre uygula",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filter": {
                                "type": "string",
                                "enum": ["blur", "sharpen", "gaussianBlur"],
                                "description": "Uygulanacak filtre"
                            }
                        },
                        "required": ["filter"]
                    }
                ),
                Tool(
                    name="photoshop_run_jsx",
                    description="ExtendScript (JSX) kodu çalıştır",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Çalıştırılacak JSX kodu"
                            }
                        },
                        "required": ["code"]
                    }
                ),
                Tool(
                    name="photoshop_export",
                    description="Dokümanı farklı formatta dışa aktar",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "Dışa aktarılacak dosya yolu"
                            },
                            "format": {
                                "type": "string",
                                "enum": ["PNG", "JPEG", "TIFF", "PDF"],
                                "description": "Dışa aktarma formatı"
                            },
                            "quality": {
                                "type": "integer",
                                "description": "JPEG kalitesi (1-12, varsayılan: 10)",
                                "minimum": 1,
                                "maximum": 12
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

            try:
                if name == "photoshop_check_connection":
                    return await self._check_connection()
                elif name == "photoshop_open_file":
                    return await self._send_command("open_file", {"filepath": arguments.get("filepath")})
                elif name == "photoshop_save_file":
                    return await self._send_command("save_file", {"filepath": arguments.get("filepath")})
                elif name == "photoshop_get_document_info":
                    return await self._send_command("get_document_info", {})
                elif name == "photoshop_create_layer":
                    return await self._send_command("create_layer", {
                        "name": arguments.get("name"),
                        "type": arguments.get("type", "normal")
                    })
                elif name == "photoshop_delete_layer":
                    return await self._send_command("delete_layer", {"layer_name": arguments.get("layer_name")})
                elif name == "photoshop_list_layers":
                    return await self._send_command("list_layers", {})
                elif name == "photoshop_resize_image":
                    return await self._send_command("resize_image", {
                        "width": arguments.get("width"),
                        "height": arguments.get("height")
                    })
                elif name == "photoshop_apply_filter":
                    return await self._send_command("apply_filter", {"filter": arguments.get("filter")})
                elif name == "photoshop_run_jsx":
                    return await self._send_command("run_jsx", {"code": arguments.get("code")})
                elif name == "photoshop_export":
                    return await self._send_command("export", {
                        "filepath": arguments.get("filepath"),
                        "format": arguments.get("format"),
                        "quality": arguments.get("quality", 10)
                    })
                else:
                    raise ValueError(f"Bilinmeyen tool: {name}")
            except Exception as e:
                logger.error(f"Tool hatası: {e}", exc_info=True)
                return [TextContent(
                    type="text",
                    text=f"Hata: {str(e)}"
                )]

    async def _check_connection(self) -> list[TextContent]:
        """Photoshop bağlantısını kontrol et"""
        if self.photoshop_connected:
            return [TextContent(
                type="text",
                text="✓ Photoshop bağlı ve hazır"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"✗ Photoshop bağlı değil\n\nPhotoshop'u başlatın ve şu JSX scriptini çalıştırın:\nphotoshop_client.jsx\n\nVeya Photoshop içinden: File > Scripts > Browse... ve photoshop_client.jsx'i seçin."
            )]

    async def _send_command(self, command: str, params: dict) -> list[TextContent]:
        """Photoshop'a komut gönder"""
        if not self.photoshop_connected:
            return [TextContent(
                type="text",
                text="Hata: Photoshop bağlı değil. Önce photoshop_client.jsx scriptini Photoshop'ta çalıştırın."
            )]

        try:
            # Socket üzerinden komut gönder
            message = json.dumps({
                "command": command,
                "params": params
            })

            # Bu basitleştirilmiş bir implementasyon
            # Gerçek uygulamada burada socket iletişimi olacak

            return [TextContent(
                type="text",
                text=f"Komut gönderildi: {command}\nParametreler: {json.dumps(params, indent=2, ensure_ascii=False)}\n\nNot: Socket iletişimi henüz implement edilmedi. photoshop_client.jsx scriptini çalıştırın."
            )]

        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Komut gönderilemedi: {e}"
            )]


async def main():
    """Ana fonksiyon"""
    logger.info("Photoshop MCP Server başlatılıyor...")
    logger.info(f"Socket port: 49494")

    photoshop_server = PhotoshopMCPServer()

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Photoshop MCP server hazır ve bağlantı bekliyor...")
        logger.info("Photoshop'ta photoshop_client.jsx scriptini çalıştırın")
        await photoshop_server.server.run(
            read_stream,
            write_stream,
            photoshop_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
