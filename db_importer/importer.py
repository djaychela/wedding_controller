from random import choices

from sqlalchemy.orm import Session

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
    EffectPreset,
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

            # print(f"Added {current_user}")


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
            # print(f"Added {current_song} -> {current_song.title}")


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
            # print(f"Added {current_vote}")


def create_state():
    with Session(ctrl_engine) as session:
        state = State(id=1)
        state.current_song_id = "1234"
        state.current_song_artist = "Dummy Artist"
        state.current_song_title = "The Best Song"
        false = False
        true = True
        config_dict = {"effect": {"config": {"background_brightness": 1.0, "background_color": "#000000", "band_count": 10, "bass_size": 8.0, "blur": 0.0, "brightness": 1.0, "flip": false, "gradient": "linear-gradient(90deg, rgb(0, 0, 0) 0%, rgb(128, 255, 0) 32%, rgb(0, 255, 0) 64%, rgb(0, 255, 127) 96%)", "gradient_roll": 0.0, "high_size": 3.0, "mids_size": 6.0, "mirror": false, "speed": 1.0, "vertical_shift": 0.12, "viscosity": 6.0}, "name": "Water", "type": "water"}}
        state.ledfx_config = config_dict
        state.ledfx_name = "LED_NAME"
        state.ledfx_type = "LED_TYPE"
        state.ledfx_colour_mode = "single"
        state.ledfx_max_colours = 1
        bands_config_dict = {"effect": {"config": {"strobe_frequency": "1/4 (.o. )", "gradient": "#ff0000", "gradient_roll": 0.0, "blur": 0.0, "beat_decay": 1, "mirror": false, "flip": false, "brightness": 1.0, "background_brightness": 1.0, "strobe_decay": 1.5, "background_color": "#000000"}, "name": "BPM Strobe", "type": "strobe"}}
        state.bands_name = "BANDS_NAME"
        state.bands_type = "BANDS_TYPE"
        state.bands_config = bands_config_dict
        state.bands_colour_mode = "single"
        state.bands_max_colours = 1
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

    colour_mode = [
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
            current_effect.colour_mode = colour_mode[idx]
            current_effect.max_colours = max_colours[idx]
            session.add(current_effect)
            session.commit()

def create_effect_presets():
    true = True
    false = False
    dict_1 = {"effect": {"config": {"background_brightness": 1.0, "background_color": "#000000", "blur": 0.0, "brightness": 1.0, "flip": false, "gradient": "linear-gradient(90deg, #00ffff 0.00%,#0000ff 100.00%)", "gradient_roll": 0.0, "mirror": false, "reactivity": 0.5, "speed": 0.52}, "name": "Block Reflections", "type": "block_reflections"}}
    dict_2 = {"effect": {"config": {"align": "left", "background_brightness": 1.0, "background_color": "#000000", "band_count": 10, "blur": 0.0, "brightness": 1.0, "flip": false, "gradient": "linear-gradient(90deg, #ff0000 0.00%,#ff7800 14.00%,#ffc800 28.00%,#00ff00 42.00%,#00c78c 56.00%,#0000ff 70.00%,#800080 84.00%,#ff00b2 98.00%)", "gradient_repeat": 10, "gradient_roll": 0.0, "mirror": false}, "name": "Equalizer", "type": "equalizer"}}
    dict_3 = {"effect": {"config": {"background_brightness": 1.0, "background_color": "#000000", "band_count": 10, "bass_decay_rate": 0.05, "blur": 0.0, "brightness": 1.0, "flip": false, "gradient": "linear-gradient(90deg, rgb(0, 0, 0) 0%, rgb(255, 204, 255) 98%)", "gradient_roll": 0.0, "mirror": true, "sparks_color": "#ffffff", "sparks_decay_rate": 0.15}, "name": "Power", "type": "power"}}
    dict_4 = {"effect": {"config": {"blur": 0.0, "gradient": "linear-gradient(90deg, rgb(0, 0, 0) 0%, rgb(153, 204, 255) 49%, rgb(153, 51, 255) 98%)", "band_count": 10, "background_brightness": 1.0, "gradient_roll": 0.0, "mirror": false, "flip_gradient": false, "brightness": 1.0, "flip": false, "background_color": "#000000"}, "name": "Bands Matrix", "type": "bands_matrix"}}

    colour_mode_list = ["gradient", "single", "adjacent", "gradient"]
    max_colours_list = [6, 1, 2, 4]
    preset_list = [dict_1, dict_2, dict_3, dict_4]
    song_id = ["043bfUkTydw0xJ5JjOT91w","003vvx7Niy0yvhvHt4a68B","5WwRKYnVy9dekqXAGPbAvU", "0a2cA9H6KuOsoHLCnjl6YL"]

    with Session(ctrl_engine) as session:
        for idx, config in enumerate(preset_list):
            current_preset = EffectPreset()
            current_preset.config = config
            current_preset.name = config["effect"]["name"]
            current_preset.type = config["effect"]["type"]
            current_preset.song_id = song_id[idx]
            current_preset.colour_mode = colour_mode_list[idx]
            current_preset.max_colours = max_colours_list[idx]
            session.add(current_preset)
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
    create_effect_presets()
