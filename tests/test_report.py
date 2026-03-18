import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_productivity_report():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/report")
    assert response.status_code == 200
    data = response.json()
    assert "total_tasks" in data
    assert "completed_tasks" in data
    assert "total_hours_spent" in data
    assert "completion_rate" in data


@pytest.mark.asyncio
async def test_get_completion_metrics():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/report/completion_metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_tasks" in data
    assert "completed_tasks" in data
    assert "completion_rate" in data
    assert "total_hours_spent" not in data


@pytest.mark.asyncio
async def test_log_task_returns_structured_response():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/log_task",
            json={
                "task_id": 0,
                "title": "Review pull request",
                "status": "pending",
                "hours_spent": 1.5,
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task logged successfully."
    assert isinstance(data["task_id"], int)


@pytest.mark.asyncio
async def test_get_task_status_returns_404_for_missing_task():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/task/99999/status")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data