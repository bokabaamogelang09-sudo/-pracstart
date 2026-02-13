from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base  

class Practitioner(Base):
    __tablename__ = "practitioners"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    hpcsa_number = Column(String, unique=True, index=True, nullable=False)
    practice_number = Column(String, nullable=True)
    practice_type = Column(String, nullable=False)  # e.g., "psychology", "gp"
    verified = Column(Boolean, default=False)
    verification_source = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to verification codes
    verification_codes = relationship("VerificationCode", back_populates="practitioner")