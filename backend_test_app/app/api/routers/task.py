from fastapi import APIRouter, Depends
from fastapi import status
from typing import List
from app.api.dependencies import get_task_service
from app.schemas.task import TaskUpdateSchema, TaskCreateSchema, TaskReadSchema
from app.services.task import TaskService

router = APIRouter(prefix="/tasks", tags=["task"])

@router.get("")
def read_tasks(task_service: TaskService = Depends(get_task_service)) -> List[TaskReadSchema]:
    return task_service.list_tasks()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
        payload: TaskCreateSchema, task_service: TaskService = Depends(get_task_service)) -> TaskReadSchema:
    return task_service.create_task(payload)

@router.patch("/{task_id}")
def update_task(
        task_id: str, payload: TaskUpdateSchema,
        task_service: TaskService = Depends(get_task_service)) -> TaskReadSchema:
    return task_service.update_task(task_id, payload)


@router.delete("/{task_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, task_service: TaskService = Depends(get_task_service)) -> None:
    task_service.delete_task(task_id)