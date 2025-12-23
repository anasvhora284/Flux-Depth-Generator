
import pytest
import os
from httpx import AsyncClient

# Set dummy env vars for testing BEFORE importing app
os.environ["MAIL_FROM"] = "test@example.com"
os.environ["MAIL_USERNAME"] = "test"
os.environ["MAIL_PASSWORD"] = "test"
os.environ["MAIL_PORT"] = "587"
os.environ["MAIL_SERVER"] = "smtp.test.com"
os.environ["SECRET_KEY"] = "supersecretkey"

from app.main import app

@pytest.fixture
def anyio_backend():
    return 'asyncio'

from httpx import AsyncClient, ASGITransport

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

# Disable startup events (DB init) for tests
@pytest.fixture(scope="session", autouse=True)
def disable_startup():
    from app.main import app
    app.router.on_startup = []

