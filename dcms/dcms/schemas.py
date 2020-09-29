from typing import List

from pydantic import BaseModel


class Message(BaseModel):
    name: str
    channel: str
    message: str

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    discriminator: str
    projects: List[Message]

    class Config:
        orm_mode = True
