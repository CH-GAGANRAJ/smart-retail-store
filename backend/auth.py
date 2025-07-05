from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from backend.databases import SessionLocal
from backend.models import User
from passlib.context import CryptContext # For password hashing (optional but recommended)
from pydantic import BaseModel # Import BaseModel

router = APIRouter(prefix="/auth")

# Password hashing context (for a real app, you'd use a stronger hash)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define Pydantic models for request bodies
class LoginRequest(BaseModel):
    username: str
    password: str
    role: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Handles user login.
    For a real application, you would hash passwords and verify them.
    This is a simplified example for the hackathon.
    """
    user = db.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # In a real app, you'd use pwd_context.verify(request.password, user.password)
    # For this hackathon, we'll do a simple plaintext comparison (NOT SECURE FOR PRODUCTION)
    if user.password != request.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if user.role != request.role:
        raise HTTPException(status_code=400, detail=f"User is not a {request.role}")

    # Return user ID and role upon successful login
    return {"message": "Login successful", "user_id": user.id, "role": user.role}

@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Registers a new user.
    For a real application, you would hash passwords before storing them.
    """
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password before storing (recommended for production)
    # hashed_password = pwd_context.hash(request.password)

    new_user = User(username=request.username, password=request.password, role=request.role) # Use hashed_password in production
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

