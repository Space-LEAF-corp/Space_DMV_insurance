from pydantic import BaseModel
from typing import Literal

SpaceAssetType = Literal[
    "orbital_satellite",
    "lunar_rover",
    "space_car",
    "training_sim_rig",
    "ground_control_terminal"
]

class SpaceAsset(BaseModel):
    id: str
    owner_id: str
    asset_type: SpaceAssetType
    model_name: str
    serial_number: str
    environment: Literal["ground", "suborbital", "orbital", "lunar"]
    safety_cert_version: str  # Space LEAF Corp safety cert ID
