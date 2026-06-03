from __future__ import annotations

from pydantic import BaseModel, Field  # type: ignore[reportUnknownVariableType]
from typing import Annotated, List
from datetime import date
from .asset import SpaceAsset
from .coverage_item import CoverageItem  # type: ignore[reportUnknownVariableType]

class Policy(BaseModel):  # type: ignore[reportUntypedBaseClass]
    id: str
    customer_id: str
    assets: List[SpaceAsset]
    coverage: List[CoverageItem]
    effective_date: date
    expiry_date: date
    premium_usd: Annotated[float, Field(..., ge=0)]
    status: str = "pending_underwriting"
    jurisdiction: str  # e.g. "US-FL", "US-CA", "EU", "INTL"
