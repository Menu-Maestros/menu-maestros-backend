import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, Request, Depends, status
from fastapi.security import HTTPBearer

from typing import List

from backend.config import settings
from backend.logger import logger

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Generates a JWT token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str):
    """Decodes and verifies a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.info("Token expired")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        logger.info("Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(request: Request):
    # Extract token from the Authorization header
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        raise HTTPException(
            status_code=401, detail="Authorization header missing")

    # Split the 'Bearer token' part
    token_type, token = authorization_header.split()
    if token_type.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid token type")

    # Verify the token and return the payload
    payload = verify_access_token(token)
    return payload  # Returns the decoded token (user data)


def require_user_type(allowed_user_types: List[str]):
    """Dependency to restrict access based on user roles."""
    def user_type_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("user_type") not in allowed_user_types:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return current_user
    return user_type_checker
