"""
mcp_servers/drive_server.py
FastMCP server exposing Google Drive-like tools.

In production, this would integrate with the Google Drive API.
For the hackathon demo, it reads OKR data from the seeded SQLite database.

Run standalone: python -m mcp_servers.drive_server
"""

from mcp.server.fastmcp import FastMCP
from db.database import SessionLocal
from db.models import OKR

mcp = FastMCP("google-drive", instructions="Search and read documents from Google Drive for OKR tracking")


@mcp.tool()
def search_documents(query: str = "OKR") -> list[dict]:
    """Search for documents in Google Drive.

    Args:
        query: Search query string
    """
    # Demo: return OKR-related document metadata
    return [
        {
            "id": "doc_001",
            "title": "Q3 OKR Tracker — FY2025",
            "type": "spreadsheet",
            "last_modified": "2025-09-15T10:30:00",
            "owner": "founder@startup.in",
            "url": "https://docs.google.com/spreadsheets/d/demo_okr",
        },
        {
            "id": "doc_002",
            "title": "Q3 Strategy & Goals",
            "type": "document",
            "last_modified": "2025-08-01T14:00:00",
            "owner": "founder@startup.in",
            "url": "https://docs.google.com/document/d/demo_strategy",
        },
    ]


@mcp.tool()
def get_okr_document() -> str:
    """Fetch the current OKR document content with all key results and progress data."""
    db = SessionLocal()
    okrs = db.query(OKR).all()
    db.close()

    lines = ["Q3 OKR Document — FY2025", "=" * 40, ""]
    for okr in okrs:
        lines.append(
            f"Objective: {okr.objective}\n"
            f"  Key Result: {okr.key_result}\n"
            f"  Owner: {okr.owner} | Progress: {okr.progress_pct}% "
            f"({okr.current_value} / {okr.target_value} {okr.unit})\n"
            f"  Status: {okr.status.value} | Deadline: {okr.deadline.strftime('%d %b %Y')}\n"
        )
    return "\n".join(lines)


@mcp.tool()
def read_document(doc_id: str) -> dict:
    """Read a specific document by its ID.

    Args:
        doc_id: Document ID to read
    """
    if doc_id == "doc_001":
        return {
            "id": doc_id,
            "title": "Q3 OKR Tracker — FY2025",
            "content": get_okr_document(),
        }
    return {"error": f"Document '{doc_id}' not found"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
