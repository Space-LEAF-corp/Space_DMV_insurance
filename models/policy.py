from __future__ import annotations

from pydantic import BaseModel, Field  # type: ignore[reportUnknownVariableType]
from typing import List
from datetime import date
from decimal import Decimal
from .asset import SpaceAsset

__all__: List[str] = []

class CoverageItem(BaseModel):  # type: ignore[reportUntypedBaseClass]
    code: str  # e.g. "COLLISION_ORBITAL", "LUNAR_DUST_DAMAGE"
    description: str
    limit_usd: float
    deductible_usd: float

class Policy(BaseModel):  # type: ignore[reportUntypedBaseClass]
    id: str
    customer_id: str
    assets: List[SpaceAsset]
    coverage: List[CoverageItem]
    effective_date: date
    expiry_date: date
    premium_usd: Decimal = Field(..., ge=0)  # type: ignore[reportUnknownVariableType]
    status: str = "pending_underwriting"  # active, cancelled, etc.
