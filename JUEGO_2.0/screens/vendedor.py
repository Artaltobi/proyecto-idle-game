# archiv9o del Puesto del VENDEDOR (convierte cajas de terminado.py en dinero)

import pygame
from settings import FPS, VELOCIDAD_BASE
from screens import economia

IMAGES_DIR = "assets/images/"



def posiciones_vendedor():
    datos_pos = {}
    datos_pos["mostrador"] = (1020, 400)
    datos_pos["trabajador"] = (940, 380)
    datos_pos["encargado"] = (820, 360)

    datos_pos["boton_encargado"] = (800, 530)
    datos_pos["boton_mejorar"] = (980, 310 - 46)

    datos_pos["texto_flotante"] = (1070, 570)
    return datos_pos


def _load(nombre, size=None):
    ruta = IMAGES_DIR + nombre
    img = pygame.image.load(ruta).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img


def _calcular_frames(level, base_segundos=VELOCIDAD_BASE):
    segundos = max(0.5, base_segundos - 0.18 * (level - 1))
    return int(segundos * FPS)


def crear_vendedor(fuente_chica):
    pos = posiciones_vendedor()
    datos = {}

    datos["img_idle"] = _load("vendedor_media.png", (140, 140))
    datos["img_work"] = _load("vendedor_billete.png", (140, 140))
    datos["img_encargado"] = _load("encargado_vendedor.png", (140, 140))

    datos["mostrador_lvl1"] = _load("mostrador_lvl1.png", (170, 140))
    datos["mostrador_lvl2"] = _load("mostrador_lvl2.png", (170, 140))
    datos["mostrador_lvl3"] = _load("mostrador_lvl3.png", (170, 140))
    datos["mostrador_lvl4"] = _load("mostrador_lvl4.png", (170, 140))

    datos["pos_mostrador"] = pos["mostrador"]
    datos["pos_trabajador"] = pos["trabajador"]
    datos["pos_encargado"] = pos["encargado"]
    datos["pos_boton_enc"] = pos["boton_encargado"]
    datos["pos_texto_flotante"] = pos["texto_flotante"]

    datos["fuente"] = fuente_chica

    datos["level"] = 1
    datos["level_max"] = 40

    datos["base_segundos"] = VELOCIDAD_BASE
    datos["frames_total"] = _calcular_frames(datos["level"], datos["base_segundos"])
    datos["frames_count"] = 0
    datos["trabajando"] = False

    datos["costo_mejora"] = 30
    datos["costo_encargado"] = 220

    datos["precio_venta"] = 10  # cuánto da cada venta

    datos["mostrador_img"] = datos["mostrador_lvl1"]
    datos["rect_mostrador"] = datos["mostrador_img"].get_rect(topleft=datos["pos_mostrador"])
    datos["rect_trabajador"] = datos["img_idle"].get_rect(topleft=datos["pos_trabajador"])

    bm_x, bm_y = pos["boton_mejorar"]
    datos["rect_mejorar"] = pygame.Rect(bm_x, bm_y, 220, 38)

    be_x, be_y = pos["boton_encargado"]
    datos["rect_encargado_btn"] = pygame.Rect(be_x, be_y, 180, 36)

    datos["mostrar_barra"] = True
    datos["barra_w"] = 180
    datos["barra_h"] = 16

    datos["flash_text"] = ""
    datos["flash_timer"] = 0

    _actualizar_sprite_mostrador(datos)
    return datos


def _actualizar_sprite_mostrador(datos):
    lvl = datos["level"]
    if lvl >= 30:
        datos["mostrador_img"] = datos["mostrador_lvl4"]
    elif lvl >= 20:
        datos["mostrador_img"] = datos["mostrador_lvl3"]
    elif lvl >= 10:
        datos["mostrador_img"] = datos["mostrador_lvl2"]
    else:
        datos["mostrador_img"] = datos["mostrador_lvl1"]

    datos["rect_mostrador"] = datos["mostrador_img"].get_rect(topleft=datos["pos_mostrador"])


def _intentar_mejorar(datos):
    if datos["level"] < datos["level_max"]:
        if economia.pagar(datos["costo_mejora"]):
            datos["level"] += 1
            datos["frames_total"] = _calcular_frames(datos["level"], datos["base_segundos"])
            datos["precio_venta"] += 3
            _actualizar_sprite_mostrador(datos)
            datos["costo_mejora"] += 20


def _intentar_comprar_encargado(datos):
    if economia.encargado_vendedor:
        return
    if economia.pagar(datos["costo_encargado"]):
        economia.encargado_vendedor = True


def manejar_evento_vendedor(datos, evento):
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if (datos["rect_mostrador"].collidepoint(evento.pos) or
            datos["rect_trabajador"].collidepoint(evento.pos)):
            if not datos["trabajando"] and economia.cajas > 0:
                datos["trabajando"] = True
                datos["frames_count"] = 0

        if datos["rect_mejorar"].collidepoint(evento.pos):
            _intentar_mejorar(datos)

        if datos["rect_encargado_btn"].collidepoint(evento.pos):
            _intentar_comprar_encargado(datos)

    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_3:
        _intentar_mejorar(datos)


def actualizar_vendedor(datos):
    if (not datos["trabajando"]) and economia.encargado_vendedor and economia.cajas > 0:
        datos["trabajando"] = True
        datos["frames_count"] = 0

    if datos["flash_timer"] > 0:
        datos["flash_timer"] -= 1

    if datos["trabajando"]:
        datos["frames_count"] += 1
        if datos["frames_count"] >= datos["frames_total"]:
            datos["trabajando"] = False
            datos["frames_count"] = 0
            if economia.vender(datos["precio_venta"]):
                datos["flash_text"] = "+$" + str(datos["precio_venta"])
                datos["flash_timer"] = FPS
            return True
    return False


def dibujar_vendedor(pantalla, datos):
    pantalla.blit(datos["mostrador_img"], datos["pos_mostrador"])
    img = datos["img_work"] if datos["trabajando"] else datos["img_idle"]
    pantalla.blit(img, datos["pos_trabajador"])

    if economia.encargado_vendedor:
        pantalla.blit(datos["img_encargado"], datos["pos_encargado"])

    if datos["mostrar_barra"] and datos["trabajando"]:
        bottom = max(datos["rect_mostrador"].bottom, datos["rect_trabajador"].bottom)
        bar_y = bottom + 8
        cx = datos["rect_mostrador"].centerx
        bar_x = cx - datos["barra_w"] // 2

        pygame.draw.rect(pantalla, (40, 40, 40),
                        (bar_x, bar_y, datos["barra_w"], datos["barra_h"]), border_radius=6)

        pct = datos["frames_count"] / max(1, datos["frames_total"])
        fill_w = int(datos["barra_w"] * pct)

        pygame.draw.rect(pantalla, (0, 180, 70),
                        (bar_x, bar_y, fill_w, datos["barra_h"]), border_radius=6)

        pygame.draw.rect(pantalla, (230, 230, 230),
                        (bar_x, bar_y, datos["barra_w"], datos["barra_h"]), 2, border_radius=6)

    # boton mejorar
    pygame.draw.rect(pantalla, (220, 220, 220), datos["rect_mejorar"], border_radius=10)
    pygame.draw.rect(pantalla, (120, 120, 120), datos["rect_mejorar"], 2, border_radius=10)
    if datos["level"] < datos["level_max"]:
        texto_btn = f"Mejorar ${datos['costo_mejora']} - Lvl {datos['level']}"
    else:
        texto_btn = f"LVL {datos['level']} - MAX LVL"
    txt = datos["fuente"].render(texto_btn, True, (20, 20, 20))
    pantalla.blit(txt, txt.get_rect(center=datos["rect_mejorar"].center))


    # boyon encargado
    color_enc = (200, 200, 200) if not economia.encargado_vendedor else (150, 150, 150)
    pygame.draw.rect(pantalla, color_enc, datos["rect_encargado_btn"], border_radius=10)
    pygame.draw.rect(pantalla, (80, 80, 80), datos["rect_encargado_btn"], 2, border_radius=10)

    if economia.encargado_vendedor:
        txt_enc = "Encargado listo"
    else:
        txt_enc = f"Encargado ${datos['costo_encargado']}"

    txt2 = datos["fuente"].render(txt_enc, True, (10, 10, 10))
    pantalla.blit(txt2, txt2.get_rect(center=datos["rect_encargado_btn"].center))

    # texto flotante
    if datos["flash_timer"] > 0:
        fx, fy = datos["pos_texto_flotante"]
        txtf = datos["fuente"].render(datos["flash_text"], True, (0, 255, 255))
        pantalla.blit(txtf, (fx, fy))

def cargar_estado_vendedor(datos, datos_save):
    datos["level"] = datos_save.get("level", 1)
    datos["costo_mejora"] = datos_save.get("costo_mejora", datos["costo_mejora"])
    datos["costo_encargado"] = datos_save.get("costo_encargado", datos["costo_encargado"])
    datos["precio_venta"] = datos_save.get("precio_venta", datos["precio_venta"])

    datos["frames_total"] = _calcular_frames(datos["level"], datos["base_segundos"])
    _actualizar_sprite_mostrador(datos)


def guardar_estado_vendedor(datos):
    return {
        "level": datos["level"],
        "costo_mejora": datos["costo_mejora"],
        "costo_encargado": datos["costo_encargado"],
        "precio_venta": datos["precio_venta"],
    }
