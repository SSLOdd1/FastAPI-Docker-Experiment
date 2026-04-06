from fastapi import FastAPI

from .database import Base, engine
from . import models
from .routes_users import router as users_router
from .routes_items import router as items_router

models.User  # just to ensure import is used

Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Full-Cycle API")

app.include_router(users_router)
app.include_router(items_router)
