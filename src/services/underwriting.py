from typing import List
from ..models.asset import SpaceAsset
from ..models.policy import CoverageItem
from .pricing import calculate_premium
from .compliance import is_asset_safety_compliant

class UnderwritingError(Exception):
    pass

def underwrite_policy(
    customer_id: str,
    assets: List[SpaceAsset],
    coverage: List[CoverageItem]
):
    # 1. Safety compliance gate
    non_compliant = [a for a in assets if not is_asset_safety_compliant(a)]
    if non_compliant:
        raise UnderwritingError("One or more assets are not safety-compliant with Space LEAF Corp standards.")

    # 2. Premium calculation
    premium = calculate_premium(assets, coverage)

    # 3. Simple rule: reject if exposure too high without commercial flag
    total_limit = sum(c.limit_usd for c in coverage) * len(assets)
    if total_limit > 5_000_000:
        # In real life: escalate to human underwriter
        raise UnderwritingError("Exposure exceeds auto-bind limit; manual review required.")

    return {
        "customer_id": customer_id,
        "premium_usd": premium,
        "status": "approved_auto"
    }
