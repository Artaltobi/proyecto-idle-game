# Pantalla principal del juego de la fábrica de medias

import pygame
from settings import WIDTH, HEIGHT, FPS, RUTA_FONDO_JUEGO
from ui import Button
from screens import economia
from screens.tejedor import (
    crear_tejedor, manejar_evento_tejedor,
    actualizar_tejedor, dibujar_tejedor,
    cargar_estado_tejedor, guardar_estado_tejedor,
)
from screens.terminado import (
    crear_terminado, manejar_evento_terminado,
    actualizar_terminado, dibujar_terminado,
    cargar_estado_terminado, guardar_estado_terminado,
)
from screens.vendedor import (
    crear_vendedor, manejar_evento_vendedor,
    actualizar_vendedor, dibujar_vendedor,
    cargar_estado_vendedor, guardar_estado_vendedor,
)


IMAGES_DIR = "assets/images/"



# ----------------- funciones comunes -----------------
def cargar_imagen(nombre, size=None):
    """Carga una imagen desde la carpeta de assets."""
    ruta = IMAGES_DIR + nombre 
    img = pygame.image.load(ruta).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img



def cargar_fondo():
    """Carga el fondo del juego. Si falla, usa un color sólido."""
    try:
        img = pygame.image.load(RUTA_FONDO_JUEGO).convert()
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        return img
    except:
        s = pygame.Surface((WIDTH, HEIGHT))
        s.fill((25, 30, 40))
        return s


def toggle_mute(sonando):
    """Pausa o reanuda la música."""
    if not pygame.mixer.get_init():
        return sonando

    if sonando:
        pygame.mixer.music.pause()
        return False
    else:
        pygame.mixer.music.unpause()
        return True


def dibujar_barra_dinero(pantalla, fuente_titulo, fuente_valor, icono_moneda, dinero_actual):
    """Dibuja la barrita de dinero arriba en el centro."""
    ancho, alto = 240, 52
    x = (pantalla.get_width() - ancho) // 2
    y = 10

    # fondo
    pygame.draw.rect(pantalla, (35, 80, 130), (x, y, ancho, alto), border_radius=14)
    # borde
    pygame.draw.rect(pantalla, (230, 230, 230), (x, y, ancho, alto), 2, border_radius=14)

    # icono
    pantalla.blit(icono_moneda, (x + 10, y + 8))

    # texto CASH
    txt_cash = fuente_titulo.render("CASH", True, (255, 255, 0))
    pantalla.blit(txt_cash, (x + 60, y + 5))

    # valor $
    txt_valor = fuente_valor.render(str(dinero_actual), True, (255, 255, 255))
    pantalla.blit(txt_valor, (x + 60, y + 22))
# -----------------------------------------------------


def run_game(pantalla, reloj, nombre_jugador, save_data):
    """Bucle principal de la fábrica de medias.
    Devuelve:
        - 'volver_menu' para salir al menú
        - 'salir_total' para cerrar el juego completo
    """
    # fondo e íconos
    fondo = cargar_fondo()
    icon_on = cargar_imagen("music_on.png", (40, 40))
    icon_off = cargar_imagen("music_off.png", (40, 40))
    icon_exit = cargar_imagen("exit.png", (40, 40))
    icon_coin = cargar_imagen("coin.png", (36, 36))

    # fuentes
    fuente_titulo = pygame.font.SysFont(None, 32)
    fuente_chica = pygame.font.SysFont(None, 24)

    # ---------- CARGAR PROGRESO DESDE save_data ----------
    datos_fabrica = save_data.get("fabrica_medias", {})

    # economía global de la fábrica
    if hasattr(economia, "cargar_desde_save"):
        economia.cargar_desde_save(datos_fabrica)

    # crear puestos
    tejedor = crear_tejedor(fuente_chica)
    terminado = crear_terminado(fuente_chica)
    vendedor = crear_vendedor(fuente_chica)

    # cargar niveles de cada puesto si existen en el save
    if "tejedor" in datos_fabrica:
        cargar_estado_tejedor(tejedor, datos_fabrica["tejedor"])
    if "terminado" in datos_fabrica:
        cargar_estado_terminado(terminado, datos_fabrica["terminado"])
    if "vendedor" in datos_fabrica:
        cargar_estado_vendedor(vendedor, datos_fabrica["vendedor"])
    # ------------------------------------------------------

    # botones de interfaz (mute y salir)
    btn_mute = Button((WIDTH - 80, 20, 48, 48), "", fuente_chica)
    btn_exit = Button((20, 20, 48, 48), "", fuente_chica)

    sonando = True if pygame.mixer.get_init() else False

    # ---------- FUNCIÓN PARA GUARDAR PROGRESO ----------
    def calcular_porcentaje_fabrica_medias(tej_data, term_data, vend_data):
        """Calcula porcentaje de progreso de esta fábrica.
        Ejemplo simple: promedio de niveles de las 3 máquinas.
        Si las 3 están en level_max (40), da 100%.
        """
        max_lvl = 40 * 3  # 3 máquinas * 40 niveles
        suma_lvls = tej_data["level"] + term_data["level"] + vend_data["level"]
        pct = int((suma_lvls / max_lvl) * 100)
        if pct > 100:
            pct = 100
        if pct < 0:
            pct = 0
        return pct

    def guardar_progreso():
        # Nos aseguramos de que exista la clave
        if "fabrica_medias" not in save_data:
            save_data["fabrica_medias"] = {}

        fab = save_data["fabrica_medias"]

        # economía (dinero, medias, cajas, encargados)
        if hasattr(economia, "volcar_a_save"):
            fab.update(economia.volcar_a_save())

        # estado de cada puesto
        fab["tejedor"] = guardar_estado_tejedor(tejedor)
        fab["terminado"] = guardar_estado_terminado(terminado)
        fab["vendedor"] = guardar_estado_vendedor(vendedor)

        # 🔥 porcentaje de progreso de ESTA fábrica
        fab["porcentaje"] = calcular_porcentaje_fabrica_medias(
            fab["tejedor"], fab["terminado"], fab["vendedor"]
        )
    # ---------------------------------------------------

    ejecutando = True
    while ejecutando:
        reloj.tick(FPS)

        # --------- eventos ---------
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                guardar_progreso()
                return "salir_total"

            # eventos de cada puesto
            manejar_evento_tejedor(tejedor, e)
            manejar_evento_terminado(terminado, e)
            manejar_evento_vendedor(vendedor, e)

            # botones de interfaz
            if btn_mute.clicked(e):
                sonando = toggle_mute(sonando)
            if btn_exit.clicked(e):
                guardar_progreso()
                return "volver_menu"

        # --------- actualizar lógica ---------
        actualizar_tejedor(tejedor)
        actualizar_terminado(terminado)
        actualizar_vendedor(vendedor)

        # --------- dibujar ---------
        pantalla.blit(fondo, (0, 0))

        # barra de dinero
        dibujar_barra_dinero(pantalla, fuente_chica, fuente_titulo, icon_coin, economia.dinero)

        # puestos
        dibujar_tejedor(pantalla, tejedor, economia.medias)
        dibujar_terminado(pantalla, terminado, economia.cajas)
        dibujar_vendedor(pantalla, vendedor)

        # iconos de interfaz
        pantalla.blit(icon_exit, icon_exit.get_rect(center=btn_exit.rect.center))
        icono_actual = icon_on if sonando else icon_off
        pantalla.blit(icono_actual, icono_actual.get_rect(center=btn_mute.rect.center))

        pygame.display.flip()
