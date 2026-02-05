from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlmodel import Session
from datetime import datetime
import os
from ..database.session import get_session
from ..models.user import User

# Initialize JWT settings
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Initialize HTTP Bearer token scheme
oauth2_scheme = HTTPBearer()


def get_current_user_from_token(
    token: str,
    session: Session
) -> Optional[User]:
    """
    Extract and validate user from JWT token.

    Args:
        token: JWT token string
        session: Database session

    Returns:
        User object if token is valid and user exists, None otherwise
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
    Get current user from Authorization header.

    Args:
        credentials: HTTP authorization credentials containing the token
        session: Database session

    Returns:
        User object for the authenticated user

    Raises:
        HTTPException: If token is invalid, expired, or user doesn't exist
    """
    return get_current_user_from_token(credentials.credentials, session)


def require_active_user(
    current_user: User = Depends(get_current_user_from_header)
) -> User:
    """
    Require that the current user is active.

    Args:
        current_user: User object obtained from token

    Returns:
        User object if user is active

    Raises:
        HTTPException: If user account is not active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is not active"
        )
    return current_user