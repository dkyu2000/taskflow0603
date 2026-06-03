"""SQLite 데이터베이스 연결 및 세션 설정 모듈."""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# 프로젝트 루트가 아닌 backend/ 안에 SQLite 파일을 생성한다.
SQLALCHEMY_DATABASE_URL = "sqlite:///./taskflow.db"

# check_same_thread=False: FastAPI 는 여러 스레드에서 같은 연결을 사용할 수 있다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """모든 ORM 모델의 베이스 클래스."""


def get_db() -> Generator[Session, None, None]:
    """요청마다 DB 세션을 생성하고 종료 시 닫는 의존성."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
