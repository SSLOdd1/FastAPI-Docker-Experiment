import pytest
from httpx import AsyncClient

from app.main import app
from app.database import Base, engine


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.mark.asyncio
async def test_items_requires_auth():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/items")
        assert res.status_code == 401


@pytest.mark.asyncio
async def test_items_with_auth():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/register", json={"username": "tyler", "password": "secret"})
        login_res = await ac.post("/login", json={"username": "tyler", "password": "secret"})
        token = login_res.json()["access_token"]

        res = await ac.get("/items", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        data = res.json()
        assert data["user"] == "tyler"
        assert "items" in data
