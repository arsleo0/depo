#!/usr/bin/env python3
"""
After Effects MCP Server - Claude Desktop & Adobe After Effects Entegrasyonu

Bu server, Claude Desktop'ın After Effects ile konuşmasını sağlar.
JSX (ExtendScript) kullanarak After Effects'i kontrol eder.
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
    format='[AE-MCP] %(levelname)s: %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# MCP Server instance
app = Server("aftereffects-mcp")

# Platform belirleme
PLATFORM = platform.system()  # 'Darwin' (Mac), 'Windows', 'Linux'

class AfterEffectsExecutor:
    """After Effects ile iletişim kuran yardımcı sınıf"""

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
                return AfterEffectsExecutor._execute_jsx_mac(script_code)
            elif PLATFORM == "Windows":
                return AfterEffectsExecutor._execute_jsx_windows(script_code)
            else:
                return {
                    "success": False,
                    "result": "",
                    "error": "Linux üzerinde After Effects desteği yok"
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
            # AppleScript ile After Effects'te JSX dosyasını çalıştır
            applescript = f'''
            tell application "Adobe After Effects 2024"
                activate
                DoScript (POSIX file "{jsx_file}")
            end tell
            '''

            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                timeout=60
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

            # After Effects COM nesnesini al
            ae = win32com.client.Dispatch("AfterEffects.Application")

            # JSX kodunu çalıştır
            result = ae.DoScript(script_code)

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
    """Claude'un kullanabileceği After Effects araçlarını listele"""
    logger.info("list_tools() çağrıldı")

    return [
        Tool(
            name="ae_check_connection",
            description="After Effects'in çalışıp çalışmadığını kontrol et",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="ae_get_project_info",
            description="Aktif proje ve composition hakkında bilgi al",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="ae_create_composition",
            description="Yeni bir composition oluştur",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Composition adı"
                    },
                    "width": {
                        "type": "number",
                        "description": "Genişlik (piksel)"
                    },
                    "height": {
                        "type": "number",
                        "description": "Yükseklik (piksel)"
                    },
                    "duration": {
                        "type": "number",
                        "description": "Süre (saniye)"
                    },
                    "frame_rate": {
                        "type": "number",
                        "description": "Frame rate (fps)"
                    }
                },
                "required": ["name", "width", "height", "duration"]
            }
        ),
        Tool(
            name="ae_list_compositions",
            description="Projedeki tüm composition'ları listele",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="ae_add_solid_layer",
            description="Aktif composition'a solid layer ekle",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Layer adı"
                    },
                    "color": {
                        "type": "string",
                        "description": "Renk (hex, örn: '#FF0000')"
                    },
                    "width": {
                        "type": "number",
                        "description": "Genişlik (opsiyonel, comp boyutu kullanılır)"
                    },
                    "height": {
                        "type": "number",
                        "description": "Yükseklik (opsiyonel, comp boyutu kullanılır)"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="ae_add_text_layer",
            description="Aktif composition'a text layer ekle",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Metin içeriği"
                    },
                    "font_size": {
                        "type": "number",
                        "description": "Font boyutu"
                    },
                    "color": {
                        "type": "string",
                        "description": "Metin rengi (hex)"
                    },
                    "position_x": {
                        "type": "number",
                        "description": "X pozisyonu"
                    },
                    "position_y": {
                        "type": "number",
                        "description": "Y pozisyonu"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="ae_import_file",
            description="Dosyayı projeye import et (video, görüntü, audio)",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Import edilecek dosyanın tam yolu"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="ae_add_footage_to_comp",
            description="Import edilen footage'ı composition'a ekle",
            inputSchema={
                "type": "object",
                "properties": {
                    "footage_name": {
                        "type": "string",
                        "description": "Footage dosya adı (import edilmiş olmalı)"
                    },
                    "comp_name": {
                        "type": "string",
                        "description": "Hedef composition adı (boş ise aktif comp)"
                    }
                },
                "required": ["footage_name"]
            }
        ),
        Tool(
            name="ae_list_layers",
            description="Aktif composition'daki tüm layer'ları listele",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="ae_apply_effect",
            description="Layer'a effect (efekt) uygula",
            inputSchema={
                "type": "object",
                "properties": {
                    "layer_name": {
                        "type": "string",
                        "description": "Layer adı"
                    },
                    "effect_name": {
                        "type": "string",
                        "enum": ["Gaussian Blur", "Glow", "Drop Shadow", "Brightness & Contrast", "Hue/Saturation"],
                        "description": "Effect adı"
                    },
                    "params": {
                        "type": "object",
                        "description": "Effect parametreleri"
                    }
                },
                "required": ["layer_name", "effect_name"]
            }
        ),
        Tool(
            name="ae_set_keyframe",
            description="Property'ye keyframe ekle (animasyon için)",
            inputSchema={
                "type": "object",
                "properties": {
                    "layer_name": {
                        "type": "string",
                        "description": "Layer adı"
                    },
                    "property": {
                        "type": "string",
                        "enum": ["position", "scale", "rotation", "opacity"],
                        "description": "Animate edilecek property"
                    },
                    "time": {
                        "type": "number",
                        "description": "Keyframe zamanı (saniye)"
                    },
                    "value": {
                        "type": "array",
                        "description": "Keyframe değeri (array: [x, y] veya single value)"
                    }
                },
                "required": ["layer_name", "property", "time", "value"]
            }
        ),
        Tool(
            name="ae_render_composition",
            description="Composition'ı render et (video export)",
            inputSchema={
                "type": "object",
                "properties": {
                    "comp_name": {
                        "type": "string",
                        "description": "Render edilecek composition adı"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Çıktı dosyası yolu (örn: /Users/x/Desktop/output.mov)"
                    },
                    "output_module": {
                        "type": "string",
                        "enum": ["H.264", "Lossless", "Apple ProRes 422", "PNG Sequence"],
                        "description": "Render formatı"
                    }
                },
                "required": ["comp_name", "output_path"]
            }
        ),
        Tool(
            name="ae_save_project",
            description="Projeyi kaydet",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Proje dosyası yolu (.aep)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="ae_execute_jsx",
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
            name="ae_create_simple_animation",
            description="Basit animasyon şablonu oluştur (intro, lower third, vb.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "template": {
                        "type": "string",
                        "enum": ["text_fade_in", "logo_reveal", "lower_third", "slide_in"],
                        "description": "Animasyon şablonu tipi"
                    },
                    "text": {
                        "type": "string",
                        "description": "Animasyonda kullanılacak metin"
                    },
                    "duration": {
                        "type": "number",
                        "description": "Animasyon süresi (saniye)"
                    }
                },
                "required": ["template"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Claude bir tool çağırdığında burası çalışır"""
    logger.info(f"Tool çağrıldı: {name} with args: {arguments}")

    try:
        if name == "ae_check_connection":
            return await handle_check_connection()

        elif name == "ae_get_project_info":
            return await handle_get_project_info()

        elif name == "ae_create_composition":
            return await handle_create_composition(arguments)

        elif name == "ae_list_compositions":
            return await handle_list_compositions()

        elif name == "ae_add_solid_layer":
            return await handle_add_solid_layer(arguments)

        elif name == "ae_add_text_layer":
            return await handle_add_text_layer(arguments)

        elif name == "ae_import_file":
            return await handle_import_file(arguments.get("file_path"))

        elif name == "ae_add_footage_to_comp":
            return await handle_add_footage_to_comp(arguments)

        elif name == "ae_list_layers":
            return await handle_list_layers()

        elif name == "ae_apply_effect":
            return await handle_apply_effect(arguments)

        elif name == "ae_set_keyframe":
            return await handle_set_keyframe(arguments)

        elif name == "ae_render_composition":
            return await handle_render_composition(arguments)

        elif name == "ae_save_project":
            return await handle_save_project(arguments.get("file_path"))

        elif name == "ae_execute_jsx":
            return await handle_execute_jsx(arguments.get("script"))

        elif name == "ae_create_simple_animation":
            return await handle_create_simple_animation(arguments)

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
    """After Effects bağlantısını kontrol et"""
    jsx_script = """
    app.name + " " + app.version;
    """

    result = AfterEffectsExecutor.execute_jsx(jsx_script)

    if result["success"]:
        return [TextContent(
            type="text",
            text=f"✅ After Effects bağlantısı başarılı!\n\n{result['result']}\n\nPlatform: {PLATFORM}"
        )]
    else:
        return [TextContent(
            type="text",
            text=f"❌ After Effects'e bağlanılamadı:\n{result['error']}\n\nLütfen After Effects'in açık olduğundan emin olun."
        )]


async def handle_get_project_info() -> list[TextContent]:
    """Aktif proje bilgilerini al"""
    jsx_script = """
    var project = app.project;
    if (project.numItems == 0) {
        "Açık proje yok veya proje boş";
    } else {
        var info = {
            projectName: project.file ? project.file.name : "Kaydedilmemiş",
            numComps: 0,
            numFootage: 0,
            activeComp: null
        };

        for (var i = 1; i <= project.numItems; i++) {
            if (project.item(i) instanceof CompItem) {
                info.numComps++;
            } else if (project.item(i) instanceof FootageItem) {
                info.numFootage++;
            }
        }

        if (app.project.activeItem && app.project.activeItem instanceof CompItem) {
            var comp = app.project.activeItem;
            info.activeComp = {
                name: comp.name,
                width: comp.width,
                height: comp.height,
                duration: comp.duration,
                frameRate: comp.frameRate,
                numLayers: comp.numLayers
            };
        }

        JSON.stringify(info);
    }
    """

    result = AfterEffectsExecutor.execute_jsx(jsx_script)

    if result["success"]:
        try:
            info = json.loads(result["result"])
            text = f"""🎬 After Effects Proje Bilgileri:

📝 Proje: {info['projectName']}
🎞️ Composition Sayısı: {info['numComps']}
📁 Footage Sayısı: {info['numFootage']}
"""
            if info['activeComp']:
                comp = info['activeComp']
                text += f"""
📺 Aktif Composition:
  - İsim: {comp['name']}
  - Boyut: {comp['width']} x {comp['height']} piksel
  - Süre: {comp['duration']:.2f} saniye
  - Frame Rate: {comp['frameRate']} fps
  - Layer Sayısı: {comp['numLayers']}
"""
            else:
                text += "\n⚠️ Aktif composition yok"

            return [TextContent(type="text", text=text)]
        except:
            return [TextContent(type="text", text=result["result"])]
    else:
        return [TextContent(type="text", text=f"❌ Hata: {result['error']}")]


async def handle_create_composition(args: dict) -> list[TextContent]:
    """Yeni composition oluştur"""
    name = args.get("name")
    width = args.get("width")
    height = args.get("height")
    duration = args.get("duration")
    frame_rate = args.get("frame_rate", 30)

    jsx_script = f"""
    var comp = app.project.items.addComp("{name}", {width}, {height}, 1, {duration}, {frame_rate});
    "Composition oluşturuldu: {name} ({width}x{height}, {duration}s, {frame_rate}fps)";
    """

    result = AfterEffectsExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_list_compositions() -> list[TextContent]:
    """Composition'ları listele"""
    jsx_script = """
    var comps = [];
    for (var i = 1; i <= app.project.numItems; i++) {
        var item = app.project.item(i);
        if (item instanceof CompItem) {
            comps.push({
                name: item.name,
                width: item.width,
                height: item.height,
                duration: item.duration,
                frameRate: item.frameRate
            });
        }
    }
    JSON.stringify(comps);
    """

    result = AfterEffectsExecutor.execute_jsx(jsx_script)

    if result["success"]:
        try:
            comps = json.loads(result["result"])
            if len(comps) == 0:
                return [TextContent(type="text", text="📭 Projede composition yok")]

            text = "🎞️ Compositions:\n\n"
            for i, comp in enumerate(comps, 1):
                text += f"{i}. {comp['name']}\n"
                text += f"   📏 {comp['width']}x{comp['height']} | ⏱️ {comp['duration']:.2f}s | 🎬 {comp['frameRate']}fps\n"
            return [TextContent(type="text", text=text)]
        except:
            return [TextContent(type="text", text=result["result"])]
    else:
        return [TextContent(type="text", text=f"❌ {result['error']}")]


async def handle_add_solid_layer(args: dict) -> list[TextContent]:
    """Solid layer ekle"""
    name = args.get("name")
    color = args.get("color", "#FF0000")
    width = args.get("width")
    height = args.get("height")

    # Hex color to RGB
    color = color.lstrip("#")
    r, g, b = int(color[0:2], 16) / 255.0, int(color[2:4], 16) / 255.0, int(color[4:6], 16) / 255.0

    jsx_script = f"""
    var comp = app.project.activeItem;
    if (comp && comp instanceof CompItem) {{
        var width = {width if width else 'comp.width'};
        var height = {height if height else 'comp.height'};
        var solidLayer = comp.layers.addSolid([{r}, {g}, {b}], "{name}", width, height, 1);
        "Solid layer eklendi: {name}";
    }} else {{
        "Hata: Aktif composition yok";
    }}
    """

    result = AfterEffectsExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_add_text_layer(args: dict) -> list[TextContent]:
    """Text layer ekle"""
    text = args.get("text")
    font_size = args.get("font_size", 60)
    color = args.get("color", "#FFFFFF")
    pos_x = args.get("position_x")
    pos_y = args.get("position_y")

    # Hex to RGB
    color = color.lstrip("#")
    r, g, b = int(color[0:2], 16) / 255.0, int(color[2:4], 16) / 255.0, int(color[4:6], 16) / 255.0

    jsx_script = f"""
    var comp = app.project.activeItem;
    if (comp && comp instanceof CompItem) {{
        var textLayer = comp.layers.addText("{text}");
        var textProp = textLayer.property("Source Text");
        var textDocument = textProp.value;
        textDocument.fontSize = {font_size};
        textDocument.fillColor = [{r}, {g}, {b}];
        textProp.setValue(textDocument);

        {"textLayer.property('Position').setValue([" + str(pos_x) + ", " + str(pos_y) + "]);" if pos_x and pos_y else ""}

        "Text layer eklendi: {text}";
    }} else {{
        "Hata: Aktif composition yok";
    }}
    """

    result = AfterEffectsExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_import_file(file_path: str) -> list[TextContent]:
    """Dosya import et"""
    jsx_script = f"""
    var importFile = new File("{file_path}");
    if (importFile.exists) {{
        var importedItem = app.project.importFile(new ImportOptions(importFile));
        "Dosya import edildi: {file_path}";
    }} else {{
        "Hata: Dosya bulunamadı: {file_path}";
    }}
    """

    result = AfterEffectsExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_add_footage_to_comp(args: dict) -> list[TextContent]:
    """Footage'ı composition'a ekle"""
    footage_name = args.get("footage_name")
    comp_name = args.get("comp_name")

    jsx_script = f"""
    var comp = {"app.project.activeItem" if not comp_name else f'findCompByName("{comp_name}")'};

    if (!comp || !(comp instanceof CompItem)) {{
        "Hata: Composition bulunamadı";
    }} else {{
        var footage = null;
        for (var i = 1; i <= app.project.numItems; i++) {{
            var item = app.project.item(i);
            if (item.name == "{footage_name}") {{
                footage = item;
                break;
            }}
        }}

        if (footage) {{
            comp.layers.add(footage);
            "Footage eklendi: {footage_name} → " + comp.name;
        }} else {{
            "Hata: Footage bulunamadı: {footage_name}";
        }}
    }}

    function findCompByName(name) {{
        for (var i = 1; i <= app.project.numItems; i++) {{
            var item = app.project.item(i);
            if (item instanceof CompItem && item.name == name) {{
                return item;
            }}
        }}
        return null;
    }}
    """

    result = AfterEffectsExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_list_layers() -> list[TextContent]:
    """Layer'ları listele"""
    jsx_script = """
    var comp = app.project.activeItem;
    if (!comp || !(comp instanceof CompItem)) {
        "Hata: Aktif composition yok";
    } else {
        var layers = [];
        for (var i = 1; i <= comp.numLayers; i++) {
            var layer = comp.layer(i);
            layers.push({
                name: layer.name,
                index: layer.index,
                enabled: layer.enabled,
                locked: layer.locked
            });
        }
        JSON.stringify(layers);
    }
    """

    result = AfterEffectsExecutor.execute_jsx(jsx_script)

    if result["success"]:
        try:
            layers = json.loads(result["result"])
            text = "📚 Layers:\n\n"
            for layer in layers:
                enabled = "👁️" if layer["enabled"] else "🚫"
                locked = "🔒" if layer["locked"] else ""
                text += f"{layer['index']}. {enabled} {locked} {layer['name']}\n"
            return [TextContent(type="text", text=text)]
        except:
            return [TextContent(type="text", text=result["result"])]
    else:
        return [TextContent(type="text", text=f"❌ {result['error']}")]


async def handle_apply_effect(args: dict) -> list[TextContent]:
    """Effect uygula"""
    layer_name = args.get("layer_name")
    effect_name = args.get("effect_name")
    params = args.get("params", {})

    jsx_script = f"""
    var comp = app.project.activeItem;
    if (!comp || !(comp instanceof CompItem)) {{
        "Hata: Aktif composition yok";
    }} else {{
        var layer = comp.layer("{layer_name}");
        if (layer) {{
            var effect = layer.property("Effects").addProperty("{effect_name}");
            "Effect uygulandı: {effect_name} → {layer_name}";
        }} else {{
            "Hata: Layer bulunamadı: {layer_name}";
        }}
    }}
    """

    result = AfterEffectsExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_set_keyframe(args: dict) -> list[TextContent]:
    """Keyframe ekle"""
    layer_name = args.get("layer_name")
    property_name = args.get("property")
    time = args.get("time")
    value = args.get("value")

    property_map = {
        "position": "Position",
        "scale": "Scale",
        "rotation": "Rotation",
        "opacity": "Opacity"
    }

    ae_property = property_map.get(property_name, "Position")
    value_str = str(value) if isinstance(value, list) else f"[{value}]"

    jsx_script = f"""
    var comp = app.project.activeItem;
    if (!comp || !(comp instanceof CompItem)) {{
        "Hata: Aktif composition yok";
    }} else {{
        var layer = comp.layer("{layer_name}");
        if (layer) {{
            var prop = layer.property("Transform").property("{ae_property}");
            prop.setValueAtTime({time}, {value_str});
            "Keyframe eklendi: {layer_name}.{property_name} @ {time}s = {value_str}";
        }} else {{
            "Hata: Layer bulunamadı: {layer_name}";
        }}
    }}
    """

    result = AfterEffectsExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_render_composition(args: dict) -> list[TextContent]:
    """Composition render et"""
    comp_name = args.get("comp_name")
    output_path = args.get("output_path")
    output_module = args.get("output_module", "H.264")

    jsx_script = f"""
    var comp = null;
    for (var i = 1; i <= app.project.numItems; i++) {{
        var item = app.project.item(i);
        if (item instanceof CompItem && item.name == "{comp_name}") {{
            comp = item;
            break;
        }}
    }}

    if (!comp) {{
        "Hata: Composition bulunamadı: {comp_name}";
    }} else {{
        var renderQueue = app.project.renderQueue;
        var renderItem = renderQueue.items.add(comp);

        renderItem.outputModule(1).file = new File("{output_path}");

        renderQueue.render();

        "Render başlatıldı: {comp_name} → {output_path}";
    }}
    """

    result = AfterEffectsExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_save_project(file_path: str) -> list[TextContent]:
    """Projeyi kaydet"""
    if not file_path:
        jsx_script = "app.project.save(); 'Proje kaydedildi';"
    else:
        jsx_script = f'app.project.save(new File("{file_path}")); "Proje kaydedildi: {file_path}";'

    result = AfterEffectsExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


async def handle_execute_jsx(script: str) -> list[TextContent]:
    """Özel JSX kodu çalıştır"""
    result = AfterEffectsExecutor.execute_jsx(script)

    if result["success"]:
        return [TextContent(type="text", text=f"✅ JSX çalıştırıldı:\n\n{result['result']}")]
    else:
        return [TextContent(type="text", text=f"❌ JSX hatası:\n{result['error']}")]


async def handle_create_simple_animation(args: dict) -> list[TextContent]:
    """Basit animasyon şablonu oluştur"""
    template = args.get("template")
    text = args.get("text", "SAMPLE TEXT")
    duration = args.get("duration", 3)

    templates = {
        "text_fade_in": f"""
        var comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem)) {{
            "Hata: Aktif composition yok";
        }} else {{
            var textLayer = comp.layers.addText("{text}");
            var opacity = textLayer.property("Transform").property("Opacity");
            opacity.setValueAtTime(0, 0);
            opacity.setValueAtTime({duration}, 100);
            "Text fade-in animasyonu oluşturuldu";
        }}
        """,

        "logo_reveal": f"""
        var comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem)) {{
            "Hata: Aktif composition yok";
        }} else {{
            var textLayer = comp.layers.addText("{text}");
            var scale = textLayer.property("Transform").property("Scale");
            scale.setValueAtTime(0, [0, 0]);
            scale.setValueAtTime({duration}, [100, 100]);
            "Logo reveal animasyonu oluşturuldu";
        }}
        """,

        "lower_third": f"""
        var comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem)) {{
            "Hata: Aktif composition yok";
        }} else {{
            var solidLayer = comp.layers.addSolid([0, 0, 0], "Background", comp.width * 0.4, 80, 1);
            solidLayer.property("Position").setValue([comp.width * 0.2, comp.height * 0.85]);

            var textLayer = comp.layers.addText("{text}");
            textLayer.property("Position").setValue([comp.width * 0.2, comp.height * 0.85]);

            var position = solidLayer.property("Transform").property("Position");
            position.setValueAtTime(0, [-comp.width * 0.2, comp.height * 0.85]);
            position.setValueAtTime(0.5, [comp.width * 0.2, comp.height * 0.85]);

            "Lower third animasyonu oluşturuldu";
        }}
        """
    }

    jsx_script = templates.get(template, f'"Bilinmeyen template: {template}"')
    result = AfterEffectsExecutor.execute_jsx(jsx_script)
    return [TextContent(type="text", text=f"✅ {result['result']}" if result["success"] else f"❌ {result['error']}")]


# ============================================================================
# MAIN
# ============================================================================

async def main():
    """MCP server'ı başlat"""
    logger.info("After Effects MCP Server başlatılıyor...")
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
