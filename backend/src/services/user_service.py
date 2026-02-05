from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate, UserLogin, UserRegister
from ..auth.security import get_password_hash, verify_password
from datetime import datetime


class UserService:
    """Service class for handling user-related business logic including authentication."""

    @staticmethod
    def create_user(session: Session, user_data: UserRegister) -> User:
        """
        Create a new user with hashed password.

        Args:
            session: Database session
            user_data: User registration data including email and password

        Returns:
            The created User object
        """
        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create user object with hashed password
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=True,
            email_verified=False
        )

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
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
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if not user or not verify_password(password, user.hashed_password):
            return None

        # Update last login time
        user.last_login = datetime.utcnow()
        session.add(user)
        session.commit()

        return user

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.

        Args:
            session: Database session
            email: User's email address

        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        return user

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.

        Args:
            session: Database session
            user_id: User's ID

        Returns:
            User object if found, None otherwise
        """
        user = session.get(User, user_id)
        return user

    @staticmethod
    def update_user_last_login(session: Session, user: User) -> User:
        """
        Update the last login time for a user.

        Args:
            session: Database session
            user: User object to update

        Returns:
            Updated User object
        """
        user.last_login = datetime.utcnow()
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def deactivate_user(session: Session, user_id: int) -> bool:
        """
        Deactivate a user account.

        Args:
            session: Database session
            user_id: ID of the user to deactivate

        Returns:
            True if user was deactivated, False if user not found
        """
        user = session.get(User, user_id)
        if not user:
            return False

        user.is_active = False
        session.add(user)
        session.commit()
        return True

    @staticmethod
    def activate_user(session: Session, user_id: int) -> bool:
        """
        Activate a user account.

        Args:
            session: Database session
            user_id: ID of the user to activate

        Returns:
            True if user was activated, False if user not found
        """
        user = session.get(User, user_id)
        if not user:
            return False

        user.is_active = True
        session.add(user)
        session.commit()
        return True

    @staticmethod
    def verify_email(session: Session, user_id: int) -> bool:
        """
        Mark a user's email as verified.

        Args:
            session: Database session
            user_id: ID of the user to verify email for

        Returns:
            True if email was verified, False if user not found
        """
        user = session.get(User, user_id)
        if not user:
            return False

        user.email_verified = True
        session.add(user)
        session.commit()
        return True