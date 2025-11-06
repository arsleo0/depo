#!/usr/bin/env python3
"""
Photoshop MCP Server - Claude Desktop & Adobe Photoshop Entegrasyonu

Bu server, Claude Desktop'ın Photoshop ile konuşmasını sağlar.
JSX (ExtendScript) kullanarak Photoshop'u kontrol eder.
"""

import asyncio
import sys
import logging
import json
import subprocess
import platform
import os
import tempfile
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

# Logları stderr'e yönlendir (stdout JSON-RPC için temiz kalmalı)
logging.basicConfig(
    level=logging.INFO,
    format='[PHOTOSHOP-MCP] %(levelname)s: %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# MCP Server instance
app = Server("photoshop-mcp")

# Platform belirleme
PLATFORM = platform.system()  # 'Darwin' (Mac), 'Windows', 'Linux'

class PhotoshopExecutor:
    """Photoshop ile iletişim kuran yardımcı sınıf"""

    @staticmethod
    def execute_jsx(script_code: str) -> dict:
        """
        JSX (ExtendScript) kodu çalıştır

        Returns:
            dict: {"success": bool, "result": str, "error": str}
        """
        try:
            logger.info(f"JSX script çalıştırılıyor (Platform: {PLATFORM})")

            if PLATFORM == "Darwin":  # macOS
                return PhotoshopExecutor._execute_jsx_mac(script_code)
            elif PLATFORM == "Windows":
                return PhotoshopExecutor._execute_jsx_windows(script_code)
            else:
                return {
                    "success": False,
                    "result": "",
                    "error": "Linux üzerinde Photoshop desteği yok (Wine deneyin)"
                }

        except Exception as e:
            logger.error(f"JSX çalıştırma hatası: {e}")
            return {
                "success": False,
                "result": "",
                "error": str(e)
            }

    @staticmethod
    def _execute_jsx_mac(script_code: str) -> dict:
        """Mac için AppleScript üzerinden JSX çalıştır"""
        # JSX kodunu temp dosyaya yaz
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsx', delete=False) as f:
            f.write(script_code)
            jsx_file = f.name

        try:
            # AppleScript ile Photoshop'ta JSX dosyasını çalıştır
            applescript = f'''
            tell application "Adobe Photoshop 2024"
                activate
                do javascript (POSIX file "{jsx_file}") show debugger on runtime error
            end tell
            '''

            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "result": result.stdout.strip(),
                    "error": ""
                }
            else:
                return {
                    "success": False,
                    "result": "",
                    "error": result.stderr.strip()
                }
        finally:
            # Temp dosyayı sil
            try:
                os.unlink(jsx_file)
            except:
                pass

    @staticmethod
    def _execute_jsx_windows(script_code: str) -> dict:
        """Windows için COM üzerinden JSX çalıştır"""
        try:
            import win32com.client

            # Photoshop COM nesnesini al
            ps = win32com.client.Dispatch("Photoshop.Application")

            # JSX kodunu çalıştır
            result = ps.DoJavaScript(script_code)

            return {
                "success": True,
                "result": str(result),
                "error": ""
            }
        except ImportError:
            return {
                "success": False,
                "result": "",
                "error": "pywin32 yüklü değil. Kurmak için: pip install pywin32"
            }
        except Exception as e:
            return {
                "success": False,
                "result": "",
                "error": str(e)
            }


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Claude'un kullanabileceği Photoshop araçlarını listele"""
    logger.info("list_tools() çağrıldı")

    return [
        Tool(
            name="photoshop_check_connection",
            description="Photoshop'un çalışıp çalışmadığını kontrol et",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="photoshop_get_info",
            description="Aktif doküman ve Photoshop hakkında bilgi al",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="photoshop_open_file",
            description="Photoshop'ta dosya aç",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Açılacak dosyanın tam yolu (PSD, JPG, PNG, vb.)"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="photoshop_save_file",
            description="Aktif dokümanı kaydet",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Kaydedilecek dosyanın tam yolu (opsiyonel, boş ise mevcut dosyayı kaydet)"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["psd", "jpg", "png", "tiff"],
                        "description": "Kayıt formatı"
                    },
                    "quality": {
                        "type": "number",
                        "description": "JPEG kalitesi (1-12, sadece JPG için)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="photoshop_create_layer",
            description="Yeni bir katman (layer) oluştur",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Katman adı"
                    },
                    "layer_type": {
                        "type": "string",
                        "enum": ["normal", "text", "shape"],
                        "description": "Katman tipi"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="photoshop_list_layers",
            description="Aktif dokümandaki tüm katmanları listele",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="photoshop_apply_filter",
            description="Aktif katmana filtre uygula",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "string",
                        "enum": ["gaussian_blur", "sharpen", "brightness_contrast", "hue_saturation", "invert"],
                        "description": "Uygulanacak filtre"
                    },
                    "params": {
                        "type": "object",
                        "description": "Filtre parametreleri (radius, amount, vb.)"
                    }
                },
                "required": ["filter"]
            }
        ),
        Tool(
            name="photoshop_add_text",
            description="Dokümana metin ekle",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Eklenecek metin"
                    },
                    "x": {
                        "type": "number",
                        "description": "X konumu (piksel)"
                    },
                    "y": {
                        "type": "number",
                        "description": "Y konumu (piksel)"
                    },
                    "font_size": {
                        "type": "number",
                        "description": "Font boyutu (pt)"
                    },
                    "color": {
                        "type": "string",
                        "description": "Renk (hex, örn: '#FF0000')"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="photoshop_resize_image",
            description="Doküman boyutunu değiştir",
            inputSchema={
                "type": "object",
                "properties": {
                    "width": {
                        "type": "number",
                        "description": "Yeni genişlik (piksel)"
                    },
                    "height": {
                        "type": "number",
                        "description": "Yeni yükseklik (piksel)"
                    },
                    "maintain_aspect": {
                        "type": "boolean",
                        "description": "En-boy oranını koru"
                    }
                },
                "required": ["width", "height"]
            }
        ),
        Tool(
            name="photoshop_crop",
            description="Görüntüyü kırp",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "Sol üst köşe X"},
                    "y": {"type": "number", "description": "Sol üst köşe Y"},
                    "width": {"type": "number", "description": "Kırpma genişliği"},
                    "height": {"type": "number", "description": "Kırpma yüksekliği"}
                },
                "required": ["x", "y", "width", "height"]
            }
        ),
        Tool(
            name="photoshop_execute_jsx",
            description="Özel JSX (ExtendScript) kodu çalıştır (gelişmiş kullanıcılar için)",
            inputSchema={
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "Çalıştırılacak JSX kodu"
                    }
                },
                "required": ["script"]
            }
        ),
        Tool(
            name="photoshop_batch_resize",
            description="Bir klasördeki tüm resimleri yeniden boyutlandır",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_folder": {
                        "type": "string",
                        "description": "Kaynak klasör yolu"
                    },
                    "output_folder": {
                        "type": "string",
                        "description": "Hedef klasör yolu"
                    },
                    "width": {"type": "number"},
                    "height": {"type": "number"},
                    "format": {
                        "type": "string",
                        "enum": ["jpg", "png"],
                        "description": "Çıktı formatı"
                    }
                },
                "required": ["input_folder", "output_folder", "width", "height"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Claude bir tool çağırdığında burası çalışır"""
    logger.info(f"Tool çağrıldı: {name} with args: {arguments}")

    try:
        if name == "photoshop_check_connection":
            return await handle_check_connection()

        elif name == "photoshop_get_info":
            return await handle_get_info()

        elif name == "photoshop_open_file":
            return await handle_open_file(arguments.get("file_path"))

        elif name == "photoshop_save_file":
            return await handle_save_file(
                arguments.get("file_path"),
                arguments.get("format", "psd"),
                arguments.get("quality", 10)
            )

        elif name == "photoshop_create_layer":
            return await handle_create_layer(
                arguments.get("name"),
                arguments.get("layer_type", "normal")
            )

        elif name == "photoshop_list_layers":
            return await handle_list_layers()

        elif name == "photoshop_apply_filter":
            return await handle_apply_filter(
                arguments.get("filter"),
                arguments.get("params", {})
            )

        elif name == "photoshop_add_text":
            return await handle_add_text(arguments)

        elif name == "photoshop_resize_image":
            return await handle_resize_image(arguments)

        elif name == "photoshop_crop":
            return await handle_crop(arguments)

        elif name == "photoshop_execute_jsx":
            return await handle_execute_jsx(arguments.get("script"))

        elif name == "photoshop_batch_resize":
            return await handle_batch_resize(arguments)

        else:
            return [TextContent(
                type="text",
                text=f"❌ Bilinmeyen tool: {name}"
            )]

    except Exception as e:
        logger.error(f"Tool hatası ({name}): {e}")
        return [TextContent(
            type="text",
            text=f"❌ Hata: {str(e)}"
        )]


# ============================================================================
# TOOL HANDLERS
# ============================================================================

async def handle_check_connection() -> list[TextContent]:
    """Photoshop bağlantısını kontrol et"""
    jsx_script = """
    app.name + " " + app.version;
    """

    result = PhotoshopExecutor.execute_jsx(jsx_script)

    if result["success"]:
        return [TextContent(
            type="text",
            text=f"✅ Photoshop bağlantısı başarılı!\n\n{result['result']}\n\nPlatform: {PLATFORM}"
        )]
    else:
        return [TextContent(
            type="text",
            text=f"❌ Photoshop'a bağlanılamadı:\n{result['error']}\n\nLütfen Photoshop'un açık olduğundan emin olun."
        )]


async def handle_get_info() -> list[TextContent]:
    """Aktif doküman bilgilerini al"""
    jsx_script = """
    if (app.documents.length == 0) {
        "Açık doküman yok";
    } else {
        var doc = app.activeDocument;
        var info = {
            name: doc.name,
            width: doc.width.as("px"),
            height: doc.height.as("px"),
            resolution: doc.resolution,
            colorMode: doc.mode.toString(),
            layerCount: doc.layers.length,
            path: doc.fullName ? doc.fullName.fsName : "Kaydedilmemiş"
        };
        JSON.stringify(info);
    }
    """

    result = PhotoshopExecutor.execute_jsx(jsx_script)

    if result["success"]:
        try:
            info = json.loads(result["result"])
            text = f"""📄 Aktif Doküman Bilgileri:

📝 İsim: {info['name']}
📏 Boyut: {info['width']} x {info['height']} piksel
🎨 Renk Modu: {info['colorMode']}
🔍 Çözünürlük: {info['resolution']} DPI
📚 Katman Sayısı: {info['layerCount']}
💾 Yol: {info['path']}
"""
            return [TextContent(type="text", text=text)]
        except:
            return [TextContent(type="text", text=result["result"])]
    else:
        return [TextContent(type="text", text=f"❌ Hata: {result['error']}")]


async def handle_open_file(file_path: str) -> list[TextContent]:
    """Dosya aç"""
    jsx_script = f"""
    var file = new File("{file_path}");
    if (file.exists) {{
        app.open(file);
        "Dosya açıldı: {file_path}";
    }} else {{
        "Hata: Dosya bulunamadı: {file_path}";
    }}
    """

    result = PhotoshopExecutor.execute_jsx(jsx_script)

    if result["success"]:
        return [TextContent(type="text", text=f"✅ {result['result']}")]
    else:
        return [TextContent(type="text", text=f"❌ {result['error']}")]


async def handle_save_file(file_path: str, format: str, quality: int) -> list[TextContent]:
    """Dosya kaydet"""
    if not file_path:
        jsx_script = "app.activeDocument.save();"
        result = PhotoshopExecutor.execute_jsx(jsx_script)
        return [TextContent(type="text", text="✅ Doküman kaydedildi" if result["success"] else f"❌ {result['error']}")]

    # Format bazlı kayıt
    jsx_script = f"""
    var doc = app.activeDocument;
    var file = new File("{file_path}");
    """

    if format == "jpg":
        jsx_script += f"""
        var jpgOptions = new JPEGSaveOptions();
        jpgOptions.quality = {quality};
        doc.saveAs(file, jpgOptions);
        """
    elif format == "png":
        jsx_script += """
        var pngOptions = new PNGSaveOptions();
        doc.saveAs(file, pngOptions);
        """
    elif format == "psd":
        jsx_script += """
        var psdOptions = new PhotoshopSaveOptions();
        doc.saveAs(file, psdOptions);
        """

    jsx_script += f'"Kaydedildi: {file_path}";'

    result = PhotoshopExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_create_layer(name: str, layer_type: str) -> list[TextContent]:
    """Yeni katman oluştur"""
    jsx_script = f"""
    var doc = app.activeDocument;
    var layer = doc.artLayers.add();
    layer.name = "{name}";
    "Katman oluşturuldu: {name}";
    """

    result = PhotoshopExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_list_layers() -> list[TextContent]:
    """Katmanları listele"""
    jsx_script = """
    var doc = app.activeDocument;
    var layers = [];
    for (var i = 0; i < doc.layers.length; i++) {
        layers.push({
            name: doc.layers[i].name,
            visible: doc.layers[i].visible,
            opacity: doc.layers[i].opacity,
            blendMode: doc.layers[i].blendMode.toString()
        });
    }
    JSON.stringify(layers);
    """

    result = PhotoshopExecutor.execute_jsx(jsx_script)

    if result["success"]:
        try:
            layers = json.loads(result["result"])
            text = "📚 Katmanlar:\n\n"
            for i, layer in enumerate(layers, 1):
                visible = "👁️" if layer["visible"] else "🚫"
                text += f"{i}. {visible} {layer['name']} (Opacity: {layer['opacity']}%)\n"
            return [TextContent(type="text", text=text)]
        except:
            return [TextContent(type="text", text=result["result"])]
    else:
        return [TextContent(type="text", text=f"❌ {result['error']}")]


async def handle_apply_filter(filter_name: str, params: dict) -> list[TextContent]:
    """Filtre uygula"""
    jsx_scripts = {
        "gaussian_blur": f"""
        var doc = app.activeDocument;
        doc.activeLayer.applyGaussianBlur({params.get('radius', 5)});
        "Gaussian Blur uygulandı";
        """,
        "sharpen": """
        var doc = app.activeDocument;
        doc.activeLayer.applySharpen();
        "Sharpen uygulandı";
        """,
        "invert": """
        var doc = app.activeDocument;
        doc.activeLayer.invert();
        "Invert uygulandı";
        """
    }

    jsx_script = jsx_scripts.get(filter_name, f'"Bilinmeyen filtre: {filter_name}"')
    result = PhotoshopExecutor.execute_jsx(jsx_script)

    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_add_text(args: dict) -> list[TextContent]:
    """Metin ekle"""
    text = args.get("text")
    x = args.get("x", 100)
    y = args.get("y", 100)
    font_size = args.get("font_size", 24)
    color = args.get("color", "#000000")

    # Hex color to RGB
    color = color.lstrip("#")
    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)

    jsx_script = f"""
    var doc = app.activeDocument;
    var textLayer = doc.artLayers.add();
    textLayer.kind = LayerKind.TEXT;

    var textItem = textLayer.textItem;
    textItem.contents = "{text}";
    textItem.size = {font_size};
    textItem.position = [{x}, {y}];

    var color = new SolidColor();
    color.rgb.red = {r};
    color.rgb.green = {g};
    color.rgb.blue = {b};
    textItem.color = color;

    "Metin eklendi: {text}";
    """

    result = PhotoshopExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_resize_image(args: dict) -> list[TextContent]:
    """Görüntüyü yeniden boyutlandır"""
    width = args.get("width")
    height = args.get("height")
    maintain_aspect = args.get("maintain_aspect", True)

    jsx_script = f"""
    var doc = app.activeDocument;
    doc.resizeImage(UnitValue({width}, "px"), UnitValue({height}, "px"), null, ResampleMethod.BICUBIC);
    "Boyutlandırıldı: {width}x{height}";
    """

    result = PhotoshopExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_crop(args: dict) -> list[TextContent]:
    """Görüntüyü kırp"""
    x = args.get("x")
    y = args.get("y")
    width = args.get("width")
    height = args.get("height")

    jsx_script = f"""
    var doc = app.activeDocument;
    var bounds = [{x}, {y}, {x + width}, {y + height}];
    doc.crop(bounds);
    "Kırpma tamamlandı";
    """

    result = PhotoshopExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_execute_jsx(script: str) -> list[TextContent]:
    """Özel JSX kodu çalıştır"""
    result = PhotoshopExecutor.execute_jsx(script)

    if result["success"]:
        return [TextContent(type="text", text=f"✅ JSX çalıştırıldı:\n\n{result['result']}")]
    else:
        return [TextContent(type="text", text=f"❌ JSX hatası:\n{result['error']}")]


async def handle_batch_resize(args: dict) -> list[TextContent]:
    """Batch resize işlemi"""
    input_folder = args.get("input_folder")
    output_folder = args.get("output_folder")
    width = args.get("width")
    height = args.get("height")
    format_type = args.get("format", "jpg")

    jsx_script = f"""
    var inputFolder = new Folder("{input_folder}");
    var outputFolder = new Folder("{output_folder}");

    if (!outputFolder.exists) outputFolder.create();

    var files = inputFolder.getFiles(/\.(jpg|jpeg|png|psd|tif|tiff)$/i);
    var processed = 0;

    for (var i = 0; i < files.length; i++) {{
        try {{
            var doc = app.open(files[i]);
            doc.resizeImage(UnitValue({width}, "px"), UnitValue({height}, "px"), null, ResampleMethod.BICUBIC);

            var saveName = doc.name.replace(/\.[^\.]+$/, ".{format_type}");
            var saveFile = new File(outputFolder + "/" + saveName);

            {"var jpgOptions = new JPEGSaveOptions(); jpgOptions.quality = 10; doc.saveAs(saveFile, jpgOptions);" if format_type == "jpg" else "var pngOptions = new PNGSaveOptions(); doc.saveAs(saveFile, pngOptions);"}

            doc.close(SaveOptions.DONOTSAVECHANGES);
            processed++;
        }} catch (e) {{}}
    }}

    processed + " dosya işlendi";
    """

    result = PhotoshopExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


# ============================================================================
# MAIN
# ============================================================================

async def main():
    """MCP server'ı başlat"""
    logger.info("Photoshop MCP Server başlatılıyor...")
    logger.info(f"Platform: {PLATFORM}")

    # MCP stdio server çalıştır
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        logger.info("MCP server hazır ve bağlantı bekliyor...")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server kapatıldı")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
