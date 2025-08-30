from datetime import timedelta, datetime, timezone
from typing import Union

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from . import schemas, models
from .config import settings
from .database import get_db

# 비밀번호 해싱을 위한 CryptContext 객체 생성
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 토큰을 자동으로 찾아주는 의존성 객체
# tokenURL은 토큰을 얻기위해 클라이언트가 요청을 보내야하는 경로
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# 비밀번호 검증 함수
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 비밀번호 해싱 함수
def get_password_hash(password):
    return pwd_context.hash(password)

# 액세스 토큰 생성 함수
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    # 받은 데이터를 우선 복사
    to_encode = data.copy()
    # 만료시간이 있다면 그냥 지금시간으로 넣기
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else : # 없다면 15분으로 넣는다
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    # 페이로드에 만료시간을 넣는다.
    to_encode.update({"exp" : expire})
    # 최종적으로 JWT를 인코딩하여 생성한다
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

# 현재 사용자를 가져오는 의존성 함수 (가장 중요)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # 인증 실패 시 발생시킬 표준 예외 객체 정의
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        # 클라이언트로부터 받은 토큰을 비밀키를 사용해 디코딩
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # 디코딩된 페이로드에서 'sub'(subject, 여기서는 이메일)값을 추출한다.
        email :str = payload.get("sub")
        # 만약 이메일 정보가 없다면
        if email is None:
            raise credentials_exception
        token_data = schemas.user.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    # 토큰이 유효하다면 페이로드의 이메일 정보로 DB의 실제 사용자를 조회한다
    user = db.query(models.user.User).filter(models.user.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user