#!/usr/bin/env python3
"""
Minimax TTS MCP Server - Claude Desktop ile Minimax Text-to-Speech API entegrasyonu
"""
import sys
import os
import asyncio
import json
from typing import Any
from pathlib import Path
import base64

# CRITICAL: Tüm logları stderr'e yönlendir
# stdout sadece MCP JSON-RPC mesajları için kullanılmalı
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[MINIMAX-TTS-MCP] %(levelname)s: %(message)s',
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
    import aiohttp
except ImportError:
    logger.error("aiohttp paketi bulunamadı. Lütfen yükleyin: pip install aiohttp")
    sys.exit(1)


class MinimaxTTSMCPServer:
    """Minimax Text-to-Speech için MCP sunucusu"""

    def __init__(self):
        self.server = Server("minimax-tts-mcp-server")
        self.api_key: str | None = os.getenv("MINIMAX_API_KEY")
        self.group_id: str | None = os.getenv("MINIMAX_GROUP_ID")
        self.output_dir: Path = Path.home() / "minimax_tts_outputs"

        # Çıktı dizinini oluştur
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Çıktı dizini: {self.output_dir}")

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
                    name="set_minimax_credentials",
                    description="Minimax API anahtarını ve Group ID'yi ayarla",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "api_key": {
                                "type": "string",
                                "description": "Minimax API Key (Bearer token)"
                            },
                            "group_id": {
                                "type": "string",
                                "description": "Minimax Group ID (19 haneli sayı)"
                            }
                        },
                        "required": ["api_key", "group_id"]
                    }
                ),
                Tool(
                    name="text_to_speech",
                    description="Metni sese dönüştür (Minimax TTS API). Ses dosyası kaydedilir ve yolu döndürülür.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Sese dönüştürülecek metin"
                            },
                            "voice_id": {
                                "type": "string",
                                "description": "Ses kimliği (örn: male-qn-qingse, female-shaonv, Affectionate_Male_Voice, vb.)",
                                "default": "male-qn-qingse"
                            },
                            "model": {
                                "type": "string",
                                "description": "Model seçimi: speech-02-hd (yüksek kalite) veya speech-02-turbo (hızlı)",
                                "enum": ["speech-02-hd", "speech-02-turbo"],
                                "default": "speech-02-hd"
                            },
                            "speed": {
                                "type": "number",
                                "description": "Konuşma hızı (0.5 - 2.0, varsayılan: 1.0)",
                                "default": 1.0
                            },
                            "vol": {
                                "type": "number",
                                "description": "Ses seviyesi (0.1 - 10.0, varsayılan: 1.0)",
                                "default": 1.0
                            },
                            "pitch": {
                                "type": "number",
                                "description": "Ses tonu yüksekliği (-12 - 12, varsayılan: 0)",
                                "default": 0
                            },
                            "output_format": {
                                "type": "string",
                                "description": "Çıktı formatı",
                                "enum": ["mp3", "wav", "pcm", "flac"],
                                "default": "mp3"
                            },
                            "filename": {
                                "type": "string",
                                "description": "Kaydedilecek dosya adı (opsiyonel, verilmezse otomatik oluşturulur)"
                            }
                        },
                        "required": ["text"]
                    }
                ),
                Tool(
                    name="list_available_voices",
                    description="Kullanılabilir ses listesini göster (yaygın sesler)",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="set_output_directory",
                    description="Ses dosyalarının kaydedileceği dizini ayarla",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Çıktı dizini yolu"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="get_api_status",
                    description="API bağlantı durumunu ve yapılandırmayı kontrol et",
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
                if name == "set_minimax_credentials":
                    return await self._set_credentials(
                        arguments.get("api_key"),
                        arguments.get("group_id")
                    )
                elif name == "text_to_speech":
                    return await self._text_to_speech(arguments)
                elif name == "list_available_voices":
                    return await self._list_voices()
                elif name == "set_output_directory":
                    return await self._set_output_directory(arguments.get("path"))
                elif name == "get_api_status":
                    return await self._get_api_status()
                else:
                    raise ValueError(f"Bilinmeyen tool: {name}")
            except Exception as e:
                logger.error(f"Tool hatası: {e}", exc_info=True)
                return [TextContent(
                    type="text",
                    text=f"Hata: {str(e)}"
                )]

    async def _set_credentials(self, api_key: str, group_id: str) -> list[TextContent]:
        """API anahtarını ve Group ID'yi ayarla"""
        if not api_key or not group_id:
            return [TextContent(
                type="text",
                text="Hata: API key ve Group ID gerekli"
            )]

        self.api_key = api_key
        self.group_id = group_id
        logger.info("Minimax credentials ayarlandı")

        return [TextContent(
            type="text",
            text=f"✅ Minimax API bilgileri ayarlandı\n- Group ID: {group_id[:5]}...{group_id[-4:]}\n- API Key: {api_key[:8]}...{api_key[-4:]}"
        )]

    async def _text_to_speech(self, arguments: dict) -> list[TextContent]:
        """Metni sese dönüştür"""
        if not self.api_key or not self.group_id:
            return [TextContent(
                type="text",
                text="❌ Hata: Önce set_minimax_credentials ile API bilgilerini ayarlayın\n"
                     "Veya MINIMAX_API_KEY ve MINIMAX_GROUP_ID ortam değişkenlerini ayarlayın"
            )]

        text = arguments.get("text")
        if not text:
            return [TextContent(
                type="text",
                text="Hata: Metin parametresi gerekli"
            )]

        # Parametreleri al
        voice_id = arguments.get("voice_id", "male-qn-qingse")
        model = arguments.get("model", "speech-02-hd")
        speed = arguments.get("speed", 1.0)
        vol = arguments.get("vol", 1.0)
        pitch = arguments.get("pitch", 0)
        output_format = arguments.get("output_format", "mp3")
        filename = arguments.get("filename")

        # Dosya adı oluştur
        if not filename:
            import time
            timestamp = int(time.time())
            filename = f"minimax_tts_{timestamp}.{output_format}"
        elif not filename.endswith(f".{output_format}"):
            filename = f"{filename}.{output_format}"

        output_path = self.output_dir / filename

        # API çağrısı yap
        url = f"https://api.minimaxi.chat/v1/t2a_v2?GroupId={self.group_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "model": model,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed,
                "vol": vol,
                "pitch": pitch
            },
            "audio_setting": {
                "format": output_format,
                "sample_rate": 32000 if model == "speech-02-hd" else 24000
            }
        }

        logger.info(f"TTS isteği gönderiliyor: {len(text)} karakter, voice={voice_id}, model={model}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"API hatası: {response.status} - {error_text}")
                        return [TextContent(
                            type="text",
                            text=f"❌ API Hatası ({response.status}): {error_text}"
                        )]

                    # Yanıtı JSON olarak oku
                    result = await response.json()

                    # Base64 encoded audio data
                    if "data" in result and "audio" in result["data"]:
                        audio_data = result["data"]["audio"]
                        # Base64 decode
                        audio_bytes = base64.b64decode(audio_data)

                        # Dosyaya yaz
                        output_path.write_bytes(audio_bytes)

                        logger.info(f"Ses dosyası kaydedildi: {output_path}")

                        file_size_kb = len(audio_bytes) / 1024

                        return [TextContent(
                            type="text",
                            text=f"✅ Ses dosyası oluşturuldu!\n\n"
                                 f"📁 Dosya: {output_path}\n"
                                 f"📊 Boyut: {file_size_kb:.2f} KB\n"
                                 f"🎤 Ses: {voice_id}\n"
                                 f"🎵 Model: {model}\n"
                                 f"📝 Metin uzunluğu: {len(text)} karakter"
                        )]
                    else:
                        logger.error(f"Beklenmeyen API yanıtı: {result}")
                        return [TextContent(
                            type="text",
                            text=f"❌ Beklenmeyen API yanıtı: {json.dumps(result, indent=2)}"
                        )]

        except aiohttp.ClientError as e:
            logger.error(f"HTTP hatası: {e}")
            return [TextContent(
                type="text",
                text=f"❌ Bağlantı hatası: {str(e)}"
            )]
        except Exception as e:
            logger.error(f"TTS hatası: {e}", exc_info=True)
            return [TextContent(
                type="text",
                text=f"❌ Hata: {str(e)}"
            )]

    async def _list_voices(self) -> list[TextContent]:
        """Yaygın ses listesini göster"""
        voices_info = """
🎤 Minimax TTS - Kullanılabilir Sesler

**Erkek Sesler:**
- `male-qn-qingse` - Erkek ses (varsayılan)
- `Affectionate_Male_Voice` - Sevecen erkek sesi
- `Audiobook_Male_Voice` - Sesli kitap erkek sesi
- `News_Male_Voice` - Haber spikeri erkek sesi

**Kadın Sesler:**
- `female-shaonv` - Genç kadın sesi
- `Gentle_Female_Voice` - Yumuşak kadın sesi
- `Mature_Female_Voice_1` - Olgun kadın sesi 1
- `Mature_Female_Voice_2` - Olgun kadın sesi 2
- `Sweet_Female_Voice` - Tatlı kadın sesi

**Özel Sesler:**
- `Cute_Child_Voice` - Sevimli çocuk sesi
- `Calm_Narration` - Sakin anlatım
- `Documentary_Narration` - Belgesel anlatımı

**Kullanım:**
`text_to_speech` tool'unda `voice_id` parametresine yukarıdaki ID'lerden birini verin.

**Modeller:**
- `speech-02-hd` - Yüksek kalite (sesli kitaplar, video voice-over için önerilir)
- `speech-02-turbo` - Hızlı ve ekonomik (gerçek zamanlı uygulamalar için)
"""
        return [TextContent(type="text", text=voices_info)]

    async def _set_output_directory(self, path: str) -> list[TextContent]:
        """Çıktı dizinini ayarla"""
        try:
            output_dir = Path(path).resolve()
            output_dir.mkdir(parents=True, exist_ok=True)
            self.output_dir = output_dir
            logger.info(f"Çıktı dizini ayarlandı: {self.output_dir}")

            return [TextContent(
                type="text",
                text=f"✅ Çıktı dizini ayarlandı: {self.output_dir}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Hata: {str(e)}"
            )]

    async def _get_api_status(self) -> list[TextContent]:
        """API durumunu kontrol et"""
        status = "✅ API bilgileri ayarlanmış" if (self.api_key and self.group_id) else "❌ API bilgileri ayarlanmamış"

        info = f"""
📊 Minimax TTS MCP Server Durumu

🔑 API Durumu: {status}
"""
        if self.api_key and self.group_id:
            info += f"   - Group ID: {self.group_id[:5]}...{self.group_id[-4:]}\n"
            info += f"   - API Key: {self.api_key[:8]}...{self.api_key[-4:]}\n"
        else:
            info += "   ⚠️  set_minimax_credentials ile ayarlayın\n"
            info += "   veya MINIMAX_API_KEY ve MINIMAX_GROUP_ID ortam değişkenlerini kullanın\n"

        info += f"\n📁 Çıktı Dizini: {self.output_dir}\n"
        info += f"🌐 API Endpoint: https://api.minimaxi.chat/v1/t2a_v2\n"

        return [TextContent(type="text", text=info)]


async def main():
    """Ana fonksiyon"""
    logger.info("Minimax TTS MCP Server başlatılıyor...")

    # Server oluştur
    minimax_server = MinimaxTTSMCPServer()

    # CRITICAL: stdio kullan - stdout sadece JSON, stderr loglar için
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("MCP server hazır ve bağlantı bekliyor...")
        await minimax_server.server.run(
            read_stream,
            write_stream,
            minimax_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
