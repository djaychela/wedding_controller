from pprint import pprint
from random import choices

import json

from sqlalchemy.orm import Session

from sqlalchemy import exc

from models_imp import (
    DbVotes,
    DbUser,
    DbTrack,
    Votes,
    User,
    Song,
    State,
    Gradient,
    Effect,
)
from database_imp import db_engine, ctrl_engine


def generate_dummy_nfc_id():
    return "".join(choices("0123456789abcdef", k=10))


def load_users():
    with Session(db_engine) as session:
        all_users = session.query(DbUser).all()
        users_list = []
        for user in all_users:
            user_dict = {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "colour": user.colour,
            }
            users_list.append(user_dict)
    return users_list


def save_users(users_list):
    with Session(ctrl_engine) as session:
        for user in users_list:
            current_user = User(id=user["id"])
            # current_user.id = user["id"]
            current_user.username = user["username"]
            current_user.first_name = user["first_name"]
            current_user.last_name = user["last_name"]
            current_user.colour = user["colour"]
            current_user.nfc_id = generate_dummy_nfc_id()
            session.add(current_user)

            session.commit()

            print(f"Added {current_user}")


def load_tracks():
    with Session(db_engine) as session:
        all_tracks = session.query(DbTrack).all()
        tracks_list = []
        for track in all_tracks:
            track_dict = {
                "id": track.track_id,
                "name": track.name,
                "artist": track.artist,
                "duration": track.duration,
            }
            tracks_list.append(track_dict)
        return tracks_list


def save_tracks(tracks_list):
    with Session(ctrl_engine) as session:
        for track in tracks_list:
            current_song = Song()
            current_song.track_id = track["id"]
            current_song.title = track["name"]
            current_song.artist = track["artist"]
            current_song.duration = track["duration"]
            session.add(current_song)
            session.commit()
            print(f"Added {current_song} -> {current_song.title}")


def load_votes():
    with Session(db_engine) as session:
        all_votes = session.query(DbVotes).all()
        votes_list = []
        for vote in all_votes:
            vote_dict = {"voter_id": vote.voter_id, "track_id": vote.track_id}
            votes_list.append(vote_dict)
    return votes_list


def save_votes(votes_list):
    with Session(ctrl_engine) as session:
        for vote in votes_list:
            current_vote = Votes()
            current_vote.track_id = vote["track_id"]
            current_vote.voter_id = vote["voter_id"]
            session.add(current_vote)
            session.commit()
            print(f"Added {current_vote}")


def create_state():
    with Session(ctrl_engine) as session:
        state = State(id=1)
        state.current_song_id = "1234"
        state.current_song_artist = "Dummy Artist"
        state.current_song_title = "The Best Song"
        state.ledfx_config = json.dumps(
            '{"url": "http://127.0.0.1:8888","name": "LedFx","version": "0.3.0"}'
        )
        state.ledfx_name = "LED_NAME"
        state.ledfx_type = "LED_TYPE"
        session.add(state)
        session.commit()


def create_gradients():
    gradient_list = [
        "linear-gradient(90deg, rgb(255, 0, 0) 0%, rgb(255, 120, 0) 14%, rgb(255, 200, 0) 28%, rgb(0, 255, 0) 42%, rgb(0, 199, 140) 56%, rgb(0, 0, 255) 70%, rgb(128, 0, 128) 84%, rgb(255, 0, 178) 98%)",
        "linear-gradient(90deg, rgb(255, 0, 0) 0%,  rgb(255, 0, 178) 98%)",
        "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(127, 127, 127) 98%)",
        "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(0, 255, 0) 98%)",
        "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(255, 0, 0) 98%)",
        "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(0, 0, 255) 98%)",
        "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(0, 255, 255) 98%)",
        "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(255, 0, 255) 98%)",
        "linear-gradient(90deg, rgb(0, 0, 0) 0%,  rgb(255, 255, 0) 98%)",
        "linear-gradient(90deg, rgb(0, 0, 0) 0%, rgb(255, 0, 0) 98%)",
    ]
    with Session(ctrl_engine) as session:
        for gradient in gradient_list:
            current_gradient = Gradient()
            current_gradient.gradient = gradient
            session.add(current_gradient)
            session.commit()


def create_effects():
    effects_list = [
        "bands_matrix",
        "block_reflections",
        "equalizer",
        "equalizer",
        "glitch",
        "marching",
        "melt",
        "melt_and_sparkle",
        "power",
        "rain",
        "water",
    ]

    colour_type = [
        "single",
        "gradient",
        "single",
        "gradient",
        "adjacent",
        "gradient",
        "single",
        "adjacent",
        "single",
        "adjacent",
        "adjacent",
    ]

    max_colours = [
        1,
        6,
        1,
        10,
        1,
        3,
        1,
        1,
        1,
        1,
        1,
    ]
    with Session(ctrl_engine) as session:
        for idx, effect in enumerate(effects_list):
            current_effect = Effect()
            current_effect.name = effect
            current_effect.type = effect
            current_effect.colour_type = colour_type[idx]
            current_effect.max_colours = max_colours[idx]
            session.add(current_effect)
            session.commit()


if __name__ == "__main__":
    # get users from db
    # create users in wedding

    # get tracks from db
    # create tracks in wedding

    # get votes from db
    # create votes in wedding

    users_list = load_users()
    save_users(users_list)
    songs_list = load_tracks()
    save_tracks(songs_list)
    votes_list = load_votes()
    save_votes(votes_list)
    # pprint(load_tracks())
    # pprint(load_votes())
    create_state()
    create_gradients()
    create_effects()
