from app.models import practitioner
from sqlalchemy import Column ,Integer,String,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,timedelta

from app.database import Base

class VerificationCode(Base):

    id = Column(Integer, primary_key=True, index=True)
    code= Column(String(6), nullable=False, index =False)

    practitioner_id = Column(
        Integer,
        ForeignKey("practitioners.id",ondelete="CASCADE"),
        nullable=False
    )
    expires_at = column (Integer, primary_key=True, index= true)
    code= Column(string(6),nullable= False,Index=True)

    practitioner_id=Column(
        Integer,ForeignKey("practiners.id",ondelete="CASCADE"),nullable=False
    )
    expires_at=column(Integer, nullable=False)
    used=Column(Boolean,default=False)
    created_at=Column(DateTime, default=datetime.utcnow)
    practitioner= relationship("practitioner",back_populates="verification_codes")



