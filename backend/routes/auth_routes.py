# routes/auth_routes.py
from fastapi import APIRouter, HTTPException
from jose import jwt
from datetime import datetime, timedelta
from models.user import UserCreate, UserLogin
from core.database import users_collection  # async MongoDB collection
from core.auth import SECRET_KEY, ALGORITHM
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

router = APIRouter(prefix="/auth", tags=["Auth"])

# JWT expiration in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Argon2 password hasher
ph = PasswordHasher()


def create_access_token(data: dict):
    """Generate a JWT token with expiration"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --------------------------
# Password utilities
# --------------------------
def hash_password(password: str) -> str:
    """Hash password with Argon2 (no length limit)"""
    return ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify password with Argon2"""
    try:
        return ph.verify(hashed, password)
    except VerifyMismatchError:
        return False


# --------------------------
# Routes
# --------------------------
@router.post("/register")
async def register_user(user: UserCreate):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = hash_password(user.password)
    new_user = {
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.utcnow(),
    }

    result = await users_collection.insert_one(new_user)
    return {
        "message": "✅ User registered successfully",
        "user_id": str(result.inserted_id)
    }


@router.post("/login")
async def login_user(user: UserLogin):
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_email": db_user["email"]
    }


@router.post("/logout")
async def logout_user():
    return {"message": "✅ Logged out successfully"}
