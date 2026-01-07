from datetime import datetime, timedelta
from jose import jwt
from app.config import JWT_SECRET, JWT_ALGORITHM, TOKEN_EXPIRE_MINUTES


def create_access_token(payload: dict):
    data = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str):
    return jwt.decode(
        token, 
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
        options={
            "verify_signature":True,
            "verify_exp":True,
        }
        )
