from pydantic import BaseModel  # type: ignore[reportUnknownVariableType]
from datetime import datetime

class Claim(BaseModel):  # type: ignore[reportUntypedBaseClass]
    id: str
    policy_id: str
    asset_id: str
    incident_time: datetime
    incident_description: str
    environment: str  # where it happened
    estimated_loss_usd: float
    status: str = "submitted"  # under_review, approved, denied
