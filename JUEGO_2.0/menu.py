# screens/menu.py
import os, json, pygame
from settings import (
    WIDTH, HEIGHT, FPS, BLANCO, RUTA_FONDO,
    RUTA_ICONO_MUSICA_ON, RUTA_ICONO_MUSICA_OFF, SAVE_PATH, TITLE
)
from ui import Button

# ----------------- helpers simples -----------------

def cargar_fondo():
    if os.path.exists(RUTA_FONDO):
        img = pygame.image.load(RUTA_FONDO).convert()
        return pygame.transform.scale(img, (WIDTH, HEIGHT))
    fondo = pygame.Surface((WIDTH, HEIGHT))
    fondo.fill((25, 30, 40))
    return fondo

def cargar_iconos_musica():
    img_on = pygame.image.load(RUTA_ICONO_MUSICA_ON).convert_alpha()
    img_off = pygame.image.load(RUTA_ICONO_MUSICA_OFF).convert_alpha()
    img_on = pygame.transform.scale(img_on, (40, 40))
    img_off = pygame.transform.scale(img_off, (40, 40))
    return img_on, img_off

def toggle_mute(sonando):
    if not pygame.mixer.get_init():
        return sonando
    if sonando:
        pygame.mixer.music.pause()
        return False
    else:
        pygame.mixer.music.unpause()
        return True

def cargar_save():
    if not os.path.exists(SAVE_PATH):
        # valores por defecto si no hay partida
        return {"money": 0, "factories": []}
    try:
        f = open(SAVE_PATH, "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        return data
    except:
        return {"money": 0, "factories": []}

def calcular_porcentaje(data):
    # si no hay fábricas, 0%
    facs = data.get("factories", [])
    if len(facs) == 0:
        return 0

    # contamos cuántas están desbloqueadas
    desbloq = 0
    for f in facs:
        if f.get("unlocked", 0) == 1:
            desbloq = desbloq + 1

    # contamos cuántas tienen nivel 40 o más
    nivel_ok = 0
    for f in facs:
        if f.get("max_level", 0) >= 40:
            nivel_ok = nivel_ok + 1

    porc = 0
    if desbloq == 3:
        porc = porc + 50
    if nivel_ok == 3:
        porc = porc + 50
    return porc

# ----------------- menú principal -----------------

def run_menu(pantalla, reloj):
    fuente_titulo = pygame.font.SysFont(None, 72)
    fuente_btn    = pygame.font.SysFont(None, 48)
    fuente_sm     = pygame.font.SysFont(None, 28)

    fondo = cargar_fondo()
    icon_on, icon_off = cargar_iconos_musica()
    sonando = True if pygame.mixer.get_init() else False

    estado = "menu"  # puede ser "menu" o "datos"

    while True:
        reloj.tick(FPS)
        pantalla.blit(fondo, (0, 0))

        btn_jugar = btn_datos = btn_salir = btn_mute = None
        btn_volver = None

        # ----------- DIBUJAR -----------
        if estado == "menu":
            titulo = fuente_titulo.render(TITLE, True, BLANCO)
            pantalla.blit(titulo, titulo.get_rect(center=(WIDTH//2, 120)))

            btn_jugar = Button((WIDTH//2-220, HEIGHT//2-80, 440, 70), "Jugar", fuente_btn)
            btn_datos = Button((WIDTH//2-220, HEIGHT//2+10, 440, 70), "Datos", fuente_btn)
            btn_salir = Button((WIDTH//2-220, HEIGHT//2+100, 440, 70), "Salir", fuente_btn)
            btn_mute  = Button((WIDTH-80, 20, 48, 48), "", fuente_sm)

            btn_jugar.draw(pantalla)
            btn_datos.draw(pantalla)
            btn_salir.draw(pantalla)

            icono = icon_on if sonando else icon_off
            pantalla.blit(icono, icono.get_rect(center=btn_mute.rect.center))

        elif estado == "datos":
            data = cargar_save()
            porc = calcular_porcentaje(data)
            dinero = data.get("money", 0)

            titulo = fuente_titulo.render("Datos de partida", True, BLANCO)
            pantalla.blit(titulo, titulo.get_rect(center=(WIDTH//2, 100)))

            txt1 = fuente_btn.render("Progreso: " + str(porc) + "%", True, BLANCO)
            txt2 = fuente_btn.render("Dinero: $" + str(dinero), True, BLANCO)
            pantalla.blit(txt1, (WIDTH//2-220, HEIGHT//2-60))
            pantalla.blit(txt2, (WIDTH//2-220, HEIGHT//2))

            y = HEIGHT//2 + 80
            for f in data.get("factories", []):
                nombre = f.get("name", "fabrica")
                desbloq = "SI" if f.get("unlocked", 0) == 1 else "NO"
                linea = nombre + " desbloqueada: " + desbloq
                txt = fuente_sm.render(linea, True, BLANCO)
                pantalla.blit(txt, (WIDTH//2-220, y))
                y = y + 30

            btn_volver = Button((WIDTH//2-150, HEIGHT-120, 300, 60), "Volver", fuente_btn)
            btn_volver.draw(pantalla)

        pygame.display.flip()

        # ----------- EVENTOS -----------
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return ("salir", None)

            if estado == "menu":
                if btn_mute and btn_mute.clicked(e):
                    sonando = toggle_mute(sonando)

                if btn_jugar and btn_jugar.clicked(e):
                    # acá no hacemos nada más, dejamos que main cargue el save
                    return ("jugar", None)

                if btn_datos and btn_datos.clicked(e):
                    estado = "datos"

                if btn_salir and btn_salir.clicked(e):
                    return ("salir", None)

            elif estado == "datos":
                if btn_volver and btn_volver.clicked(e):
                    estado = "menu"
