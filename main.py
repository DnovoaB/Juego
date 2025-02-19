import pygame
from levels.level_1 import Level1
from levels.level_2 import Level2
from levels.level_3 import Level3
from levels.level_4 import Level4
from src.utils import draw_text, load_image
from src.player import Player

# Configuración de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Geralt: La Sombra del Abismo")

        self.clock = pygame.time.Clock()
        self.running = True
        self.levels = [Level1, Level2, Level3, Level4]
        self.current_level_index = 0
        self.player = Player(50, 300)
        self.background = load_image("assets/images/ui/menu_background.png")

    def run(self):
        while self.running:
            self.show_main_menu()
            for level_class in self.levels:
                level = level_class(self.screen)
                level.run()
                if not self.running:
                    break  # Si el usuario cierra el juego, salir del bucle

            self.show_game_over_screen()

    def show_main_menu(self):
        menu_running = True
        while menu_running:
            self.screen.blit(self.background, (0, 0))
            draw_text(self.screen, "Geralt: La Sombra del Abismo", (SCREEN_WIDTH // 2 - 150, 100))
            draw_text(self.screen, "Presiona ENTER para comenzar", (SCREEN_WIDTH // 2 - 100, 300))
            draw_text(self.screen, "Presiona ESC para salir", (SCREEN_WIDTH // 2 - 80, 350))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    menu_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        menu_running = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        menu_running = False

    def show_game_over_screen(self):
        game_over_running = True
        while game_over_running:
            self.screen.fill((0, 0, 0))
            draw_text(self.screen, "Juego Terminado", (SCREEN_WIDTH // 2 - 80, 250))
            draw_text(self.screen, "Presiona ENTER para reiniciar", (SCREEN_WIDTH // 2 - 100, 300))
            draw_text(self.screen, "Presiona ESC para salir", (SCREEN_WIDTH // 2 - 80, 350))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    game_over_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.current_level_index = 0  # Reinicia niveles
                        game_over_running = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        game_over_running = False

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
