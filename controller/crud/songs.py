from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import models, schemas

from ..helpers import colour_helpers

def get_songs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Song).offset(skip).limit(limit).all()


def get_song(song_id: str, db: Session):
    return db.query(models.Song).filter(models.Song.track_id == song_id).first()


def get_song_colours(song_id: str, db: Session, mode="dict"):
    voters = db.query(models.Votes).filter(models.Votes.track_id == song_id).all()
    if voters:
        colours = {}
        for idx, voter in enumerate(voters):
            current_voter = db.query(models.User).filter(models.User.id == voter.voter_id).first()
            colours[idx] = current_voter.colour
        if mode == "dict":
            return colours
        else:
            return [v for k,v in colours.items()]
    else:
        # TODO: return a random single colour here
        return [colour_helpers.generate_random_hex_colour()]



