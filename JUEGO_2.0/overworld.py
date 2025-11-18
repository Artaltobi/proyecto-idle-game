import pygame
from settings import WIDTH, HEIGHT
from screens.game import run_game as run_fabrica_medias
from save import save_game
from ui import Button

MAP_SCALE = 2
PLAYER_SPEED = 6
PLAYER_SCALE = 0.2

FABRICAS = {
    1: pygame.Rect(350, 450, 450, 450),
    2: pygame.Rect(1700, 700, 450, 450),
    3: pygame.Rect(2150, 1450, 450, 450)
}

# Iconos de UI (mute / menú) vienen de la carpeta del juego de fábrica
IMAGES_DIR_UI = "mi_juego/assets/images/"
# Sprites del personaje y fondo del overworld
IMAGES_DIR_OVERWORLD = "JUEGO_2.0/assets/images/"


# ---------- helpers ----------

def cargar_imagen_ui(nombre, size=None):
    ruta = IMAGES_DIR_UI + nombre
    img = pygame.image.load(ruta).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img


def cargar_sprite_overworld(nombre, scale=PLAYER_SCALE):
    """Carga y escala un sprite del overworld."""
    ruta = IMAGES_DIR_OVERWORLD + nombre
    img = pygame.image.load(ruta).convert_alpha()
    w = int(img.get_width() * scale)
    h = int(img.get_height() * scale)
    return pygame.transform.scale(img, (w, h))


def toggle_mute(sonando):
    """Pausa o reanuda la música global."""
    if not pygame.mixer.get_init():
        return sonando

    if sonando:
        pygame.mixer.music.pause()
        return False
    else:
        pygame.mixer.music.unpause()
        return True
# ------------------------------


class OverworldScreen:
    def __init__(self, game, save_data):
        self.game = game
        self.save_data = save_data

        self.fabrica_actual = None
        self.morido = False      # 🔥 estado de muerte
        self.salir_al_menu = False  # 🔙 flag para volver al menú

        # ---------- mapa de fondo ----------
        original = pygame.image.load(
            IMAGES_DIR_OVERWORLD + "fondo_overworld.png"
        ).convert()

        big_width = original.get_width() * MAP_SCALE
        big_height = original.get_height() * MAP_SCALE
        self.map_surface = pygame.transform.scale(original, (big_width, big_height))
        self.map_rect = self.map_surface.get_rect()

        # ---------- jugador ----------
        # sprites escalados
        self.pj_frente = cargar_sprite_overworld("pj_frente.png")
        self.pj_derecha = cargar_sprite_overworld("pj_derecha.png")
        self.pj_izquierda = cargar_sprite_overworld("pj_izquierda.png")
        self.pj_atras = cargar_sprite_overworld("pj_atras.png")

        # tamaño lógico para colisiones, basado en el sprite escalado
        self.player_size = max(self.pj_frente.get_width(), self.pj_frente.get_height())

        # posición inicial en el centro del mapa
        self.player_x = self.map_rect.centerx
        self.player_y = self.map_rect.centery

        # sprite actual (empieza mirando al frente)
        self.player_img = self.pj_frente

        # zona de muerte en la esquina inferior izquierda (ajustá a gusto)
        self.death_zone = pygame.Rect(0, self.map_rect.height - 500, 500, 500)

        self.font = pygame.font.SysFont(None, 36)
        self.font_big = pygame.font.SysFont(None, 72)

        # ---------- UI: botones e íconos (mute + menú) ----------
        self.icon_on = cargar_imagen_ui("music_on.png", (40, 40))
        self.icon_off = cargar_imagen_ui("music_off.png", (40, 40))
        self.icon_menu = cargar_imagen_ui("exit.png", (40, 40))

        # mismos tamaños/posiciones que en game.py
        self.btn_mute = Button((WIDTH - 80, 20, 48, 48), "", self.font)
        self.btn_menu = Button((20, 20, 48, 48), "", self.font)

        self.sonando = True if pygame.mixer.get_init() else False
        # --------------------------------------------------------

    # 👇 NUEVO: función para perder todo el progreso
    def perder_progreso(self):
        """Resetea todo el save cuando el jugador muere."""
        self.save_data.clear()
        self.save_data.update({
            "nombre": self.game.nombre_jugador,
            "fabrica_medias": {},
            "fabrica_shorts": {},
            "fabrica_remeras": {},
        })
        save_game(self.save_data)

    def entrar_a_fabrica(self):
        """Entra al minijuego de la fábrica según la fábrica actual."""
        if not self.fabrica_actual:
            return

        resultado = run_fabrica_medias(
            self.game.pantalla,
            self.game.reloj,
            self.game.nombre_jugador,
            self.save_data,
        )

        # Al volver de la fábrica, guardamos en disco
        save_game(self.save_data)

        # si desde la fábrica eligió cerrar todo
        if resultado == "salir_total":
            self.game.ejecutando = False

    def update(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

            # si está muerto, solo escuchamos ENTER para respawn
            if self.morido and e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                self.respawn()

            # clicks de mouse (botones mute / menú)
            if not self.morido and e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.btn_mute.clicked(e):
                    self.sonando = toggle_mute(self.sonando)
                if self.btn_menu.clicked(e):
                    # marcar que queremos volver al menú
                    self.salir_al_menu = True

        # si está muerto, no se mueve ni entra a fábricas
        if self.morido:
            return

        # si ya apretó el botón de menú, no seguimos procesando movimiento
        if self.salir_al_menu:
            return

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        # primero resolvemos movimiento
        if keys[pygame.K_w]:
            dy = -PLAYER_SPEED
        if keys[pygame.K_s]:
            dy = PLAYER_SPEED
        if keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_d]:
            dx = PLAYER_SPEED

        # luego elegimos sprite según la última dirección pulsada
        if keys[pygame.K_w]:
            self.player_img = self.pj_atras
        elif keys[pygame.K_s]:
            self.player_img = self.pj_frente
        elif keys[pygame.K_d]:
            self.player_img = self.pj_derecha
        elif keys[pygame.K_a]:
            self.player_img = self.pj_izquierda
        else:
            # quieto: mirando al frente
            self.player_img = self.pj_frente

        # mover jugador
        self.player_x += dx
        self.player_y += dy

        # evitar salir del mapa
        if self.player_x < 0:
            self.player_x = 0
        if self.player_y < 0:
            self.player_y = 0
        if self.player_x > self.map_rect.width:
            self.player_x = self.map_rect.width
        if self.player_y > self.map_rect.height:
            self.player_y = self.map_rect.height

        # detectar muerte por agua 🔥
        jugador_rect_mundo = pygame.Rect(
            self.player_x - self.player_size / 2,
            self.player_y - self.player_size / 2,
            self.player_size,
            self.player_size
        )
        if jugador_rect_mundo.colliderect(self.death_zone):
            self.morido = True
            self.perder_progreso()   # 👈 acá se borra TODO el progreso
            return

        # detectar fábrica cercana
        self.fabrica_actual = None
        for fid, rect in FABRICAS.items():
            if self.jugador_cerca(rect):
                self.fabrica_actual = fid
                break

        # entrar con E
        if keys[pygame.K_e] and self.fabrica_actual:
            self.entrar_a_fabrica()

    def get_camera_offset(self):
        offset_x = int(self.player_x - WIDTH / 2)
        offset_y = int(self.player_y - HEIGHT / 2)

        if offset_x < 0:
            offset_x = 0
        if offset_y < 0:
            offset_y = 0

        max_offset_x = self.map_rect.width - WIDTH
        max_offset_y = self.map_rect.height - HEIGHT

        if offset_x > max_offset_x:
            offset_x = max_offset_x
        if offset_y > max_offset_y:
            offset_y = max_offset_y

        return offset_x, offset_y

    def draw(self, surface):
        offset_x, offset_y = self.get_camera_offset()

        surface.blit(self.map_surface, (-offset_x, -offset_y))

        # ---------- dibujar jugador con sprite ----------
        center_x = int(self.player_x - offset_x)
        center_y = int(self.player_y - offset_y)
        sprite_rect = self.player_img.get_rect(center=(center_x, center_y))
        surface.blit(self.player_img, sprite_rect)
        # ------------------------------------------------

        # dibujar fábricas (rectángulos de referencia)
        for fid, rect in FABRICAS.items():
            pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(
                rect.x - offset_x,
                rect.y - offset_y,
                rect.width,
                rect.height
            ), 2)

        # dibujar zona de muerte (debug, podés borrar esto después)
        pygame.draw.rect(surface, (0, 0, 255), pygame.Rect(
            self.death_zone.x - offset_x,
            self.death_zone.y - offset_y,
            self.death_zone.width,
            self.death_zone.height
        ), 2)

        # texto si estás cerca de una fábrica
        if self.fabrica_actual and not self.morido:
            txt = self.font.render("Presiona E para entrar", True, (255, 255, 255))
            surface.blit(txt, (WIDTH // 2 - 150, HEIGHT - 80))

        # botones de interfaz (menu + mute)
        surface.blit(self.icon_menu, self.icon_menu.get_rect(center=self.btn_menu.rect.center))
        icono_actual = self.icon_on if self.sonando else self.icon_off
        surface.blit(icono_actual, icono_actual.get_rect(center=self.btn_mute.rect.center))

        # pantalla de muerte
        if self.morido:
            self.draw_death_screen(surface)

    def draw_death_screen(self, surface):
        # capa oscura
        capa = pygame.Surface((WIDTH, HEIGHT))
        capa.set_alpha(160)
        capa.fill((0, 0, 0))
        surface.blit(capa, (0, 0))

        txt1 = self.font_big.render("Te ahogaste", True, (255, 50, 50))
        txt2 = self.font.render("Perdiste todo el progreso", True, (255, 255, 255))
        txt3 = self.font.render("ENTER para volver a intentarlo", True, (255, 255, 255))

        surface.blit(txt1, txt1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        surface.blit(txt2, txt2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))
        surface.blit(txt3, txt3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

    def respawn(self):
        self.morido = False
        self.player_x = self.map_rect.centerx
        self.player_y = self.map_rect.centery

    def jugador_cerca(self, rect):
        p = pygame.Rect(
            self.player_x - self.player_size / 2,
            self.player_y - self.player_size / 2,
            self.player_size,
            self.player_size
        )
        return p.colliderect(rect)
