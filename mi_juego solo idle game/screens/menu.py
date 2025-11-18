# screens/menu.py
import os, json, pygame
from settings import (
    WIDTH, HEIGHT, FPS, BLANCO, RUTA_FONDO,
    RUTA_ICONO_MUSICA_ON, RUTA_ICONO_MUSICA_OFF, SAVE_PATH, TITLE
)
from ui import Button, TextInput

def _cargar_fondo():
    if os.path.exists(RUTA_FONDO):
        img = pygame.image.load(RUTA_FONDO).convert()
        return pygame.transform.scale(img, (WIDTH, HEIGHT))
    s = pygame.Surface((WIDTH, HEIGHT)); s.fill((25,30,40)); return s

def _cargar_iconos_musica():
    def _load(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (40, 40))
    return _load(RUTA_ICONO_MUSICA_ON), _load(RUTA_ICONO_MUSICA_OFF)

def _toggle_mute(sonando: bool) -> bool:
    if not pygame.mixer.get_init():
        return sonando
    if sonando:
        pygame.mixer.music.pause();  return False
    else:
        pygame.mixer.music.unpause(); return True

def _hay_guardado() -> bool:
    return os.path.exists(SAVE_PATH)

def _guardar_save(nombre: str):
    try:
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump({"nombre": nombre}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("no se pudo guardar:", e)

def _cargar_save_nombre() -> str:
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return str(data.get("nombre", "")).strip()
    except:
        return ""

def run_menu(pantalla, reloj):
    f_h1  = pygame.font.SysFont(None, 72)
    f_btn = pygame.font.SysFont(None, 48)
    f_sm  = pygame.font.SysFont(None, 28)

    fondo = _cargar_fondo()
    icon_on, icon_off = _cargar_iconos_musica()
    sonando = True if pygame.mixer.get_init() else False

    estado = "menu_principal"
    nombre = ""
    tiene_save = _hay_guardado()

    # esto dice a donde ir despues de escribir nombre
    siguiente_despues_nombre = "jugar"   # por defecto lo dejamos en jugar
    input_box = None

    while True:
        reloj.tick(FPS)
        pantalla.blit(fondo, (0, 0))

        btn_jugar = btn_mute = btn_cont = btn_volver = None
        btn_continuar = btn_nueva = None

        if estado == "menu_principal":
            titulo = f_h1.render(TITLE, True, BLANCO)
            pantalla.blit(titulo, titulo.get_rect(center=(WIDTH//2, 110)))

            btn_jugar = Button((WIDTH//2-220, HEIGHT//2-40, 440, 80), "Jugar", f_btn)
            btn_mute  = Button((WIDTH-80, 20, 48, 48), "", f_sm)

            btn_jugar.draw(pantalla)
            icono = icon_on if sonando else icon_off
            pantalla.blit(icono, icono.get_rect(center=btn_mute.rect.center))

        elif estado == "pedir_nombre":
            titulo = f_h1.render("Escribe tu nombre:", True, BLANCO)
            pantalla.blit(titulo, titulo.get_rect(center=(WIDTH//2, 180)))

            if input_box is None:
                input_box = TextInput((WIDTH//2-260, HEIGHT//2-35, 520, 70), f_btn)
                input_box.texto = ""

            btn_cont   = Button((WIDTH//2-220, HEIGHT//2+80, 440, 70), "Continuar", f_btn)
            btn_volver = Button((WIDTH//2-220, HEIGHT//2+170, 440, 70), "Volver", f_btn)
            btn_mute   = Button((WIDTH-80, 20, 48, 48), "", f_sm)

            input_box.update(); input_box.draw(pantalla)
            btn_cont.draw(pantalla); btn_volver.draw(pantalla)
            icono = icon_on if sonando else icon_off
            pantalla.blit(icono, icono.get_rect(center=btn_mute.rect.center))

        elif estado == "continuar_o_nueva":
            titulo = f_h1.render("Menu", True, BLANCO)
            pantalla.blit(titulo, titulo.get_rect(center=(WIDTH//2, 110)))

            btn_continuar = Button((WIDTH//2-220, HEIGHT//2-60, 440, 80), "Continuar", f_btn)
            btn_nueva     = Button((WIDTH//2-220, HEIGHT//2+40, 440, 80), "Nueva partida", f_btn)
            btn_mute      = Button((WIDTH-80, 20, 48, 48), "", f_sm)

            if not tiene_save:
                btn_continuar.color_base = btn_continuar.color_hover = (170,170,170)

            btn_continuar.draw(pantalla); btn_nueva.draw(pantalla)
            icono = icon_on if sonando else icon_off
            pantalla.blit(icono, icono.get_rect(center=btn_mute.rect.center))

        pygame.display.flip()

        # ------------- eventos -------------
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return ("salir", nombre)

            if estado == "menu_principal":
                if btn_mute and btn_mute.clicked(e):
                    sonando = _toggle_mute(sonando)
                if btn_jugar and btn_jugar.clicked(e):
                    # ACA estaba el problema: antes ponias "continuar_o_nueva"
                    siguiente_despues_nombre = "jugar"
                    input_box = None
                    estado = "pedir_nombre"

            elif estado == "pedir_nombre":
                if btn_mute and btn_mute.clicked(e):
                    sonando = _toggle_mute(sonando)

                if btn_volver and btn_volver.clicked(e):
                    estado = "menu_principal"
                    input_box = None
                    continue

                res = input_box.handle_event(e) if input_box else None

                if (e.type == pygame.MOUSEBUTTONDOWN and btn_cont and btn_cont.is_hover()) or res == "enter":
                    if input_box and input_box.texto.strip() != "":
                        nombre = input_box.texto.strip()
                        if siguiente_despues_nombre == "jugar":
                            _guardar_save(nombre)
                            return ("jugar", nombre)
                        else:
                            estado = "continuar_o_nueva"
                            tiene_save = _hay_guardado()

            elif estado == "continuar_o_nueva":
                if btn_mute and btn_mute.clicked(e):
                    sonando = _toggle_mute(sonando)

                if btn_continuar and btn_continuar.clicked(e) and tiene_save:
                    n = _cargar_save_nombre()
                    if n: nombre = n
                    return ("jugar", nombre)

                if btn_nueva and btn_nueva.clicked(e):
                    # aca si queremos que vuelva a pedir nombre y entre directo
                    siguiente_despues_nombre = "jugar"
                    input_box = None
                    estado = "pedir_nombre"
