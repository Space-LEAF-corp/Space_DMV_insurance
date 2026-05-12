from typing import Literal

JurisdictionCode = str  # keep flexible, but you can narrow later

def validate_jurisdiction(jurisdiction: JurisdictionCode) -> bool:
    """
    Structural check only, not legal advice.
    """
    allowed = {"US-FL", "US-CA", "US-TX", "EU", "INTL"}
    return jurisdiction in allowed

def max_auto_bind_limit(jurisdiction: JurisdictionCode) -> float:
    """
    Example structural rule: different auto-bind limits per jurisdiction.
    """
    table = {
        "US-FL": 3_000_000,
        "US-CA": 2_000_000,
        "US-TX": 4_000_000,
        "EU": 2_500_000,
        "INTL": 1_500_000,
    }
    return table.get(jurisdiction, 1_000_000)
