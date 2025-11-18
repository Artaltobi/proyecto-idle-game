# screens/tejedor.py
# puesto del tejedor (maquina + trabajador + encargado)

import pygame
from settings import FPS, VELOCIDAD_BASE
from screens import economia

IMAGES_DIR = "mi_juego/assets/images/"


# ----------------- POSICIONES TEJEDOR -----------------
def posiciones_tejedor():
    datos_pos = {}
    # personaje + máquina
    datos_pos["maquina"] = (200, 310)
    datos_pos["trabajador"] = (140, 400)
    datos_pos["encargado"] = (20, 390)
    datos_pos["boton_encargado"] = (10, 540)
    datos_pos["boton_mejorar"] = (140, 310 - 46)
    datos_pos["texto_flotante"] = (230, 570)

    return datos_pos
# ------------------------------------------------------


def _load(nombre, size=None):
    ruta = IMAGES_DIR + nombre
    img = pygame.image.load(ruta).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img


def _calcular_frames(level, base_segundos=VELOCIDAD_BASE):
    segundos = max(0.5, base_segundos - 0.18 * (level - 1))
    return int(segundos * FPS)


def crear_tejedor(fuente_chica):
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

    # botón de mejorar usa la posición que definimos arriba
    bm_x, bm_y = pos["boton_mejorar"]
    datos["rect_mejorar"] = pygame.Rect(bm_x, bm_y, 220, 38)

    # botón encargado
    be_x, be_y = pos["boton_encargado"]
    datos["rect_encargado_btn"] = pygame.Rect(be_x, be_y, 180, 36)

    # barra
    datos["mostrar_barra"] = True
    datos["barra_w"] = 180
    datos["barra_h"] = 16

    # texto flotante
    datos["flash_text"] = ""
    datos["flash_timer"] = 0

    _actualizar_sprite_maquina(datos)
    return datos


def _actualizar_sprite_maquina(datos):
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
    # el botón de mejorar ya lo pusimos fijo desde posiciones_tejedor()


def _intentar_mejorar(datos):
    if datos["level"] < datos["level_max"]:
        if economia.pagar(datos["costo_mejora"]):
            datos["level"] += 1
            datos["frames_total"] = _calcular_frames(datos["level"], datos["base_segundos"])
            _actualizar_sprite_maquina(datos)
            datos["costo_mejora"] += 15


def _intentar_comprar_encargado(datos):
    if economia.encargado_tejedor:
        return
    if economia.pagar(datos["costo_encargado"]):
        economia.encargado_tejedor = True


def manejar_evento_tejedor(datos, evento):
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if (datos["rect_maquina"].collidepoint(evento.pos) or
            datos["rect_trabajador"].collidepoint(evento.pos)):
            if not datos["trabajando"]:
                datos["trabajando"] = True
                datos["frames_count"] = 0

        if datos["rect_mejorar"].collidepoint(evento.pos):
            _intentar_mejorar(datos)

        if datos["rect_encargado_btn"].collidepoint(evento.pos):
            _intentar_comprar_encargado(datos)

    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_1:
        _intentar_mejorar(datos)


def actualizar_tejedor(datos):
    # auto
    if (not datos["trabajando"]) and economia.encargado_tejedor:
        datos["trabajando"] = True
        datos["frames_count"] = 0

    if datos["flash_timer"] > 0:
        datos["flash_timer"] -= 1

    if datos["trabajando"]:
        datos["frames_count"] += 1
        if datos["frames_count"] >= datos["frames_total"]:
            datos["trabajando"] = False
            datos["frames_count"] = 0
            economia.producir_media()
            datos["flash_text"] = "+1 media"
            datos["flash_timer"] = FPS
            return True
    return False


def dibujar_tejedor(pantalla, datos, cantidad_medias):
    pantalla.blit(datos["machine_img"], datos["pos_maquina"])
    img = datos["img_work"] if datos["trabajando"] else datos["img_idle"]
    pantalla.blit(img, datos["pos_trabajador"])

    if economia.encargado_tejedor:
        pantalla.blit(datos["img_encargado"], datos["pos_encargado"])

    # barra de cargas
    if datos["mostrar_barra"] and datos["trabajando"]:
        bottom = max(datos["rect_maquina"].bottom, datos["rect_trabajador"].bottom)
        bar_y = bottom + 8
        cx = datos["rect_maquina"].centerx
        bar_x = cx - datos["barra_w"] // 2
        pygame.draw.rect(pantalla, (40, 40, 40), (bar_x, bar_y, datos["barra_w"], datos["barra_h"]), border_radius=6)
        pct = datos["frames_count"] / max(1, datos["frames_total"])
        fill_w = int(datos["barra_w"] * pct)
        pygame.draw.rect(pantalla, (0, 180, 70), (bar_x, bar_y, fill_w, datos["barra_h"]), border_radius=6)
        pygame.draw.rect(pantalla, (230, 230, 230), (bar_x, bar_y, datos["barra_w"], datos["barra_h"]), 2, border_radius=6)

    # botón de mejorar
    pygame.draw.rect(pantalla, (220, 220, 220), datos["rect_mejorar"], border_radius=10)
    pygame.draw.rect(pantalla, (120, 120, 120), datos["rect_mejorar"], 2, border_radius=10)
    texto_btn = f"Mejorar ${datos['costo_mejora']} - Lvl {datos['level']}"
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

    # contador
    txt_med = datos["fuente"].render(str(cantidad_medias), True, (255, 255, 255))
    pantalla.blit(txt_med, (datos["pos_trabajador"][0] + 50, datos["pos_trabajador"][1] + 170))

    # texto flotante
    if datos["flash_timer"] > 0:
        fx, fy = datos["pos_texto_flotante"]
        txtf = datos["fuente"].render(datos["flash_text"], True, (0, 255, 255))
        pantalla.blit(txtf, (fx, fy))
