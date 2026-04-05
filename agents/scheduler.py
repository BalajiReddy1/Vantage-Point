"""
agents/scheduler.py
Proactive alerting system — the "Chief of Staff" differentiator.

Runs on a background loop, detects health degradation, and creates alerts.
This makes the system proactive rather than reactive.
"""

import asyncio
from datetime import datetime
from db.database import SessionLocal
from db.models import Alert, Brief, RiskSeverity


async def check_health_change():
    """
    Compare the latest brief's health with the previous one.
    If health degraded, create a proactive alert.
    """
    db = SessionLocal()
    try:
        briefs = db.query(Brief).order_by(Brief.generated_at.desc()).limit(2).all()

        if len(briefs) < 2:
            return None

        current = briefs[0]
        previous = briefs[1]

        health_order = {"GREEN": 0, "AMBER": 1, "RED": 2}
        current_level = health_order.get(current.health, 0)
        previous_level = health_order.get(previous.health, 0)

        if current_level > previous_level:
            # Health degraded
            alert = Alert(
                alert_type="health_degradation",
                title=f"Health status changed: {previous.health} → {current.health}",
                message=(
                    f"Your business health has degraded from {previous.health} to {current.health}. "
                    f"Current risks: {current.risk_count}, Active signals: {current.signal_count}. "
                    f"Review the latest situation brief for details."
                ),
                severity=RiskSeverity.high if current.health == "RED" else RiskSeverity.medium,
                previous_health=previous.health,
                current_health=current.health,
            )
            db.add(alert)
            db.commit()
            print(f"[Scheduler] ⚠️ ALERT: Health degraded {previous.health} → {current.health}")
            return {
                "type": "health_degradation",
                "previous": previous.health,
                "current": current.health,
            }
        elif current_level < previous_level:
            # Health improved
            alert = Alert(
                alert_type="health_improvement",
                title=f"Health improved: {previous.health} → {current.health}",
                message=f"Your business health has improved from {previous.health} to {current.health}.",
                severity=RiskSeverity.low,
                previous_health=previous.health,
                current_health=current.health,
            )
            db.add(alert)
            db.commit()
            print(f"[Scheduler] ✅ Health improved {previous.health} → {current.health}")

        return None
    finally:
        db.close()


async def proactive_loop(interval_minutes: int = 120):
    """
    Background loop that periodically generates briefs and checks for health changes.
    """
    from agents.orchestrator import run as orchestrator_run

    print(f"[Scheduler] Proactive monitoring started (every {interval_minutes} min)")

    while True:
        try:
            await asyncio.sleep(interval_minutes * 60)
            print(f"\n[Scheduler] Running proactive health check at {datetime.now().isoformat()}")

            # Generate a fresh brief
            await orchestrator_run(query="[Proactive Check] Automated health assessment")

            # Check for health changes
            await check_health_change()

        except asyncio.CancelledError:
            print("[Scheduler] Proactive monitoring stopped.")
            break
        except Exception as e:
            print(f"[Scheduler] Error in proactive check: {e}")
            await asyncio.sleep(60)  # Wait a minute before retrying
