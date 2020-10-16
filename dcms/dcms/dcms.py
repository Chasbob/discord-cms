import logging
import os
import random
import string
import sys
from datetime import datetime, timedelta
from typing import List, Optional

from authlib.integrations.starlette_client import OAuth
from fastapi import Depends, FastAPI, Header, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_contrib.pagination import Pagination
from fastapi_contrib.serializers.common import ModelSerializer
from sqlalchemy.orm import Session
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from orm import crud

from dcms import schemas


config = Config()

logger = logging.getLogger(__name__)
oauth = OAuth(config=config)

oauth.register(name='discord',
               access_token_url='https://discord.com/api/oauth2/token',
               authorize_url='https://discord.com/api/oauth2/authorize',
               api_base_url='https://discord.com/api/',
               client_kwargs={'scope': 'identify guilds'})


def _random_id():
    return "".join(random.choice(string.ascii_letters) for i in range(12))


hostname = os.getenv("DOMAINNAME")

app = FastAPI(root_path=os.getenv('API_ROOT_PATH', '/'))
app.add_middleware(SessionMiddleware, secret_key=_random_id())

origins = [
    f"http://{hostname}",
    f"https://{hostname}",
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   expose_headers=["Content-Range", "Content-Lenght"])


def remove_prefix(text):
    if text.startswith("Bearer "):
        return text[len("Bearer "):]


# Dependency
def get_db():
    db = crud.SessionLocal()
    try:
        yield db
    finally:
        db.close()


crud.models.Base.metadata.create_all(bind=crud.engine)


@app.get("/me", tags=["auth"])
async def check_auth(request: Request,
                     db: Session = Depends(get_db),
                     authorization: Optional[str] = Header(None)):
    if authorization:
        user_token = crud.Token.get(db,
                                    access_token=remove_prefix(authorization))
        if user_token:
            user = crud.User.get(db, id=user_token.user_id)
            return user
        else:
            return Response(status_code=401)


@app.get("/login", tags=["auth"])
async def login_via_discord(request: Request):
    redirect_uri = request.url_for('auth_via_discord')
    return await oauth.discord.authorize_redirect(request, redirect_uri)


@app.get("/auth", tags=["auth"])
async def auth_via_discord(
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
):
    token = await oauth.discord.authorize_access_token(request)
    resp = await oauth.discord.get('users/@me', token=token)
    user_json = resp.json()
    user = crud.User.get_or_create(db, id=user_json['id'])
    user.update(**user_json)
    user_token = crud.Token.get_or_create(db, user_id=user.id)
    user_token.update(**token)
    user.token = user_token
    db.commit()
    user = crud.User.get(db, id=user_json['id'])
    token = crud.Token.get(db, user_id=user.id)
    return RedirectResponse(
        f"https://{hostname}?token={token.to_token()['access_token']}")


@app.post("/code-to-token", tags=["auth"])
def get_token_from_code():
    return {}


@app.get("/guilds")
async def get_user_guilds(
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
        authorization: Optional[str] = Header(None),
):
    logger.warning(f"guilds => token={authorization}")
    if authorization:
        user_token = crud.Token.get(db,
                                    access_token=remove_prefix(authorization))
        if user_token:
            guilds = crud.Guild.list(db)
            response.headers['Content-Range'] = f'0-9/{len(guilds)}'
            return guilds
        else:
            return Response(status_code=401)
    return Response(status_code=403)


@app.get("/messages", tags=["messages"])
def list_messages(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
) -> List[schemas.Message]:
    if authorization:
        user_token = crud.Token.get(db,
                                    access_token=remove_prefix(authorization))
        if user_token:
            messages = crud.Message.list(db, user=user_token.user)
            response.headers['Content-Range'] = f'0-9/{len(messages)}'
            return messages
    return Response(status_code=403)


@app.get("/messages/{msg_id}", tags=["messages"])
def get_message(msg_id: str,
                db: Session = Depends(get_db),
                authorization: Optional[str] = Header(None)):
    if authorization:
        user_token = crud.Token.get(db,
                                    access_token=remove_prefix(authorization))
        if user_token:
            msg = crud.Message.get(db, id=msg_id, user_id=user_token.user_id)
            return msg
        return Response(status_code=401)
    return Response(status_code=403)


@app.put("/messages/{msg_id}", tags=["messages"])
async def put_message(*,
                      msg_id: str,
                      message: schemas.Message,
                      db: Session = Depends(get_db),
                      authorization: Optional[str] = Header(None)):
    if authorization:
        user_token = crud.Token.get(db,
                                    access_token=remove_prefix(authorization))
        if user_token:
            msg = crud.Message.get(db, id=msg_id, user_id=user_token.user_id)
            msg.update(**dict(message))
            db.commit()
            return crud.Message.get(db, id=msg_id)
