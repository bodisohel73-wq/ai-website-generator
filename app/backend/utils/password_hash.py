from passlib.context import CryptContext

# Production-ready bcrypt password hashing context
# - Automatically handles salting and work factor
# - Secure defaults with deprecated="auto" for future-proofing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    # Higher rounds = more secure (but slower)
    # 12 is the recommended minimum for 2025+
    bcrypt__default_rounds=12,
)


def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt.

    Never store or log the plain password.
    """
    if not password:
        raise ValueError("Password cannot be empty")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its bcrypt hash.

    Returns True if the password matches, False otherwise.
    Constant-time comparison is handled by passlib.
    """
    if not plain_password or not hashed_password:
        return False
    return pwd_context.verify(plain_password, hashed_password)
