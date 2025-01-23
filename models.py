from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()
class User(Base):

    __tablename__= "user"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(50), index=True)
    age: int = Column(Integer, nullable = True)
    email: str = Column(String(50), unique=True, index=True)
    password: str = Column(String(50))