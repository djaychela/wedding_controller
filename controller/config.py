# config.py - global constants are set here, and imported into modules where they are used.

# used for specific songs where bands behaviour is non-standard
SPECIAL_SONGS = ["2NVpYQqdraEcQwqT7GhUkh", "6LNdC4inw5abVNMQ1YUHN6", "63xdwScd1Ai1GigAwQxE8y"]

# disabled wristbands for first dance
WRISTBANDS_DISABLED = ["2NVpYQqdraEcQwqT7GhUkh"]

# general config for which API calls are present
STICKS = True
# Sticks 2 were on a separate Virtual, so had a separate API call
STICKS_2 = False
# Bands were dmx-controlled via a single directly-addressed WLED instance so needed a separate call
BANDS = False

# This disables the Mixx-controlled song-database mode, so that song votes are ignored (more colours available)
STANDALONE = True

# Sets the base URL for LedFX API calls - should be the IP of the LedFX instance (127.0.0.1 for local)
API_BASE_URL = "http://192.168.1.238:8888"

# Sets the API endpoints based on the above.  Dependent on your LedFX setup
STICKS_API_ENDPOINT = f"{API_BASE_URL}/api/virtuals/virtual-1/effects"
STICKS_2_API_ENDPOINT = f"{API_BASE_URL}/api/virtuals/virtual-2/effects"
BANDS_API_ENDPOINT = f"{API_BASE_URL}/api/virtuals/wled-bands/effects"
DMX_API_ENDPOINT = f"{API_BASE_URL}/api/virtuals/virtual-dmx/effects"

# Sets the API endpoint for the bands controller - a directly addressed WLED instance. 
WLED_BANDS_API_ENDPOINT = "http://192.168.1.33/json"

# Sets the base URL for wedding controller API - note port difference from base URL!
WEDDING_BASE_URL = "http://127.0.0.1:8000"

# API URLs for timed_calls.py:
EFFECT_URL = f"{WEDDING_BASE_URL}/state/change_effect"
COLOUR_URL = f"{WEDDING_BASE_URL}/state/change_colour"
VIRTUAL_URL = f"{API_BASE_URL}/api/virtuals/virtual-1/effects"

# Sets the mode - running or otherwise.  "run" - Normal or "test" for text output of API call without making it.
MODE = "run"

# Sets whether there will be output to the console:
CONSOLE_OUTPUT = False

# Sets the timeout in seconds for timed_calls.py
TIMED_CALL_TIMEOUT = 120

# Effect type to never choose - caused issues!
NEVER_CHOOSE_EFFECTS_TYPE = ["gradient"]
