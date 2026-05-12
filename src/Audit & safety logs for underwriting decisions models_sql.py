from sqlalchemy import DateTime, JSON
from datetime import datetime

class UnderwritingAuditORM(Base):
    __tablename__ = "underwriting_audit"

    id = Column(String, primary_key=True)
    policy_id = Column(String, ForeignKey("policies.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    decision_status = Column(String, nullable=False)  # approved_auto, rejected, manual_review
    jurisdiction = Column(String, nullable=False)
    safety_snapshot = Column(JSON, nullable=False)  # safety certs, non-weaponization flags, kid-safe modes
    reason = Column(Text, nullable=True)

    policy = relationship("PolicyORM", back_populates="audit_logs")
