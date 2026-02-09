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
from app.services.task_service import (
    create_task,
    get_tasks,
    update_task,
    delete_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("")
async def task_create(
    payload: TaskCreateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    
    created_task = create_task(
        db = db,
        current_user = current_user,
        title = payload.title,
        description = payload.description,
    )
    
    return success_response(data = TaskResponse.model_validate(created_task).model_dump(mode="json")
                            , message = "Task created successfully."
                            , status_code = status.HTTP_201_CREATED)


@router.get("")
async def list_tasks(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_tasks = get_tasks(db = db, current_user = current_user)
    
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
    
    try:
        updated_task = update_task( db = db,
                                    task_id = task_id,
                                    current_user = current_user,
                                    title = payload.title,
                                    description = payload.description,
                                    status_value = payload.status,
                                )
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
    delete_task(db = db, task_id = task_id, current_user = current_user)
    
    return success_response(message = "Task deleted successfully.", status_code = status.HTTP_200_OK)