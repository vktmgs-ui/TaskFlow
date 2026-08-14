from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class ProjectCreate(BaseModel):
    name: str
    owner_id: int


class TaskCreate(BaseModel):
    title: str
    priority: str = Field(
        ...,
        pattern="^(low|medium|high)$"
    )
    due_date: str | None = None
    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be blank")

        return value
class TaskUpdate(BaseModel):
    title: str
    priority: str = Field(
        ...,
        pattern="^(low|medium|high)$"
    )
    due_date: str | None = None
    completed: bool = False

class QuickAddRequest(BaseModel):
    description: str
    project_id: int