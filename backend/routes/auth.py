from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user import User, UserCreate, UserLogin, Token
from auth.auth import authenticate_user, create_access_token, get_current_user
from services.database import DatabaseService
from datetime import timedelta

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_database() -> DatabaseService:
    db_service = DatabaseService()
    await db_service.connect()
    try:
        yield db_service
    finally:
        await db_service.disconnect()

@router.post("/register", response_model=User)
async def register(user: UserCreate, db: DatabaseService = Depends(get_database)):
    # Check if user already exists
    existing_user = await db.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    created_user = await db.create_user(user)
    return created_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: DatabaseService = Depends(get_database)):
    user = await authenticate_user(db.db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_active_user(token: str = Depends(oauth2_scheme),
                                 db: DatabaseService = Depends(get_database)) -> User:
    user = await get_current_user(token, db.db)
    return user