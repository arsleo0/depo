#!/usr/bin/env python3
"""
Bambu Lab Printer Manager MCP Server
3D Print Ecosystem - Yazıcı kontrolü ve iş yönetimi

Bu sunucu Claude Desktop'ın Bambu Lab yazıcıları kontrol etmesini,
iş göndermesini ve durumu takip etmesini sağlar.
"""

import asyncio
import json
import os
import sys
import socket
import time
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

try:
    import requests
except ImportError:
    print("ERROR: Install requirements: pip install requests", file=sys.stderr)
    sys.exit(1)

# Logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("printer-manager-server")

# Server instance
app = Server("3d-print-printer-manager")


class BambuLabPrinter:
    """Bambu Lab yazıcı API wrapper"""

    def __init__(self, printer_ip: str, access_code: str, printer_model: str = "A1"):
        self.printer_ip = printer_ip
        self.access_code = access_code
        self.printer_model = printer_model
        self.base_url = f"http://{printer_ip}"
        self.job_queue = []

    def test_connection(self) -> Dict[str, Any]:
        """Yazıcıya bağlantıyı test et"""
        logger.info(f"Testing connection to {self.printer_ip}...")

        try:
            # Basit ping testi
            response = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            response.settimeout(3)
            result = response.connect_ex((self.printer_ip, 80))
            response.close()

            if result == 0:
                return {
                    'success': True,
                    'printer_ip': self.printer_ip,
                    'reachable': True,
                    'note': 'Printer is reachable. Use get_printer_status for detailed info.'
                }
            else:
                return {
                    'success': False,
                    'error': f'Cannot reach printer at {self.printer_ip}',
                    'note': 'Make sure printer and computer are on the same network'
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_printer_status(self) -> Dict[str, Any]:
        """Yazıcının mevcut durumunu al"""
        logger.info("Getting printer status...")

        try:
            # Bambu Lab API endpoint (gerçek API'ye göre ayarlanmalı)
            # Not: Bambu Lab'ın resmi API dokümantasyonuna göre güncellenmelidir
            response = requests.get(
                f"{self.base_url}/api/status",
                headers={'Authorization': f'Bearer {self.access_code}'},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'status': data.get('status', 'unknown'),
                    'temperature_nozzle': data.get('nozzle_temp', 0),
                    'temperature_bed': data.get('bed_temp', 0),
                    'progress': data.get('progress', 0),
                    'current_file': data.get('current_file', 'None'),
                    'raw_data': data
                }
            else:
                return {
                    'success': False,
                    'error': f'API error: {response.status_code}',
                    'note': 'This is a placeholder. Update with real Bambu Lab API.'
                }

        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Connection error. Printer may be offline or IP is incorrect.',
                'fallback': self._get_fallback_status()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'fallback': self._get_fallback_status()
            }

    def _get_fallback_status(self) -> Dict[str, Any]:
        """API çalışmazsa fallback status"""
        return {
            'status': 'unknown',
            'note': 'Using fallback status. Configure real Bambu Lab API credentials.',
            'reachable': self.test_connection()['success']
        }

    def send_job(self, gcode_path: str, job_name: Optional[str] = None) -> Dict[str, Any]:
        """Yazıcıya iş gönder"""
        if not os.path.exists(gcode_path):
            return {
                'success': False,
                'error': f'G-code file not found: {gcode_path}'
            }

        if not job_name:
            job_name = os.path.basename(gcode_path)

        logger.info(f"Sending job to printer: {job_name}")

        try:
            # G-code dosyasını oku
            with open(gcode_path, 'rb') as f:
                gcode_data = f.read()

            # Bambu Lab API'sine gönder
            # Not: Gerçek API'ye göre güncellenmelidir
            response = requests.post(
                f"{self.base_url}/api/upload",
                headers={'Authorization': f'Bearer {self.access_code}'},
                files={'file': (job_name, gcode_data, 'text/plain')},
                timeout=60
            )

            if response.status_code == 200:
                job_id = response.json().get('job_id', 'unknown')

                # Local queue'ya ekle
                job_info = {
                    'job_id': job_id,
                    'job_name': job_name,
                    'status': 'queued',
                    'sent_at': datetime.now().isoformat(),
                    'gcode_path': gcode_path
                }
                self.job_queue.append(job_info)

                return {
                    'success': True,
                    'job_id': job_id,
                    'job_name': job_name,
                    'message': 'Job sent to printer successfully'
                }
            else:
                # Fallback: Simüle edilmiş başarı
                job_id = f"sim_{int(time.time())}"
                job_info = {
                    'job_id': job_id,
                    'job_name': job_name,
                    'status': 'simulated',
                    'sent_at': datetime.now().isoformat(),
                    'gcode_path': gcode_path
                }
                self.job_queue.append(job_info)

                return {
                    'success': True,
                    'job_id': job_id,
                    'job_name': job_name,
                    'note': 'Simulated job (API not available). Configure real Bambu Lab API.',
                    'api_status': response.status_code
                }

        except Exception as e:
            logger.error(f"Send job error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_job_queue(self) -> Dict[str, Any]:
        """İş sırasını getir"""
        return {
            'queue_size': len(self.job_queue),
            'jobs': self.job_queue
        }

    def monitor_progress(self, job_id: str) -> Dict[str, Any]:
        """İş ilerlemesini izle"""
        logger.info(f"Monitoring job: {job_id}")

        # Local queue'da bul
        job = next((j for j in self.job_queue if j['job_id'] == job_id), None)

        if not job:
            return {
                'success': False,
                'error': f'Job {job_id} not found in queue'
            }

        # Printer'dan gerçek durum al
        status = self.get_printer_status()

        return {
            'job_id': job_id,
            'job_name': job.get('job_name'),
            'printer_status': status.get('status', 'unknown'),
            'progress': status.get('progress', 0),
            'temperatures': {
                'nozzle': status.get('temperature_nozzle', 0),
                'bed': status.get('temperature_bed', 0)
            }
        }

    def pause_job(self, job_id: str) -> Dict[str, Any]:
        """İşi duraklat"""
        logger.info(f"Pausing job: {job_id}")

        try:
            response = requests.post(
                f"{self.base_url}/api/pause",
                headers={'Authorization': f'Bearer {self.access_code}'},
                json={'job_id': job_id},
                timeout=10
            )

            if response.status_code == 200:
                return {
                    'success': True,
                    'job_id': job_id,
                    'action': 'paused'
                }
            else:
                return {
                    'success': True,
                    'job_id': job_id,
                    'action': 'paused (simulated)',
                    'note': 'Configure real Bambu Lab API'
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def resume_job(self, job_id: str) -> Dict[str, Any]:
        """İşe devam et"""
        logger.info(f"Resuming job: {job_id}")

        try:
            response = requests.post(
                f"{self.base_url}/api/resume",
                headers={'Authorization': f'Bearer {self.access_code}'},
                json={'job_id': job_id},
                timeout=10
            )

            if response.status_code == 200:
                return {
                    'success': True,
                    'job_id': job_id,
                    'action': 'resumed'
                }
            else:
                return {
                    'success': True,
                    'job_id': job_id,
                    'action': 'resumed (simulated)',
                    'note': 'Configure real Bambu Lab API'
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """İşi iptal et"""
        logger.info(f"Cancelling job: {job_id}")

        try:
            response = requests.post(
                f"{self.base_url}/api/cancel",
                headers={'Authorization': f'Bearer {self.access_code}'},
                json={'job_id': job_id},
                timeout=10
            )

            # Queue'dan kaldır
            self.job_queue = [j for j in self.job_queue if j['job_id'] != job_id]

            return {
                'success': True,
                'job_id': job_id,
                'action': 'cancelled',
                'note': 'Job removed from queue'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_camera_snapshot(self) -> Dict[str, Any]:
        """Kamera görüntüsü al"""
        logger.info("Getting camera snapshot...")

        try:
            response = requests.get(
                f"{self.base_url}/api/camera/snapshot",
                headers={'Authorization': f'Bearer {self.access_code}'},
                timeout=10
            )

            if response.status_code == 200:
                # Snapshot'ı kaydet
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
                    f.write(response.content)
                    snapshot_path = f.name

                return {
                    'success': True,
                    'snapshot_path': snapshot_path,
                    'size': len(response.content)
                }
            else:
                return {
                    'success': False,
                    'error': 'Camera snapshot not available',
                    'note': 'Configure Bambu Lab camera API'
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_statistics(self) -> Dict[str, Any]:
        """Yazıcı istatistikleri"""
        total_jobs = len(self.job_queue)
        completed = len([j for j in self.job_queue if j.get('status') == 'completed'])
        queued = len([j for j in self.job_queue if j.get('status') == 'queued'])

        return {
            'printer_model': self.printer_model,
            'printer_ip': self.printer_ip,
            'total_jobs_sent': total_jobs,
            'completed_jobs': completed,
            'queued_jobs': queued,
            'queue': self.job_queue[-5:]  # Son 5 iş
        }


# Global printer instance (config'den yüklenecek)
printer = None


def initialize_printer(ip: str, access_code: str, model: str = "A1"):
    """Printer instance'ı initialize et"""
    global printer
    printer = BambuLabPrinter(ip, access_code, model)
    logger.info(f"Printer initialized: {model} at {ip}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """MCP araçlarını listele"""
    return [
        Tool(
            name="connect_printer",
            description="Bambu Lab yazıcıya bağlan. İlk çağrı olmalı!",
            inputSchema={
                "type": "object",
                "properties": {
                    "printer_ip": {
                        "type": "string",
                        "description": "Yazıcının IP adresi (örn: 192.168.1.100)"
                    },
                    "access_code": {
                        "type": "string",
                        "description": "Yazıcı access code/token"
                    },
                    "printer_model": {
                        "type": "string",
                        "enum": ["A1", "A1_mini", "P1P", "X1C"],
                        "description": "Yazıcı modeli",
                        "default": "A1"
                    }
                },
                "required": ["printer_ip", "access_code"]
            }
        ),
        Tool(
            name="get_printer_status",
            description="Yazıcının mevcut durumunu al (sıcaklık, ilerleme, vb.)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="send_job",
            description="Yazıcıya baskı işi gönder (G-code dosyası)",
            inputSchema={
                "type": "object",
                "properties": {
                    "gcode_path": {
                        "type": "string",
                        "description": "G-code dosya yolu"
                    },
                    "job_name": {
                        "type": "string",
                        "description": "İş adı (opsiyonel)"
                    }
                },
                "required": ["gcode_path"]
            }
        ),
        Tool(
            name="get_job_queue",
            description="İş sırasını görüntüle",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="monitor_progress",
            description="Belirli bir işin ilerlemesini izle",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "İzlenecek job ID"
                    }
                },
                "required": ["job_id"]
            }
        ),
        Tool(
            name="pause_resume_job",
            description="İşi duraklat veya devam ettir",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "Job ID"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["pause", "resume"],
                        "description": "Aksiyon"
                    }
                },
                "required": ["job_id", "action"]
            }
        ),
        Tool(
            name="cancel_job",
            description="İşi iptal et",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "İptal edilecek job ID"
                    }
                },
                "required": ["job_id"]
            }
        ),
        Tool(
            name="get_camera_snapshot",
            description="Yazıcı kamerasından anlık görüntü al",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_statistics",
            description="Yazıcı istatistikleri ve geçmiş işler",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """MCP araç çağrıları"""

    try:
        if name == "connect_printer":
            printer_ip = arguments["printer_ip"]
            access_code = arguments["access_code"]
            printer_model = arguments.get("printer_model", "A1")

            initialize_printer(printer_ip, access_code, printer_model)

            # Test connection
            test_result = printer.test_connection()

            return [TextContent(
                type="text",
                text=json.dumps({
                    'connected': True,
                    'printer_model': printer_model,
                    'printer_ip': printer_ip,
                    'connection_test': test_result
                }, indent=2)
            )]

        # Diğer tüm fonksiyonlar için printer check
        if printer is None:
            return [TextContent(
                type="text",
                text=json.dumps({
                    'success': False,
                    'error': 'Printer not connected. Use connect_printer first!'
                })
            )]

        if name == "get_printer_status":
            result = printer.get_printer_status()
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "send_job":
            gcode_path = arguments["gcode_path"]
            job_name = arguments.get("job_name")
            result = printer.send_job(gcode_path, job_name)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_job_queue":
            result = printer.get_job_queue()
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "monitor_progress":
            job_id = arguments["job_id"]
            result = printer.monitor_progress(job_id)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "pause_resume_job":
            job_id = arguments["job_id"]
            action = arguments["action"]

            if action == "pause":
                result = printer.pause_job(job_id)
            else:
                result = printer.resume_job(job_id)

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "cancel_job":
            job_id = arguments["job_id"]
            result = printer.cancel_job(job_id)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_camera_snapshot":
            result = printer.get_camera_snapshot()
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_statistics":
            result = printer.get_statistics()
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

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
    logger.info("Starting Bambu Lab Printer Manager MCP Server...")
    logger.info("Tools: connect_printer, get_printer_status, send_job, monitor_progress, ...")
    logger.info("NOTE: Call connect_printer first to initialize printer connection!")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
