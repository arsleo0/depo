#!/usr/bin/env python3
"""
Workflow Orchestrator MCP Server
3D Print Ecosystem - Ana koordinatör

Bu sunucu tüm 3D baskı workflow'unu yönetir ve
diğer MCP sunucuları koordine eder.
"""

import asyncio
import json
import os
import sys
import sqlite3
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path
import logging

# MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("ERROR: MCP SDK not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("workflow-orchestrator")

# Server instance
app = Server("3d-print-workflow-orchestrator")


class ProjectDatabase:
    """SQLite database for project management"""

    def __init__(self, db_path: str = "projects.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Database tabloları oluştur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                niche TEXT,
                status TEXT,
                created_at TEXT,
                updated_at TEXT,
                market_research TEXT,
                model_path TEXT,
                gcode_path TEXT,
                job_id TEXT,
                notes TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflow_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                step TEXT,
                status TEXT,
                details TEXT,
                timestamp TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        ''')

        conn.commit()
        conn.close()

    def create_project(self, name: str, niche: str) -> int:
        """Yeni proje oluştur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now().isoformat()

        cursor.execute('''
            INSERT INTO projects (name, niche, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, niche, 'created', now, now))

        project_id = cursor.lastrowid
        conn.commit()
        conn.close()

        logger.info(f"Project created: {name} (ID: {project_id})")
        return project_id

    def update_project(self, project_id: int, **kwargs):
        """Proje bilgilerini güncelle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Güncellenebilir alanlar
        allowed_fields = ['name', 'niche', 'status', 'market_research',
                         'model_path', 'gcode_path', 'job_id', 'notes']

        updates = []
        values = []

        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(f"{key} = ?")
                values.append(json.dumps(value) if isinstance(value, (dict, list)) else value)

        if updates:
            values.append(datetime.now().isoformat())
            values.append(project_id)

            query = f"UPDATE projects SET {', '.join(updates)}, updated_at = ? WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()

        conn.close()

    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Proje bilgilerini al"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        row = cursor.fetchone()

        conn.close()

        if row:
            columns = ['id', 'name', 'niche', 'status', 'created_at', 'updated_at',
                      'market_research', 'model_path', 'gcode_path', 'job_id', 'notes']
            project = dict(zip(columns, row))

            # JSON fields parse et
            if project['market_research']:
                try:
                    project['market_research'] = json.loads(project['market_research'])
                except:
                    pass

            return project

        return None

    def list_projects(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Projeleri listele"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM projects ORDER BY updated_at DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()

        conn.close()

        columns = ['id', 'name', 'niche', 'status', 'created_at', 'updated_at',
                  'market_research', 'model_path', 'gcode_path', 'job_id', 'notes']

        projects = []
        for row in rows:
            project = dict(zip(columns, row))
            projects.append(project)

        return projects

    def log_workflow_step(self, project_id: int, step: str, status: str, details: Any = None):
        """Workflow adımını logla"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO workflow_logs (project_id, step, status, details, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (project_id, step, status, json.dumps(details) if details else None,
              datetime.now().isoformat()))

        conn.commit()
        conn.close()

    def get_workflow_logs(self, project_id: int) -> List[Dict[str, Any]]:
        """Proje workflow loglarını al"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM workflow_logs WHERE project_id = ? ORDER BY timestamp ASC
        ''', (project_id,))

        rows = cursor.fetchall()
        conn.close()

        columns = ['id', 'project_id', 'step', 'status', 'details', 'timestamp']

        logs = []
        for row in rows:
            log = dict(zip(columns, row))
            if log['details']:
                try:
                    log['details'] = json.loads(log['details'])
                except:
                    pass
            logs.append(log)

        return logs


class WorkflowOrchestrator:
    """Ana workflow orchestrator"""

    def __init__(self, db: ProjectDatabase, output_dir: str = "output"):
        self.db = db
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def start_full_workflow(self, niche: str, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Tam otomatik workflow başlat (pazar araştırması → model → slice → print)"""

        if not project_name:
            project_name = f"{niche}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        logger.info(f"Starting full workflow for niche: {niche}")

        # Proje oluştur
        project_id = self.db.create_project(project_name, niche)

        # Workflow planı
        workflow_plan = {
            'project_id': project_id,
            'project_name': project_name,
            'niche': niche,
            'steps': [
                '1. Market Research (analyze_competition)',
                '2. Generate 3D Model (create_parametric_model or generate_model_with_ai)',
                '3. Optimize Model (optimize_for_printing)',
                '4. Slice Model (slice_model)',
                '5. Send to Printer (send_job)',
                '6. Monitor Progress (monitor_progress)'
            ],
            'status': 'planned',
            'note': 'Bu workflow Claude tarafından adım adım yürütülecek. Her adım için ilgili MCP sunucu araçlarını kullanın.'
        }

        self.db.log_workflow_step(project_id, 'workflow_start', 'success', workflow_plan)

        return workflow_plan

    def market_research_step(self, project_id: int) -> Dict[str, Any]:
        """Pazar araştırması adımı - talimatlar"""

        project = self.db.get_project(project_id)
        if not project:
            return {'success': False, 'error': 'Project not found'}

        instructions = {
            'project_id': project_id,
            'niche': project['niche'],
            'step': 'market_research',
            'action_required': 'Şu MCP araçlarını kullanın:',
            'mcp_tools': [
                {
                    'tool': 'analyze_competition',
                    'server': 'market-research',
                    'parameters': {
                        'keyword': project['niche']
                    }
                }
            ],
            'next_step': 'Sonuçları project\'e kaydedin: save_research_results'
        }

        self.db.log_workflow_step(project_id, 'market_research', 'in_progress', instructions)

        return instructions

    def save_research_results(self, project_id: int, results: Dict[str, Any]) -> Dict[str, Any]:
        """Pazar araştırması sonuçlarını kaydet"""

        self.db.update_project(project_id, market_research=results, status='research_completed')
        self.db.log_workflow_step(project_id, 'market_research', 'completed', results)

        return {
            'success': True,
            'project_id': project_id,
            'research_saved': True,
            'next_step': 'model_generation'
        }

    def model_generation_step(self, project_id: int, model_type: str = 'parametric') -> Dict[str, Any]:
        """3D model oluşturma adımı - talimatlar"""

        project = self.db.get_project(project_id)
        if not project:
            return {'success': False, 'error': 'Project not found'}

        # Model output path
        model_filename = f"{project['name']}_model.stl"
        model_path = os.path.join(self.output_dir, model_filename)

        instructions = {
            'project_id': project_id,
            'step': 'model_generation',
            'model_type': model_type,
            'action_required': 'Şu MCP araçlarını kullanın:',
            'mcp_tools': []
        }

        if model_type == 'parametric':
            instructions['mcp_tools'].append({
                'tool': 'create_parametric_model',
                'server': 'model-generator',
                'parameters': {
                    'model_type': 'plant_pot',  # Örnek
                    'parameters': {'diameter': 10, 'height': 10},
                    'output_path': model_path
                }
            })
        else:  # AI generation
            instructions['mcp_tools'].append({
                'tool': 'generate_model_with_ai',
                'server': 'model-generator',
                'parameters': {
                    'prompt': f"3D printable {project['niche']}",
                    'output_path': model_path
                }
            })

        instructions['output_path'] = model_path
        instructions['next_step'] = 'save_model_path ile kaydedin'

        self.db.log_workflow_step(project_id, 'model_generation', 'in_progress', instructions)

        return instructions

    def save_model_path(self, project_id: int, model_path: str) -> Dict[str, Any]:
        """Model path'i kaydet"""

        self.db.update_project(project_id, model_path=model_path, status='model_generated')
        self.db.log_workflow_step(project_id, 'model_generation', 'completed', {'model_path': model_path})

        return {
            'success': True,
            'project_id': project_id,
            'model_path': model_path,
            'next_step': 'slicing'
        }

    def slicing_step(self, project_id: int) -> Dict[str, Any]:
        """Slicing adımı - talimatlar"""

        project = self.db.get_project(project_id)
        if not project or not project['model_path']:
            return {'success': False, 'error': 'Model not found'}

        # G-code output path
        gcode_filename = f"{project['name']}_gcode.gcode"
        gcode_path = os.path.join(self.output_dir, gcode_filename)

        instructions = {
            'project_id': project_id,
            'step': 'slicing',
            'action_required': 'Şu MCP araçlarını kullanın:',
            'mcp_tools': [
                {
                    'tool': 'slice_model',
                    'server': 'slicer',
                    'parameters': {
                        'input_path': project['model_path'],
                        'output_path': gcode_path,
                        'printer': 'A1',
                        'material': 'PLA',
                        'quality': 'standard'
                    }
                }
            ],
            'output_path': gcode_path,
            'next_step': 'save_gcode_path ile kaydedin'
        }

        self.db.log_workflow_step(project_id, 'slicing', 'in_progress', instructions)

        return instructions

    def save_gcode_path(self, project_id: int, gcode_path: str) -> Dict[str, Any]:
        """G-code path'i kaydet"""

        self.db.update_project(project_id, gcode_path=gcode_path, status='sliced')
        self.db.log_workflow_step(project_id, 'slicing', 'completed', {'gcode_path': gcode_path})

        return {
            'success': True,
            'project_id': project_id,
            'gcode_path': gcode_path,
            'next_step': 'printing'
        }

    def printing_step(self, project_id: int) -> Dict[str, Any]:
        """Printing adımı - talimatlar"""

        project = self.db.get_project(project_id)
        if not project or not project['gcode_path']:
            return {'success': False, 'error': 'G-code not found'}

        instructions = {
            'project_id': project_id,
            'step': 'printing',
            'action_required': 'Şu MCP araçlarını kullanın:',
            'mcp_tools': [
                {
                    'tool': 'send_job',
                    'server': 'printer-manager',
                    'parameters': {
                        'gcode_path': project['gcode_path'],
                        'job_name': project['name']
                    }
                }
            ],
            'next_step': 'save_job_id ile kaydedin'
        }

        self.db.log_workflow_step(project_id, 'printing', 'in_progress', instructions)

        return instructions

    def save_job_id(self, project_id: int, job_id: str) -> Dict[str, Any]:
        """Job ID'yi kaydet"""

        self.db.update_project(project_id, job_id=job_id, status='printing')
        self.db.log_workflow_step(project_id, 'printing', 'started', {'job_id': job_id})

        return {
            'success': True,
            'project_id': project_id,
            'job_id': job_id,
            'status': 'Baskı başladı! monitor_progress ile takip edebilirsiniz.'
        }

    def get_project_summary(self, project_id: int) -> Dict[str, Any]:
        """Proje özeti ve durum raporu"""

        project = self.db.get_project(project_id)
        if not project:
            return {'success': False, 'error': 'Project not found'}

        logs = self.db.get_workflow_logs(project_id)

        summary = {
            'project': project,
            'workflow_logs': logs,
            'completed_steps': [log['step'] for log in logs if log['status'] == 'completed'],
            'current_status': project['status']
        }

        return summary


# Global instances
db = ProjectDatabase()
orchestrator = WorkflowOrchestrator(db)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """MCP araçlarını listele"""
    return [
        Tool(
            name="start_full_workflow",
            description="Tam otomatik 3D baskı workflow'unu başlat (pazar araştırması → model → slice → print)",
            inputSchema={
                "type": "object",
                "properties": {
                    "niche": {
                        "type": "string",
                        "description": "Ürün nişi/kategorisi (örn: 'plant pot', 'phone holder')"
                    },
                    "project_name": {
                        "type": "string",
                        "description": "Proje adı (opsiyonel, otomatik oluşturulur)"
                    }
                },
                "required": ["niche"]
            }
        ),
        Tool(
            name="market_research_step",
            description="Pazar araştırması adımı için talimatlar al",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "Proje ID"
                    }
                },
                "required": ["project_id"]
            }
        ),
        Tool(
            name="save_research_results",
            description="Pazar araştırması sonuçlarını kaydet",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer"},
                    "results": {"type": "object"}
                },
                "required": ["project_id", "results"]
            }
        ),
        Tool(
            name="model_generation_step",
            description="3D model oluşturma adımı için talimatlar",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer"},
                    "model_type": {
                        "type": "string",
                        "enum": ["parametric", "ai"],
                        "default": "parametric"
                    }
                },
                "required": ["project_id"]
            }
        ),
        Tool(
            name="save_model_path",
            description="Model dosya yolunu kaydet",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer"},
                    "model_path": {"type": "string"}
                },
                "required": ["project_id", "model_path"]
            }
        ),
        Tool(
            name="slicing_step",
            description="Slicing adımı için talimatlar",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer"}
                },
                "required": ["project_id"]
            }
        ),
        Tool(
            name="save_gcode_path",
            description="G-code dosya yolunu kaydet",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer"},
                    "gcode_path": {"type": "string"}
                },
                "required": ["project_id", "gcode_path"]
            }
        ),
        Tool(
            name="printing_step",
            description="Printing adımı için talimatlar",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer"}
                },
                "required": ["project_id"]
            }
        ),
        Tool(
            name="save_job_id",
            description="Printer job ID'yi kaydet",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer"},
                    "job_id": {"type": "string"}
                },
                "required": ["project_id", "job_id"]
            }
        ),
        Tool(
            name="get_project_summary",
            description="Proje özeti ve durum raporu",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "integer"}
                },
                "required": ["project_id"]
            }
        ),
        Tool(
            name="list_projects",
            description="Tüm projeleri listele",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "default": 20
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """MCP araç çağrıları"""

    try:
        if name == "start_full_workflow":
            niche = arguments["niche"]
            project_name = arguments.get("project_name")
            result = orchestrator.start_full_workflow(niche, project_name)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "market_research_step":
            project_id = arguments["project_id"]
            result = orchestrator.market_research_step(project_id)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "save_research_results":
            project_id = arguments["project_id"]
            results = arguments["results"]
            result = orchestrator.save_research_results(project_id, results)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "model_generation_step":
            project_id = arguments["project_id"]
            model_type = arguments.get("model_type", "parametric")
            result = orchestrator.model_generation_step(project_id, model_type)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "save_model_path":
            project_id = arguments["project_id"]
            model_path = arguments["model_path"]
            result = orchestrator.save_model_path(project_id, model_path)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "slicing_step":
            project_id = arguments["project_id"]
            result = orchestrator.slicing_step(project_id)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "save_gcode_path":
            project_id = arguments["project_id"]
            gcode_path = arguments["gcode_path"]
            result = orchestrator.save_gcode_path(project_id, gcode_path)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "printing_step":
            project_id = arguments["project_id"]
            result = orchestrator.printing_step(project_id)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "save_job_id":
            project_id = arguments["project_id"]
            job_id = arguments["job_id"]
            result = orchestrator.save_job_id(project_id, job_id)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_project_summary":
            project_id = arguments["project_id"]
            result = orchestrator.get_project_summary(project_id)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "list_projects":
            limit = arguments.get("limit", 20)
            projects = db.list_projects(limit)
            return [TextContent(type="text", text=json.dumps({
                'total': len(projects),
                'projects': projects
            }, indent=2))]

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
    logger.info("Starting Workflow Orchestrator MCP Server...")
    logger.info("Database: " + db.db_path)
    logger.info("Tools: start_full_workflow, market_research_step, model_generation_step, ...")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
