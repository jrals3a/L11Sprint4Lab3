# app/repositories/database_task_repository.py
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models.sqlalchemy_task import Base, SQLAlchemyTask
from app.repositories.base import ITaskRepository


class DatabaseTaskRepository(ITaskRepository):
    """SQLAlchemy-backed task repository.

    Implements ITaskRepository using SQLite via SQLAlchemy ORM.
    TaskService cannot tell the difference between this and FileTaskRepository
    — both satisfy the same interface.

    Database path is controlled via db_url:
        Production:  sqlite:///tasks.db
        Tests:       sqlite:///:memory:

    The :memory: URL creates a fresh in-memory database for each test —
    no file cleanup needed, no test isolation issues.
    """

    def __init__(self, db_url: str = "sqlite:///tasks.db") -> None:
        self._engine = create_engine(db_url)
        Base.metadata.create_all(self._engine)

    def add_task(self, title: str, description: str = "") -> dict[str, Any]:
        """Add a new task. Returns the created task as a dict."""
        if not title or not str(title).strip():
            raise ValueError("Title cannot be empty")
        with Session(self._engine) as session:
            task = SQLAlchemyTask(
                title=title,
                description=description if description is not None else "",
                completed=False,
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            return task.to_dict()

    def get_all_tasks(self) -> list[dict[str, Any]]:
        """Return all tasks as dicts."""
        with Session(self._engine) as session:
            tasks = session.query(SQLAlchemyTask).all()
            return [t.to_dict() for t in tasks]

    def complete_task(self, task_id: int) -> dict[str, Any] | None:
        """Mark a task complete. Returns updated task or None."""
        with Session(self._engine) as session:
            task = session.get(SQLAlchemyTask, task_id)
            if task is None:
                return None
            task.completed = True  # SQLAlchemyTask is an ORM model, not a domain model
            session.commit()       # mark_complete() lives on Task — not SQLAlchemyTask
            session.refresh(task)
            return task.to_dict()

    def delete_task(self, task_id: int) -> dict[str, Any] | None:
        """Delete a task. Returns deleted task or None."""
        with Session(self._engine) as session:
            task = session.get(SQLAlchemyTask, task_id)
            if task is None:
                return None
            result = task.to_dict()
            session.delete(task)
            session.commit()
            return result

    def clear_tasks(self) -> None:
        """Remove all tasks."""
        with Session(self._engine) as session:
            session.query(SQLAlchemyTask).delete()
            session.commit()
