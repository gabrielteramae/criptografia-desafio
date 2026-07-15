from sqlalchemy.orm import Session
from app import models, schemas


def create_entity(db: Session, entity: schemas.EntityCreate) -> models.Entity:
    db_entity = models.Entity(**entity.model_dump())
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity


def get_entity(db: Session, entity_id: int) -> models.Entity | None:
    return db.query(models.Entity).filter(models.Entity.id == entity_id).first()


def get_entities(db: Session, skip: int = 0, limit: int = 100) -> list[models.Entity]:
    return db.query(models.Entity).offset(skip).limit(limit).all()


def update_entity(db: Session, entity_id: int, entity: schemas.EntityUpdate) -> models.Entity | None:
    db_entity = get_entity(db, entity_id)
    if db_entity is None:
        return None
    for field, value in entity.model_dump().items():
        setattr(db_entity, field, value)
    db.commit()
    db.refresh(db_entity)
    return db_entity


def delete_entity(db: Session, entity_id: int) -> bool:
    db_entity = get_entity(db, entity_id)
    if db_entity is None:
        return False
    db.delete(db_entity)
    db.commit()
    return True
