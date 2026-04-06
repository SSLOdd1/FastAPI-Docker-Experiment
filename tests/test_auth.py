import pytest
from httpx import AsyncClient

from app.main import app
from app.database import Base, engine, SessionLocal
from app import models


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # register
        res = await ac.post("/register", json={"username": "tyler", "password": "secret"})
        assert res.status_code == 201
        data = res.json()
        assert data["username"] == "tyler"

        # login
        res = await ac.post("/login", json={"username": "tyler", "password": "secret"})
        assert res.status_code == 200
        token = res.json()["access_token"]
        assert token
