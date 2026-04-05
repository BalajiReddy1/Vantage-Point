"""
main.py
FastAPI application — the API-based deployment layer.

Satisfies: "Deploy as an API-based system"

Endpoints:
  GET  /health         — liveness check
  POST /brief          — generate a full situation brief (main workflow)
  POST /ask            — ask a specific question (flexible query)
  GET  /history        — fetch past briefs from DB
  GET  /okrs           — current OKR scores
  GET  /risks          — active risks
  GET  /signals        — Gmail signals
  GET  /alerts         — proactive alerts
  POST /alerts/{id}/ack — acknowledge an alert
  GET  /dashboard-data — all data in one call for the React dashboard
"""

import os
import asyncio
from datetime import datetime
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.database import init_db, get_db
from db.models import Brief, OKR, Risk, Signal, Alert
from agents.orchestrator import run as orchestrator_run
from agents.scheduler import check_health_change


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    print("[Startup] Database initialized.")

    # Optional: start proactive monitoring
    # scheduler_task = asyncio.create_task(proactive_loop(120))

    yield

    # Shutdown
    # scheduler_task.cancel()
    print("[Shutdown] Server stopped.")


app = FastAPI(
    title="Vantage Point API",
    description="AI Intelligence Platform for Decision Makers — Multi-Agent System powered by Google Gemini",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class AskRequest(BaseModel):
    query: str = "How are we doing?"

class BriefResponse(BaseModel):
    brief: str
    health: str
    generated_at: str
    elapsed_ms: int
    agents_run: list[str]
    risk_count: int
    signal_count: int


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "vantage-point", "time": datetime.now().isoformat()}


@app.post("/api/brief", response_model=BriefResponse, summary="Generate a full Situation Brief")
async def generate_brief():
    """Main endpoint — triggers the full multi-agent workflow."""
    result = await orchestrator_run(query="Give me the full situation brief.")

    # Check for health changes after generating
    await check_health_change()

    return BriefResponse(
        brief=result["brief"],
        health=result["health"],
        generated_at=result["metadata"]["generated_at"],
        elapsed_ms=result["metadata"]["elapsed_ms"],
        agents_run=result["metadata"]["agents_run"],
        risk_count=len(result["risks"]),
        signal_count=len(result["signals"]),
    )


@app.post("/api/ask", summary="Ask the Situation Room a specific question")
async def ask(request: AskRequest):
    """Flexible query endpoint — the Orchestrator runs the full pipeline."""
    result = await orchestrator_run(query=request.query)
    await check_health_change()
    return {
        "query": request.query,
        "brief": result["brief"],
        "health": result["health"],
        "risks": result["risks"],
        "signals": result["signals"],
        "okr_snapshot": result["okr_snapshot"],
        "calendar_events": result.get("calendar_events", []),
        "metadata": result["metadata"],
    }


@app.get("/api/history", summary="Fetch past situation briefs")
def get_history(limit: int = 10, db: Session = Depends(get_db)):
    briefs = db.query(Brief).order_by(Brief.generated_at.desc()).limit(limit).all()
    return [{
        "id": b.id,
        "query": b.query,
        "health": b.health,
        "brief_text": b.brief_text,
        "risk_count": b.risk_count,
        "signal_count": b.signal_count,
        "generated_at": b.generated_at.isoformat(),
    } for b in briefs]


@app.get("/api/okrs", summary="Current OKR scores")
def get_okrs(db: Session = Depends(get_db)):
    okrs = db.query(OKR).all()
    return [{
        "id": o.id,
        "objective": o.objective,
        "key_result": o.key_result,
        "owner": o.owner,
        "progress_pct": o.progress_pct,
        "current": o.current_value,
        "target": o.target_value,
        "unit": o.unit,
        "status": o.status.value,
        "deadline": o.deadline.strftime("%d %b %Y"),
        "days_left": (o.deadline - datetime.now()).days,
    } for o in okrs]


@app.get("/api/risks", summary="Active risks")
def get_risks(db: Session = Depends(get_db)):
    risks = db.query(Risk).filter(Risk.resolved == 0).all()
    return [{
        "id": r.id,
        "title": r.title,
        "description": r.description,
        "severity": r.severity.value,
        "source_agent": r.source_agent,
        "created_at": r.created_at.isoformat() if r.created_at else None,
    } for r in risks]


@app.get("/api/signals", summary="Gmail signals")
def get_signals(db: Session = Depends(get_db)):
    signals = db.query(Signal).order_by(Signal.detected_at.desc()).all()
    return [{
        "id": s.id,
        "subject": s.subject,
        "sender": s.sender,
        "summary": s.summary,
        "signal_type": s.signal_type,
        "severity": s.severity.value,
        "source": s.source,
        "detected_at": s.detected_at.isoformat() if s.detected_at else None,
    } for s in signals]


@app.get("/api/alerts", summary="Proactive alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(Alert.triggered_at.desc()).limit(20).all()
    return [{
        "id": a.id,
        "type": a.alert_type,
        "title": a.title,
        "message": a.message,
        "severity": a.severity.value,
        "previous_health": a.previous_health,
        "current_health": a.current_health,
        "triggered_at": a.triggered_at.isoformat() if a.triggered_at else None,
        "acknowledged": bool(a.acknowledged),
    } for a in alerts]


@app.post("/api/alerts/{alert_id}/ack", summary="Acknowledge an alert")
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.acknowledged = 1
    db.commit()
    return {"status": "acknowledged", "alert_id": alert_id}


@app.get("/api/dashboard-data", summary="All dashboard data in one call")
def dashboard_data(db: Session = Depends(get_db)):
    """Aggregated endpoint for the React dashboard — reduces API calls."""
    okrs = db.query(OKR).all()
    risks = db.query(Risk).filter(Risk.resolved == 0).all()
    signals = db.query(Signal).order_by(Signal.detected_at.desc()).all()
    alerts = db.query(Alert).filter(Alert.acknowledged == 0).order_by(Alert.triggered_at.desc()).limit(5).all()
    latest_brief = db.query(Brief).order_by(Brief.generated_at.desc()).first()

    return {
        "okrs": [{
            "id": o.id,
            "objective": o.objective,
            "key_result": o.key_result,
            "owner": o.owner,
            "progress_pct": o.progress_pct,
            "current": o.current_value,
            "target": o.target_value,
            "unit": o.unit,
            "status": o.status.value,
            "deadline": o.deadline.strftime("%d %b %Y"),
            "days_left": (o.deadline - datetime.now()).days,
        } for o in okrs],
        "risks": [{
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "severity": r.severity.value,
            "source_agent": r.source_agent,
        } for r in risks],
        "signals": [{
            "id": s.id,
            "subject": s.subject,
            "sender": s.sender,
            "summary": s.summary,
            "signal_type": s.signal_type,
            "severity": s.severity.value,
            "source": s.source,
        } for s in signals],
        "alerts": [{
            "id": a.id,
            "title": a.title,
            "message": a.message,
            "severity": a.severity.value,
            "type": a.alert_type,
        } for a in alerts],
        "latest_brief": {
            "brief_text": latest_brief.brief_text if latest_brief else None,
            "health": latest_brief.health if latest_brief else "GREEN",
            "generated_at": latest_brief.generated_at.isoformat() if latest_brief else None,
            "risk_count": latest_brief.risk_count if latest_brief else 0,
            "signal_count": latest_brief.signal_count if latest_brief else 0,
        },
    }


# ---------------------------------------------------------------------------
# Serve React frontend (production build)
# ---------------------------------------------------------------------------

# Mount static files from React build if available
frontend_build_path = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.exists(frontend_build_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_build_path, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve React SPA — all non-API routes go to index.html"""
        file_path = os.path.join(frontend_build_path, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_build_path, "index.html"))
