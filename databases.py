from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os

engine = create_engine('postgresql://postgres:postgres@localhost/pizza_delivery')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()