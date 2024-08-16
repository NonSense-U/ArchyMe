from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}'

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
except Exception as e:
    print(f"Failed to create engine: {e}")
    raise

try:
    session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)
except Exception as e:
    print(f"Failed to create session maker: {e}")
    raise


Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()