# save.py
import json, os

SAVE_PATH = "save.json"

DEFAULT_DATA = {
    "money": 0,
    "factories": [
        {"name": "medias",  "unlocked": 1, "max_level": 1},
        {"name": "shorts",  "unlocked": 0, "max_level": 0},
        {"name": "remeras", "unlocked": 0, "max_level": 0}
    ]
}

def load_game():
    if not os.path.exists(SAVE_PATH):
        return DEFAULT_DATA
    try:
        f = open(SAVE_PATH, "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        return data
    except:
        return DEFAULT_DATA
