# screens/game.py
# versión sencilla y procedural del juego principal

import pygame
from settings import WIDTH, HEIGHT, FPS, RUTA_FONDO_JUEGO
from ui import Button
from screens import economia
from screens.tejedor import (
    crear_tejedor, manejar_evento_tejedor,
    actualizar_tejedor, dibujar_tejedor
)
from screens.terminado import (
    crear_terminado, manejar_evento_terminado,
    actualizar_terminado, dibujar_terminado
)
from screens.vendedor import (
    crear_vendedor, manejar_evento_vendedor,
    actualizar_vendedor, dibujar_vendedor
)

IMAGES_DIR = "mi_juego/assets/images/"


# ----------------- funciones comunes -----------------
def cargar_imagen(nombre, size=None):
    ruta = IMAGES_DIR + nombre
    img = pygame.image.load(ruta).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img


def cargar_fondo():
    try:
        img = pygame.image.load(RUTA_FONDO_JUEGO).convert()
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        return img
    except:
        s = pygame.Surface((WIDTH, HEIGHT))
        s.fill((25, 30, 40))
        return s


def toggle_mute(sonando):
    if not pygame.mixer.get_init():
        return sonando
    if sonando:
        pygame.mixer.music.pause()
        return False
    else:
        pygame.mixer.music.unpause()
        return True


def dibujar_barra_dinero(pantalla, fuente1, fuente2, icono_moneda, dinero_actual):
    ancho, alto = 240, 52
    x = (pantalla.get_width() - ancho) // 2
    y = 10
    pygame.draw.rect(pantalla, (35, 80, 130), (x, y, ancho, alto), border_radius=14)
    pygame.draw.rect(pantalla, (230, 230, 230), (x, y, ancho, alto), 2, border_radius=14)
    pantalla.blit(icono_moneda, (x + 10, y + 8))
    txt_cash = fuente1.render("CASH", True, (255, 255, 0))
    pantalla.blit(txt_cash, (x + 60, y + 5))
    txt_valor = fuente2.render(str(dinero_actual), True, (255, 255, 255))
    pantalla.blit(txt_valor, (x + 60, y + 22))
# -----------------------------------------------------


def run_game(pantalla, reloj, nombre_jugador):
    fondo = cargar_fondo()
    icon_on = cargar_imagen("music_on.png", (40, 40))
    icon_off = cargar_imagen("music_off.png", (40, 40))
    icon_exit = cargar_imagen("exit.png", (40, 40))
    icon_coin = cargar_imagen("coin.png", (36, 36))

    f_btn = pygame.font.SysFont(None, 32)
    f_small = pygame.font.SysFont(None, 24)

    # crear puestos (cada archivo tiene sus posiciones)
    tejedor = crear_tejedor(f_small)
    terminado = crear_terminado(f_small)
    vendedor = crear_vendedor(f_small)

    # botones de interfaz
    btn_mute = Button((WIDTH - 80, 20, 48, 48), "", f_small)
    btn_exit = Button((20, 20, 48, 48), "", f_small)
    sonando = True if pygame.mixer.get_init() else False

    # empezar partida limpia
    economia.reset()

    ejecutando = True
    while ejecutando:
        reloj.tick(FPS)

        # --------- eventos ---------
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "salir_total"

            manejar_evento_tejedor(tejedor, e)
            manejar_evento_terminado(terminado, e)
            manejar_evento_vendedor(vendedor, e)

            if btn_mute.clicked(e):
                sonando = toggle_mute(sonando)
            if btn_exit.clicked(e):
                return "volver_menu"

        # --------- actualizar ---------
        actualizar_tejedor(tejedor)
        actualizar_terminado(terminado)
        actualizar_vendedor(vendedor)

        # --------- dibujar ---------
        pantalla.blit(fondo, (0, 0))

        # dinero arriba
        dibujar_barra_dinero(pantalla, f_small, f_btn, icon_coin, economia.dinero)

        # cada puesto
        dibujar_tejedor(pantalla, tejedor, economia.medias)
        dibujar_terminado(pantalla, terminado, economia.cajas)
        dibujar_vendedor(pantalla, vendedor)

        # iconos
        pantalla.blit(icon_exit, icon_exit.get_rect(center=btn_exit.rect.center))
        icono_actual = icon_on if sonando else icon_off
        pantalla.blit(icono_actual, icono_actual.get_rect(center=btn_mute.rect.center))

        pygame.display.flip()
