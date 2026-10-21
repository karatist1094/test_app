from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.task import TaskORM


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[TaskORM]:
        return list(self.db.scalars(select(TaskORM)).all())

    def get_by_id(self, task_id: str) -> TaskORM:
        task: TaskORM | None = self.db.get(TaskORM, task_id)
        return task

    def create(self, title: str) -> TaskORM:
        new_task = TaskORM(title=title, completed=False)
        self.db.add(new_task)
        return new_task

    def delete(self, task_id: str) -> bool:
        task = self.get_by_id(task_id)
        if task is None:
            return False
        self.db.delete(task)
        self.db.commit()
        return True
