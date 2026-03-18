import pytest
from httpx import AsyncClient
from app.main import MOCK_TASKS, DeveloperTask, TaskStatus


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_status_returns_ok(client: AsyncClient) -> None:
    resp = await client.get("/status")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_tasks_returns_list(client: AsyncClient) -> None:
    resp = await client.get("/tasks")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == len(MOCK_TASKS)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_productivity_report_structure(client: AsyncClient) -> None:
    resp = await client.get("/report")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_tasks" in data
    assert "completed_tasks" in data
    assert "total_hours_spent" in data
    assert "completion_rate" in data


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_adds_task_with_new_id(client: AsyncClient) -> None:
    initial_count = len(MOCK_TASKS)
    new_task = {
        "task_id": 0,
        "title": "Test task",
        "status": "pending",
        "hours_spent": 2.0,
    }
    resp = await client.post("/log_task", json=new_task)
    assert resp.status_code == 200
    body = resp.json()
    assert "message" in body
    assert len(MOCK_TASKS) == initial_count + 1
    # The new task should have a proper auto-assigned ID
    new_id = max(MOCK_TASKS.keys())
    assert MOCK_TASKS[new_id].title == "Test task"
