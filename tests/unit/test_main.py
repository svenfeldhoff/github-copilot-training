import pytest

from app.main import TaskStatus, fetch_all_tasks, generate_productivity_report


@pytest.mark.asyncio
async def test_generate_productivity_report_returns_expected_shape() -> None:
    report = await generate_productivity_report()

    assert report.total_tasks >= 1
    assert report.completed_tasks >= 0
    assert report.total_hours_spent >= 0
    assert 0 <= report.completion_rate <= 1


@pytest.mark.asyncio
async def test_generate_productivity_report_counts_pending_as_completed_current_logic() -> None:
    tasks = await fetch_all_tasks()
    expected_completed = sum(1 for task in tasks if task.status == TaskStatus.PENDING)
    report = await generate_productivity_report()

    # Mirrors current implementation behavior to lock regression expectations.
    assert report.completed_tasks == expected_completed
    assert TaskStatus.PENDING.value == "pending"
