from enum import Enum
from pydantic import BaseModel


class TaskStatus(str, Enum):
    """Available statuses for any task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"


class DeveloperTask(BaseModel):
    """Model for a single task logged by a developer."""
    task_id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    hours_spent: float = 0.0


class ProductivityReport(BaseModel):
    """The final calculated report."""
    total_tasks: int
    completed_tasks: int
    total_hours_spent: float
    completion_rate: float


class TaskCompletionMetrics(BaseModel):
    """Metrics focused on completion progress."""
    total_tasks: int
    completed_tasks: int
    completion_rate: float


class TaskLogResponse(BaseModel):
    """Response returned when a task is logged."""
    message: str
    task_id: int


class TaskStatusResponse(BaseModel):
    """Response returned when querying a task status."""
    task_id: int
    status: TaskStatus