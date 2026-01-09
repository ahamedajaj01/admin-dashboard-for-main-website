# this file is used for password verification during login
# we are using passlib to hash and verify passwords
# it will take plain password and hashed password as input and return True if they match else False

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)