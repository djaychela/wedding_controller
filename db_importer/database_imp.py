from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CTRL_SQLALCHEMY_DATABASE_URL = "sqlite:///../wedding_controller.db"

ctrl_engine = create_engine(
    CTRL_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

CtrlSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ctrl_engine)

CtrlBase=declarative_base()

DB_SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite3"

db_engine = create_engine(
    DB_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

DbSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

DbBase=declarative_base()