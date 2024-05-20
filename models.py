from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Source(Base):
    __tablename__ = "source"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    config = Column(String)

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
    config: dict

    class Config:
        orm_mode = True
