from pydantic import BaseModel, Field
from typing import Optional

class PractitionerCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    hpcsa_number: str = Field(..., pattern=r"^PS\d{7}$")  # Format: PS1234567
    practice_number: Optional[str] = None
    practice_type: str = Field(..., description="psychology, gp, physiotherapy, etc.")

class PractitionerResponse(BaseModel):
    id: int
    full_name: str
    hpcsa_number: str
    practice_type: str
    verified: bool
    verification_source: Optional[str]

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)
    
    