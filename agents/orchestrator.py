"""
agents/orchestrator.py
PRIMARY AGENT — coordinates all sub-agents.

This is the core of the multi-agent system as required by the problem statement:
"Implement a primary agent coordinating one or more sub-agents"

Workflow:
  1. Receive a query from the API
  2. Run Signal Watcher + OKR Tracker + Risk Spotter in parallel (asyncio)
  3. Pass all outputs to the Advisor agent for synthesis
  4. Save the brief to the DB
  5. Return the final structured response

The Orchestrator never calls Google tools directly — it delegates to sub-agents.
"""

import asyncio
import json
from datetime import datetime

from agents import signal_watcher, okr_tracker, risk_spotter, advisor
from db.database import SessionLocal
from db.models import Brief


async def run(query: str = "Give me the situation brief.") -> dict:
    """
    Main entry point. Coordinates all sub-agents and returns the situation brief.
    """
    started_at = datetime.now()

    # -------------------------------------------------------------------------
    # Step 1: Run data-gathering agents IN PARALLEL
    # -------------------------------------------------------------------------
    print(f"\n{'='*60}")
    print(f"[Command Center] Query: {query}")
    print(f"[Command Center] Dispatching intelligence agents...")
    print(f"{'='*60}")

    signal_task = asyncio.create_task(signal_watcher.run({}))
    okr_task = asyncio.create_task(okr_tracker.run({}))
    risk_task = asyncio.create_task(risk_spotter.run({}))

    signal_data, okr_data, risk_data = await asyncio.gather(
        signal_task, okr_task, risk_task
    )

    print(f"[Command Center] Agents complete. "
          f"Signals: {signal_data['high_risk_count']} high, "
          f"OKRs: {len(okr_data['off_track'])} off-track, "
          f"Risks: {risk_data['high_risk_count']} high")

    # -------------------------------------------------------------------------
    # Step 2: Pass all gathered data to the Advisor for synthesis
    # -------------------------------------------------------------------------
    print(f"[Command Center] Invoking Senior Synthesizer...")

    advisor_data = await advisor.run({
        "query": query,
        "signal_data": signal_data,
        "okr_data": okr_data,
        "risk_data": risk_data,
    })

    # -------------------------------------------------------------------------
    # Step 3: Determine overall health status
    # -------------------------------------------------------------------------
    health = _compute_health(signal_data, okr_data, risk_data)

    # -------------------------------------------------------------------------
    # Step 4: Persist brief to DB (structured storage requirement)
    # -------------------------------------------------------------------------
    db = SessionLocal()
    try:
        brief_record = Brief(
            query=query,
            brief_text=advisor_data["brief"],
            health=health,
            okr_snapshot=json.dumps([{
                "kr": o["key_result"][:80],
                "progress": o["progress_pct"],
                "status": o["status"],
            } for o in okr_data["okrs"]]),
            risk_count=len(risk_data["risks"]),
            signal_count=len(signal_data["signals"]),
        )
        db.add(brief_record)
        db.commit()
    finally:
        db.close()

    elapsed_ms = int((datetime.now() - started_at).total_seconds() * 1000)
    print(f"[Command Center] ✅ Intelligence brief synthesized in {elapsed_ms}ms | Health: {health}")
    print(f"{'='*60}\n")

    return {
        "brief": advisor_data["brief"],
        "health": health,
        "okr_snapshot": okr_data["okrs"],
        "risks": risk_data["risks"],
        "signals": signal_data["signals"],
        "calendar_events": risk_data.get("calendar_events", []),
        "calendar_conflicts": risk_data.get("calendar_conflicts", []),
        "metadata": {
            "query": query,
            "generated_at": started_at.isoformat(),
            "elapsed_ms": elapsed_ms,
            "tokens_used": advisor_data.get("output_tokens", 0),
            "agents_run": ["signal_watcher", "okr_tracker", "risk_spotter", "advisor"],
        }
    }


def _compute_health(signal_data: dict, okr_data: dict, risk_data: dict) -> str:
    """Simple health signal: RED / AMBER / GREEN"""
    if (risk_data["high_risk_count"] >= 2 or
            signal_data["high_risk_count"] >= 1 or
            len(okr_data["off_track"]) >= 2):
        return "RED"
    if (risk_data["high_risk_count"] >= 1 or
            len(okr_data["at_risk"]) >= 2):
        return "AMBER"
    return "GREEN"
