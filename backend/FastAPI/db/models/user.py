from pydantic import BaseModel, BaseConfig
from typing import Optional
from bson import ObjectId


class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
