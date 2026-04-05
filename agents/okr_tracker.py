"""
agents/okr_tracker.py
Sub-agent #2 — scores OKR progress and detects drift.

Responsibility:
  - Pull OKR data from DB (sourced from Google Drive MCP)
  - Calculate % progress for each key result
  - Flag OKRs as on_track / at_risk / off_track
  - Return structured scores to the Orchestrator
"""

from datetime import datetime
from db.database import SessionLocal
from db.models import OKR, OKRStatus
from tools.mcp_client import fetch_okr_document


async def run(context: dict) -> dict:
    """
    Entry point called by the Orchestrator.
    Returns: { okrs: [...], off_track: [...], at_risk: [...], summary: str }
    """
    print("[Performance Auditor] Scoring key results...")

    # Also fetch from Drive MCP to demonstrate MCP integration
    _doc = await fetch_okr_document()

    db = SessionLocal()
    okrs = db.query(OKR).all()

    scored = []
    for okr in okrs:
        days_left = (okr.deadline - datetime.now()).days
        progress = okr.progress_pct

        # Recompute status dynamically
        if progress >= 90:
            status = OKRStatus.on_track
        elif progress >= 60:
            status = OKRStatus.at_risk
        else:
            status = OKRStatus.off_track

        # Update DB status
        okr.status = status
        db.add(okr)

        scored.append({
            "key_result": okr.key_result,
            "owner": okr.owner,
            "progress_pct": progress,
            "current": okr.current_value,
            "target": okr.target_value,
            "unit": okr.unit,
            "days_left": days_left,
            "status": status.value,
            "deadline": okr.deadline.strftime("%d %b %Y"),
        })

    db.commit()
    db.close()

    off_track = [o for o in scored if o["status"] == "off_track"]
    at_risk = [o for o in scored if o["status"] == "at_risk"]
    on_track = [o for o in scored if o["status"] == "on_track"]

    summary_lines = [f"OKR Scorecard — {len(scored)} key results tracked:"]
    for okr in scored:
        bar = _progress_bar(okr["progress_pct"])
        summary_lines.append(
            f"  {bar} {okr['progress_pct']}% — {okr['key_result'][:60]} "
            f"[{okr['status'].upper()}] ({okr['days_left']}d left)"
        )

    print(f"[Performance Auditor] {len(on_track)} on-track, {len(at_risk)} at-risk, {len(off_track)} off-track")

    return {
        "agent": "okr_tracker",
        "okrs": scored,
        "off_track": off_track,
        "at_risk": at_risk,
        "on_track": on_track,
        "summary": "\n".join(summary_lines),
    }


def _progress_bar(pct: float, width: int = 10) -> str:
    filled = int((pct / 100) * width)
    return "[" + "█" * filled + "░" * (width - filled) + "]"
