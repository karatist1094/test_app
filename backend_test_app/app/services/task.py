from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.task import TaskRepository
from app.schemas.task import TaskReadSchema, TaskCreateSchema, TaskUpdateSchema


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskRepository(db)

    def list_tasks(self) -> List[TaskReadSchema]:
        tasks_orm = self.task_repository.get_all()
        return [TaskReadSchema.model_validate(task) for task in tasks_orm]

    def create_task(self, task_create: TaskCreateSchema) -> TaskReadSchema:
        try:
            task_orm = self.task_repository.create(title=task_create.title)
        except:
            raise HTTPException(status_code=404, detail="Task not found")

        self.db.commit()
        return TaskReadSchema.model_validate(task_orm)

    def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskReadSchema:
        task_for_update = self.task_repository.get_by_id(task_id)
        if task_for_update is None:
            raise HTTPException(status_code=404, detail="Task not found")

        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed

        self.db.commit()
        return TaskReadSchema.model_validate(task_for_update)

    def delete_task(self, task_id: str) -> None:
        if not self.task_repository.delete(task_id):
            raise HTTPException(status_code=404, detail="Task not found")
