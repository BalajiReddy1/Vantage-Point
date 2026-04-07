"""
data/seed.py
Seeds the database with realistic dummy data for the demo.
Run once before demoing: python -m data.seed

This simulates:
  - Q3 OKRs for a B2B SaaS startup
  - Gmail signals (client at risk, unanswered threads, blocker)
  - Active risks logged by agents
"""

import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from db.database import SessionLocal, init_db
from db.models import OKR, Signal, Risk, OKRStatus, RiskSeverity


def seed():
    init_db()
    db = SessionLocal()

    # Clear existing data
    for model in [OKR, Signal, Risk]:
        db.query(model).delete()

    # --- OKRs ---
    okrs = [
        OKR(
            objective="Grow recurring revenue to hit Series A metrics",
            key_result="Reach ₹50L MRR by end of Q3",
            owner="Founder",
            target_value=5000000,
            current_value=3100000,
            unit="INR",
            deadline=datetime.now() + timedelta(days=28),
            status=OKRStatus.at_risk,
        ),
        OKR(
            objective="Grow recurring revenue to hit Series A metrics",
            key_result="Close 20 new paid customers in Q3",
            owner="Sales",
            target_value=20,
            current_value=11,
            unit="customers",
            deadline=datetime.now() + timedelta(days=28),
            status=OKRStatus.at_risk,
        ),
        OKR(
            objective="Build a world-class product",
            key_result="Ship v2.0 with 3 flagship features",
            owner="Engineering",
            target_value=3,
            current_value=2,
            unit="features",
            deadline=datetime.now() + timedelta(days=14),
            status=OKRStatus.on_track,
        ),
        OKR(
            objective="Build a world-class product",
            key_result="Achieve NPS score of 45+",
            owner="Product",
            target_value=45,
            current_value=38,
            unit="NPS",
            deadline=datetime.now() + timedelta(days=28),
            status=OKRStatus.at_risk,
        ),
        OKR(
            objective="Reduce churn below 2%",
            key_result="Monthly churn rate under 2%",
            owner="Customer Success",
            target_value=2,
            current_value=3.4,
            unit="%",
            deadline=datetime.now() + timedelta(days=28),
            status=OKRStatus.off_track,
        ),
    ]
    db.add_all(okrs)

    # --- Gmail Signals ---
    signals = [
        Signal(
            source="gmail",
            subject="Re: Renewal discussion — not happy with recent downtime",
            sender="priya.mehta@acmecorp.in",
            summary="Acme Corp's VP of Ops flagged 3 downtime incidents. Renewal is in 18 days. High churn risk.",
            signal_type="client_at_risk",
            severity=RiskSeverity.high,
            raw_snippet="We've had 3 outages this month alone. I need assurance before we sign renewal...",
        ),
        Signal(
            source="gmail",
            subject="Integration API — still waiting on docs",
            sender="dev@startupxyz.io",
            summary="StartupXYZ dev team has been waiting 9 days for API integration docs. Onboarding stalled.",
            signal_type="unanswered",
            severity=RiskSeverity.medium,
            raw_snippet="Hey, we pinged last week too. Without the docs we can't go live...",
        ),
        Signal(
            source="gmail",
            subject="Investor update request — Q3 numbers",
            sender="rajan@vcfirm.com",
            summary="Lead investor requesting Q3 metrics update before board meeting next Friday.",
            signal_type="deadline",
            severity=RiskSeverity.medium,
            raw_snippet="Can you share the MRR, churn, and NPS numbers by Thursday?",
        ),
        Signal(
            source="gmail",
            subject="Team offsite — conflicting with sprint demo",
            sender="ananya@team.internal",
            summary="Team offsite is booked same day as customer sprint demo. Scheduling conflict.",
            signal_type="blocker",
            severity=RiskSeverity.low,
            raw_snippet="Just realized the offsite clashes with the TechWave demo on the 18th...",
        ),
    ]
    db.add_all(signals)

    # --- Risks ---
    risks = [
        Risk(
            title="Acme Corp renewal at risk",
            description="Key account (₹4.2L ARR) flagged 3 downtime incidents. Renewal in 18 days with no resolution sent.",
            severity=RiskSeverity.high,
            source_agent="signal_watcher",
            related_okr_id=2,
        ),
        Risk(
            title="MRR 38% short of Q3 target with 28 days left",
            description="Current MRR ₹31L vs target ₹50L. Requires ₹19L more — implies ~9 new enterprise deals in 28 days.",
            severity=RiskSeverity.high,
            source_agent="okr_tracker",
            related_okr_id=1,
        ),
        Risk(
            title="Churn rate above target (3.4% vs 2% goal)",
            description="Churn has worsened 2 months in a row. No CS intervention plan filed yet.",
            severity=RiskSeverity.medium,
            source_agent="risk_spotter",
            related_okr_id=5,
        ),
        Risk(
            title="v2.0 launch window tight — 14 days, 1 feature remaining",
            description="Feature 3 (Advanced Analytics) not yet in staging. QA cycle needs at least 5 days.",
            severity=RiskSeverity.medium,
            source_agent="risk_spotter",
            related_okr_id=3,
        ),
    ]
    db.add_all(risks)

    db.commit()
    db.close()
    print("✅ Seeded: 5 OKRs, 4 signals, 4 risks")


if __name__ == "__main__":
    seed()
