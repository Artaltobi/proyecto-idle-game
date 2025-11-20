import pygame
from settings import GRIS_OSCURO

class Button:
    # boton rectangular con borde redondeado y hover
    def __init__(self, rect, texto, fuente,
                color_base=(230,230,230), color_hover=(200,200,200), color_texto=(20,20,20)):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.fuente = fuente
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_texto = color_texto
    def draw(self, surface):
        color = self.color_hover if self.is_hover() else self.color_base
        pygame.draw.rect(surface, color, self.rect, border_radius=22)
        pygame.draw.rect(surface, GRIS_OSCURO, self.rect, width=2, border_radius=22)
        if self.texto:
            img = self.fuente.render(self.texto, True, self.color_texto)
            surface.blit(img, img.get_rect(center=self.rect.center))
    def is_hover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hover()


class TextInput:
    # cuadro de texto editable basico con cursor que parpadea
    def __init__(self, rect, fuente, max_len=16, placeholder="....."):
        self.rect = pygame.Rect(rect)
        self.fuente = fuente
        self.max_len = max_len
        self.placeholder = placeholder
        self.texto = ""
        self.activo = False        
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 450 

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.cursor_timer >= self.cursor_interval:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = now

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.activo = self.rect.collidepoint(event.pos)

        if not self.activo:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "enter"
            elif event.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            else:
                if len(self.texto) < self.max_len and event.unicode.isprintable():
                    self.texto += event.unicode
        return None

    def draw(self, surface):
        # caja
        pygame.draw.rect(surface, (235,235,235), self.rect, border_radius=18)
        pygame.draw.rect(surface, GRIS_OSCURO, self.rect, 2, border_radius=18)

        # texto
        mostrar = self.texto if (self.texto != "" or self.activo) else self.placeholder
        color_txt = (30,30,30) if self.texto != "" or self.activo else (120,120,120)
        img = self.fuente.render(mostrar, True, color_txt)
        pos_txt = img.get_rect(midleft=(self.rect.x + 18, self.rect.centery))
        surface.blit(img, pos_txt)

        # cursor
        if self.activo and self.cursor_visible:
            x = pos_txt.right + 2
            pygame.draw.line(surface, (30,30,30), (x, self.rect.y+12), (x, self.rect.bottom-12), 2)
