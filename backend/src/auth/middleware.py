from typing import Optional
from fastapi import HTTPException, status, Request
from jose import JWTError, jwt
from sqlmodel import Session
from datetime import datetime
import os
from ..database.session import get_session
from ..models.user import User

# Initialize JWT settings
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


class AuthMiddleware:
    """
    Authentication middleware to verify JWT tokens on incoming requests.

    This middleware handles:
    - JWT token validation
    - User identification from token
    - Token expiration checking
    - Authorization header parsing
    """

    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """
        Verify a JWT token and return its payload.

        Args:
            token: JWT token string

        Returns:
            Payload dictionary if token is valid, None otherwise
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            # Check if token is expired
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
                return None

            return payload
        except JWTError:
            return None

    @staticmethod
    def get_user_from_token(token: str) -> Optional[User]:
        """
        Get user from JWT token.

        Args:
            token: JWT token string

        Returns:
            User object if token is valid and user exists, None otherwise
        """
        payload = AuthMiddleware.verify_token(token)

        if payload is None:
            return None

        # Extract user info from token
        user_id = payload.get("user_id")
        user_email = payload.get("email")

        if user_id is None or user_email is None:
            return None

        # Verify the user exists in the database
        with next(get_session()) as session:
            user = session.get(User, user_id)
            if user and user.email == user_email and user.is_active:
                return user

        return None

    @staticmethod
    async def authenticate_request(request: Request) -> Optional[User]:
        """
        Authenticate a request by extracting and validating the JWT token.

        Args:
            request: Incoming FastAPI request

        Returns:
            User object if authentication succeeds, None otherwise
        """
        # Get authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        # Extract token
        token = auth_header[len("Bearer "):]

        # Get user from token
        user = AuthMiddleware.get_user_from_token(token)

        return user

    @staticmethod
    async def validate_token_in_request(request: Request) -> bool:
        """
        Validate that the request contains a valid JWT token.

        Args:
            request: Incoming FastAPI request

        Returns:
            True if token is valid, raises HTTPException otherwise
        """
        user = await AuthMiddleware.authenticate_request(request)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Attach user info to request for use in route handlers
        request.state.user = user
        return True