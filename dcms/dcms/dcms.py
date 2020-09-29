from typing import Optional, List
import os
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.responses import RedirectResponse
from starlette_authlib.middleware import AuthlibMiddleware as SessionMiddleware
from sqlalchemy.orm import Session
from starlette.requests import Request
import logging
import string
import random

from dcms import crud
from dcms import schemas
from dcms import client

from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

config = Config()

logger = logging.getLogger(__name__)

oauth = OAuth(config=config)

oauth.register(name='discord',
               access_token_url='https://discord.com/api/oauth2/token',
               authorize_url='https://discord.com/api/oauth2/authorize',
               api_base_url='https://discord.com/api/',
               client_kwargs={'scope': 'identify guilds'})

RANDOM_ID_LENGTH = 12
RANDOM_ID_CHARS = string.ascii_letters


def _random_id():
    return "".join(
        random.choice(RANDOM_ID_CHARS) for i in range(RANDOM_ID_LENGTH))


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=_random_id())


# Dependency
def get_db():
    db = crud.SessionLocal()
    try:
        yield db
    finally:
        db.close()


crud.models.Base.metadata.create_all(bind=crud.engine)


@app.get("/login", tags=["auth"])
async def login_via_discord(request: Request):
    redirect_uri = request.url_for('auth_via_discord')
    return await oauth.discord.authorize_redirect(request, redirect_uri)


@app.get("/auth", tags=["auth"])
async def auth_via_discord(request: Request, db: Session = Depends(get_db)):
    token = await oauth.discord.authorize_access_token(request)
    logger.warning(token)
    logger.warning(type(token))
    resp = await oauth.discord.get('users/@me', token=token)
    user_json = resp.json()
    user = crud.User.get_or_create(db, id=user_json['id'])
    user.update(**user_json)
    user_token = crud.Token.create(db, **token)
    user.token = user_token
    request.session.update({"user": user_json['id']})
    db.commit()
    return crud.User.get(db, id=user_json['id'])


@app.get("/bot")
async def get_bot_guilds():
    return await client.guilds()


@app.get("/guilds")
async def get_user_guilds(request: Request, db: Session = Depends(get_db)):
    if (user_id := request.session.get('user')):
        user = crud.User.get(db, id=user_id)
        resp = await oauth.discord.get('users/@me/guilds',
                                       token=user.token.to_token())
        return resp.json()
    else:
        return RedirectResponse(request.url_for('login_via_discord'))


@app.get("/messages", tags=["messages"])
def list_messages(db: Session = Depends(get_db)) -> List[schemas.Message]:
    return crud.Message.list(db)


@app.get("/messages/{id}", tags=["messages"])
def get_message(id: int,
                response_model: Optional[schemas.Message],
                db: Session = Depends(get_db)):
    return crud.Message.get(db, id=id)
