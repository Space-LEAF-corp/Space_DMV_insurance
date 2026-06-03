from typing import List, Dict, Any, Callable, cast
from models.asset import SpaceAsset
from models.policy import CoverageItem
from .pricing import calculate_premium as _calculate_premium_raw  # type: ignore[reportUnknownVariableType]
from .compliance import is_asset_safety_compliant as _is_asset_safety_compliant_raw  # type: ignore[reportUnknownVariableType]
# cast the imported symbol to a precise Callable type for static type checkers
_is_asset_safety_compliant = cast(Callable[[SpaceAsset], bool], _is_asset_safety_compliant_raw)

# cast the imported premium calculator to a precise Callable type for static type checkers
_calculate_premium = cast(Callable[[List[SpaceAsset], List[CoverageItem]], float], _calculate_premium_raw)


# explicit typed wrapper for imported function to satisfy static type checkers
def is_asset_safety_compliant(asset: SpaceAsset) -> bool:
    assert isinstance(asset, SpaceAsset), f"Expected SpaceAsset, got {type(asset)}"
    result: bool = _is_asset_safety_compliant(asset)
    return result

class UnderwritingError(Exception):
    pass

def underwrite_policy(
    customer_id: str,
    assets: List[SpaceAsset],
    coverage: List[CoverageItem]
) -> Dict[str, Any]:
    # use the cast-typed premium calculator
    calculate_premium = _calculate_premium
    # 1. Safety compliance gate
    non_compliant: List[SpaceAsset] = [a for a in assets if not is_asset_safety_compliant(a)]
    if non_compliant:
        raise UnderwritingError("One or more assets are not safety-compliant with Space LEAF Corp standards.")

    # 2. Premium calculation
    premium = calculate_premium(assets, coverage)

    # 3. Simple rule: reject if exposure too high without commercial flag
    # Explicit list comprehension and annotation to help static type checkers
    total_limit: float = sum((c.limit_usd for c in coverage), 0.0) * float(len(assets))
    if total_limit > 5_000_000:
        # In real life: escalate to human underwriter
        raise UnderwritingError("Exposure exceeds auto-bind limit; manual review required.")

    return {
        "customer_id": customer_id,
        "premium_usd": premium,
        "status": "approved_auto"
    }
