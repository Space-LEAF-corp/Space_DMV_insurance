from sqlalchemy import Column, String, Text, ForeignKey, DateTime, JSON  # type: ignore[import]
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped  # type: ignore[import]
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class UnderwritingAuditORM(Base):
    __tablename__ = "underwriting_audit"

    id: Mapped[str] = Column(String, primary_key=True)
    policy_id: Mapped[str] = Column(String, ForeignKey("policies.id"), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    decision_status = Column(String, nullable=False)  # approved_auto, rejected, manual_review
    jurisdiction = Column(String, nullable=False)
    safety_snapshot = Column(JSON, nullable=False)  # safety certs, non-weaponization flags, kid-safe modes
    reason = Column(Text, nullable=True)

    policy = relationship("PolicyORM", back_populates="audit_logs")
