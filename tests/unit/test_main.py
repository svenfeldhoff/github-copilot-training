import pytest
from app.main import TaskStatus, generate_productivity_report, MOCK_TASKS, DeveloperTask


@pytest.mark.asyncio
async def test_generate_productivity_report_counts_complete_tasks() -> None:
    """generate_productivity_report should count COMPLETE tasks, not PENDING ones."""
    report = await generate_productivity_report()
    expected_completed = sum(
        1 for task in MOCK_TASKS.values() if task.status == TaskStatus.COMPLETE
    )
    assert report.completed_tasks == expected_completed


@pytest.mark.asyncio
async def test_generate_productivity_report_total_tasks() -> None:
    report = await generate_productivity_report()
    assert report.total_tasks == len(MOCK_TASKS)


@pytest.mark.asyncio
async def test_generate_productivity_report_completion_rate() -> None:
    report = await generate_productivity_report()
    expected_rate = round(report.completed_tasks / report.total_tasks, 2)
    assert report.completion_rate == expected_rate


@pytest.mark.asyncio
async def test_generate_productivity_report_total_hours() -> None:
    report = await generate_productivity_report()
    expected_hours = round(sum(t.hours_spent for t in MOCK_TASKS.values()), 2)
    assert report.total_hours_spent == expected_hours
