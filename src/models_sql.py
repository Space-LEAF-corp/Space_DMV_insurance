from __future__ import annotations
from datetime import date
from typing import List
from sqlalchemy import String, Boolean, Date, Float, ForeignKey, Text  # type: ignore[import]
from sqlalchemy.orm import DeclarativeMeta, Mapped, mapped_column, relationship  # type: ignore[import]
from .db import Base as _Base  # type: ignore[import]
# Keep the SQLAlchemy Base with a simple assignment to avoid type-checker
# complaints about an untyped declarative base class.
Base = _Base  # type: ignore[reportUnknownVariableType]

class CustomerORM(Base):
    __tablename__ = "customers"
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)  # type: ignore[reportUnknownVariableType]
    full_name: Mapped[str] = mapped_column(String, nullable=False)  # type: ignore[reportUnknownVariableType]
    email: Mapped[str] = mapped_column(String, nullable=False, index=True)  # type: ignore[reportUnknownVariableType]
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)  # type: ignore[reportUnknownVariableType]
    country: Mapped[str] = mapped_column(String, nullable=False)  # type: ignore[reportUnknownVariableType]
    is_commercial_operator: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)  # type: ignore[reportUnknownVariableType]

    policies: Mapped[List["PolicyORM"]] = relationship("PolicyORM", back_populates="customer")  # type: ignore[reportUnknownVariableType]


class PolicyORM(Base):
    __tablename__ = "policies"
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)  # type: ignore[reportUnknownVariableType]
    customer_id: Mapped[str] = mapped_column(String, ForeignKey("customers.id"), nullable=False)  # type: ignore[reportUnknownVariableType]
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)  # type: ignore[reportUnknownVariableType]
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)  # type: ignore[reportUnknownVariableType]
    premium_usd: Mapped[float] = mapped_column(Float, nullable=False)  # type: ignore[reportUnknownVariableType]
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending_underwriting")  # type: ignore[reportUnknownVariableType]
    jurisdiction: Mapped[str] = mapped_column(String, nullable=False)  # type: ignore[reportUnknownVariableType]

    customer: Mapped["CustomerORM"] = relationship("CustomerORM", back_populates="policies")  # type: ignore[reportUnknownVariableType]
    coverage_items: Mapped[List["CoverageItemORM"]] = relationship("CoverageItemORM", back_populates="policy")  # type: ignore[reportUnknownVariableType]
    audit_logs: Mapped[List["UnderwritingAuditORM"]] = relationship("UnderwritingAuditORM", back_populates="policy")  # type: ignore[reportUnknownVariableType]


class CoverageItemORM(Base):
    __tablename__ = "coverage_items"
    id: Mapped[str] = mapped_column(String, primary_key=True)  # type: ignore[reportUnknownVariableType]
    policy_id: Mapped[str] = mapped_column(String, ForeignKey("policies.id"), nullable=False)  # type: ignore[reportUnknownVariableType]
    code: Mapped[str] = mapped_column(String, nullable=False)  # type: ignore[reportUnknownVariableType]
    description: Mapped[str] = mapped_column(Text, nullable=False)  # type: ignore[reportUnknownVariableType]
    limit_usd: Mapped[float] = mapped_column(Float, nullable=False)  # type: ignore[reportUnknownVariableType]
    deductible_usd: Mapped[float] = mapped_column(Float, nullable=False)  # type: ignore[reportUnknownVariableType]

    policy: Mapped["PolicyORM"] = relationship("PolicyORM", back_populates="coverage_items")  # type: ignore[reportUnknownVariableType]

class UnderwritingAuditORM(Base):
    __tablename__ = "underwriting_audit_logs"
    id: Mapped[str] = mapped_column(String, primary_key=True)  # type: ignore[reportUnknownVariableType]
    policy_id: Mapped[str] = mapped_column(String, ForeignKey("policies.id"), nullable=False)  # type: ignore[reportUnknownVariableType]
    event: Mapped[str] = mapped_column(String, nullable=False)  # type: ignore[reportUnknownVariableType]
    notes: Mapped[str] = mapped_column(Text, nullable=True)  # type: ignore[reportUnknownVariableType]
    created_at: Mapped[date] = mapped_column(Date, nullable=False)  # type: ignore[reportUnknownVariableType]

    policy: Mapped["PolicyORM"] = relationship("PolicyORM", back_populates="audit_logs")  # type: ignore[reportUnknownVariableType]
