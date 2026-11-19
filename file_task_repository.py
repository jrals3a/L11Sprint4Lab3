# app/repositories/file_task_repository.py
from typing import Any

from app.models.task import Task
from app.repositories.base import ITaskRepository
from app.services.task_storage import load_tasks, save_tasks


class FileTaskRepository(ITaskRepository):
    """File-backed task repository.

    Implements ITaskRepository by wrapping the existing load_tasks() and
    save_tasks() functions from task_storage.py.

    File I/O behavior is unchanged from Sprint 3 — this class is the bridge
    between the ITaskRepository interface and the existing storage functions.

    task_storage.py remains as the raw I/O layer; this class wraps it.
    """

    def __init__(self) -> None:
        self._tasks: list[Task] = []
        for t in load_tasks():
            self._tasks.append(
                Task(
                    id=t["id"],
                    title=t["title"],
                    description=t.get("description", ""),
                    completed=t.get("completed", False),
                )
            )

    def add_task(self, title: str, description: str = "") -> dict[str, Any]:
        """Add a new task with auto-incrementing ID."""
        if not title or not str(title).strip():
            raise ValueError("Title cannot be empty")
        next_id = max((task.id for task in self._tasks), default=0) + 1
        new_task = Task(
            id=next_id,
            title=title,
            description=description if description is not None else "",
        )
        self._tasks.append(new_task)
        save_tasks([t.to_dict() for t in self._tasks])
        return new_task.to_dict()

    def get_all_tasks(self) -> list[dict[str, Any]]:
        """Return all tasks as dicts."""
        return [t.to_dict() for t in self._tasks]

    def complete_task(self, task_id: int) -> dict[str, Any] | None:
        """Mark a task complete. Returns updated task or None."""
        for task in self._tasks:
            if task.id == task_id:
                task.mark_complete()
                save_tasks([t.to_dict() for t in self._tasks])
                return task.to_dict()
        return None

    def delete_task(self, task_id: int) -> dict[str, Any] | None:
        """Delete a task. Returns deleted task or None."""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                deleted = self._tasks.pop(i)
                save_tasks([t.to_dict() for t in self._tasks])
                return deleted.to_dict()
        return None

    def clear_tasks(self) -> None:
        """Remove all tasks."""
        self._tasks = []
        save_tasks([])
