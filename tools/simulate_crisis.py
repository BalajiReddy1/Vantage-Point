"""
tools/simulate_crisis.py
Live demo tool — injects a realistic crisis event into the database.

Usage (run from project root with venv activated):
  python -m tools.simulate_crisis                          # random crisis
  python -m tools.simulate_crisis --scenario client_loss   # specific scenario
  python -m tools.simulate_crisis --scenario funding_pull
  python -m tools.simulate_crisis --scenario key_hire_quit
  python -m tools.simulate_crisis --scenario data_breach
  python -m tools.simulate_crisis --scenario competitor
  python -m tools.simulate_crisis --reset                  # remove injected items

The injected data is tagged with source_agent='demo_inject' so it can be
cleanly removed with --reset without touching the base seed data.
"""

import sys
import os
import argparse
import random
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import SessionLocal, init_db
from db.models import Signal, Risk, RiskSeverity

# ---------------------------------------------------------------------------
# Crisis Scenarios — each one injects a Signal + a Risk
# ---------------------------------------------------------------------------

SCENARIOS = {
    "client_loss": {
        "signal": {
            "source": "gmail",
            "subject": "URGENT: Contract termination notice — QuantumLeap Technologies",
            "sender": "legal@quantumleap.io",
            "summary": "QuantumLeap (₹8.5L ARR) has sent a formal termination notice citing repeated SLA violations. 30-day exit clause activated.",
            "signal_type": "client_at_risk",
            "severity": RiskSeverity.high,
            "raw_snippet": "Please find attached our formal notice of contract termination per Section 12.3. We have identified alternative vendors.",
        },
        "risk": {
            "title": "QuantumLeap Technologies contract termination — ₹8.5L ARR at risk",
            "description": "Largest enterprise client has issued formal termination notice. Loss would drop MRR by 17% and jeopardize Series A metrics. Requires immediate executive escalation.",
            "severity": RiskSeverity.high,
        },
    },
    "funding_pull": {
        "signal": {
            "source": "gmail",
            "subject": "Re: Series A — need to discuss timeline adjustments",
            "sender": "deepak.sharma@peakventures.in",
            "summary": "Lead investor is signaling cold feet on Series A timeline. Requested emergency call to 'reassess market conditions' before term sheet.",
            "signal_type": "investor_risk",
            "severity": RiskSeverity.high,
            "raw_snippet": "Given recent market shifts, we'd like to revisit the timeline before finalizing terms. Can we talk tomorrow morning?",
        },
        "risk": {
            "title": "Series A timeline at risk — lead investor requesting reassessment",
            "description": "Peak Ventures (lead investor) wants to pause the term sheet process. If delayed past Q3, runway drops below 4 months with no bridge option on the table.",
            "severity": RiskSeverity.high,
        },
    },
    "key_hire_quit": {
        "signal": {
            "source": "gmail",
            "subject": "Resignation — effective 2 weeks from today",
            "sender": "arjun.k@team.internal",
            "summary": "Head of Engineering has submitted resignation. Cited burnout and competing offer. Owns all v2.0 architecture decisions.",
            "signal_type": "blocker",
            "severity": RiskSeverity.high,
            "raw_snippet": "This wasn't easy, but I've decided to move on. Happy to help transition over the next two weeks.",
        },
        "risk": {
            "title": "Head of Engineering resignation — v2.0 launch at risk",
            "description": "Arjun owns the v2.0 architecture and is the only person with full context on Feature 3 (Advanced Analytics). 14-day notice period overlaps with launch window.",
            "severity": RiskSeverity.high,
        },
    },
    "data_breach": {
        "signal": {
            "source": "gmail",
            "subject": "SECURITY ALERT: Unusual API access pattern detected",
            "sender": "alerts@infrasec.internal",
            "summary": "Monitoring flagged 12,000 unauthorized API calls from an unknown IP in the last 6 hours. Customer PII endpoints were accessed.",
            "signal_type": "security_alert",
            "severity": RiskSeverity.high,
            "raw_snippet": "Automated alert: IP 203.45.xx.xx made 12,847 requests to /api/customers endpoint between 02:00-08:00 UTC.",
        },
        "risk": {
            "title": "Potential data breach — unauthorized API access to customer PII",
            "description": "Security monitoring detected bulk unauthorized access to customer data endpoints. If confirmed, triggers mandatory breach notification under DPDP Act within 72 hours.",
            "severity": RiskSeverity.high,
        },
    },
    "competitor": {
        "signal": {
            "source": "gmail",
            "subject": "FYI: just saw this — competitor launched same feature",
            "sender": "marketing@team.internal",
            "summary": "Direct competitor (NovaBuild) launched their version of Advanced Analytics today with a free tier. 3 prospects have already asked about it.",
            "signal_type": "competitive_intel",
            "severity": RiskSeverity.high,
            "raw_snippet": "NovaBuild just posted on LinkedIn — they shipped analytics with a freemium model. Two of our pipeline deals pinged me asking to compare.",
        },
        "risk": {
            "title": "Competitive threat — NovaBuild launched equivalent feature with free tier",
            "description": "Direct competitor shipped Advanced Analytics (our v2.0 flagship feature) before us, with aggressive freemium pricing. 3 active pipeline deals are now at risk of churning to competitor.",
            "severity": RiskSeverity.high,
        },
    },
}


DEMO_TAG = "demo_inject"


def inject(scenario_name: str):
    """Inject a crisis scenario into the live database."""
    if scenario_name not in SCENARIOS:
        print(f"Unknown scenario: {scenario_name}")
        print(f"Available: {', '.join(SCENARIOS.keys())}")
        return

    sc = SCENARIOS[scenario_name]
    init_db()
    db = SessionLocal()

    signal = Signal(
        **sc["signal"],
        detected_at=datetime.utcnow(),
    )
    # Tag it so we can clean up later
    signal.source = f"gmail|{DEMO_TAG}"

    risk = Risk(
        **sc["risk"],
        source_agent=DEMO_TAG,
        created_at=datetime.utcnow(),
    )

    db.add(signal)
    db.add(risk)
    db.commit()

    print(f"\n{'='*60}")
    print(f"  💥 CRISIS INJECTED: {scenario_name}")
    print(f"{'='*60}")
    print(f"  Signal: {sc['signal']['subject']}")
    print(f"  Risk:   {sc['risk']['title']}")
    print(f"{'='*60}")
    print(f"\n  → Now hit 'Synthesize Intelligence' in the UI.")
    print(f"  → The AI will detect this new signal in real-time.\n")

    db.close()


def reset():
    """Remove all demo-injected items."""
    init_db()
    db = SessionLocal()

    deleted_signals = db.query(Signal).filter(
        Signal.source.contains(DEMO_TAG)
    ).delete(synchronize_session=False)

    deleted_risks = db.query(Risk).filter(
        Risk.source_agent == DEMO_TAG
    ).delete(synchronize_session=False)

    db.commit()
    db.close()

    print(f"\n  🧹 Cleaned up: {deleted_signals} signal(s), {deleted_risks} risk(s) removed.")
    print(f"  Database is back to baseline seed data.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inject a live crisis for demo purposes")
    parser.add_argument("--scenario", type=str, default=None,
                        help="Scenario to inject: client_loss, funding_pull, key_hire_quit, data_breach, competitor")
    parser.add_argument("--reset", action="store_true",
                        help="Remove all previously injected demo data")
    args = parser.parse_args()

    if args.reset:
        reset()
    elif args.scenario:
        inject(args.scenario)
    else:
        # Pick a random scenario for surprise factor
        choice = random.choice(list(SCENARIOS.keys()))
        inject(choice)
