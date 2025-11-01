#!/usr/bin/env python3
"""
Text-generation-webui MCP Server - Claude Desktop ile Text-generation-webui arasında köprü kurar
"""
import sys
import os
import asyncio
import json
from typing import Any, Optional
import aiohttp

# CRITICAL: Tüm logları stderr'e yönlendir
# stdout sadece MCP JSON-RPC mesajları için kullanılmalı
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[TEXTGEN-MCP] %(levelname)s: %(message)s',
    stream=sys.stderr  # stdout DEĞİL, stderr kullan!
)
logger = logging.getLogger(__name__)

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
except ImportError:
    logger.error("mcp paketi bulunamadı. Lütfen yükleyin: pip install mcp")
    sys.exit(1)


class TextGenWebUIMCPServer:
    """Text-generation-webui için MCP sunucusu"""

    def __init__(self):
        self.server = Server("textgen-webui-mcp-server")
        self.base_url: str = "http://127.0.0.1:5000"
        self.api_key: Optional[str] = None

        # Tool'ları kaydet
        self._register_handlers()

    def _get_headers(self) -> dict:
        """API başlıklarını hazırla"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _register_handlers(self):
        """MCP handler'ları kaydet"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Kullanılabilir araçları listele"""
            logger.info("Araçlar listeleniyor...")
            return [
                Tool(
                    name="set_textgen_config",
                    description="Text-generation-webui bağlantı ayarlarını yapılandır (URL ve API key)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "base_url": {
                                "type": "string",
                                "description": "Text-generation-webui API URL'i (örn: http://127.0.0.1:5000)",
                                "default": "http://127.0.0.1:5000"
                            },
                            "api_key": {
                                "type": "string",
                                "description": "API anahtarı (opsiyonel)"
                            }
                        }
                    }
                ),
                Tool(
                    name="list_models",
                    description="Text-generation-webui'de yüklü modelleri listele",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="chat_completion",
                    description="Chat formatında model ile konuş (instruction-following modeller için)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "messages": {
                                "type": "array",
                                "description": "Chat mesajları (örn: [{'role': 'user', 'content': 'Merhaba'}])",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "role": {
                                            "type": "string",
                                            "enum": ["system", "user", "assistant"]
                                        },
                                        "content": {
                                            "type": "string"
                                        }
                                    },
                                    "required": ["role", "content"]
                                }
                            },
                            "max_tokens": {
                                "type": "integer",
                                "description": "Maksimum üretilecek token sayısı",
                                "default": 512
                            },
                            "temperature": {
                                "type": "number",
                                "description": "Yaratıcılık seviyesi (0.0-2.0)",
                                "default": 0.7
                            },
                            "top_p": {
                                "type": "number",
                                "description": "Nucleus sampling parametresi",
                                "default": 0.9
                            }
                        },
                        "required": ["messages"]
                    }
                ),
                Tool(
                    name="text_completion",
                    description="Basit metin tamamlama (prompt'tan devam eder)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Tamamlanacak metin"
                            },
                            "max_tokens": {
                                "type": "integer",
                                "description": "Maksimum üretilecek token sayısı",
                                "default": 512
                            },
                            "temperature": {
                                "type": "number",
                                "description": "Yaratıcılık seviyesi (0.0-2.0)",
                                "default": 0.7
                            },
                            "top_p": {
                                "type": "number",
                                "description": "Nucleus sampling parametresi",
                                "default": 0.9
                            },
                            "stop": {
                                "type": "array",
                                "description": "Durma token'ları",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["prompt"]
                    }
                ),
                Tool(
                    name="get_model_info",
                    description="Şu anda yüklü olan model hakkında bilgi al",
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
                if name == "set_textgen_config":
                    return await self._set_textgen_config(
                        arguments.get("base_url", "http://127.0.0.1:5000"),
                        arguments.get("api_key")
                    )
                elif name == "list_models":
                    return await self._list_models()
                elif name == "chat_completion":
                    return await self._chat_completion(
                        arguments.get("messages"),
                        arguments.get("max_tokens", 512),
                        arguments.get("temperature", 0.7),
                        arguments.get("top_p", 0.9)
                    )
                elif name == "text_completion":
                    return await self._text_completion(
                        arguments.get("prompt"),
                        arguments.get("max_tokens", 512),
                        arguments.get("temperature", 0.7),
                        arguments.get("top_p", 0.9),
                        arguments.get("stop")
                    )
                elif name == "get_model_info":
                    return await self._get_model_info()
                else:
                    raise ValueError(f"Bilinmeyen tool: {name}")
            except Exception as e:
                logger.error(f"Tool hatası: {e}", exc_info=True)
                return [TextContent(
                    type="text",
                    text=f"Hata: {str(e)}"
                )]

    async def _set_textgen_config(self, base_url: str, api_key: Optional[str] = None) -> list[TextContent]:
        """Text-generation-webui bağlantı ayarlarını yapılandır"""
        # URL'den sondaki / işaretini kaldır
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key

        logger.info(f"Text-generation-webui URL ayarlandı: {self.base_url}")

        # Bağlantıyı test et
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/v1/models",
                    headers=self._get_headers(),
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        return [TextContent(
                            type="text",
                            text=f"✓ Text-generation-webui bağlantısı başarılı!\nURL: {self.base_url}\nAPI Key: {'Ayarlandı' if api_key else 'Yok'}"
                        )]
                    else:
                        return [TextContent(
                            type="text",
                            text=f"⚠ Bağlantı ayarlandı ama sunucu yanıt vermiyor (HTTP {response.status})\nURL: {self.base_url}\nLütfen Text-generation-webui'nin çalıştığından emin olun."
                        )]
        except Exception as e:
            logger.warning(f"Bağlantı testi başarısız: {e}")
            return [TextContent(
                type="text",
                text=f"⚠ Bağlantı ayarlandı ama sunucuya ulaşılamadı: {e}\nURL: {self.base_url}\nLütfen Text-generation-webui'nin çalıştığından ve URL'in doğru olduğundan emin olun."
            )]

    async def _list_models(self) -> list[TextContent]:
        """Yüklü modelleri listele"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/v1/models",
                    headers=self._get_headers(),
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status != 200:
                        return [TextContent(
                            type="text",
                            text=f"Hata: API'den yanıt alınamadı (HTTP {response.status})"
                        )]

                    data = await response.json()
                    models = data.get("data", [])

                    if not models:
                        return [TextContent(
                            type="text",
                            text="Hiç model yüklü değil."
                        )]

                    models_text = "\n".join([
                        f"- {model.get('id', 'unknown')}"
                        for model in models
                    ])

                    return [TextContent(
                        type="text",
                        text=f"Yüklü Modeller ({len(models)} adet):\n{models_text}"
                    )]
        except Exception as e:
            logger.error(f"Model listesi alınamadı: {e}")
            return [TextContent(
                type="text",
                text=f"Hata: {e}\n\nText-generation-webui'nin çalıştığından emin olun.\nEğer çalışıyorsa, önce 'set_textgen_config' ile bağlantı ayarlarını yapılandırın."
            )]

    async def _chat_completion(
        self,
        messages: list[dict],
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> list[TextContent]:
        """Chat tamamlama"""
        if not messages:
            return [TextContent(
                type="text",
                text="Hata: En az bir mesaj gerekli"
            )]

        try:
            payload = {
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "stream": False
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/v1/chat/completions",
                    headers=self._get_headers(),
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return [TextContent(
                            type="text",
                            text=f"Hata: API'den yanıt alınamadı (HTTP {response.status})\n{error_text}"
                        )]

                    data = await response.json()

                    # Yanıtı çıkar
                    if "choices" in data and len(data["choices"]) > 0:
                        message = data["choices"][0].get("message", {})
                        content = message.get("content", "")

                        # Kullanım istatistikleri
                        usage = data.get("usage", {})
                        stats = f"\n\n---\n📊 Token Kullanımı: Prompt: {usage.get('prompt_tokens', '?')}, Tamamlama: {usage.get('completion_tokens', '?')}, Toplam: {usage.get('total_tokens', '?')}"

                        return [TextContent(
                            type="text",
                            text=f"{content}{stats}"
                        )]
                    else:
                        return [TextContent(
                            type="text",
                            text="Hata: API'den beklenmeyen yanıt formatı"
                        )]
        except Exception as e:
            logger.error(f"Chat tamamlama hatası: {e}")
            return [TextContent(
                type="text",
                text=f"Hata: {e}"
            )]

    async def _text_completion(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stop: Optional[list[str]] = None
    ) -> list[TextContent]:
        """Basit metin tamamlama"""
        if not prompt:
            return [TextContent(
                type="text",
                text="Hata: Prompt gerekli"
            )]

        try:
            payload = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "stream": False
            }

            if stop:
                payload["stop"] = stop

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/v1/completions",
                    headers=self._get_headers(),
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return [TextContent(
                            type="text",
                            text=f"Hata: API'den yanıt alınamadı (HTTP {response.status})\n{error_text}"
                        )]

                    data = await response.json()

                    # Yanıtı çıkar
                    if "choices" in data and len(data["choices"]) > 0:
                        text = data["choices"][0].get("text", "")

                        # Kullanım istatistikleri
                        usage = data.get("usage", {})
                        stats = f"\n\n---\n📊 Token Kullanımı: Prompt: {usage.get('prompt_tokens', '?')}, Tamamlama: {usage.get('completion_tokens', '?')}, Toplam: {usage.get('total_tokens', '?')}"

                        return [TextContent(
                            type="text",
                            text=f"{text}{stats}"
                        )]
                    else:
                        return [TextContent(
                            type="text",
                            text="Hata: API'den beklenmeyen yanıt formatı"
                        )]
        except Exception as e:
            logger.error(f"Metin tamamlama hatası: {e}")
            return [TextContent(
                type="text",
                text=f"Hata: {e}"
            )]

    async def _get_model_info(self) -> list[TextContent]:
        """Aktif model bilgisi"""
        try:
            # Önce model listesini al
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/v1/models",
                    headers=self._get_headers(),
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status != 200:
                        return [TextContent(
                            type="text",
                            text=f"Hata: Model bilgisi alınamadı (HTTP {response.status})"
                        )]

                    data = await response.json()
                    models = data.get("data", [])

                    if not models:
                        return [TextContent(
                            type="text",
                            text="Hiç model yüklü değil."
                        )]

                    # İlk modeli aktif model olarak kabul et
                    model = models[0]
                    model_id = model.get("id", "unknown")
                    owned_by = model.get("owned_by", "N/A")
                    created = model.get("created", "N/A")

                    info = f"""🤖 Aktif Model Bilgisi:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Model ID: {model_id}
👤 Sahip: {owned_by}
📅 Oluşturma: {created}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Toplam yüklü model sayısı: {len(models)}
"""

                    return [TextContent(
                        type="text",
                        text=info
                    )]
        except Exception as e:
            logger.error(f"Model bilgisi alınamadı: {e}")
            return [TextContent(
                type="text",
                text=f"Hata: {e}"
            )]


async def main():
    """Ana fonksiyon"""
    logger.info("Text-generation-webui MCP Server başlatılıyor...")

    # Server oluştur
    textgen_server = TextGenWebUIMCPServer()

    # CRITICAL: stdio kullan - stdout sadece JSON, stderr loglar için
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("MCP server hazır ve bağlantı bekliyor...")
        await textgen_server.server.run(
            read_stream,
            write_stream,
            textgen_server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
