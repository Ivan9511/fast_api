from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import json
from database import engine, Base, get_db
from models import Source, SourceCreate, SourceUpdate, SourceResponse, Config

app = FastAPI()

# Создание таблицы в базе данных, если она еще не создана
Base.metadata.create_all(bind=engine)

@app.get("/get/source")
def get_source(db: Session = Depends(get_db)):    
    sources = db.query(Source).all()
    return sources

@app.post("/post/source", response_model=SourceResponse)
def post_source(source: SourceCreate, db: Session = Depends(get_db)):
    source_data = Source(
        name=source.name,
        url=source.url,
        config=json.dumps(source.config.dict())
    )
    db.add(source_data)
    db.commit()
    db.refresh(source_data)
    return SourceResponse(
        id=source_data.id,
        name=source_data.name,
        url=source_data.url,
        config=json.loads(source_data.config)
    )

@app.get("/get/source/{id}", response_model=SourceResponse)
def get_source_by_id(id: int, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == id).first()
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    source.config = json.loads(source.config)
    return source

@app.get("/get/source/by-url", response_model=SourceResponse)
def get_source_by_url(url: str, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.url == url).first()
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    source.config = json.loads(source.config)
    return source

@app.put("/put/source/{id}", response_model=SourceResponse)
def update_source(id: int, source: SourceUpdate, db: Session = Depends(get_db)):
    source_data = db.query(Source).filter(Source.id == id).first()
    if source_data is None:
        raise HTTPException(status_code=404, detail="Source not found")
    
    if source.name is not None:
        source_data.name = source.name
    if source.url is not None:
        source_data.url = source.url
    if source.config is not None:
        source_data.config = json.dumps(source.config.dict())
    
    db.commit()
    db.refresh(source_data)
    source_data.config = json.loads(source_data.config)
    return source_data

@app.delete("/delete/source/{id}", response_model=SourceResponse)
def delete_source(id: int, db: Session = Depends(get_db)):
    source_data = db.query(Source).filter(Source.id == id).first()
    if source_data is None:
        raise HTTPException(status_code=404, detail="Source not found")
    
    db.delete(source_data)
    db.commit()
    source_data.config = json.loads(source_data.config)
    return source_data

# uvicorn main:app --reload