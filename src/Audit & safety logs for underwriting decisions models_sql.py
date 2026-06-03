from __future__ import annotations

from typing import Optional, Any, Literal, Dict, TYPE_CHECKING
import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, ForeignKey, DateTime, JSON  # type: ignore[import]
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column  # type: ignore[import]

# Avoid importing PolicyORM at type-check time to prevent import resolution issues in editors/linters.
# Relationship uses a forward string reference so a direct import isn't required here.
if TYPE_CHECKING:
    # Provide a lightweight stub for type-checkers to recognize PolicyORM without
    # performing a runtime import which can cause import-resolution issues.
    class PolicyORM:  # pragma: no cover - type checking only
        pass

class Base(DeclarativeBase):  # type: ignore[misc]
    pass

class UnderwritingAuditORM(Base):
    __tablename__ = "underwriting_audit"

    # specify a length for the primary key string to satisfy type checkers
    id: Mapped[str] = mapped_column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)  # type: ignore[assignment]
    policy_id: Mapped[str] = mapped_column(String(255), ForeignKey("policies.id"), nullable=False)  # type: ignore[assignment]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)  # type: ignore[assignment]
    decision_status: Mapped[Literal["approved_auto", "rejected", "manual_review"]] = mapped_column(String(255), nullable=False)  # type: ignore[assignment]  # approved_auto, rejected, manual_review
    jurisdiction: Mapped[str] = mapped_column(String(255), nullable=False)  # type: ignore[assignment]
    safety_snapshot: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)  # type: ignore[assignment]  # safety certs, non-weaponization flags, kid-safe modes
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # type: ignore[assignment]

    policy: Mapped[PolicyORM] = relationship("PolicyORM", back_populates="audit_logs")  # type: ignore[assignment]
