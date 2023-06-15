from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import models, schemas

def create_gradient(db: Session, gradient: schemas.GradientCreate):
    db_gradient = models.Gradient(gradient = gradient.gradient)
    db.add(db_gradient)
    db.commit()
    db.refresh(db_gradient)
    return db_gradient

def get_gradients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Gradient).offset(skip).limit(limit).all()

def get_random_gradient(db: Session):
    return db.query(models.Gradient).order_by(func.random()).first()
