"""
mcp_servers/gmail_server.py
FastMCP server exposing Gmail-like tools.

In production, this would integrate with the Gmail API.
For the hackathon demo, it reads from the seeded SQLite database.

Run standalone: python -m mcp_servers.gmail_server
"""

from mcp.server.fastmcp import FastMCP
from db.database import SessionLocal
from db.models import Signal

mcp = FastMCP("gmail-signals", instructions="Search and classify email signals for the Situation Room")


@mcp.tool()
def search_emails(query: str = "unread", max_results: int = 20) -> list[dict]:
    """Search emails matching a query. Returns subject, sender, snippet, and classification.

    Args:
        query: Search filter like 'unread', 'client', 'urgent'
        max_results: Maximum number of results to return
    """
    db = SessionLocal()
    signals = db.query(Signal).order_by(Signal.detected_at.desc()).limit(max_results).all()
    db.close()

    return [{
        "subject": s.subject,
        "sender": s.sender,
        "snippet": s.raw_snippet or "",
        "summary": s.summary,
        "signal_type": s.signal_type,
        "severity": s.severity.value,
        "detected_at": s.detected_at.isoformat() if s.detected_at else None,
    } for s in signals]


@mcp.tool()
def classify_signal(subject: str, snippet: str) -> dict:
    """Classify an email signal by severity and type.

    Args:
        subject: Email subject line
        snippet: Email body snippet
    """
    # Simple keyword-based classification for demo
    severity = "low"
    signal_type = "informational"

    risk_keywords = ["churn", "cancel", "unhappy", "complaint", "downtime", "outage", "risk"]
    blocker_keywords = ["blocker", "blocked", "waiting", "stalled", "stuck"]
    deadline_keywords = ["deadline", "due", "urgent", "asap", "overdue", "by friday", "by thursday"]

    combined = (subject + " " + snippet).lower()

    if any(kw in combined for kw in risk_keywords):
        severity = "high"
        signal_type = "client_at_risk"
    elif any(kw in combined for kw in blocker_keywords):
        severity = "medium"
        signal_type = "blocker"
    elif any(kw in combined for kw in deadline_keywords):
        severity = "medium"
        signal_type = "deadline"

    return {"signal_type": signal_type, "severity": severity}


@mcp.tool()
def get_email_thread(subject: str) -> dict:
    """Get full email thread by subject.

    Args:
        subject: Subject line to search for
    """
    db = SessionLocal()
    signal = db.query(Signal).filter(Signal.subject.contains(subject)).first()
    db.close()

    if signal:
        return {
            "subject": signal.subject,
            "sender": signal.sender,
            "summary": signal.summary,
            "full_snippet": signal.raw_snippet,
            "severity": signal.severity.value,
        }
    return {"error": f"No thread found matching '{subject}'"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
