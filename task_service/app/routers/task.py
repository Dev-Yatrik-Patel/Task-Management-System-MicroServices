from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.core.responses import success_response
from app.schemas.task import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse,
)
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("")
async def task_create(
    payload: TaskCreateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TaskService(db,current_user)
    created_task = service.create_task(title = payload.title, description = payload.description)
    
    return success_response(data = TaskResponse.model_validate(created_task).model_dump(mode="json")
                            , message = "Task created successfully."
                            , status_code = status.HTTP_201_CREATED)


@router.get("")
async def list_tasks(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TaskService(db,current_user)
    user_tasks = service.get_tasks()
    
    data = [TaskResponse.model_validate(i).model_dump(mode="json")  for i in user_tasks]
    
    return success_response(data = data
                            , message = "Tasks fetched successfully."
                            , status_code = status.HTTP_200_OK)


@router.put("/{task_id}")
async def task_update(
    task_id: int,
    payload: TaskUpdateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TaskService(db,current_user)
    try:
        updated_task = service.update_task(task_id = task_id, title = payload.title, description = payload.description, status_value = payload.status)
        return success_response(data = TaskResponse.model_validate(updated_task).model_dump(mode="json")
                            , message = "Task updated successfully."
                            , status_code = status.HTTP_200_OK)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.delete("/{task_id}")
async def task_delete(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TaskService(db,current_user)
    service.delete_task(task_id = task_id)
    
    return success_response(message = "Task deleted successfully.", status_code = status.HTTP_200_OK)