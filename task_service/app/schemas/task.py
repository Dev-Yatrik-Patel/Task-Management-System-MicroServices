from pydantic import BaseModel, ConfigDict


class TaskCreateRequest(BaseModel):
    title: str
    description: str | None = None


class TaskUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str

    model_config = ConfigDict(from_attributes= True)