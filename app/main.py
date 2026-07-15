from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Crypto Transparent API",
    description="CRUD com criptografia transparente de campos sensiveis (AES via Fernet)",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"status": "ok", "service": "crypto-transparent-api"}


@app.post("/entities", response_model=schemas.EntityRead, status_code=201)
def create_entity(entity: schemas.EntityCreate, db: Session = Depends(get_db)):
    return crud.create_entity(db, entity)


@app.get("/entities", response_model=list[schemas.EntityRead])
def list_entities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_entities(db, skip, limit)


@app.get("/entities/{entity_id}", response_model=schemas.EntityRead)
def read_entity(entity_id: int, db: Session = Depends(get_db)):
    db_entity = crud.get_entity(db, entity_id)
    if db_entity is None:
        raise HTTPException(status_code=404, detail="Entity not found")
    return db_entity


@app.put("/entities/{entity_id}", response_model=schemas.EntityRead)
def update_entity(entity_id: int, entity: schemas.EntityUpdate, db: Session = Depends(get_db)):
    db_entity = crud.update_entity(db, entity_id, entity)
    if db_entity is None:
        raise HTTPException(status_code=404, detail="Entity not found")
    return db_entity


@app.delete("/entities/{entity_id}", status_code=204)
def delete_entity(entity_id: int, db: Session = Depends(get_db)):
    if not crud.delete_entity(db, entity_id):
        raise HTTPException(status_code=404, detail="Entity not found")
