from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship

from .database import Base
from sqlalchemy.sql.schema import CheckConstraint


class Guild(Base):
    __tablename__ = "guild"

    id = Column(String, primary_key=True)
    name = Column(String)
    messages = relationship("Message", back_populates="guild")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    username = Column(String)
    discriminator = Column(String)
    messages = relationship("Message", back_populates="user")
    token = relationship("Token", uselist=False, back_populates="user")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Message(Base):
    __tablename__ = "message"

    id = Column(String, primary_key=True)
    name = Column(String, unique=False)
    channel = Column(String, unique=False, index=True)
    content = Column(String)
    user = relationship("User")
    user_id = Column(String, ForeignKey("user.id"))
    guild_id = Column(String, ForeignKey("guild.id"))
    guild = relationship("Guild", back_populates="messages")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True)
    token_type = Column(String(length=40))
    access_token = Column(String(length=200))
    refresh_token = Column(String(length=200))
    expires_at = Column('expires_at', Integer, CheckConstraint('expires_at>5'))
    user = relationship("User", back_populates="token")
    user_id = Column(String, ForeignKey("user.id"))

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )

    def __init__(self, **entries):

        # NOTE: Do not call superclass
        #       (which is otherwise a default behaviour).
        #super(User, self).__init__(**entries)

        self.__dict__.update(entries)
