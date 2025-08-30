# app/crud/user.py
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..security import get_password_hash

from app import schemas, models

# 비밀번호 해싱을 위한 CryptContext 객체 생성
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ID로 특정 유저를 조회하는 함수
def get_user(db: Session, user_id: int):
    # db.query로 조회할 테이블 모델을 지정한다. filter로는 조건을 지정한다.
    # .first는 그 조회한 결과 중 제일 첫번째 결과를 반환한다. 없으면 None을 반환한다.
    return db.query(models.user.User).filter(models.user.User.id == user_id).first()

# 이메일로 특정 유저를 조회하는 함수
def get_user_by_email(db: Session, email: str):
    return db.query(models.user.User).filter(models.user.User.email == email).first()

# 특정 범위의 유저 목록을 조회하는 함수 ( 예: 페이지네이션)
def get_users(db: Session, skip: int = 0, limit: int = 100):
    # .offset(skip)은 건너 뛸 row의 수, limit(limit)는 가져올 row의 수
    return db.query(models.user.User).offset(skip).limit(limit).all()

# 유저를 생성하는 함수
def create_user(db:Session, user:schemas.user.UserCreate):
    # 입력받은 비밀번호를 bcrypt 알고리즘을 통해 해싱한다.
    password = pwd_context.hash(user.password)
    # 입력받은 비밀번호를 해싱한다.
    hashed_password = get_password_hash(user.password)

    # 해싱된 비밀번호를 저장한다
    db_user = models.user.User(email=user.email, hashed_password=hashed_password)

    # SQLAlchemy 모델 객체를 생성한다
    # db_user = models.User(email=user.email, hashed_password=password)

    # 세션에 객체를 추가한다
    db.add(db_user)

    # 변경사항을 커밋한다
    db.commit()

    # DB에 저장된 객체의 최신 상태를 반영한다.
    db.refresh(db_user)

    # dbuser를 반환한다.
    return db_user

# 유저를 삭제하는 함수
def delete_user(db:Session, user_id:int):
    db_user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
    # 세션에 객체를 삭제
    if db_user:
        db.delete(db_user)
        # 변경사항을 커밋한다
        db.commit()

    # dbuser를 반환한다.
    return db_user