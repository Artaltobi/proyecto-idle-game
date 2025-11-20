import pygame
from settings import WIDTH, HEIGHT, FPS, RUTA_MUSICA 
from menu import run_menu
from overworld import OverworldScreen
from save import load_game


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Idle Factory")
    reloj = pygame.time.Clock()

    # -- MUSICA DE FONDO ----
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(RUTA_MUSICA)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("No se pudo cargar la música:", e)

    # Clase simple para guardar datos globales del juego
    class Game:
        def __init__(self, pantalla, reloj, nombre_jugador):
            self.pantalla = pantalla
            self.reloj = reloj
            self.nombre_jugador = nombre_jugador
            self.ejecutando = True  # si se pone en False, se cierra todo

    corriendo = True
    while corriendo:
        # ---- MENU PRINCIPAL ----
        accion, _ = run_menu(pantalla, reloj)

        if accion == "salir":
            corriendo = False

        elif accion == "jugar":
            # cargamos el save
            datos = load_game()
            nombre = datos.get("nombre", "Jugador")

            # creamos el objeto Game y el overworld
            game = Game(pantalla, reloj, nombre)
            overworld = OverworldScreen(game, datos)

            jugando = True
            while jugando and game.ejecutando:
                reloj.tick(FPS)

                overworld.update()
                overworld.draw(pantalla)
                pygame.display.flip()

                if overworld.salir_al_menu:
                    jugando = False   # salimos del overworld y volvemos al menú

            # si desde algún lado pusimos game.ejecutando = False → cerrar todo
            if not game.ejecutando:
                corriendo = False

    pygame.quit()


if __name__ == "__main__":
    main()
