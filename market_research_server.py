#!/usr/bin/env python3
"""
Market Research MCP Server
3D Print Ecosystem - Pazar Araştırması ve Trend Analizi

Bu sunucu Claude Desktop'ın internetten ürün, fiyat ve pazar araştırması
yapmasını sağlar.
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

# MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("ERROR: MCP SDK not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Web scraping ve analiz kütüphaneleri
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Install requirements: pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)

# Logger kurulumu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("market-research-server")

# Server instance
app = Server("3d-print-market-research")


class MarketResearchEngine:
    """Pazar araştırması ve trend analizi motoru"""

    def __init__(self):
        self.cache = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def search_etsy(self, keyword: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Etsy'de ürün araştırması"""
        logger.info(f"Searching Etsy for: {keyword}")

        # Etsy search URL
        url = f"https://www.etsy.com/search?q={keyword.replace(' ', '+')}"

        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            products = []
            # Etsy ürün kartlarını parse et
            items = soup.find_all('div', {'class': lambda x: x and 'listing' in x.lower()}, limit=limit)

            for item in items:
                try:
                    # Title
                    title_elem = item.find('h3') or item.find('a', {'class': lambda x: x and 'listing' in x.lower()})
                    title = title_elem.get_text(strip=True) if title_elem else "Unknown"

                    # Price
                    price_elem = item.find('span', {'class': lambda x: x and 'price' in x.lower()})
                    price = price_elem.get_text(strip=True) if price_elem else "N/A"

                    # Rating
                    rating_elem = item.find('span', {'class': lambda x: x and 'rating' in x.lower()})
                    rating = rating_elem.get_text(strip=True) if rating_elem else "N/A"

                    # Link
                    link_elem = item.find('a', href=True)
                    link = link_elem['href'] if link_elem else ""

                    products.append({
                        'title': title,
                        'price': price,
                        'rating': rating,
                        'link': link,
                        'platform': 'etsy'
                    })
                except Exception as e:
                    logger.warning(f"Error parsing Etsy item: {e}")
                    continue

            logger.info(f"Found {len(products)} products on Etsy")
            return products

        except Exception as e:
            logger.error(f"Etsy search error: {e}")
            return []

    def search_thingiverse(self, keyword: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Thingiverse'de model araştırması"""
        logger.info(f"Searching Thingiverse for: {keyword}")

        url = f"https://www.thingiverse.com/search?q={keyword.replace(' ', '+')}&type=things"

        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            models = []
            items = soup.find_all('div', {'class': lambda x: x and 'thing' in x.lower()}, limit=limit)

            for item in items:
                try:
                    title_elem = item.find('a', {'class': lambda x: x and 'thing-link' in x.lower()})
                    title = title_elem.get_text(strip=True) if title_elem else "Unknown"

                    link_elem = item.find('a', href=True)
                    link = f"https://www.thingiverse.com{link_elem['href']}" if link_elem else ""

                    # Likes
                    likes_elem = item.find('span', {'class': lambda x: x and 'like' in x.lower()})
                    likes = likes_elem.get_text(strip=True) if likes_elem else "0"

                    # Downloads
                    downloads_elem = item.find('span', {'class': lambda x: x and 'download' in x.lower()})
                    downloads = downloads_elem.get_text(strip=True) if downloads_elem else "0"

                    models.append({
                        'title': title,
                        'likes': likes,
                        'downloads': downloads,
                        'link': link,
                        'platform': 'thingiverse'
                    })
                except Exception as e:
                    logger.warning(f"Error parsing Thingiverse item: {e}")
                    continue

            logger.info(f"Found {len(models)} models on Thingiverse")
            return models

        except Exception as e:
            logger.error(f"Thingiverse search error: {e}")
            return []

    def analyze_competition(self, keyword: str) -> Dict[str, Any]:
        """Rekabet analizi"""
        logger.info(f"Analyzing competition for: {keyword}")

        etsy_products = self.search_etsy(keyword, limit=10)
        thingiverse_models = self.search_thingiverse(keyword, limit=10)

        # Basit metrikler
        avg_price = "N/A"
        if etsy_products:
            prices = []
            for p in etsy_products:
                try:
                    # "$12.99" formatından fiyat çıkar
                    price_str = p['price'].replace('$', '').replace(',', '')
                    price = float(price_str.split()[0])
                    prices.append(price)
                except:
                    continue

            if prices:
                avg_price = f"${sum(prices) / len(prices):.2f}"

        competition_score = "Medium"
        if len(etsy_products) > 50:
            competition_score = "High"
        elif len(etsy_products) < 20:
            competition_score = "Low"

        return {
            'keyword': keyword,
            'etsy_results': len(etsy_products),
            'thingiverse_results': len(thingiverse_models),
            'average_price': avg_price,
            'competition_level': competition_score,
            'analysis_date': datetime.now().isoformat(),
            'sample_products': etsy_products[:5],
            'sample_models': thingiverse_models[:5]
        }

    def find_niche_opportunities(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Niş fırsat tespiti"""
        logger.info(f"Finding niche opportunities for {len(keywords)} keywords")

        opportunities = []

        for keyword in keywords:
            analysis = self.analyze_competition(keyword)

            # Scoring: Düşük rekabet + orta/yüksek fiyat = iyi fırsat
            score = 0

            if analysis['competition_level'] == 'Low':
                score += 40
            elif analysis['competition_level'] == 'Medium':
                score += 20

            # Fiyat faktörü
            if analysis['average_price'] != 'N/A':
                try:
                    price = float(analysis['average_price'].replace('$', ''))
                    if price > 20:
                        score += 30
                    elif price > 10:
                        score += 20
                    else:
                        score += 10
                except:
                    pass

            # Thingiverse varlığı (referans modeller)
            if analysis['thingiverse_results'] > 0:
                score += 20

            # Etsy varlığı (market demand)
            if analysis['etsy_results'] > 5:
                score += 10

            analysis['opportunity_score'] = score
            opportunities.append(analysis)

        # Score'a göre sırala
        opportunities.sort(key=lambda x: x['opportunity_score'], reverse=True)

        return opportunities

    def get_trending_keywords(self) -> List[str]:
        """3D baskı için trend keywords (statik liste + dinamik)"""

        # Base trending keywords
        base_keywords = [
            "plant pot",
            "phone holder",
            "desk organizer",
            "cookie cutter",
            "christmas ornament",
            "keychain",
            "vase",
            "phone stand",
            "pencil holder",
            "cable organizer",
            "succulent planter",
            "fidget toy",
            "bathroom organizer",
            "kitchen gadget",
            "home decor"
        ]

        logger.info(f"Returning {len(base_keywords)} trending keywords")
        return base_keywords

    def generate_market_report(self, niche: str) -> Dict[str, Any]:
        """Detaylı pazar raporu"""
        logger.info(f"Generating market report for: {niche}")

        analysis = self.analyze_competition(niche)

        # Recommendations
        recommendations = []

        if analysis['competition_level'] == 'Low':
            recommendations.append("✅ Düşük rekabet - Giriş için uygun")
        elif analysis['competition_level'] == 'High':
            recommendations.append("⚠️ Yüksek rekabet - Farklılaşma gerekli")

        if analysis['average_price'] != 'N/A':
            try:
                price = float(analysis['average_price'].replace('$', ''))
                if price > 15:
                    recommendations.append(f"💰 İyi fiyat aralığı (${price:.2f})")
                else:
                    recommendations.append(f"💵 Düşük fiyat aralığı (${price:.2f}) - Hacim gerekli")
            except:
                pass

        if analysis['thingiverse_results'] > 10:
            recommendations.append("📚 Çok sayıda referans model mevcut")

        report = {
            **analysis,
            'recommendations': recommendations,
            'next_steps': [
                "1. Referans modelleri incele (Thingiverse)",
                "2. Fiyat stratejisi belirle",
                "3. Farklılaşma noktaları bul",
                "4. İlk prototip oluştur"
            ]
        }

        return report


# Global engine instance
research_engine = MarketResearchEngine()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """MCP araçlarını listele"""
    return [
        Tool(
            name="search_products",
            description="Etsy veya Thingiverse'de ürün/model ara. Keyword bazlı arama yapar.",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Aranacak kelime/cümle (örn: 'plant pot', 'phone holder')"
                    },
                    "platform": {
                        "type": "string",
                        "enum": ["etsy", "thingiverse", "both"],
                        "description": "Arama yapılacak platform",
                        "default": "both"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maksimum sonuç sayısı",
                        "default": 20
                    }
                },
                "required": ["keyword"]
            }
        ),
        Tool(
            name="analyze_competition",
            description="Belirli bir keyword için rekabet analizi yap. Fiyat, popülerlik vs.",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Analiz edilecek keyword"
                    }
                },
                "required": ["keyword"]
            }
        ),
        Tool(
            name="find_niche_opportunities",
            description="Birden fazla keyword arasından en iyi niş fırsatları bul. Otomatik skorlama yapar.",
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Analiz edilecek keyword listesi"
                    }
                },
                "required": ["keywords"]
            }
        ),
        Tool(
            name="get_trending_keywords",
            description="3D baskı için trend olan keywords listesini al",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="generate_market_report",
            description="Belirli bir niş için detaylı pazar raporu oluştur (analiz + tavsiyeler)",
            inputSchema={
                "type": "object",
                "properties": {
                    "niche": {
                        "type": "string",
                        "description": "Rapor oluşturulacak niş/kategori"
                    }
                },
                "required": ["niche"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """MCP araç çağrıları"""

    try:
        if name == "search_products":
            keyword = arguments["keyword"]
            platform = arguments.get("platform", "both")
            limit = arguments.get("limit", 20)

            results = []

            if platform in ["etsy", "both"]:
                etsy_results = research_engine.search_etsy(keyword, limit)
                results.extend(etsy_results)

            if platform in ["thingiverse", "both"]:
                thingiverse_results = research_engine.search_thingiverse(keyword, limit)
                results.extend(thingiverse_results)

            output = {
                'keyword': keyword,
                'platform': platform,
                'total_results': len(results),
                'results': results
            }

            return [TextContent(
                type="text",
                text=json.dumps(output, indent=2, ensure_ascii=False)
            )]

        elif name == "analyze_competition":
            keyword = arguments["keyword"]
            analysis = research_engine.analyze_competition(keyword)

            return [TextContent(
                type="text",
                text=json.dumps(analysis, indent=2, ensure_ascii=False)
            )]

        elif name == "find_niche_opportunities":
            keywords = arguments["keywords"]
            opportunities = research_engine.find_niche_opportunities(keywords)

            output = {
                'analyzed_keywords': len(keywords),
                'opportunities': opportunities,
                'top_3': opportunities[:3]
            }

            return [TextContent(
                type="text",
                text=json.dumps(output, indent=2, ensure_ascii=False)
            )]

        elif name == "get_trending_keywords":
            keywords = research_engine.get_trending_keywords()

            output = {
                'total_keywords': len(keywords),
                'keywords': keywords,
                'note': 'Bu keywordleri find_niche_opportunities ile analiz edebilirsiniz'
            }

            return [TextContent(
                type="text",
                text=json.dumps(output, indent=2, ensure_ascii=False)
            )]

        elif name == "generate_market_report":
            niche = arguments["niche"]
            report = research_engine.generate_market_report(niche)

            return [TextContent(
                type="text",
                text=json.dumps(report, indent=2, ensure_ascii=False)
            )]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Tool execution error: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=f"ERROR: {str(e)}"
        )]


async def main():
    """MCP server'ı başlat"""
    logger.info("Starting Market Research MCP Server...")
    logger.info("Tools: search_products, analyze_competition, find_niche_opportunities, get_trending_keywords, generate_market_report")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
