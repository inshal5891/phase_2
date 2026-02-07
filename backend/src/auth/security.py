from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Depends
from pydantic import BaseModel
import os
from sqlmodel import Session
from ..database.session import get_session
from ..models.user import User

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize JWT settings
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Initialize HTTP Bearer token scheme
oauth2_scheme = HTTPBearer()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.

    Args:
        plain_password: The plaintext password to verify
        hashed_password: The hashed password to compare against

    Returns:
        True if the passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for the given password.

    Args:
        password: The plaintext password to hash

    Returns:
        The hashed password
    """
    return pwd_context.hash(password)


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.

    Args:
        session: Database session
        email: User's email address
        password: User's plaintext password

    Returns:
        User object if authentication successful, None otherwise
    """
    from ..services.user_service import UserService
    return UserService.authenticate_user(session, email, password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    """
    Get the current user from the JWT token in the request.

    Args:
        credentials: HTTP authorization credentials containing the token
        session: Database session

    Returns:
        User object for the authenticated user

    Raises:
        HTTPException: If token is invalid, expired, or user doesn't exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if username is None or user_id is None:
            raise credentials_exception

        # Verify the user still exists in the database
        user = session.get(User, user_id)
        if user is None or user.email != username or not user.is_active:
            raise credentials_exception

        return user
    except JWTError:
        raise credentials_exception


async def get_current_user_from_header(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    """
    Get current user from Authorization header (alternative method for dependency injection).

    Args:
        credentials: HTTP authorization credentials containing the token
        session: Database session

    Returns:
        User object for the authenticated user

    Raises:
        HTTPException: If token is invalid, expired, or user doesn't exist
    """
    return await get_current_user(credentials, session)


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current active user from the JWT token.

    Args:
        current_user: User object obtained from token

    Returns:
        User object if user is active

    Raises:
        HTTPException: If user account is not active
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user