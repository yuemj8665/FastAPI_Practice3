from fastapi import FastAPI
from .routers import user, auth
from .database import engine, Base



# models.Base.metadata.create_all(bind=engine)는 데이터 베이스에 필요한 모든 테이블을 생성한다.
# SQLAlchemy 모델을 기반으로 작동한다.
Base.metadata.create_all(bind=engine)
# FastAPI 애플리케이션 인스턴스
app = FastAPI()

# user.py에서 정의한 router를 메인 앱에 포함시킨다.
# 이제 /users로 시작하는 모든 요청은 user.router가 처리한다.
app.include_router(user.router)
app.include_router(auth.router)

#최상위 경로에 대한 간단한 GET 엔드포인트
@app.get("/")
def root():
    return {"message": "Hello World"}
