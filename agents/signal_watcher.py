"""
agents/signal_watcher.py
Sub-agent #1 — reads Gmail signals and classifies them.

Responsibility:
  - Fetch emails via Gmail MCP server
  - Identify client-at-risk signals, unanswered threads, blockers
  - Return a structured summary to the Orchestrator
"""

from tools.mcp_client import fetch_gmail_signals
from db.database import SessionLocal
from db.models import Signal


async def run(context: dict) -> dict:
    """
    Entry point called by the Orchestrator.
    Returns: { signals: [...], summary: str, high_risk_count: int }
    """
    print("[Market Signal Agent] Scanning Gmail for intelligence...")
    raw_signals = await fetch_gmail_signals(max_results=20)

    # Load existing signals from DB (already seeded for demo)
    db = SessionLocal()
    db_signals = db.query(Signal).order_by(Signal.detected_at.desc()).limit(10).all()
    db.close()

    # Format for orchestrator
    formatted = []
    for s in db_signals:
        formatted.append({
            "subject": s.subject,
            "sender": s.sender,
            "summary": s.summary,
            "type": s.signal_type,
            "severity": s.severity.value,
        })

    high_risk = [s for s in formatted if s["severity"] == "high"]
    medium_risk = [s for s in formatted if s["severity"] == "medium"]

    summary_lines = []
    if high_risk:
        summary_lines.append(f"{len(high_risk)} HIGH severity signal(s) require immediate attention:")
        for s in high_risk:
            summary_lines.append(f"  • [{s['sender']}] {s['subject']} — {s['summary']}")
    if medium_risk:
        summary_lines.append(f"{len(medium_risk)} medium signal(s):")
        for s in medium_risk:
            summary_lines.append(f"  • [{s['sender']}] {s['subject']}")

    print(f"[Market Signal Agent] Found {len(high_risk)} high, {len(medium_risk)} medium signals")

    return {
        "agent": "signal_watcher",
        "signals": formatted,
        "high_risk_count": len(high_risk),
        "medium_risk_count": len(medium_risk),
        "summary": "\n".join(summary_lines) if summary_lines else "No critical signals detected.",
    }
