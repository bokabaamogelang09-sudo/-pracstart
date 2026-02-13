from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Practitioner(Base):
    __tablename__ = "practitioners"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    practice_number = Column(String, unique=True, index=True, nullable=False)
    profession = Column(String, nullable=False)

    role= Column(String,default="practitioner")
    is_verified = Column(Boolean, default=False)

    verification_source = Column(String, nullable=True)
    verification_code=Column(String, nullable=True)

    verification_expires_at=Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

