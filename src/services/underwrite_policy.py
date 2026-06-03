from typing import Any
from decimal import Decimal

from services.premium import calculate_premium  # type: ignore
from services.regulation import validate_jurisdiction, max_auto_bind_limit
from services.exceptions import UnderwritingError  # type: ignore

__all__: list[str] = []


def is_asset_safety_compliant(asset: Any) -> bool:
    """Check if an asset meets Space LEAF Corp safety standards."""
    return getattr(asset, "safety_compliant", False)

def underwrite_policy(
    customer_id: str,
    assets: list[Any],
    coverage: list[Any],
    jurisdiction: str
) -> dict[str, object]:
    if not validate_jurisdiction(jurisdiction):
        raise UnderwritingError("Unsupported jurisdiction for automatic underwriting.")

    non_compliant = [a for a in assets if not is_asset_safety_compliant(a)]
    if non_compliant:
        raise UnderwritingError("One or more assets are not safety-compliant with Space LEAF Corp standards.")

    # ensure premium is a float for typing consumers; calculate_premium may return Decimal or other numeric type
    # calculate_premium is imported with ignored typing, so infer as Any before narrowing
    # calculate_premium is imported with ignored typing; treat result as Any before narrowing
    premium_result: Any = calculate_premium(assets, coverage) # pyright: ignore[reportUnknownVariableType]
    if not isinstance(premium_result, (int, float, Decimal)):
        raise UnderwritingError("Unsupported premium type returned from calculation.")
    premium: float = float(premium_result)
    total_limit = sum(c.limit_usd for c in coverage) * len(assets)

    if total_limit > max_auto_bind_limit(jurisdiction):
        raise UnderwritingError("Exposure exceeds auto-bind limit for this jurisdiction; manual review required.")

    return {
        "customer_id": customer_id,
        "premium_usd": premium,
        "status": "approved_auto",
        "jurisdiction": jurisdiction,
    }
