import uuid
from sqlalchemy.orm import Session
from typing import List, Dict
from ..models.asset import SpaceAsset

def build_safety_snapshot(assets: List[SpaceAsset]) -> Dict:
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
    db: Session,
    policy_id: str,
    decision_status: str,
    jurisdiction: str,
    safety_snapshot: Dict,
    reason: str | None = None,
):
    from ..models_sql import UnderwritingAuditORM

    entry = UnderwritingAuditORM(
        id=str(uuid.uuid4()),
        policy_id=policy_id,
        decision_status=decision_status,
        jurisdiction=jurisdiction,
        safety_snapshot=safety_snapshot,
        reason=reason,
    )
    db.add(entry)
    db.commit()
