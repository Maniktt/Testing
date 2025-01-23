from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from app.models import Base
from app.config import DBConfig


engine = create_engine(DBConfig.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


        # Create the tables
        Base.metadata.create_all(bind=engine)
        """
        Base.metadata.create_all() will automatically generate all the tables that are defined 
        by SQLAlchemy models (like your User model) in your database.
        bind=engine tells SQLAlchemy to use the provided database engine (engine) to 
        execute the SQL statements that create the tables.
        """
