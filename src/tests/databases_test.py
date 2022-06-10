from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Base

TEST_DB_URL = 'sqlite:///./test_db'

test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()