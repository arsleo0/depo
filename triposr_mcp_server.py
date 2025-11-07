#!/usr/bin/env python3
"""
TripoSR MCP Server - Claude Desktop ile TripoSR arasında köprü kurar
Görüntüden 3D model oluşturma için AI kullanır
"""
import sys
import os
import asyncio
import json
from typing import Any
from pathlib import Path
import tempfile

# CRITICAL: Tüm logları stderr'e yönlendir
# stdout sadece MCP JSON-RPC mesajları için kullanılmalı
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[TRIPOSR-MCP] %(levelname)s: %(message)s',
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

try:
    import torch
    from PIL import Image
    import numpy as np
except ImportError:
    logger.error("Gerekli paketler bulunamadı. Lütfen yükleyin: pip install torch pillow numpy")
    sys.exit(1)

try:
    # TripoSR modelini yükle
    from tsr.system import TSR
    from tsr.utils import remove_background, resize_foreground
except ImportError:
    logger.warning("TripoSR bulunamadı. Model yüklenemeyecek. GitHub'dan yükleyin: https://github.com/VAST-AI-Research/TripoSR")
    TSR = None


class TripoSRMCPServer:
    """TripoSR için MCP sunucusu - Görüntüden 3D model oluşturma"""

    def __init__(self):
        self.server = Server("triposr-mcp-server")
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_dir = str(Path.home() / "Desktop" / "triposr_outputs")

        # Çıktı dizinini oluştur
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        logger.info(f"TripoSR MCP Server başlatılıyor... (Device: {self.device})")

        # Tool'ları kaydet
        self._register_handlers()

    def _load_model(self):
        """TripoSR modelini yükle (lazy loading)"""
        if self.model is None and TSR is not None:
            try:
                logger.info("TripoSR modeli yükleniyor... (Bu birkaç dakika sürebilir)")
                self.model = TSR.from_pretrained(
                    "stabilityai/TripoSR",
                    config_name="config.yaml",
                    weight_name="model.ckpt",
                )
                self.model.to(self.device)
                logger.info(f"TripoSR modeli başarıyla yüklendi! (Device: {self.device})")
            except Exception as e:
                logger.error(f"Model yüklenirken hata: {e}")
                raise
        return self.model

    def _register_handlers(self):
        """MCP handler'ları kaydet"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Kullanılabilir araçları listele"""
            logger.info("Araçlar listeleniyor...")
            return [
                Tool(
                    name="check_triposr_status",
                    description="TripoSR durumunu ve ayarlarını kontrol et",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="set_output_directory",
                    description="3D modellerin kaydedileceği çıktı dizinini ayarla",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Çıktı dizini (ör: /Users/name/Desktop/models)"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="generate_3d_from_image",
                    description="Bir görüntüden 3D model oluştur (TripoSR AI kullanarak)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_path": {
                                "type": "string",
                                "description": "Kaynak görüntü dosyasının tam yolu"
                            },
                            "output_name": {
                                "type": "string",
                                "description": "Çıktı dosya adı (uzantısız, ör: 'my_model')"
                            },
                            "remove_background": {
                                "type": "boolean",
                                "description": "Arka planı otomatik kaldır (önerilen: true)",
                                "default": True
                            },
                            "foreground_ratio": {
                                "type": "number",
                                "description": "Ön plan oranı (0.5-1.0, varsayılan: 0.85)",
                                "default": 0.85
                            }
                        },
                        "required": ["image_path", "output_name"]
                    }
                ),
                Tool(
                    name="batch_generate_3d",
                    description="Birden fazla görüntüden toplu 3D model oluştur",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Görüntü dosyalarının yolları listesi"
                            },
                            "remove_background": {
                                "type": "boolean",
                                "description": "Arka planı otomatik kaldır",
                                "default": True
                            }
                        },
                        "required": ["image_paths"]
                    }
                ),
                Tool(
                    name="list_generated_models",
                    description="Oluşturulmuş 3D modelleri listele",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Tool çağrılarını işle"""
            logger.info(f"Tool çağrıldı: {name}")

            try:
                if name == "check_triposr_status":
                    return await self._check_status()
                elif name == "set_output_directory":
                    return await self._set_output_directory(arguments.get("path"))
                elif name == "generate_3d_from_image":
                    return await self._generate_3d_from_image(
                        arguments.get("image_path"),
                        arguments.get("output_name"),
                        arguments.get("remove_background", True),
                        arguments.get("foreground_ratio", 0.85)
                    )
                elif name == "batch_generate_3d":
                    return await self._batch_generate_3d(
                        arguments.get("image_paths", []),
                        arguments.get("remove_background", True)
                    )
                elif name == "list_generated_models":
                    return await self._list_generated_models()
                else:
                    return [TextContent(
                        type="text",
                        text=f"❌ Bilinmeyen tool: {name}"
                    )]

            except Exception as e:
                logger.error(f"Tool hatası ({name}): {e}", exc_info=True)
                return [TextContent(
                    type="text",
                    text=f"❌ Hata: {str(e)}"
                )]

    async def _check_status(self) -> list[TextContent]:
        """TripoSR durumunu kontrol et"""
        status = {
            "✅ TripoSR MCP Server": "Çalışıyor",
            "🖥️ Device": self.device,
            "📦 Model Yüklü": "Evet" if self.model else "Hayır (ilk kullanımda yüklenecek)",
            "📁 Çıktı Dizini": self.output_dir,
            "🔧 PyTorch": torch.__version__,
            "🎮 CUDA Mevcut": "Evet ✅" if torch.cuda.is_available() else "Hayır (CPU kullanılacak)"
        }

        if torch.cuda.is_available():
            status["🎮 GPU"] = torch.cuda.get_device_name(0)
            status["💾 GPU Bellek"] = f"{torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB"

        result = "\n".join([f"{k}: {v}" for k, v in status.items()])

        return [TextContent(
            type="text",
            text=f"**TripoSR Durum Raporu**\n\n{result}"
        )]

    async def _set_output_directory(self, path: str) -> list[TextContent]:
        """Çıktı dizinini ayarla"""
        try:
            output_path = Path(path).expanduser().resolve()
            output_path.mkdir(parents=True, exist_ok=True)
            self.output_dir = str(output_path)

            return [TextContent(
                type="text",
                text=f"✅ Çıktı dizini ayarlandı: {self.output_dir}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Dizin oluşturulamadı: {e}"
            )]

    async def _generate_3d_from_image(
        self,
        image_path: str,
        output_name: str,
        remove_bg: bool = True,
        foreground_ratio: float = 0.85
    ) -> list[TextContent]:
        """Görüntüden 3D model oluştur"""
        try:
            # Modeli yükle (lazy loading)
            if TSR is None:
                return [TextContent(
                    type="text",
                    text="❌ TripoSR yüklü değil! Lütfen şu adımları takip edin:\n\n"
                         "1. GitHub'dan klonlayın: git clone https://github.com/VAST-AI-Research/TripoSR.git\n"
                         "2. Kurulum yapın: cd TripoSR && pip install -r requirements.txt && pip install -e .\n"
                         "3. MCP server'ı yeniden başlatın"
                )]

            model = self._load_model()

            # Görüntüyü yükle
            logger.info(f"Görüntü yükleniyor: {image_path}")
            image_path = Path(image_path).expanduser().resolve()

            if not image_path.exists():
                return [TextContent(
                    type="text",
                    text=f"❌ Görüntü bulunamadı: {image_path}"
                )]

            image = Image.open(image_path)

            # Arka planı kaldır (opsiyonel)
            if remove_bg:
                logger.info("Arka plan kaldırılıyor...")
                image = remove_background(image)
                image = resize_foreground(image, foreground_ratio)

            # 3D model oluştur
            logger.info("3D model oluşturuluyor... (Bu 30-60 saniye sürebilir)")

            with torch.no_grad():
                # Görüntüyü model formatına çevir
                from torchvision.transforms import functional as TF
                image_tensor = TF.to_tensor(image).unsqueeze(0).to(self.device)

                # Model inference
                scene_codes = model([image_tensor], device=self.device)

            # Mesh'i kaydet
            output_path = Path(self.output_dir) / f"{output_name}.obj"
            logger.info(f"Model kaydediliyor: {output_path}")

            # GLB ve OBJ formatlarında kaydet
            mesh = model.extract_mesh(scene_codes[0])
            mesh.export(str(output_path))

            # GLB formatında da kaydet
            glb_path = Path(self.output_dir) / f"{output_name}.glb"
            mesh.export(str(glb_path))

            return [TextContent(
                type="text",
                text=f"✅ 3D model başarıyla oluşturuldu!\n\n"
                     f"📁 OBJ: {output_path}\n"
                     f"📁 GLB: {glb_path}\n\n"
                     f"🎨 Kaynak Görüntü: {image_path}\n"
                     f"🔧 Device: {self.device}\n"
                     f"🖼️ Arka Plan Kaldırıldı: {'Evet' if remove_bg else 'Hayır'}\n\n"
                     f"💡 İpucu: Bu modeli Blender, Unity, Godot gibi 3D yazılımlarda kullanabilirsiniz!"
            )]

        except Exception as e:
            logger.error(f"3D oluşturma hatası: {e}", exc_info=True)
            return [TextContent(
                type="text",
                text=f"❌ 3D model oluşturulamadı: {str(e)}"
            )]

    async def _batch_generate_3d(
        self,
        image_paths: list[str],
        remove_bg: bool = True
    ) -> list[TextContent]:
        """Toplu 3D model oluştur"""
        results = []
        success_count = 0

        for i, image_path in enumerate(image_paths, 1):
            logger.info(f"İşleniyor {i}/{len(image_paths)}: {image_path}")

            # Output adını görüntü dosyasından al
            output_name = Path(image_path).stem + "_3d"

            result = await self._generate_3d_from_image(
                image_path,
                output_name,
                remove_bg
            )

            if "✅" in result[0].text:
                success_count += 1

            results.append(f"[{i}/{len(image_paths)}] {Path(image_path).name}: {'✅' if '✅' in result[0].text else '❌'}")

        summary = "\n".join(results)

        return [TextContent(
            type="text",
            text=f"**Toplu 3D Oluşturma Tamamlandı**\n\n"
                 f"✅ Başarılı: {success_count}/{len(image_paths)}\n"
                 f"📁 Çıktı Dizini: {self.output_dir}\n\n"
                 f"**Detaylar:**\n{summary}"
        )]

    async def _list_generated_models(self) -> list[TextContent]:
        """Oluşturulmuş modelleri listele"""
        try:
            output_path = Path(self.output_dir)

            obj_files = sorted(output_path.glob("*.obj"))
            glb_files = sorted(output_path.glob("*.glb"))

            if not obj_files and not glb_files:
                return [TextContent(
                    type="text",
                    text=f"📁 {self.output_dir}\n\nHenüz model oluşturulmamış."
                )]

            obj_list = "\n".join([f"  • {f.name} ({f.stat().st_size / 1024:.1f} KB)" for f in obj_files])
            glb_list = "\n".join([f"  • {f.name} ({f.stat().st_size / 1024:.1f} KB)" for f in glb_files])

            result = f"**Oluşturulmuş 3D Modeller**\n\n📁 Dizin: {self.output_dir}\n\n"

            if obj_files:
                result += f"**OBJ Dosyaları ({len(obj_files)}):**\n{obj_list}\n\n"

            if glb_files:
                result += f"**GLB Dosyaları ({len(glb_files)}):**\n{glb_list}\n\n"

            result += "💡 İpucu: Bu modelleri Blender, Unity, Godot veya herhangi bir 3D yazılımda açabilirsiniz!"

            return [TextContent(
                type="text",
                text=result
            )]

        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Liste alınırken hata: {e}"
            )]

    async def run(self):
        """MCP sunucusunu başlat"""
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            logger.info("TripoSR MCP Server hazır! 🚀")
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def main():
    """Ana fonksiyon"""
    server = TripoSRMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
