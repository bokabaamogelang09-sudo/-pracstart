from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.practitioner import Practitioner
from app.schemas.practitioner import (
    PractitionerCreate,
    PractitionerResponse,
    PractitionerVerify,
)
from app.utils.security import generate_verification_code, verification_expiry

router = APIRouter(
    prefix="/practitioners",
    tags=["Practitioners"],
)

# =========================
# — REGISTRATION
# =========================
@router.post(
    "/register",
    response_model=PractitionerResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_practitioner(
    payload: PractitionerCreate,
    db: Session = Depends(get_db),
):
    existing_practitioner = (
        db.query(Practitioner)
        .filter(Practitioner.email == payload.email)
        .first()
    )

    if existing_practitioner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Practitioner with this email already exists",
        )

    verification_code = generate_verification_code()

    practitioner = Practitioner(
        full_name=payload.full_name,
        email=payload.email,
        practice_number=payload.practice_number,
        profession=payload.profession,
        is_verified=False,
        verification_code=verification_code,
        verification_expires_at=verification_expiry(),
    )

    db.add(practitioner)
    db.commit()
    db.refresh(practitioner)

    # TEMP: log code (replace with email/SMS)
    print(f" Verification code for {practitioner.email}: {verification_code}")

    return practitioner


# =========================
# — VERIFICATION
# =========================
@router.post("/verify", status_code=status.HTTP_200_OK)
def verify_practitioner(
    payload: PractitionerVerify,
    db: Session = Depends(get_db),
):
    practitioner = (
        db.query(Practitioner)
        .filter(Practitioner.email == payload.email)
        .first()
    )

    if not practitioner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Practitioner not found",
        )

    if practitioner.is_verified:
        return {
            "status": "verified",
            "message": "Practitioner already verified",
        }

    if practitioner.verification_expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code expired",
        )

    if practitioner.verification_code != payload.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code",
        )

    # Mark as verified
    practitioner.is_verified = True
    practitioner.verification_code = None
    practitioner.verification_expires_at = None

    db.commit()
    db.refresh(practitioner)

    return {
        "status": "success",
        "message": "Practitioner successfully verified",
    }
