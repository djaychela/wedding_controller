from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. crud import songs

from .. import schemas
from .. dependencies import get_db
from .. helpers import colour_helpers

router = APIRouter(prefix="/songs")



@router.get("/", response_model=list[schemas.Song])
def get_all_songs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    song_list = songs.get_songs(db, skip=skip, limit=limit)
    return song_list

@router.get("/dummy")
def dummy_call(db: Session = Depends(get_db)):
    colourscheme = colour_helpers.create_colourscheme(db)
    refined_gradient_s = colour_helpers.refine_colourscheme(db, colourscheme, "gradient", "song")
    refined_adjacent_s = colour_helpers.refine_colourscheme(db, colourscheme, "adjacent", "song")
    refined_single_s = colour_helpers.refine_colourscheme(db, colourscheme, "single", "song")
    refined_gradient_f = colour_helpers.refine_colourscheme(db, colourscheme, "gradient", "floor")
    refined_adjacent_f = colour_helpers.refine_colourscheme(db, colourscheme, "adjacent", "floor")
    refined_single_f = colour_helpers.refine_colourscheme(db, colourscheme, "single", "floor")
    return {"0": colourscheme, "1 - GS": refined_gradient_s, "2 - AS": refined_adjacent_s, "3 - SS": refined_single_s, "4 - GF": refined_gradient_f, "5 - AF": refined_adjacent_f, "6 - SF": refined_single_f,}

@router.get("/{song_id}")
def get_song_details(song_id: str, db: Session = Depends(get_db)):
    song = songs.get_song(song_id, db)
    return song

@router.get("/{song_id}/colours/")
def get_song_colours(song_id: str, db: Session = Depends(get_db)):
    colours = songs.get_song_colours(db, song_id)
    return colours

