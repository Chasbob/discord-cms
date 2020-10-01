import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dcms.crud.base import make_crud

from dcms.crud import models

User = make_crud(models.User)
Message = make_crud(models.Message)
Token = make_crud(models.Token)
Guild = make_crud(models.Guild)

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()