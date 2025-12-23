
import pytest
from httpx import AsyncClient

# Mock Authenticated User (This is a simplified example, in real app we'd need to mock the dependency override)
# For now, we assume the test simple endpoints that don't need auth OR we rely on standard auth flow if applicable.
# However, the endpoints require `current_user`. 
# We need to override the dependency via `app.dependency_overrides`.

from app.main import app
from app.api import deps
from app.models.user import User

async def override_get_current_active_user():
    return User(id="test_user_id", email="test@example.com", is_active=True)

app.dependency_overrides[deps.get_current_active_user] = override_get_current_active_user

@pytest.mark.anyio
async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Flux Depth Generator API"}

@pytest.mark.anyio
async def test_list_models(client: AsyncClient):
    response = await client.get("/api/v1/depth/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) == 3
    assert data["models"][0]["id"] == "vits"

@pytest.mark.anyio
async def test_get_jobs_empty(client: AsyncClient):
    response = await client.get("/api/v1/depth/jobs")
    # This might fail if the Mock DB isn't setup inside fixtures correctly, 
    # but let's see if it returns a list locally.
    # Ideally we'd mock bulk_processor too.
    assert response.status_code == 200
    assert isinstance(response.json(), list)
