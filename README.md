# TaskFlow · 업무 관리 앱

업무를 추가하고 상태를 관리하는 풀스택 웹 앱입니다.

- **백엔드**: FastAPI + SQLite (SQLAlchemy)
- **프론트엔드**: Vanilla JS + Tailwind (CDN)
- 모든 API는 `/api/` 경로 prefix를 사용합니다.

## 기능

- 업무 추가 (제목 + 우선순위)
- 업무 상태 변경: `대기(todo)` → `진행중(doing)` → `완료(done)`
- 업무 삭제
- 상태별 칸반 보드 보기

## 폴더 구조

```
taskflow/
├── backend/        FastAPI 서버
│   ├── main.py        앱 진입점 · 라우트 · 정적 파일 서빙
│   ├── database.py    SQLite 연결 / 세션
│   ├── models.py      Task ORM 모델
│   ├── schemas.py     Pydantic 스키마
│   └── requirements.txt
└── frontend/       정적 프론트엔드
    ├── index.html
    └── app.js
```

## 실행 방법

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

브라우저에서 http://127.0.0.1:8000 접속 — 백엔드가 프론트엔드 정적 파일을 함께 서빙합니다.
API 문서는 http://127.0.0.1:8000/docs 에서 확인할 수 있습니다.

> SQLite 파일(`backend/taskflow.db`)은 서버 최초 실행 시 자동 생성됩니다.

## API 요약

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/tasks` | 업무 목록 조회 (`?status_filter=todo` 등으로 필터) |
| POST | `/api/tasks` | 업무 추가 |
| GET | `/api/tasks/{id}` | 업무 단건 조회 |
| PUT | `/api/tasks/{id}` | 업무 수정 |
| PATCH | `/api/tasks/{id}/status` | 상태 변경 |
| DELETE | `/api/tasks/{id}` | 업무 삭제 |
