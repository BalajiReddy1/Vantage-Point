"""
agents/risk_spotter.py
Sub-agent #3 — cross-references Calendar, OKRs, and signals to detect risks.

Responsibility:
  - Fetch upcoming calendar events via Calendar MCP
  - Cross-reference deadlines with OKR progress
  - Identify scheduling conflicts
  - Pull active risks from DB
  - Return a prioritized risk list to the Orchestrator
"""

from datetime import datetime, timedelta
from db.database import SessionLocal
from db.models import Risk, RiskSeverity
from tools.mcp_client import fetch_upcoming_events, fetch_calendar_conflicts


async def run(context: dict) -> dict:
    """
    Entry point called by the Orchestrator.
    Returns: { risks: [...], calendar_conflicts: [...], summary: str }
    """
    print("[Asset Guardian] Scanning for risk flags and calendar conflicts...")

    events = await fetch_upcoming_events(days_ahead=30)
    conflicts = await fetch_calendar_conflicts()

    # Load active risks from DB
    db = SessionLocal()
    db_risks = db.query(Risk).filter(Risk.resolved == 0).order_by(Risk.severity).all()
    db.close()

    formatted_risks = []
    for r in db_risks:
        formatted_risks.append({
            "title": r.title,
            "description": r.description,
            "severity": r.severity.value,
            "source": r.source_agent,
            "created_at": r.created_at.strftime("%d %b") if r.created_at else "—",
        })

    # Add calendar-derived risks from MCP conflicts
    for conflict in conflicts:
        event_titles = [e["title"] for e in conflict.get("events", [])]
        if len(event_titles) >= 2:
            formatted_risks.append({
                "title": f"Scheduling conflict: {event_titles[0]} vs {event_titles[1]}",
                "description": f"Both events on {conflict['date']}. {conflict.get('recommendation', '')}",
                "severity": "medium",
                "source": "risk_spotter_calendar",
            })

    high = [r for r in formatted_risks if r["severity"] == "high"]
    medium = [r for r in formatted_risks if r["severity"] == "medium"]

    summary_lines = [f"{len(formatted_risks)} active risk(s) detected:"]
    for r in sorted(formatted_risks, key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["severity"]]):
        icon = "🔴" if r["severity"] == "high" else "🟡" if r["severity"] == "medium" else "🟢"
        summary_lines.append(f"  {icon} [{r['severity'].upper()}] {r['title']}")

    print(f"[Asset Guardian] {len(high)} high, {len(medium)} medium risks")

    return {
        "agent": "risk_spotter",
        "risks": formatted_risks,
        "calendar_events": events,
        "calendar_conflicts": conflicts,
        "high_risk_count": len(high),
        "medium_risk_count": len(medium),
        "summary": "\n".join(summary_lines),
    }
