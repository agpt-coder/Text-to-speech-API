import os
from datetime import datetime, timedelta

import jwt
from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    """
    This model outlines the structure of the response returned after successfully refreshing the user's authentication token. A new JWT token is provided.
    """

    new_token: str


SECRET_KEY = os.getenv("JWT_SECRET_KEY")

ALGORITHM = os.getenv("JWT_ALGORITHM")


async def refresh_token(existing_token: str) -> RefreshTokenResponse:
    """
    Refresh user's JWT token

    Validates the provided JWT token and issues a new JWT token. This function assumes the presence of
    a JWT_SECRET_KEY and JWT_ALGORITHM in the environment variables for signing the token.

    Args:
        existing_token (str): The current valid JWT token provided by the user for validation.

    Returns:
        RefreshTokenResponse: This model outlines the structure of the response returned after successfully
        refreshing the user's authentication token. A new JWT token is provided.

    Raises:
        jwt.ExpiredSignatureError: If the existing token is expired.
        jwt.InvalidTokenError: If the existing token is invalid for any other reason.
    """
    try:
        payload = jwt.decode(existing_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        exp = datetime.utcnow() + timedelta(days=1)
        new_payload = {"sub": user_id, "exp": exp}
        new_token = jwt.encode(new_payload, SECRET_KEY, algorithm=ALGORITHM)
        return RefreshTokenResponse(new_token=new_token)
    except jwt.ExpiredSignatureError:
        raise Exception("The provided token has expired. Please login again.")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token. Please check the token and try again.")
