from fastapi import APIRouter, HTTPException, Depends
from app.auth.schemas import LoginRequest, TokenResponse
from app.utils.jwt import create_access_token

from app.utils.security import verify_password # password verification function
from app.db.session import get_db # database session
from sqlalchemy.orm import session
from app.models.login_model import AdminUser
from app.auth.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: session = Depends(get_db)):
    user = db.query(AdminUser).filter(AdminUser.email==data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user.email,
        "role": "admin"
    })

    return {"access_token": token}

@router.get("/me")
def get_me(current_user: AdminUser = Depends(get_current_user)):
    return{
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }
