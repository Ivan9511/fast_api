from pydantic import BaseModel
from typing import Dict

class Config(BaseModel):
    rule: str
    next_page_rule: str
    title: str
    content: str
    date: str

class SourceCreate(BaseModel):
    name: str
    url: str
    config: Config

class SourceUpdate(BaseModel):
    name: str = None
    url: str = None
    config: Config = None

class SourceResponse(BaseModel):
    id: int
    name: str
    url: str
    config: dict[str, str]

    class Config:
        orm_mode = True
