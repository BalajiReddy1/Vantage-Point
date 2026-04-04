"""
db/models.py
Structured data store — covers the "Store and retrieve structured data from a database"
requirement from the problem statement.

Tables:
  - okrs          : OKR definitions with target and current values
  - signals       : Parsed Gmail signals (client risks, blockers)
  - risks         : Active risks detected by the Risk Spotter agent
  - briefs        : Historical situation briefs (audit trail)
  - alerts        : Proactive alerts triggered by health changes
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum
from sqlalchemy.orm import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class OKRStatus(str, enum.Enum):
    on_track = "on_track"
    at_risk = "at_risk"
    off_track = "off_track"


class RiskSeverity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class OKR(Base):
    __tablename__ = "okrs"

    id = Column(Integer, primary_key=True)
    objective = Column(String(300), nullable=False)
    key_result = Column(String(300), nullable=False)
    owner = Column(String(100))
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, default=0.0)
    unit = Column(String(50))                   # e.g. "customers", "revenue_inr", "%"
    deadline = Column(DateTime, nullable=False)
    status = Column(Enum(OKRStatus), default=OKRStatus.on_track)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def progress_pct(self) -> float:
        if self.target_value == 0:
            return 0.0
        return round((self.current_value / self.target_value) * 100, 1)

    def __repr__(self):
        return f"<OKR {self.key_result[:40]} — {self.progress_pct}%>"


class Signal(Base):
    """A parsed signal from Gmail — client risk, unanswered thread, blocker mention."""
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True)
    source = Column(String(50), default="gmail")    # gmail | calendar | drive
    subject = Column(String(300))
    sender = Column(String(200))
    summary = Column(Text)
    signal_type = Column(String(100))               # e.g. "client_at_risk", "blocker", "unanswered"
    severity = Column(Enum(RiskSeverity), default=RiskSeverity.medium)
    detected_at = Column(DateTime, default=datetime.utcnow)
    raw_snippet = Column(Text)


class Risk(Base):
    """An active risk item surfaced by the Risk Spotter agent."""
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    severity = Column(Enum(RiskSeverity), default=RiskSeverity.medium)
    source_agent = Column(String(100))              # which agent raised this
    related_okr_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Integer, default=0)           # 0 = open, 1 = resolved


class Brief(Base):
    """A saved situation brief — every generated brief is stored for history."""
    __tablename__ = "briefs"

    id = Column(Integer, primary_key=True)
    query = Column(Text)                            # what the founder asked
    brief_text = Column(Text)                       # full narrative output
    health = Column(String(10), default="GREEN")    # RED / AMBER / GREEN
    okr_snapshot = Column(Text)                     # JSON snapshot of OKR scores
    risk_count = Column(Integer, default=0)
    signal_count = Column(Integer, default=0)
    generated_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    """Proactive alert triggered when health status changes."""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    alert_type = Column(String(50))                 # health_change, deadline_approaching, etc.
    title = Column(String(300))
    message = Column(Text)
    severity = Column(Enum(RiskSeverity), default=RiskSeverity.medium)
    previous_health = Column(String(10), nullable=True)
    current_health = Column(String(10), nullable=True)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    acknowledged = Column(Integer, default=0)       # 0 = unread, 1 = acknowledged
