# save.py
import json

# El save va en la misma carpeta donde está main.py
SAVE_PATH = "save.json"


def load_game():
    """Carga el save.json si existe, sino crea uno por defecto."""
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Si no existe el archivo, devolvemos el save inicial
        return crear_save_por_defecto()
    except:
        # Si se rompe el json o algo raro, también arrancamos de cero
        return crear_save_por_defecto()


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
