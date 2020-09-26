from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship
import string
import random

from .database import Base

RANDOM_ID_LENGTH = 12
RANDOM_ID_CHARS = string.ascii_letters


def _random_id():
    return "".join(
        random.choice(RANDOM_ID_CHARS) for i in range(RANDOM_ID_LENGTH))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)
    projects = relationship("Post", back_populates="user", lazy="dynamic")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    channel = Column(String, unique=False, index=True)
    message = Column(String, unique=True, index=True)
    user = Column(Integer, ForeignKey('users'))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="projects")
