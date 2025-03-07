from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from pathlib import Path

from .. crud import state
from .. dependencies import get_db
from .. import api_calls

router = APIRouter(prefix="")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get('/change_colour', response_class=HTMLResponse)
async def change_colour(request: Request, db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    api_response = api_calls.new_random_colour(db, current_state.current_song_id)
    colour = api_response['config']['gradient']
    current_state = state.get_state(db)
    return templates.TemplateResponse("updated.html", {"request": request, "type": "Colour", 'data': colour})

@router.get('/change_effect', response_class=HTMLResponse)
async def change_effect(request: Request, db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    api_response = api_calls.new_random_effect(db, current_state.current_song_id)
    data = api_response['name']
    current_state = state.get_state(db) 
    return templates.TemplateResponse("updated.html", {"request": request, "type": "Effect", 'data': data})