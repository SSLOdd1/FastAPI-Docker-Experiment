from fastapi import Depends
from sqlalchemy.orm import Session

from .database import get_db
from .auth import get_current_user
from . import models


def get_db_dep(db: Session = Depends(get_db)):
    return db


def get_current_user_dep(user: models.User = Depends(get_current_user)):
    return user
