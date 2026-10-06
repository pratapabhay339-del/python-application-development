from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError


Status = Literal["pending", "in_progress", "completed"]


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=100)


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)
    status: Status = "pending"
    priority: int = Field(default=3, ge=1, le=5)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    status: Status | None = None
    priority: int | None = Field(default=None, ge=1, le=5)


def validate(model, payload):
    try:
        return model.model_validate(payload), None
    except ValidationError as exc:
        return None, exc.errors()
