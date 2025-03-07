from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from typing import Annotated

from pathlib import Path

from .. crud import crud

from .. import schemas
from .. dependencies import get_db

router = APIRouter(prefix="/users",)

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    # crud.get_user_colours_for_song(db, 2)
    return users

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found!")
    return db_user

@router.get("/register_nfc/")
def register_nfc_get(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # print(f"{BASE_PATH=}")
    users = crud.get_users(db, skip=skip, limit=limit)
    user_list = []
    for user in users:
        user_list.append({"username": user.username, "id": user.id})
    return templates.TemplateResponse("register_nfc.html", {"request": request, "user_list": user_list})
    
@router.post("/register_nfc/")
def register_nfc_post(request: Request, user_id: Annotated[int, Form()], nfc_id: Annotated[str, Form()], db: Session = Depends(get_db)):
    updated_user = crud.update_user_nfc_id(db, user_id, nfc_id)
    url = router.url_path_for('register_nfc_get')
    return templates.TemplateResponse("nfc_complete.html", {"request": request, "user": updated_user, "url": url})
    