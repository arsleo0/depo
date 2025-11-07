#!/usr/bin/env python3
"""
OpenSCAD MCP Server - Claude Desktop ile OpenSCAD arasında köprü kurar
Geometri üretimi, 3D modelleme ve CAD işlemleri için
"""
import sys
import os
import asyncio
import json
import subprocess
from typing import Any
from pathlib import Path

# CRITICAL: Tüm logları stderr'e yönlendir
# stdout sadece MCP JSON-RPC mesajları için kullanılmalı
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[OPENSCAD-MCP] %(levelname)s: %(message)s',
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


class OpenSCADMCPServer:
    """OpenSCAD için MCP sunucusu"""

    def __init__(self):
        self.server = Server("openscad-mcp-server")
        self.work_dir: str | None = None
        self.openscad_executable = "openscad"  # Sistem PATH'inde olmalı

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
                    name="set_openscad_workdir",
                    description="OpenSCAD çalışma dizinini ayarla",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Çalışma dizini yolu"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="list_scad_files",
                    description="Çalışma dizinindeki tüm .scad dosyalarını listele",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="read_scad_file",
                    description="Bir OpenSCAD dosyasını oku",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Okunacak .scad dosyasının yolu"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="write_scad_file",
                    description="Bir OpenSCAD dosyası yaz veya güncelle",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Yazılacak .scad dosyasının yolu"
                            },
                            "content": {
                                "type": "string",
                                "description": "OpenSCAD kod içeriği"
                            }
                        },
                        "required": ["file_path", "content"]
                    }
                ),
                Tool(
                    name="render_to_png",
                    description="OpenSCAD dosyasını PNG görüntü olarak render et",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "scad_file": {
                                "type": "string",
                                "description": "Render edilecek .scad dosyası"
                            },
                            "output_file": {
                                "type": "string",
                                "description": "Çıktı PNG dosyası (opsiyonel, otomatik oluşturulur)"
                            },
                            "width": {
                                "type": "number",
                                "description": "Görüntü genişliği (varsayılan: 800)"
                            },
                            "height": {
                                "type": "number",
                                "description": "Görüntü yüksekliği (varsayılan: 600)"
                            }
                        },
                        "required": ["scad_file"]
                    }
                ),
                Tool(
                    name="export_to_stl",
                    description="OpenSCAD dosyasını STL formatına dönüştür (3D baskı için)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "scad_file": {
                                "type": "string",
                                "description": "Dönüştürülecek .scad dosyası"
                            },
                            "output_file": {
                                "type": "string",
                                "description": "Çıktı STL dosyası (opsiyonel, otomatik oluşturulur)"
                            }
                        },
                        "required": ["scad_file"]
                    }
                ),
                Tool(
                    name="generate_basic_shape",
                    description="Temel 3D geometrik şekil kodu üret (cube, sphere, cylinder, cone)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "shape": {
                                "type": "string",
                                "description": "Şekil tipi: cube, sphere, cylinder, cone, torus",
                                "enum": ["cube", "sphere", "cylinder", "cone", "torus"]
                            },
                            "size": {
                                "type": "number",
                                "description": "Boyut (küp için kenar uzunluğu, küre için yarıçap, vb.)"
                            },
                            "height": {
                                "type": "number",
                                "description": "Yükseklik (silindir ve koni için)"
                            }
                        },
                        "required": ["shape"]
                    }
                ),
                Tool(
                    name="check_openscad_installed",
                    description="OpenSCAD'in kurulu ve çalışır durumda olup olmadığını kontrol et",
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
                if name == "set_openscad_workdir":
                    return await self._set_openscad_workdir(arguments.get("path"))
                elif name == "list_scad_files":
                    return await self._list_scad_files()
                elif name == "read_scad_file":
                    return await self._read_scad_file(arguments.get("file_path"))
                elif name == "write_scad_file":
                    return await self._write_scad_file(
                        arguments.get("file_path"),
                        arguments.get("content")
                    )
                elif name == "render_to_png":
                    return await self._render_to_png(
                        arguments.get("scad_file"),
                        arguments.get("output_file"),
                        arguments.get("width", 800),
                        arguments.get("height", 600)
                    )
                elif name == "export_to_stl":
                    return await self._export_to_stl(
                        arguments.get("scad_file"),
                        arguments.get("output_file")
                    )
                elif name == "generate_basic_shape":
                    return await self._generate_basic_shape(
                        arguments.get("shape"),
                        arguments.get("size", 10),
                        arguments.get("height")
                    )
                elif name == "check_openscad_installed":
                    return await self._check_openscad_installed()
                else:
                    raise ValueError(f"Bilinmeyen tool: {name}")
            except Exception as e:
                logger.error(f"Tool hatası: {e}", exc_info=True)
                return [TextContent(
                    type="text",
                    text=f"Hata: {str(e)}"
                )]

    async def _set_openscad_workdir(self, path: str) -> list[TextContent]:
        """Çalışma dizinini ayarla"""
        work_path = Path(path).resolve()

        if not work_path.exists():
            # Dizin yoksa oluştur
            work_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Çalışma dizini oluşturuldu: {work_path}")

        self.work_dir = str(work_path)
        logger.info(f"OpenSCAD çalışma dizini ayarlandı: {self.work_dir}")

        return [TextContent(
            type="text",
            text=f"OpenSCAD çalışma dizini ayarlandı: {self.work_dir}"
        )]

    async def _list_scad_files(self) -> list[TextContent]:
        """Tüm .scad dosyalarını listele"""
        if not self.work_dir:
            return [TextContent(
                type="text",
                text="Hata: Önce set_openscad_workdir ile çalışma dizinini ayarlayın"
            )]

        scad_files = list(Path(self.work_dir).rglob("*.scad"))
        files_text = "\n".join([str(f.relative_to(self.work_dir)) for f in scad_files])

        return [TextContent(
            type="text",
            text=f"OpenSCAD Dosyaları ({len(scad_files)} adet):\n{files_text if files_text else '(Henüz dosya yok)'}"
        )]

    async def _read_scad_file(self, file_path: str) -> list[TextContent]:
        """OpenSCAD dosyasını oku"""
        if not self.work_dir:
            return [TextContent(
                type="text",
                text="Hata: Önce set_openscad_workdir ile çalışma dizinini ayarlayın"
            )]

        full_path = Path(self.work_dir) / file_path

        if not full_path.exists():
            return [TextContent(
                type="text",
                text=f"Hata: Dosya bulunamadı: {file_path}"
            )]

        try:
            content = full_path.read_text(encoding='utf-8')
            return [TextContent(
                type="text",
                text=f"=== {file_path} ===\n{content}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Dosya okunamadı: {e}"
            )]

    async def _write_scad_file(self, file_path: str, content: str) -> list[TextContent]:
        """OpenSCAD dosyası yaz"""
        if not self.work_dir:
            return [TextContent(
                type="text",
                text="Hata: Önce set_openscad_workdir ile çalışma dizinini ayarlayın"
            )]

        full_path = Path(self.work_dir) / file_path

        try:
            # Dizin yoksa oluştur
            full_path.parent.mkdir(parents=True, exist_ok=True)

            full_path.write_text(content, encoding='utf-8')
            logger.info(f"Dosya yazıldı: {file_path}")

            return [TextContent(
                type="text",
                text=f"Başarılı: {file_path} dosyası yazıldı/güncellendi ({len(content)} karakter)"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Dosya yazılamadı: {e}"
            )]

    async def _render_to_png(self, scad_file: str, output_file: str | None,
                             width: int, height: int) -> list[TextContent]:
        """OpenSCAD dosyasını PNG olarak render et"""
        if not self.work_dir:
            return [TextContent(
                type="text",
                text="Hata: Önce set_openscad_workdir ile çalışma dizinini ayarlayın"
            )]

        scad_path = Path(self.work_dir) / scad_file
        if not scad_path.exists():
            return [TextContent(
                type="text",
                text=f"Hata: SCAD dosyası bulunamadı: {scad_file}"
            )]

        # Çıktı dosyası belirtilmemişse otomatik oluştur
        if not output_file:
            output_file = scad_path.stem + ".png"

        output_path = Path(self.work_dir) / output_file

        try:
            # OpenSCAD komutunu çalıştır
            cmd = [
                self.openscad_executable,
                "-o", str(output_path),
                "--imgsize", f"{width},{height}",
                "--render",
                str(scad_path)
            ]

            logger.info(f"OpenSCAD render komutu: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60  # 60 saniye timeout
            )

            if result.returncode != 0:
                error_msg = result.stderr or result.stdout
                return [TextContent(
                    type="text",
                    text=f"Hata: OpenSCAD render başarısız:\n{error_msg}"
                )]

            return [TextContent(
                type="text",
                text=f"Başarılı: {scad_file} → {output_file} ({width}x{height})\nDosya konumu: {output_path}"
            )]

        except FileNotFoundError:
            return [TextContent(
                type="text",
                text="Hata: OpenSCAD bulunamadı. Lütfen OpenSCAD'in yüklü ve PATH'e eklenmiş olduğundan emin olun."
            )]
        except subprocess.TimeoutExpired:
            return [TextContent(
                type="text",
                text="Hata: OpenSCAD render işlemi zaman aşımına uğradı (60 saniye)"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: Render işlemi başarısız: {e}"
            )]

    async def _export_to_stl(self, scad_file: str, output_file: str | None) -> list[TextContent]:
        """OpenSCAD dosyasını STL formatına dönüştür"""
        if not self.work_dir:
            return [TextContent(
                type="text",
                text="Hata: Önce set_openscad_workdir ile çalışma dizinini ayarlayın"
            )]

        scad_path = Path(self.work_dir) / scad_file
        if not scad_path.exists():
            return [TextContent(
                type="text",
                text=f"Hata: SCAD dosyası bulunamadı: {scad_file}"
            )]

        # Çıktı dosyası belirtilmemişse otomatik oluştur
        if not output_file:
            output_file = scad_path.stem + ".stl"

        output_path = Path(self.work_dir) / output_file

        try:
            # OpenSCAD komutunu çalıştır
            cmd = [
                self.openscad_executable,
                "-o", str(output_path),
                str(scad_path)
            ]

            logger.info(f"OpenSCAD STL export komutu: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # STL export daha uzun sürebilir
            )

            if result.returncode != 0:
                error_msg = result.stderr or result.stdout
                return [TextContent(
                    type="text",
                    text=f"Hata: STL export başarısız:\n{error_msg}"
                )]

            # Dosya boyutunu al
            file_size = output_path.stat().st_size
            size_mb = file_size / (1024 * 1024)

            return [TextContent(
                type="text",
                text=f"Başarılı: {scad_file} → {output_file}\nDosya boyutu: {size_mb:.2f} MB\nKonum: {output_path}"
            )]

        except FileNotFoundError:
            return [TextContent(
                type="text",
                text="Hata: OpenSCAD bulunamadı. Lütfen OpenSCAD'in yüklü ve PATH'e eklenmiş olduğundan emin olun."
            )]
        except subprocess.TimeoutExpired:
            return [TextContent(
                type="text",
                text="Hata: STL export işlemi zaman aşımına uğradı (120 saniye)"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: STL export başarısız: {e}"
            )]

    async def _generate_basic_shape(self, shape: str, size: float, height: float | None) -> list[TextContent]:
        """Temel geometrik şekil kodu üret"""

        templates = {
            "cube": f"// Küp\ncube([{size}, {size}, {size}], center=true);",

            "sphere": f"// Küre\nsphere(r={size}, $fn=100);",

            "cylinder": f"// Silindir\ncylinder(h={height or size*2}, r={size}, center=true, $fn=100);",

            "cone": f"// Koni\ncylinder(h={height or size*2}, r1={size}, r2=0, center=true, $fn=100);",

            "torus": f"""// Torus
rotate_extrude($fn=100)
translate([{size*2}, 0, 0])
circle(r={size}, $fn=100);"""
        }

        if shape not in templates:
            return [TextContent(
                type="text",
                text=f"Hata: Geçersiz şekil tipi: {shape}. Kullanılabilir: cube, sphere, cylinder, cone, torus"
            )]

        code = templates[shape]

        return [TextContent(
            type="text",
            text=f"OpenSCAD kod üretildi ({shape}):\n\n```openscad\n{code}\n```\n\nBu kodu write_scad_file ile kaydedebilir veya mevcut bir dosyaya ekleyebilirsiniz."
        )]

    async def _check_openscad_installed(self) -> list[TextContent]:
        """OpenSCAD kurulumunu kontrol et"""
        try:
            result = subprocess.run(
                [self.openscad_executable, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )

            version_info = result.stdout or result.stderr

            return [TextContent(
                type="text",
                text=f"✅ OpenSCAD kurulu ve çalışıyor!\n\nVersiyon bilgisi:\n{version_info}"
            )]

        except FileNotFoundError:
            return [TextContent(
                type="text",
                text="""❌ OpenSCAD bulunamadı!

Kurulum talimatları:

**macOS:**
brew install openscad

**Ubuntu/Debian:**
sudo apt-get install openscad

**Windows:**
https://openscad.org/downloads.html adresinden indir

**Arch Linux:**
sudo pacman -S openscad

Kurulumdan sonra OpenSCAD'in PATH'e eklendiğinden emin olun.
"""
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Hata: OpenSCAD kontrolü başarısız: {e}"
            )]


async def main():
    """Ana fonksiyon"""
    logger.info("OpenSCAD MCP Server başlatılıyor...")

    # Server oluştur
    openscad_server = OpenSCADMCPServer()

    # CRITICAL: stdio kullan - stdout sadece JSON, stderr loglar için
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("MCP server hazır ve bağlantı bekliyor...")
        await openscad_server.server.run(
            read_stream,
            write_stream,
            openscad_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
