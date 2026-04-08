from datetime import datetime, timedelta
from typing import Dict, Any

from jose import jwt, JWTError

from app.backend.config import settings

def create_access_token(data: Dict[str, Any]) -> str:
    """Create a new JWT access token with expiration.

    The token includes the provided data + standard 'exp' claim
    using the configured ACCESS_TOKEN_EXPIRE_MINUTES.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt: str = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def verify_access_token(token: str) -> Dict[str, Any]:
    """Verify and decode a JWT access token.

    Returns the decoded payload if valid.
    Automatically handles expiration via the 'exp' claim.

    Raises:
        JWTError: if token is invalid, expired, or signature doesn't match.
    """
    try:
        payload: Dict[str, Any] = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError as exc:
        # Re-raise with clear context for easier debugging in services
        raise JWTError(f"Could not validate credentials: {str(exc)}") from exc
