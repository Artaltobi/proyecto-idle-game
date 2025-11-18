# main.py
import pygame
from settings import WIDTH, HEIGHT, FPS
from menu import run_menu
from overworld import OverworldScreen
from save import load_game


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Idle Factory")
    reloj = pygame.time.Clock()

    game = None  # se define después

    corriendo = True
    while corriendo:
        accion, _ = run_menu(pantalla, reloj)

        if accion == "salir":
            corriendo = False

        elif accion == "jugar":
            datos = load_game()

            # Creamos overworld pasando game + save_data
            # Primero creamos un objeto temporal para pasarlo a overworld
            class Dummy:
                pass
            game = Dummy()

            overworld = OverworldScreen(game, datos)

            jugando = True
            while jugando:
                reloj.tick(FPS)

                overworld.update()
                overworld.draw(pantalla)

                pygame.display.flip()

                # si overworld quiere salir (por pygame.QUIT) va a cerrar todo
                # si querés agregar salir al menú, lo hacemos después

    pygame.quit()


if __name__ == "__main__":
    main()
