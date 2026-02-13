from fastapi import Depends, HTTPException,status
from app.dependencies.auth import get_current_user

def require_role(required_role:str):
    def role_checker(user=Depends(get_current_user)):
        if user.get("role") != require_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficent permissions"

            )
          return user
        return role_checker    