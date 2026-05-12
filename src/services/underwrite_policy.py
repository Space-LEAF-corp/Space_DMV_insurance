from .regulation import validate_jurisdiction, max_auto_bind_limit

def underwrite_policy(
    customer_id: str,
    assets: List[SpaceAsset],
    coverage: List[CoverageItem],
    jurisdiction: str
):
    if not validate_jurisdiction(jurisdiction):
        raise UnderwritingError("Unsupported jurisdiction for automatic underwriting.")

    non_compliant = [a for a in assets if not is_asset_safety_compliant(a)]
    if non_compliant:
        raise UnderwritingError("One or more assets are not safety-compliant with Space LEAF Corp standards.")

    premium = calculate_premium(assets, coverage)
    total_limit = sum(c.limit_usd for c in coverage) * len(assets)

    if total_limit > max_auto_bind_limit(jurisdiction):
        raise UnderwritingError("Exposure exceeds auto-bind limit for this jurisdiction; manual review required.")

    return {
        "customer_id": customer_id,
        "premium_usd": premium,
        "status": "approved_auto",
        "jurisdiction": jurisdiction,
    }
