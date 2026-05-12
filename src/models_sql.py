from sqlalchemy import Column, String, Boolean, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .db import Base

class CustomerORM(Base):
    __tablename__ = "customers"
    id = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    country = Column(String, nullable=False)
    is_commercial_operator = Column(Boolean, default=False)

    policies = relationship("PolicyORM", back_populates="customer")


class PolicyORM(Base):
    __tablename__ = "policies"
    id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    effective_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    premium_usd = Column(Float, nullable=False)
    status = Column(String, default="pending_underwriting")
    jurisdiction = Column(String, nullable=False)

    customer = relationship("CustomerORM", back_populates="policies")
    coverage_items = relationship("CoverageItemORM", back_populates="policy")
    audit_logs = relationship("UnderwritingAuditORM", back_populates="policy")


class CoverageItemORM(Base):
    __tablename__ = "coverage_items"
    id = Column(String, primary_key=True)
    policy_id = Column(String, ForeignKey("policies.id"), nullable=False)
    code = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    limit_usd = Column(Float, nullable=False)
    deductible_usd = Column(Float, nullable=False)

    policy = relationship("PolicyORM", back_populates="coverage_items")
