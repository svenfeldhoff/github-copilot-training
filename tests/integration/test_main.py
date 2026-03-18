import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.integration
async def test_status_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/status")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
@pytest.mark.integration
async def test_tasks_returns_task_list(client: AsyncClient) -> None:
    response = await client.get("/tasks")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert {"task_id", "title", "status", "hours_spent"}.issubset(data[0].keys())


@pytest.mark.asyncio
@pytest.mark.integration
async def test_report_returns_productivity_fields(client: AsyncClient) -> None:
    response = await client.get("/report")

    assert response.status_code == 200
    data = response.json()
    assert "total_tasks" in data
    assert "completed_tasks" in data
    assert "total_hours_spent" in data
    assert "completion_rate" in data


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_returns_message(client: AsyncClient) -> None:
    response = await client.post(
        "/log_task",
        json={
            "task_id": 0,
            "title": "Review pull request",
            "status": "pending",
            "hours_spent": 1.5,
        },
    )

    assert response.status_code == 200
    assert "Task ID" in response.json()
