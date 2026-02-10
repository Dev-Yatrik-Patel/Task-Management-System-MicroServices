from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.task import Task

class TaskService:
    
    def __init__(self, db: Session, current_user: dict):
        self.db = db
        self.current_user = current_user
        self.valid_status = {"pending", "completed"}
        
    def get_tasks(self):
        auth_user_id = self.current_user["auth_user_id"]
        return self.db.query(Task).filter(Task.auth_user_id == auth_user_id).all()

    def create_task(self, title: str, description: str | None):
        
        auth_user_id = self.current_user["auth_user_id"]
        
        task = Task(
            title=title,
            description=description,
            auth_user_id=auth_user_id,
        )
        
        self.db.add(task)    
        self.db.commit()
        self.db.refresh(task)
        
        return task


    def get_task_by_id(self, task_id: int) -> Task:
        
        auth_user_id = self.current_user["auth_user_id"]
        
        task = self.db.query(Task).filter(Task.id == task_id).first()

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

    def update_task(self, task_id: int, title: str | None, description: str | None, status_value: str | None ):
        
        task = self.get_task_by_id(task_id = task_id)

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status_value is not None:
            if status_value not in self.valid_status:
                raise ValueError("Invalid task status")
            task.status = status_value

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: int):
        task = self.get_task_by_id(task_id = task_id)
        self.db.delete(task)
        self.db.commit()