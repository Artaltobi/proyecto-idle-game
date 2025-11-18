# screens/overworld.py
import pygame
from settings import WIDTH, HEIGHT

MAP_SCALE = 2
PLAYER_SPEED = 10

FABRICAS = {
    1: pygame.Rect(350, 450, 450, 450),
    2: pygame.Rect(1700, 700, 450, 450),
    3: pygame.Rect(2150, 1450, 450, 450)
}

class OverworldScreen:
    def __init__(self, game, save_data):
        self.game = game
        self.save_data = save_data

        self.fabrica_actual = None  # 🔥 MUY IMPORTANTE

        original = pygame.image.load("JUEGO_2.0/assets/images/fondo_overworld.png").convert()

        big_width = original.get_width() * MAP_SCALE
        big_height = original.get_height() * MAP_SCALE
        self.map_surface = pygame.transform.scale(original, (big_width, big_height))
        self.map_rect = self.map_surface.get_rect()

        self.player_size = 20
        self.player_x = self.map_rect.centerx
        self.player_y = self.map_rect.centery

        self.font = pygame.font.SysFont(None, 36)  # 🔥 fuente para el texto

    def update(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0
        if keys[pygame.K_w]:
            dy = -PLAYER_SPEED
        if keys[pygame.K_s]:
            dy = PLAYER_SPEED
        if keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_d]:
            dx = PLAYER_SPEED

        # detectar fábrica cercana
        self.fabrica_actual = None
        for fid, rect in FABRICAS.items():
            if self.jugador_cerca(rect):
                self.fabrica_actual = fid
                break

        # entrar con E
        if keys[pygame.K_e] and self.fabrica_actual:
            self.game.change_screen("factory", self.save_data, self.fabrica_actual)

        # mover jugador
        self.player_x += dx
        self.player_y += dy

        # evitar salir del mapa
        self.player_x = max(0, min(self.player_x, self.map_rect.width))
        self.player_y = max(0, min(self.player_y, self.map_rect.height))

    def get_camera_offset(self):
        offset_x = int(self.player_x - WIDTH / 2)
        offset_y = int(self.player_y - HEIGHT / 2)

        offset_x = max(0, min(offset_x, self.map_rect.width - WIDTH))
        offset_y = max(0, min(offset_y, self.map_rect.height - HEIGHT))

        return offset_x, offset_y

    def draw(self, surface):
        offset_x, offset_y = self.get_camera_offset()

        surface.blit(self.map_surface, (-offset_x, -offset_y))

        # dibujar jugador
        screen_x = int(self.player_x - offset_x - self.player_size / 2)
        screen_y = int(self.player_y - offset_y - self.player_size / 2)

        player_rect = pygame.Rect(screen_x, screen_y, self.player_size, self.player_size)
        pygame.draw.rect(surface, (255, 255, 0), player_rect)

        # dibujar fábricas
        for fid, rect in FABRICAS.items():
            pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(
                rect.x - offset_x,
                rect.y - offset_y,
                rect.width,
                rect.height
            ), 2)

        # texto si estás cerca
        if self.fabrica_actual:
            texto = self.font.render("Presiona E para entrar", True, (255,255,255))
            surface.blit(texto, (WIDTH//2 - 150, HEIGHT - 80))

    def jugador_cerca(self, rect):
        p = pygame.Rect(self.player_x, self.player_y, self.player_size, self.player_size)
        return p.colliderect(rect)
