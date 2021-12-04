from typing import Optional
from pydantic import BaseModel

class InputCreateUser(BaseModel):
    login: str
    password: str
    phone_number: str
    email: Optional[str] = None