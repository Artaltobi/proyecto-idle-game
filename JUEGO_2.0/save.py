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

# save.py
import json
import os

SAVE_PATH = "JUEGO_2.0/save.json"


def load_game():
    if not os.path.exists(SAVE_PATH):
        return crear_save_por_defecto()
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_game(datos):
    """Guarda el diccionario 'datos' en save.json."""
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def crear_save_por_defecto():
    """Save inicial si no existe archivo."""
    return {
        "nombre": "Jugador",
        "fabrica_medias": {
            "dinero": 10000,
            "medias": 0,
            "cajas": 0,
            "encargado_tejedor": False,
            "encargado_terminado": False,
            "encargado_vendedor": False,
            "tejedor": {"level": 1, "costo_mejora": 20, "costo_encargado": 150},
            "terminado": {"level": 1, "costo_mejora": 25, "costo_encargado": 180},
            "vendedor": {
                "level": 1,
                "costo_mejora": 30,
                "costo_encargado": 220,
                "precio_venta": 10,
            },
        },
    }
