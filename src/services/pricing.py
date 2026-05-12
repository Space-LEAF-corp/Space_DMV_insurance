from typing import List
from ..models.asset import SpaceAsset
from ..models.policy import CoverageItem

def base_rate_for_environment(env: str) -> float:
    table = {
        "ground": 0.002,
        "suborbital": 0.005,
        "orbital": 0.01,
        "lunar": 0.015,
    }
    return table.get(env, 0.02)

def calculate_premium(assets: List[SpaceAsset], coverage: List[CoverageItem]) -> float:
    premium = 0.0
    for asset in assets:
        env_rate = base_rate_for_environment(asset.environment)
        asset_sum_insured = sum(c.limit_usd for c in coverage)
        premium += asset_sum_insured * env_rate
    return round(premium, 2)
