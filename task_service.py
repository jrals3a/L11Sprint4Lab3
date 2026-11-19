# app/services/task_service.py
from typing import Any

from app.repositories.base import ITaskRepository


class TaskService:
    """Service layer for task management operations.

    Depends on ITaskRepository — not any specific storage implementation.
    TaskService does not know whether the backend is a file, a database,
    or a test double. It only knows it has an ITaskRepository.

    Inject via create_app():
        create_app()              → FileTaskRepository (default)
        create_app(use_db=True)   → DatabaseTaskRepository (Sprint 4 Lab 2)
        create_app(service=mock)  → mocker.MagicMock() (tests)
    """

    def __init__(self, repository: ITaskRepository) -> None:
        self._repository = repository

    def get_all_tasks(self) -> list[dict[str, Any]]:
        """Return all tasks as dicts (for JSON serialization)."""
        return self._repository.get_all_tasks()

    def get_tasks(self) -> list[dict[str, Any]]:
        """Alias for get_all_tasks() — retained for US003 compatibility."""
        return self.get_all_tasks()

    def add_task(self, title: str, description: str = "") -> dict[str, Any]:
        """Add a new task."""
        if not title or not str(title).strip():
            raise ValueError("Title cannot be empty")
        return self._repository.add_task(title, description)

    def complete_task(self, task_id: int) -> dict[str, Any] | None:
        """Mark a task as completed."""
        return self._repository.complete_task(task_id)

    def delete_task(self, task_id: int) -> dict[str, Any] | None:
        """Delete a task from the system."""
        return self._repository.delete_task(task_id)

    def clear_tasks(self) -> None:
        """Clear all tasks — used by /api/tasks/reset."""
        self._repository.clear_tasks()
