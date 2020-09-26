from .base import make_crud

from .. import models

User = make_crud(models.User)
Post = make_crud(models.Post)
