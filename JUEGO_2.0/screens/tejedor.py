# screens/tejedor.py
# Puesto del TEJEDOR (máquina + trabajador + encargado)

import pygame
from settings import FPS, VELOCIDAD_BASE
from screens import economia

IMAGES_DIR = "assets/images/"


# ----------------- POSICIONES TEJEDOR -----------------
def posiciones_tejedor():
    """Devuelve un diccionario con todas las posiciones del puesto."""
    datos_pos = {}

    datos_pos["maquina"] = (200, 310)
    datos_pos["trabajador"] = (140, 400)
    datos_pos["encargado"] = (20, 390)

    datos_pos["boton_encargado"] = (10, 540)
    datos_pos["boton_mejorar"] = (140, 310 - 46)

    datos_pos["texto_flotante"] = (230, 570)

    return datos_pos
# ------------------------------------------------------


def _load(nombre, size=None):
    """Carga imagen del tejedor."""
    ruta = IMAGES_DIR + nombre
    img = pygame.image.load(ruta).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img


def _calcular_frames(level, base_segundos=VELOCIDAD_BASE):
    """Convierte la velocidad (segundos) en cantidad de frames según el nivel."""
    segundos = max(0.5, base_segundos - 0.18 * (level - 1))
    return int(segundos * FPS)


def crear_tejedor(fuente_chica):
    """Crea y devuelve el diccionario con todos los datos del tejedor."""
    pos = posiciones_tejedor()
    datos = {}

    # sprites
    datos["img_idle"] = _load("tejedor_frente.png", (140, 140))
    datos["img_work"] = _load("tejedor_espaldas.png", (140, 140))
    datos["img_encargado"] = _load("encargado_tejedor.png", (140, 140))

    datos["machine_lvl1"] = _load("machine_lvl1.png", (180, 220))
    datos["machine_lvl2"] = _load("machine_lvl2.png", (180, 220))
    datos["machine_lvl3"] = _load("machine_lvl3.png", (180, 220))
    datos["machine_lvl4"] = _load("machine_lvl4.png", (180, 220))

    # posiciones
    datos["pos_maquina"] = pos["maquina"]
    datos["pos_trabajador"] = pos["trabajador"]
    datos["pos_encargado"] = pos["encargado"]
    datos["pos_boton_enc"] = pos["boton_encargado"]
    datos["pos_texto_flotante"] = pos["texto_flotante"]

    datos["fuente"] = fuente_chica

    # estado
    datos["level"] = 1
    datos["level_max"] = 40

    datos["base_segundos"] = VELOCIDAD_BASE
    datos["frames_total"] = _calcular_frames(datos["level"], datos["base_segundos"])
    datos["frames_count"] = 0
    datos["trabajando"] = False

    # costos
    datos["costo_mejora"] = 20
    datos["costo_encargado"] = 150

    # imagen actual + rects
    datos["machine_img"] = datos["machine_lvl1"]
    datos["rect_maquina"] = datos["machine_img"].get_rect(topleft=datos["pos_maquina"])
    datos["rect_trabajador"] = datos["img_idle"].get_rect(topleft=datos["pos_trabajador"])

    # botón de mejorar
    bm_x, bm_y = pos["boton_mejorar"]
    datos["rect_mejorar"] = pygame.Rect(bm_x, bm_y, 220, 38)

    # botón de encargado
    be_x, be_y = pos["boton_encargado"]
    datos["rect_encargado_btn"] = pygame.Rect(be_x, be_y, 180, 36)

    # barra de progreso
    datos["mostrar_barra"] = True
    datos["barra_w"] = 180
    datos["barra_h"] = 16

    # texto flotante al producir
    datos["flash_text"] = ""
    datos["flash_timer"] = 0

    _actualizar_sprite_maquina(datos)
    return datos


def _actualizar_sprite_maquina(datos):
    """Cambia la imagen de la máquina según el nivel."""
    lvl = datos["level"]
    if lvl >= 30:
        datos["machine_img"] = datos["machine_lvl4"]
    elif lvl >= 20:
        datos["machine_img"] = datos["machine_lvl3"]
    elif lvl >= 10:
        datos["machine_img"] = datos["machine_lvl2"]
    else:
        datos["machine_img"] = datos["machine_lvl1"]

    datos["rect_maquina"] = datos["machine_img"].get_rect(topleft=datos["pos_maquina"])


def _intentar_mejorar(datos):
    """Si hay plata y no se llegó al máximo, mejora el tejedor."""
    if datos["level"] < datos["level_max"]:
        if economia.pagar(datos["costo_mejora"]):
            datos["level"] += 1
            datos["frames_total"] = _calcular_frames(datos["level"], datos["base_segundos"])
            _actualizar_sprite_maquina(datos)
            datos["costo_mejora"] += 15


def _intentar_comprar_encargado(datos):
    """Compra el encargado del tejedor si hay plata y aún no existe."""
    if economia.encargado_tejedor:
        return
    if economia.pagar(datos["costo_encargado"]):
        economia.encargado_tejedor = True


def manejar_evento_tejedor(datos, evento):
    """Maneja clics y teclas sobre el tejedor."""
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        # click en máquina o trabajador → producir (si no está ya trabajando)
        if (datos["rect_maquina"].collidepoint(evento.pos) or
            datos["rect_trabajador"].collidepoint(evento.pos)):
            if not datos["trabajando"]:
                datos["trabajando"] = True
                datos["frames_count"] = 0

        # botón mejorar
        if datos["rect_mejorar"].collidepoint(evento.pos):
            _intentar_mejorar(datos)

        # botón encargado
        if datos["rect_encargado_btn"].collidepoint(evento.pos):
            _intentar_comprar_encargado(datos)

    # tecla de acceso rápido
    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_1:
        _intentar_mejorar(datos)


def actualizar_tejedor(datos):
    """Actualiza el estado del tejedor cada frame."""
    # auto-click del encargado
    if (not datos["trabajando"]) and economia.encargado_tejedor:
        datos["trabajando"] = True
        datos["frames_count"] = 0

    # texto flotante
    if datos["flash_timer"] > 0:
        datos["flash_timer"] -= 1

    # progreso de la tarea
    if datos["trabajando"]:
        datos["frames_count"] += 1

        if datos["frames_count"] >= datos["frames_total"]:
            # terminó de tejer una media
            datos["trabajando"] = False
            datos["frames_count"] = 0
            economia.producir_media()
            datos["flash_text"] = "+1 media"
            datos["flash_timer"] = FPS
            return True

    return False


def dibujar_tejedor(pantalla, datos, cantidad_medias):
    """Dibuja máquina, trabajador, botones y barras del tejedor."""
    # máquina
    pantalla.blit(datos["machine_img"], datos["pos_maquina"])

    # trabajador (idle o trabajando)
    img = datos["img_work"] if datos["trabajando"] else datos["img_idle"]
    pantalla.blit(img, datos["pos_trabajador"])

    # encargado (si fue comprado)
    if economia.encargado_tejedor:
        pantalla.blit(datos["img_encargado"], datos["pos_encargado"])

    # barra de progreso
    if datos["mostrar_barra"] and datos["trabajando"]:
        bottom = max(datos["rect_maquina"].bottom, datos["rect_trabajador"].bottom)
        bar_y = bottom + 8
        cx = datos["rect_maquina"].centerx
        bar_x = cx - datos["barra_w"] // 2

        pygame.draw.rect(pantalla, (40, 40, 40),
                        (bar_x, bar_y, datos["barra_w"], datos["barra_h"]), border_radius=6)

        pct = datos["frames_count"] / max(1, datos["frames_total"])
        fill_w = int(datos["barra_w"] * pct)

        pygame.draw.rect(pantalla, (0, 180, 70),
                        (bar_x, bar_y, fill_w, datos["barra_h"]), border_radius=6)

        pygame.draw.rect(pantalla, (230, 230, 230),
                        (bar_x, bar_y, datos["barra_w"], datos["barra_h"]), 2, border_radius=6)

    # botón de mejorar
    pygame.draw.rect(pantalla, (220, 220, 220), datos["rect_mejorar"], border_radius=10)
    pygame.draw.rect(pantalla, (120, 120, 120), datos["rect_mejorar"], 2, border_radius=10)
    if datos["level"] < datos["level_max"]:
        texto_btn = f"Mejorar ${datos['costo_mejora']} - Lvl {datos['level']}"
    else:
        texto_btn = f"LVL {datos['level']} - MAX LVL"
    txt = datos["fuente"].render(texto_btn, True, (20, 20, 20))
    pantalla.blit(txt, txt.get_rect(center=datos["rect_mejorar"].center))


    # botón de encargado
    color_enc = (200, 200, 200) if not economia.encargado_tejedor else (150, 150, 150)
    pygame.draw.rect(pantalla, color_enc, datos["rect_encargado_btn"], border_radius=10)
    pygame.draw.rect(pantalla, (80, 80, 80), datos["rect_encargado_btn"], 2, border_radius=10)

    if economia.encargado_tejedor:
        txt_enc = "Encargado listo"
    else:
        txt_enc = f"Encargado ${datos['costo_encargado']}"

    txt2 = datos["fuente"].render(txt_enc, True, (10, 10, 10))
    pantalla.blit(txt2, txt2.get_rect(center=datos["rect_encargado_btn"].center))

    # contador de medias
    txt_med = datos["fuente"].render(str(cantidad_medias), True, (255, 255, 255))
    pantalla.blit(txt_med, (datos["pos_trabajador"][0] + 50, datos["pos_trabajador"][1] + 170))

    # texto flotante
    if datos["flash_timer"] > 0:
        fx, fy = datos["pos_texto_flotante"]
        txtf = datos["fuente"].render(datos["flash_text"], True, (0, 255, 255))
        pantalla.blit(txtf, (fx, fy))

def cargar_estado_tejedor(datos, datos_save):
    """Restaura nivel y costos del tejedor desde el save."""
    datos["level"] = datos_save.get("level", 1)
    datos["costo_mejora"] = datos_save.get("costo_mejora", datos["costo_mejora"])
    datos["costo_encargado"] = datos_save.get("costo_encargado", datos["costo_encargado"])

    datos["frames_total"] = _calcular_frames(datos["level"], datos["base_segundos"])
    _actualizar_sprite_maquina(datos)


def guardar_estado_tejedor(datos):
    """Devuelve un dict con lo importante del tejedor para guardar."""
    return {
        "level": datos["level"],
        "costo_mejora": datos["costo_mejora"],
        "costo_encargado": datos["costo_encargado"],
    }
