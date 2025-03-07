from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. crud import crud

from .. import schemas, state
from .. dependencies import get_db, led_fx_post, create_gradient

router = APIRouter(prefix="/ledfx")


@router.get("/random/preset", response_model=schemas.EffectPreset)
def random_ledfx(db: Session = Depends(get_db)):
    db_effect = crud.get_random_effect(db=db)
    led_fx_post(db, db_effect)
    return db_effect

@router.get("/random/both", response_model=schemas.EffectPreset)
def random_effect_random_gradient(db: Session = Depends(get_db)):
    db_effect = crud.get_random_effect(db=db)
    db_gradient = crud.get_random_gradient(db=db)
    db_effect.config["gradient"] = db_gradient.gradient
    led_fx_post(db, db_effect)
    # print(create_gradient(["#FF0000", "#00FF00", "#0000FF"]))
    return db_effect

@router.get("/random/gradient", response_model=schemas.EffectPreset)
def random_gradient(db: Session = Depends(get_db)):
    # get effect based on current settings
    current_effect = state.get_current_effect(db)
    # get, add and post random gradient to ledfx
    db_gradient = crud.get_random_gradient(db=db)
    current_effect.config["gradient"] = db_gradient.gradient
    led_fx_post(db, current_effect)

    return current_effect

@router.post("/set/gradient", response_model=schemas.EffectPreset)
def set_gradient(gradient: schemas.Gradient, db: Session = Depends(get_db)):
    # get effect based on current settings
    current_effect = state.get_current_effect(db)
    gradient_list = gradient.gradient.split(",")
    gradient_list = [gradient.strip().replace("'","") for gradient in gradient_list]
    new_gradient = create_gradient(gradient_list)
    current_effect.config["gradient"] = new_gradient
    led_fx_post(db, current_effect)

    return current_effect

@router.post("/set/effect", response_model=schemas.EffectPreset)
def set_effect(effect: schemas.EffectPresetSelect, db: Session = Depends(get_db)):
    current_effect = state.get_current_effect(db)
    current_effect.name = effect.name
    current_effect.type = effect.type
    led_fx_post(db, current_effect)

    return current_effect


