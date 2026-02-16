from fastapi import Depend, HTTPException,status
from app.models.practitioner import practitioner
def require_role(required_role:str):
    def role_checker(current_user:Practitioner=Depend()):
        if current _user.role!=required_role:
            raise HTTPException(status_code=status,HTTP_403_FORBIDDEN,
            detail="iNSUFFICIENT PERMISSIONS",
            )
            return current_user
        return role_checker

