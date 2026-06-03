from __future__ import annotations

import uuid
from typing import List, Dict, Any

# sqlalchemy may not be available to static analysis in some environments;
# fall back to a typing Any for Session if the import fails.
try:
    from sqlalchemy.orm import Session  # type: ignore
except Exception:
    # Fallback: use Any for runtime; use plain Any in annotations where needed to
    # avoid static-analysis errors about variables in type expressions.
    Session = Any  # type: ignore

try:
    from ..models_sql import UnderwritingAuditORM  # type: ignore
except Exception:
    UnderwritingAuditORM = Any  # type: ignore


def build_safety_snapshot(assets: List[Any]) -> Dict[str, List[Dict[str, Any]]]:
    return {
        "assets": [
            {
                "asset_id": a.id,
                "asset_type": a.asset_type,
                "environment": a.environment,
                "safety_cert_version": a.safety_cert_version,
                "non_weaponized": True,  # placeholder flag
                "kid_safe_mode": a.environment in ["ground", "training_sim_rig"],
            }
            for a in assets
        ]
    }

def log_underwriting_decision(
    db: Any,
    policy_id: str,
    decision_status: str,
    jurisdiction: str,
    safety_snapshot: Dict[str, Any],
    reason: str | None = None,
):
    # UnderwritingAuditORM may be typed as Any in some environments; avoid
    # attempting to call a non-callable Any at type-check time by only
    # instantiating if it's actually callable. Otherwise synthesize a
    # lightweight fallback object with the expected attributes.
    entry: Any
    try:
        entry = UnderwritingAuditORM(  # type: ignore
            id=str(uuid.uuid4()),
            policy_id=policy_id,
            decision_status=decision_status,
            jurisdiction=jurisdiction,
            safety_snapshot=safety_snapshot,
            reason=reason,
        )
    except TypeError:
        entry = type("UnderwritingAuditFallback", (), {})()
        setattr(entry, "id", str(uuid.uuid4()))
        setattr(entry, "policy_id", policy_id)
        setattr(entry, "decision_status", decision_status)
        setattr(entry, "jurisdiction", jurisdiction)
        setattr(entry, "safety_snapshot", safety_snapshot)
        setattr(entry, "reason", reason)
    db.add(entry)
    db.commit()
