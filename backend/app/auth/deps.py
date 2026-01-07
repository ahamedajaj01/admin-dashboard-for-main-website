from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.jwt import decode_access_token
from jose import JWTError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.login_model import AdminUser

security = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> AdminUser:
    # Token must exist
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token is missing"
        )
    token = credentials.credentials

    # decode and validate JWT token
    try:
        payload = decode_access_token(token)
    except JWTError:    
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # validate required claims
    email: str | None = payload.get("sub")
    role: str | None = payload.get("role")

    if not email or not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing claims in token"
        )
    
    #  Load user from db (source of truth)
    user = db.query(AdminUser).filter(AdminUser.email == email).first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    
    # optional: role verification 
    if user.role != role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token role mismatch"
        )
    
    return user


