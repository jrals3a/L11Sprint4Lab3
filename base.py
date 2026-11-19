# app/repositories/base.py
from abc import ABC, abstractmethod
from typing import Any


class ITaskRepository(ABC):
    """Interface contract for all task repository implementations.

    Any class that implements this interface can be injected into TaskService.
    TaskService does not know or care whether the backend is a file, a database,
    or a test double — it only knows it has an ITaskRepository.

    Implementations:
        FileTaskRepository  — wraps TaskStorage (file I/O)
        DatabaseTaskRepository — SQLAlchemy (Sprint 4 Lab 2)
    """

    @abstractmethod
    def add_task(self, title: str, description: str = "") -> dict[str, Any]:
        """Add a new task. Returns the created task as a dict."""
        ...

    @abstractmethod
    def get_all_tasks(self) -> list[dict[str, Any]]:
        """Return all tasks as a list of dicts."""
        ...

    @abstractmethod
    def complete_task(self, task_id: int) -> dict[str, Any] | None:
        """Mark a task complete. Returns updated task dict or None if not found."""
        ...

    @abstractmethod
    def delete_task(self, task_id: int) -> dict[str, Any] | None:
        """Delete a task. Returns deleted task dict or None if not found."""
        ...

    @abstractmethod
    def clear_tasks(self) -> None:
        """Remove all tasks. Used by the /api/tasks/reset endpoint."""
        ...
