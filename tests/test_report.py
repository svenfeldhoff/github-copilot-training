import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_productivity_report():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/report")
    assert response.status_code == 200
    data = response.json()
    assert "total_tasks" in data
    assert "completed_tasks" in data
    assert "total_hours_spent" in data
    assert "completion_rate" in data