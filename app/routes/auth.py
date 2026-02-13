from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.models.practitioner import practitioner
from app.utils.jwt import create_access_token

router = APIRouter(prefix="/auth",tags=["Auth"])
def login(email:str,db:Session=Depends(get_db)):
    practitioner =db.query(Practitioner).filter(
        Practitioner.email==email,
        Practitioner.is_verified==True
    
    ).first()

    if not practitioner:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials or not verified"
            )
        access_token= create_access_token(
            data{

                "sub":practitioner.id,
                "role":practitioner.role,
                "email":practitioner.email
            },
            expire_delta=timedelta(minutes=30)
        )    

        return{
            "access_token":token,
            "token_type":"bearer"
        }

def create_access_token