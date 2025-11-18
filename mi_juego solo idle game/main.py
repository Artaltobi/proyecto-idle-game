import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE, RUTA_MUSICA
from screens.menu import run_menu
from screens.game import run_game  # NUEVO import

def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    reloj = pygame.time.Clock()

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(RUTA_MUSICA)
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("No se pudo iniciar musica:", e)

    decision, nombre = run_menu(pantalla, reloj)

    if decision == "jugar":
        resultado = run_game(pantalla, reloj, nombre)
        if resultado == "salir_total":
            pygame.quit(); return
        # si vuelve al menu, podrías reabrir el menu:
        # decision, nombre = run_menu(pantalla, reloj)

    pygame.quit()

if __name__ == "__main__":
    main()
