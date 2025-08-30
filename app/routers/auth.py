from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.security import verify_password, create_access_token

from app.database import get_db
from app import crud, schemas


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# 토큰 발급 엔드포인트
@router.post("/token", response_model=schemas.user.Token)
def login_for_access_token(db:Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # DB에서 받은 데이터로 사용자 정보 조회
    user = crud.user.get_user_by_email(db, email=form_data.username)
    # 유저가 없거나 패스워드 틀리다면 Expcetion
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 성공하면 액세스 토큰을 생성한다
    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}
