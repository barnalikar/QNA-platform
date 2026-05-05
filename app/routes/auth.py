from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.security import hash_password, verify_password
from app.auth_utils import create_token
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

router = APIRouter()

# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- REGISTER ----------------
class RegisterData(BaseModel):
    name: str
    email: str
    password: str

@router.post("/register")
def register(data: RegisterData, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password)
    )

    db.add(user)
    db.commit()

    return {"message": "User registered successfully"}

# ---------------- LOGIN (SWAGGER) ----------------
from pydantic import BaseModel
from app.auth_utils import create_token

class LoginData(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        return {"error": "User not found"}

    if not verify_password(data.password, user.password):
        return {"error": "Invalid password"}

    token = create_token({"user_id": user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "plan": user.plan
    }