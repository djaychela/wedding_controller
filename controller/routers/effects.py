from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..crud import crud

from .. import schemas
from ..database import SessionLocal, engine
from ..dependencies import get_db

router = APIRouter(prefix="/effects")

@router.post("/", response_model=schemas.EffectPreset)
def create_effect(effect: schemas.EffectPreset, db: Session = Depends(get_db)):
    effect = crud.create_effect(db=db, effect=effect)
    return effect

@router.get("/", response_model=list[schemas.EffectPreset])
def read_effects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    effects = crud.get_effects(db, skip=skip, limit=limit)
    return effects

@router.get("/{effect_id}", response_model=schemas.EffectPreset)
def read_effect(effect_id: int, db: Session = Depends(get_db)):
    db_effect = crud.get_effect_by_id(db, effect_id=effect_id)
    if db_effect is None:
        raise HTTPException(status_code=404, detail="User Not Found!")
    return db_effect

@router.get("/types/")
def read_effect_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    effects = crud.get_effect_types(db, skip=skip, limit=limit)
    return effects