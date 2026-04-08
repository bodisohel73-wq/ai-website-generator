
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

from app.backend.utils.password_hash import hash_password, verify_password
from app.backend.utils.jwt_handler import create_access_token
from app.backend.models.user_model import user_helper

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest):
    """Register a new user with hashed password."""
    db = get_db()
    users_collection = db["users"]

    # Check for existing user
    if users_collection.find_one({"email": request.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Hash password using utility
    hashed_password = hash_password(request.password)

    user_data = {
        "email": request.email,
        "password": hashed_password,
        "created_at": datetime.utcnow(),
    }

    # Insert into MongoDB
    result = users_collection.insert_one(user_data)

    # Retrieve and clean the created document
    created_user = users_collection.find_one({"_id": result.inserted_id})
    user_dict = user_helper(created_user)

    return {
        "message": "User created successfully",
        "user": {
            "id": user_dict["id"],
            "email": user_dict["email"],
        },
    }


@router.post("/login")
async def login(request: LoginRequest):
    """Authenticate user and return JWT access token."""
    db = get_db()
    users_collection = db["users"]

    # Find user by email
    user_doc = users_collection.find_one({"email": request.email})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert to clean dict and verify password using utility
    user_dict = user_helper(user_doc)
    if not verify_password(request.password, user_dict.get("password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT using utility
    access_token = create_access_token(
        data={"sub": user_dict["email"], "user_id": user_dict["id"]}
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )
