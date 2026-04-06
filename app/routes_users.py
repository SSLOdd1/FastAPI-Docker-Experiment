from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas, auth
from .deps import get_db_dep

router = APIRouter(tags=["users"])


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db_dep)):
    existing = db.query(models.User).filter(models.User.username == user_in.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed = auth.hash_password(user_in.password)
    user = models.User(username=user_in.username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token)
def login(user_in: schemas.UserCreate, db: Session = Depends(get_db_dep)):
    user = auth.authenticate_user(db, user_in.username, user_in.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
