import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


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
async def test_completion_metrics_excludes_total_hours(client: AsyncClient) -> None:
    response = await client.get("/report/completion_metrics")

    assert response.status_code == 200
    data = response.json()
    assert "total_tasks" in data
    assert "completed_tasks" in data
    assert "completion_rate" in data
    assert "total_hours_spent" not in data


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_returns_structured_response(client: AsyncClient) -> None:
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
    data = response.json()
    assert data["message"] == "Task logged successfully."
    assert isinstance(data["task_id"], int)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_task_status_returns_404_for_missing_task(client: AsyncClient) -> None:
    response = await client.get("/task/99999/status")

    assert response.status_code == 404
    assert "detail" in response.json()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_task_status_returns_existing_task_status(client: AsyncClient) -> None:
    response = await client.get("/task/1/status")

    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == 1
    assert data["status"] in {"pending", "in_progress", "complete"}
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_log_task_with_invalid_status_returns_422(client: AsyncClient) -> None:
        response = await client.post(
            "/log_task",
            json={
                "task_id": 0,
                "title": "Review pull request",
                "status": "invalid_status",
                "hours_spent": 1.5,
            },
        )

        assert response.status_code == 422


    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_log_task_with_missing_required_field_returns_422(client: AsyncClient) -> None:
        response = await client.post(
            "/log_task",
            json={
                "task_id": 0,
                "title": "Review pull request",
                "hours_spent": 1.5,
            },
        )

        assert response.status_code == 422


    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_log_task_with_negative_hours_returns_422(client: AsyncClient) -> None:
        response = await client.post(
            "/log_task",
            json={
                "task_id": 0,
                "title": "Review pull request",
                "status": "pending",
                "hours_spent": -1.5,
            },
        )

        assert response.status_code == 422


    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_log_task_increments_task_id(client: AsyncClient) -> None:
        response1 = await client.post(
            "/log_task",
            json={
                "task_id": 0,
                "title": "Task one",
                "status": "pending",
                "hours_spent": 1.0,
            },
        )
        task_id_1 = response1.json()["task_id"]

        response2 = await client.post(
            "/log_task",
            json={
                "task_id": 0,
                "title": "Task two",
                "status": "pending",
                "hours_spent": 2.0,
            },
        )
        task_id_2 = response2.json()["task_id"]

        assert task_id_2 > task_id_1


    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_report_completion_rate_accuracy(client: AsyncClient) -> None:
        response = await client.get("/report")

        assert response.status_code == 200
        data = response.json()
        assert data["completion_rate"] == round(1 / 3, 2)


    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_report_total_hours_spent_sum(client: AsyncClient) -> None:
        response = await client.get("/report")

        assert response.status_code == 200
        data = response.json()
        expected_hours = round(8.5 + 15.0 + 0.0, 2)
        assert data["total_hours_spent"] == expected_hours


    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_task_status_returns_correct_status(client: AsyncClient) -> None:
        response = await client.get("/task/1/status")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "complete"


    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_task_status_for_in_progress_task(client: AsyncClient) -> None:
        response = await client.get("/task/2/status")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "in_progress"


    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_tasks_response_structure(client: AsyncClient) -> None:
        response = await client.get("/tasks")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("task_id" in task and "title" in task for task in data)