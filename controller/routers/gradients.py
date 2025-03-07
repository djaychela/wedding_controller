from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. crud import gradients, dancefloor

from .. import schemas
from .. dependencies import get_db, create_gradient

router = APIRouter(prefix="/gradients")

@router.post("/", response_model=schemas.Gradient)
def list_gradients(gradient: schemas.Gradient, db: Session = Depends(get_db)):
    return gradients.create_gradient(db=db, gradient=gradient)

@router.get("/", response_model=list[schemas.Gradient])
def read_gradients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_gradients = gradients.get_gradients(db, skip=skip, limit=limit)
    return all_gradients

@router.get("/random", response_model=schemas.Gradient)
def get_random_gradient(db: Session = Depends(get_db)):
    random_gradient = gradients.get_random_gradient(db)
    # print(random_gradient.__dict__['gradient'])
    return random_gradient

@router.get("/dancefloor")
def get_dancefloor_gradient(db: Session = Depends(get_db)):
    colours = dancefloor.get_dancefloor_colours(db)
    colours_list = [colour[0] for colour in colours]
    gradient = create_gradient(colours_list)
    return gradient