from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pydantic import BaseModel
import os

from app.core.config import get_settings
from app.modules.swarm import SwarmManager
from app.modules.attack import AttackManager
from app.modules.intel import IntelManager
from app.modules.kill import KillManager


# Request/Response models
class GeneratePersonaRequest(BaseModel):
    archetype: Optional[str] = None


class SpawnSwarmRequest(BaseModel):
    count: int = 100


class InitiateCallRequest(BaseModel):
    target_number: str
    persona_id: str


class DialListRequest(BaseModel):
    phone_numbers: List[str]


class AnalyzeTranscriptRequest(BaseModel):
    call_session_id: str


class SubmitReportRequest(BaseModel):
    intelligence_id: str
    report_type: str = "both"


# Initialize FastAPI app
app = FastAPI(
    title="ScamSinkhole ASI",
    description="Offensive ASI defense system against scammers",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
settings = get_settings()
swarm_manager = SwarmManager()
attack_manager = AttackManager()
intel_manager = IntelManager()
kill_manager = KillManager()


# WebSocket connections for live updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


# Serve UI
@app.get("/")
async def serve_ui():
    """Serve the war room UI."""
    ui_path = os.path.join(os.path.dirname(__file__), "..", "ui", "index.html")
    return FileResponse(ui_path)


@app.get("/api")
async def root():
    return {
        "service": "ScamSinkhole ASI",
        "status": "operational",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Swarm endpoints
@app.post("/api/swarm/generate-persona")
async def generate_persona(request: GeneratePersonaRequest):
    """Generate a single persona."""
    persona = await swarm_manager.generate_persona(request.archetype)
    await manager.broadcast({
        "type": "persona_created",
        "persona_id": persona.id,
        "name": persona.name
    })
    return persona


@app.post("/api/swarm/spawn")
async def spawn_swarm(request: SpawnSwarmRequest):
    """Spawn multiple personas."""
    personas = await swarm_manager.spawn_swarm(request.count)
    await manager.broadcast({
        "type": "swarm_spawned",
        "count": len(personas)
    })
    return {"personas": personas, "count": len(personas)}


@app.get("/api/swarm/personas")
async def get_personas():
    """Get all personas."""
    personas = swarm_manager.get_all_personas()
    return {"personas": personas, "count": len(personas)}


@app.get("/api/swarm/personas/{persona_id}")
async def get_persona(persona_id: str):
    """Get a specific persona."""
    persona = swarm_manager.get_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return persona


# Attack endpoints
@app.post("/api/attack/initiate-call")
async def initiate_call(request: InitiateCallRequest):
    """Initiate a call to a scammer."""
    persona = swarm_manager.get_persona(request.persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    session = await attack_manager.initiate_call(request.target_number, persona)
    await manager.broadcast({
        "type": "call_initiated",
        "session_id": session.id,
        "target": request.target_number
    })
    return session


@app.post("/api/attack/dial-list")
async def dial_list(request: DialListRequest):
    """Dial multiple scam numbers."""
    personas = swarm_manager.get_all_personas()
    if not personas:
        raise HTTPException(status_code=400, detail="No personas available. Generate personas first.")
    
    sessions = await attack_manager.dial_scam_list(request.phone_numbers, personas)
    await manager.broadcast({
        "type": "batch_calls_initiated",
        "count": len(sessions)
    })
    return {"sessions": sessions, "count": len(sessions)}


@app.get("/api/attack/sessions")
async def get_sessions():
    """Get all call sessions."""
    sessions = attack_manager.get_all_sessions()
    return {"sessions": sessions, "count": len(sessions)}


@app.get("/api/attack/sessions/active")
async def get_active_sessions():
    """Get active call sessions."""
    sessions = attack_manager.get_active_sessions()
    return {"sessions": sessions, "count": len(sessions)}


@app.get("/api/attack/sessions/{session_id}")
async def get_session(session_id: str):
    """Get a specific call session."""
    session = attack_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.post("/api/attack/sessions/{session_id}/end")
async def end_call(session_id: str):
    """End a call session."""
    success = await attack_manager.end_call(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    await manager.broadcast({
        "type": "call_ended",
        "session_id": session_id
    })
    return {"status": "ended", "session_id": session_id}


# Intel endpoints
@app.post("/api/intel/analyze")
async def analyze_transcript(request: AnalyzeTranscriptRequest):
    """Analyze a call transcript for intelligence."""
    session = attack_manager.get_session(request.call_session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    intelligence = await intel_manager.analyze_transcript(session)
    await manager.broadcast({
        "type": "intelligence_extracted",
        "intelligence_id": intelligence.id,
        "confidence": intelligence.confidence_score
    })
    return intelligence


@app.get("/api/intel/intelligence")
async def get_all_intelligence():
    """Get all intelligence data."""
    intelligence = intel_manager.get_all_intelligence()
    return {"intelligence": intelligence, "count": len(intelligence)}


@app.get("/api/intel/intelligence/high-value")
async def get_high_value_intelligence(min_confidence: float = 0.7):
    """Get high-confidence intelligence."""
    intelligence = intel_manager.get_high_value_intelligence(min_confidence)
    return {"intelligence": intelligence, "count": len(intelligence)}


@app.get("/api/intel/intelligence/{intelligence_id}")
async def get_intelligence(intelligence_id: str):
    """Get specific intelligence data."""
    intelligence = intel_manager.get_intelligence(intelligence_id)
    if not intelligence:
        raise HTTPException(status_code=404, detail="Intelligence not found")
    return intelligence


# Kill endpoints
@app.post("/api/kill/report")
async def submit_report(request: SubmitReportRequest):
    """Submit intelligence report to carriers/authorities."""
    intelligence = intel_manager.get_intelligence(request.intelligence_id)
    if not intelligence:
        raise HTTPException(status_code=404, detail="Intelligence not found")
    
    report = await kill_manager.auto_report(intelligence)
    await manager.broadcast({
        "type": "report_submitted",
        "report_id": report.id,
        "status": report.status
    })
    return report


@app.get("/api/kill/reports")
async def get_reports():
    """Get all reports."""
    reports = kill_manager.get_all_reports()
    return {"reports": reports, "count": len(reports)}


@app.get("/api/kill/reports/{report_id}")
async def get_report(report_id: str):
    """Get a specific report."""
    report = kill_manager.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


# WebSocket endpoint for live updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle any incoming messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Statistics endpoint
@app.get("/api/stats")
async def get_statistics():
    """Get overall statistics."""
    personas = swarm_manager.get_all_personas()
    sessions = attack_manager.get_all_sessions()
    active_sessions = attack_manager.get_active_sessions()
    intelligence = intel_manager.get_all_intelligence()
    reports = kill_manager.get_all_reports()
    
    completed_sessions = [s for s in sessions if s.status == "completed"]
    total_duration = sum(s.duration_seconds or 0 for s in completed_sessions)
    
    return {
        "personas_count": len(personas),
        "total_calls": len(sessions),
        "active_calls": len(active_sessions),
        "completed_calls": len(completed_sessions),
        "total_call_duration_seconds": total_duration,
        "intelligence_extracted": len(intelligence),
        "reports_submitted": len(reports),
        "confirmed_reports": len([r for r in reports if r.status == "confirmed"])
    }
