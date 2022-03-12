from typing import Optional
from pydantic import BaseModel

class OutputUser(BaseModel):
    id: str
    login: str
    
    phone_number: str
    email: Optional[str] = None