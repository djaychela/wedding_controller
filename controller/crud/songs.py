from sqlalchemy.orm import Session

from .. import models

from ..helpers import colour_helpers

def get_songs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Song).offset(skip).limit(limit).all()


def get_song(song_id: str, db: Session):
    return db.query(models.Song).filter(models.Song.track_id == song_id).first()

def get_song_artist_title(db: Session, song_id: str):
    song = db.query(models.Song).filter(models.Song.track_id == song_id).first()
    if song:
        return f"{song.artist} - {song.title}"
    else:
        return "Unknown Artist - Unknown Title"


def get_song_colours(db: Session, song_id: str, mode="dict", strict=False):
    # print("songs.get_song_colours...")
    # print(f"{song_id=}, {mode=}, {strict=}")
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
        if strict:
            return []
        else:
            # print("returning a random colour")
            return [colour_helpers.generate_random_hex_colour()]

def get_song_votes(db: Session, song_id: str):
    voters = db.query(models.Votes).filter(models.Votes.track_id == song_id).all()
    return len(voters)
