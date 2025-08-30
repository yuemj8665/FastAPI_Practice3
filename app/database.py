# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# 접속 할 데이터베이스 설정
DATABASE_URL = settings.DATABASE_URL
# 엔진 생성
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# ORM 모델의 부모클래스
Base = declarative_base()

# API 요청마다 세션을 생성하고 요청으 끝나면 닫는 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()