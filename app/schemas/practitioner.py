from pydantic import BaseModel ,EmailStr

class PractitionerCreate(BaseModel):
    full_name:str
    email:EmailStr
    practice_number: str
    profession: str

class PractitionerResponse(BaseModel):
    id:int
    full_name:str
    email:EmailStr
    practice_number:str
    profession:str
    is_verified:bool

class config:
    from_attributes=True

class verifycodeRequest(BaseModel):
    email:EmailStr
    verification_code:str
    