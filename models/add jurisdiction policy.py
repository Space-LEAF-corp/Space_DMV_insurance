from pydantic import BaseModel, Field
from typing import List
from datetime import date
from .asset import SpaceAsset

class Policy(BaseModel):
    id: str
    customer_id: str
    assets: List[SpaceAsset]
    coverage: List[CoverageItem]
    effective_date: date
    expiry_date: date
    premium_usd: float = Field(..., ge=0)
    status: str = "pending_underwriting"
    jurisdiction: str  # e.g. "US-FL", "US-CA", "EU", "INTL"
