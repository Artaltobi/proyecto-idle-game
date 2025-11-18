# settings.py
# constantes y rutas de recursos

import os   

# ventana
WIDTH, HEIGHT = 1280, 720
FPS = 40
TITLE = "Joga Socks Tycoon"

# velocidad base de produccion 
VELOCIDAD_BASE = 5.0

# colores basicos
BLANCO = (245, 245, 245)
NEGRO  = (20, 20, 20)
GRIS   = (120, 120, 120)
GRIS_OSCURO = (60, 60, 60)

# rutas base
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

# imagenes
RUTA_FONDO            = os.path.join(IMAGES_DIR, "fondomenu.png")
RUTA_ICONO_MUSICA_ON  = os.path.join(IMAGES_DIR, "music_on.png")
RUTA_ICONO_MUSICA_OFF = os.path.join(IMAGES_DIR, "music_off.png")

# sonidos
RUTA_MUSICA = os.path.join(SOUNDS_DIR, "music.mp3")

# guardado simple
SAVE_PATH = os.path.join(BASE_DIR, "save.json")

# fondo del juego e icono de salir
RUTA_FONDO_JUEGO = os.path.join(IMAGES_DIR, "fondojuego.png")
RUTA_ICONO_EXIT  = os.path.join(IMAGES_DIR, "exit.png")
