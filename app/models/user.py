from sqlalchemy import Column, Integer, String
from ..database import Base

# User Model은 users 테이블과 매핑된다.
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)