"""
tools/mcp_client.py
Wrappers that call the MCP servers (Gmail, Calendar, Drive).

Each function directly calls the MCP server tool functions.
In production, these would use the MCP client protocol over stdio/HTTP transport.
For the demo, we call the server functions directly for reliability.

This satisfies: "Integrate multiple tools via MCP (e.g., calendar, task manager, notes)"
"""

import asyncio
from typing import Optional


# ---------------------------------------------------------------------------
# Gmail MCP wrapper
# ---------------------------------------------------------------------------

async def fetch_gmail_signals(max_results: int = 20) -> list[dict]:
    """
    Fetches email signals via the Gmail MCP server.
    """
    from mcp_servers.gmail_server import search_emails
    return search_emails(max_results=max_results)


# ---------------------------------------------------------------------------
# Google Calendar MCP wrapper
# ---------------------------------------------------------------------------

async def fetch_upcoming_events(days_ahead: int = 30) -> list[dict]:
    """
    Fetches upcoming calendar events via the Calendar MCP server.
    """
    from mcp_servers.calendar_server import get_upcoming_events
    return get_upcoming_events(days_ahead=days_ahead)


async def fetch_calendar_conflicts() -> list[dict]:
    """
    Checks for scheduling conflicts via the Calendar MCP server.
    """
    from mcp_servers.calendar_server import check_conflicts
    return check_conflicts()


async def fetch_approaching_deadlines(threshold_days: int = 7) -> list[dict]:
    """
    Fetches deadlines approaching within the threshold.
    """
    from mcp_servers.calendar_server import get_deadline_proximity
    return get_deadline_proximity(threshold_days=threshold_days)


# ---------------------------------------------------------------------------
# Google Drive MCP wrapper
# ---------------------------------------------------------------------------

async def fetch_okr_document() -> Optional[str]:
    """
    Fetches the OKR document content via the Drive MCP server.
    """
    from mcp_servers.drive_server import get_okr_document
    return get_okr_document()


async def search_drive_documents(query: str = "OKR") -> list[dict]:
    """
    Searches for documents via the Drive MCP server.
    """
    from mcp_servers.drive_server import search_documents
    return search_documents(query=query)
