"""요청/응답에 사용하는 Pydantic 스키마."""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class StatusEnum(str, Enum):
    """업무 상태 값."""

    todo = "todo"
    doing = "doing"
    done = "done"


class PriorityEnum(str, Enum):
    """우선순위 값."""

    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    """업무 생성 요청 본문."""

    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    priority: PriorityEnum = PriorityEnum.medium


class TaskUpdate(BaseModel):
    """업무 수정 요청 본문. 전달된 필드만 변경한다."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: StatusEnum | None = None
    priority: PriorityEnum | None = None


class TaskStatusUpdate(BaseModel):
    """상태만 변경할 때 쓰는 요청 본문."""

    status: StatusEnum


class TaskOut(BaseModel):
    """업무 응답 스키마."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: StatusEnum
    priority: PriorityEnum
    created_at: datetime
    updated_at: datetime
