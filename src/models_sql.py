from __future__ import annotations
from datetime import date
from typing import List
from sqlalchemy import String, Boolean, Date, Float, ForeignKey, Text  # type: ignore[import]
from sqlalchemy.orm import DeclarativeMeta, Mapped, mapped_column, relationship  # type: ignore[import]
from .db import Base as _Base  # type: ignore[import]

Base: DeclarativeMeta = _Base  # type: ignore[assignment]

class CustomerORM(Base):
    __tablename__ = "customers"
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)  # type: ignore[reportUnknownVariableType]
    full_name: Mapped[str] = mapped_column(String, nullable=False)  # type: ignore[reportUnknownVariableType]
    email: Mapped[str] = mapped_column(String, nullable=False, index=True)  # type: ignore[reportUnknownVariableType]
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)  # type: ignore[reportUnknownVariableType]
    country: Mapped[str] = mapped_column(String, nullable=False)  # type: ignore[reportUnknownVariableType]
    is_commercial_operator: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    policies: Mapped[List[PolicyORM]] = relationship("PolicyORM", back_populates="customer")


class PolicyORM(Base):
    __tablename__ = "policies"
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"), nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)  # type: ignore[reportUnknownVariableType]
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)  # type: ignore[reportUnknownVariableType]
    premium_usd: Mapped[float] = mapped_column(Float, nullable=False)  # type: ignore[reportUnknownVariableType]
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending_underwriting")
    jurisdiction: Mapped[str] = mapped_column(String, nullable=False)

    customer: Mapped[CustomerORM] = relationship(CustomerORM, back_populates="policies")
    coverage_items: Mapped[List[CoverageItemORM]] = relationship("CoverageItemORM", back_populates="policy")
    audit_logs: Mapped[List[UnderwritingAuditORM]] = relationship("UnderwritingAuditORM", back_populates="policy")


class CoverageItemORM(Base):
    __tablename__ = "coverage_items"
    id: Mapped[str] = mapped_column(String, primary_key=True)  # type: ignore[reportUnknownVariableType]
    policy_id: Mapped[str] = mapped_column(ForeignKey("policies.id"), nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False)  # type: ignore[reportUnknownVariableType]
    description: Mapped[str] = mapped_column(Text, nullable=False)  # type: ignore[reportUnknownVariableType]
    limit_usd: Mapped[float] = mapped_column(Float, nullable=False)  # type: ignore[reportUnknownVariableType]
    deductible_usd: Mapped[float] = mapped_column(Float, nullable=False)  # type: ignore[reportUnknownVariableType]

    policy: Mapped["PolicyORM"] = relationship("PolicyORM", back_populates="coverage_items")


class UnderwritingAuditORM(Base):
    __tablename__ = "underwriting_audit_logs"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    policy_id: Mapped[str] = mapped_column(ForeignKey("policies.id"), nullable=False)
    event: Mapped[str] = mapped_column(String, nullable=False)  # type: ignore[reportUnknownVariableType]
    notes: Mapped[str] = mapped_column(Text, nullable=True)  # type: ignore[reportUnknownVariableType]
    created_at: Mapped[date] = mapped_column(Date, nullable=False)  # type: ignore[reportUnknownVariableType]

    policy: Mapped["PolicyORM"] = relationship("PolicyORM", back_populates="audit_logs")
