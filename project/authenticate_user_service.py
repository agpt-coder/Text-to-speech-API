from datetime import datetime, timedelta

import jwt
import prisma
import prisma.models
from passlib.context import CryptContext
from pydantic import BaseModel


class AuthenticateUserResponse(BaseModel):
    """
    Response model for a successful user authentication, including the JWT token for session management.
    """

    token: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "YOUR_SECRET_KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hashed version.

    Args:
        plain_password (str): The plaintext password entered by the user.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_by_email(email: str):
    """
    Retrieve a user from the database by their email address.

    Args:
        email (str): The email address of the user to retrieve.

    Returns:
        User object or None if no user is found.
    """
    return await prisma.models.User.prisma().find_unique(where={"email": email})


async def authenticate_user(email: str, password: str) -> AuthenticateUserResponse:
    """
    Authenticate user and return JWT token

    Args:
        email (str): The email address associated with the user's account.
        password (str): The password for the user's account.

    Returns:
        AuthenticateUserResponse: Response model for a successful user authentication, including the JWT token for session management.
    """
    user = await get_user_by_email(email)
    if not user or not await verify_password(password, user.password):
        raise Exception("Invalid login credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode(
        {"sub": user.email, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return AuthenticateUserResponse(token=token)
