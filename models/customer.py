from pydantic import BaseModel, EmailStr  # type: ignore[import]
from datetime import date

class Customer(BaseModel):  # type: ignore[reportUntypedBaseClass]
    id: str
    full_name: str
    email: EmailStr
    date_of_birth: date
    country: str
    is_commercial_operator: bool = False  # company vs individual
