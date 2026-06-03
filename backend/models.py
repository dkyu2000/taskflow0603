"""업무(Task) ORM 모델 정의."""
from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


def _now() -> datetime:
    """UTC 기준 현재 시각 반환."""
    return datetime.now(timezone.utc)


class Task(Base):
    """업무 한 건을 표현하는 테이블."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    # 업무 상태: todo(대기), doing(진행중), done(완료)
    status: Mapped[str] = mapped_column(String(20), default="todo", nullable=False)
    # 우선순위: low, medium, high
    priority: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_now, onupdate=_now)
