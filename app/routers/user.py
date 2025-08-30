from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from .. import crud, schemas, models
from ..database import get_db
from ..security import verify_password, create_access_token, get_current_user
from starlette import status

router = APIRouter(
    prefix="/users",
    tags=["user"]
)
# 전체 사용자 확인용 API 엔드포인트
@router.get("/all", response_model=list[schemas.user.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users

# 사용자 생성 API 엔드포인트
@router.post("/", response_model=schemas.user.User)
def create_user_endpoint(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    # crud.get_user_by_email 함수를 사용해 이미 이메일이 등록되어있는지 확인
    db_user = crud.user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # 버그 수정: 자기 자신을 호출하는 대신 crud.create_user를 호출
    return crud.user.create_user(db=db, user=user)

# 특정 사용자 조회 API 엔드포인트
@router.get("/{user_id}", response_model=schemas.user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    # 버그 수정: user_id로 사용자를 조회하도록 crud.get_user 호출
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 특정 사용자 삭제 API 엔드포인트
@router.delete("/{user_id}", response_model=schemas.user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    # 버그 수정: user_id로 사용자를 조회하도록 crud.get_user 호출
    delete_user = crud.user.delete_user(db, user_id=user_id)
    if delete_user is None:
        # 삭제 할 유저가 없다면 404
        raise HTTPException(status_code=404, detail="User not found")
    return delete_user

# "나"의 정보를 가져오는 보호된 엔드포인트를 추가한다.
@router.get("/me/", response_model=schemas.user.User)
def read_user_me(current_user: schemas.user = Depends(get_current_user)):
    # get_current_user 의존성은 요청 헤더의 토큰을 검증하고,
    # 유효하다면 해당 사용자 정보를 current_user에 넣는다
    # 토큰이 유효하지 않다면 401 에러를 발생시킬것이다.
    return current_user