"""
mcp_servers/calendar_server.py
FastMCP server exposing Google Calendar-like tools.

In production, this would integrate with the Google Calendar API.
For the hackathon demo, it returns realistic dummy calendar data.

Run standalone: python -m mcp_servers.calendar_server
"""

from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("google-calendar", instructions="Manage calendar events and detect scheduling conflicts")


def _get_demo_events() -> list[dict]:
    """Generate realistic demo calendar events."""
    now = datetime.now()
    return [
        {
            "id": "evt_001",
            "title": "Board meeting — Q3 review",
            "start_time": (now + timedelta(days=5)).isoformat(),
            "end_time": (now + timedelta(days=5, hours=2)).isoformat(),
            "attendees": ["rajan@vcfirm.com", "founder@startup.in"],
            "note": "Investor expects MRR, churn, NPS numbers",
            "priority": "high",
        },
        {
            "id": "evt_002",
            "title": "Acme Corp renewal call",
            "start_time": (now + timedelta(days=18)).isoformat(),
            "end_time": (now + timedelta(days=18, hours=1)).isoformat(),
            "attendees": ["priya.mehta@acmecorp.in"],
            "note": "High churn risk account — prepare incident response",
            "priority": "high",
        },
        {
            "id": "evt_003",
            "title": "v2.0 sprint demo — TechWave",
            "start_time": (now + timedelta(days=12)).isoformat(),
            "end_time": (now + timedelta(days=12, hours=1)).isoformat(),
            "attendees": ["demo@techwave.io"],
            "note": "Feature 3 must be in staging before this",
            "priority": "medium",
        },
        {
            "id": "evt_004",
            "title": "Team offsite",
            "start_time": (now + timedelta(days=12)).isoformat(),
            "end_time": (now + timedelta(days=12, hours=8)).isoformat(),
            "attendees": ["ananya@team.internal"],
            "note": "Conflicts with TechWave demo — scheduling risk",
            "priority": "low",
        },
        {
            "id": "evt_005",
            "title": "Investor update prep session",
            "start_time": (now + timedelta(days=3)).isoformat(),
            "end_time": (now + timedelta(days=3, hours=1)).isoformat(),
            "attendees": ["founder@startup.in", "cfo@startup.in"],
            "note": "Prepare slides for board meeting",
            "priority": "medium",
        },
    ]


@mcp.tool()
def get_upcoming_events(days_ahead: int = 30) -> list[dict]:
    """Fetch upcoming calendar events for the next N days.

    Args:
        days_ahead: Number of days to look ahead
    """
    events = _get_demo_events()
    cutoff = datetime.now() + timedelta(days=days_ahead)
    return [e for e in events if datetime.fromisoformat(e["start_time"]) <= cutoff]


@mcp.tool()
def check_conflicts(date: str = "") -> list[dict]:
    """Check for scheduling conflicts on a given date or across all dates.

    Args:
        date: Optional ISO date string (YYYY-MM-DD). If empty, checks all dates.
    """
    from collections import defaultdict

    events = _get_demo_events()
    by_day = defaultdict(list)
    for e in events:
        day = e["start_time"][:10]
        by_day[day].append(e)

    conflicts = []
    for day, day_events in by_day.items():
        if date and day != date:
            continue
        if len(day_events) >= 2:
            conflicts.append({
                "date": day,
                "events": [{"title": e["title"], "time": e["start_time"]} for e in day_events],
                "recommendation": "Consider rescheduling one of these events.",
            })
    return conflicts


@mcp.tool()
def get_deadline_proximity(threshold_days: int = 7) -> list[dict]:
    """Find events happening within the next N days that need preparation.

    Args:
        threshold_days: Number of days threshold for "approaching" deadlines
    """
    events = _get_demo_events()
    now = datetime.now()
    approaching = []
    for e in events:
        start = datetime.fromisoformat(e["start_time"])
        days_until = (start - now).days
        if 0 <= days_until <= threshold_days:
            approaching.append({
                "title": e["title"],
                "days_until": days_until,
                "priority": e.get("priority", "medium"),
                "note": e.get("note", ""),
            })
    return sorted(approaching, key=lambda x: x["days_until"])


if __name__ == "__main__":
    mcp.run(transport="stdio")
