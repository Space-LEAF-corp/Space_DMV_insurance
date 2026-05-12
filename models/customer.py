from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class Customer(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    date_of_birth: date
    country: str
    is_commercial_operator: bool = False  # company vs individual
