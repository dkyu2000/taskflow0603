"""FastAPI 진입점. 업무 CRUD API 와 프론트엔드 정적 파일 서빙."""
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db

# 앱 시작 시 테이블을 생성한다(이미 있으면 무시).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow", description="업무 관리 앱 API")

# 개발 편의를 위해 모든 출처 허용(운영 시에는 제한 권장).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 프론트엔드 디렉터리 경로(backend/ 기준 ../frontend).
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


def get_task_or_404(task_id: int, db: Session) -> models.Task:
    """주어진 id 의 업무를 조회하고 없으면 404 를 던진다."""
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="업무를 찾을 수 없습니다.")
    return task


@app.get("/api/tasks", response_model=list[schemas.TaskOut])
def list_tasks(
    status_filter: schemas.StatusEnum | None = None,
    db: Session = Depends(get_db),
) -> list[models.Task]:
    """업무 목록 조회. status 쿼리로 상태별 필터링 가능."""
    query = select(models.Task).order_by(models.Task.created_at.desc())
    if status_filter is not None:
        query = query.where(models.Task.status == status_filter.value)
    return list(db.scalars(query).all())


@app.post("/api/tasks", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)) -> models.Task:
    """업무 추가."""
    task = models.Task(
        title=payload.title,
        description=payload.description,
        priority=payload.priority.value,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.get("/api/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)) -> models.Task:
    """업무 단건 조회."""
    return get_task_or_404(task_id, db)


@app.put("/api/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)
) -> models.Task:
    """업무 수정. 전달된 필드만 변경한다."""
    task = get_task_or_404(task_id, db)
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        # Enum 은 문자열 값으로 저장한다.
        setattr(task, field, value.value if hasattr(value, "value") else value)
    db.commit()
    db.refresh(task)
    return task


@app.patch("/api/tasks/{task_id}/status", response_model=schemas.TaskOut)
def change_status(
    task_id: int, payload: schemas.TaskStatusUpdate, db: Session = Depends(get_db)
) -> models.Task:
    """업무 상태 변경 전용 엔드포인트."""
    task = get_task_or_404(task_id, db)
    task.status = payload.status.value
    db.commit()
    db.refresh(task)
    return task


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    """업무 삭제."""
    task = get_task_or_404(task_id, db)
    db.delete(task)
    db.commit()


# 프론트엔드 정적 파일 서빙(API 라우트보다 뒤에 등록해야 한다).
if FRONTEND_DIR.exists():
    @app.get("/")
    def serve_index() -> FileResponse:
        """루트 접속 시 index.html 반환."""
        return FileResponse(FRONTEND_DIR / "index.html")

    app.mount("/", StaticFiles(directory=FRONTEND_DIR), name="static")
