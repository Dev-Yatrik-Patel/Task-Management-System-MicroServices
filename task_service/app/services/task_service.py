from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.task import Task

VALID_STATUSES = {"pending", "completed"}

def create_task(db: Session, current_user: dict, title: str, description: str | None):
    
    auth_user_id = current_user["auth_user_id"]
    
    task = Task(
        title=title,
        description=description,
        auth_user_id=auth_user_id,
    )
    
    db.add(task)    
    db.commit()
    db.refresh(task)
    
    return task

def get_tasks(db: Session, current_user: int):
    auth_user_id = current_user["auth_user_id"]
    return db.query(Task).filter(Task.auth_user_id == auth_user_id).all()


def get_task_by_id(db: Session, current_user: dict, task_id: int) -> Task:
    
    auth_user_id = current_user["auth_user_id"]
    
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if task.auth_user_id != auth_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task",
        )

    return task

def update_task(
    db: Session,
    task_id: int,
    current_user: dict,
    title: str | None,
    description: str | None,
    status_value: str | None,
):
    
    task = get_task_by_id(db = db, task_id = task_id, current_user = current_user)

    if title is not None:
        task.title = title
    if description is not None:
        if description not in VALID_STATUSES:
            raise ValueError("Invalid task status")
        task.description = description
    if status_value is not None:
        task.status = status_value

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, current_user: dict, task_id: int):
    task = get_task_by_id(db = db, task_id = task_id, current_user = current_user)
    db.delete(task)
    db.commit()