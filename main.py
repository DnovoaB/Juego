import pygame
import sys
import os
from levels.level_1 import Level1
from levels.level_2 import Level2
from levels.level_3 import Level3
from levels.level_4 import Level4
from src.utils import draw_text, play_music, stop_music

class Game:
    def __init__(self):
        # Inicializar Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Configuración de la ventana
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Geralt: La Sombra del Abismo")
        
        # Estados del juego
        self.current_level = 1
        self.game_state = "MENU"
        self.clock = pygame.time.Clock()
        
        # Intentar reproducir música del menú
        try:
            if os.path.exists(os.path.join("assets/sounds", "menu_theme.mp3")):
                play_music("menu_theme.mp3", volume=0.5)
            else:
                print("⚠️ Música del menú no encontrada, continuando sin música")
        except Exception as e:
            print(f"⚠️ Error al iniciar la música: {e}")

    def main_menu(self):
        """Pantalla del menú principal."""
        while self.game_state == "MENU":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_state = "PLAYING"
                        stop_music()
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        return False

            # Dibujar menú
            self.screen.fill((0, 0, 0))
            
            # Título
            draw_text(
                self.screen,
                "Geralt: La Sombra del Abismo",
                (200, 150),
                font_size=50,
                color=(255, 215, 0)
            )
            
            # Opciones del menú
            draw_text(
                self.screen,
                "Presiona ENTER para comenzar",
                (250, 300)
            )
            draw_text(
                self.screen,
                "Presiona ESC para salir",
                (300, 350)
            )
            
            # Créditos
            draw_text(
                self.screen,
                "© 2024 Tu Nombre",
                (350, 550),
                font_size=20,
                color=(128, 128, 128)
            )
            
            pygame.display.flip()
            self.clock.tick(60)

    def game_over_screen(self):
        """Pantalla de Game Over."""
        play_music("game_over.mp3", loop=False, volume=0.7)
        
        while self.game_state == "GAME_OVER":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.current_level = 1
                        self.game_state = "PLAYING"
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "MENU"
                        return True

            # Dibujar pantalla de game over
            self.screen.fill((0, 0, 0))
            draw_text(
                self.screen,
                "GAME OVER",
                (300, 200),
                font_size=60,
                color=(255, 0, 0)
            )
            draw_text(
                self.screen,
                "Presiona R para reintentar",
                (250, 300)
            )
            draw_text(
                self.screen,
                "Presiona ESC para volver al menú",
                (200, 350)
            )
            
            pygame.display.flip()
            self.clock.tick(60)

    def victory_screen(self):
        """Pantalla de Victoria."""
        play_music("victory.mp3", loop=False, volume=0.7)
        
        while self.game_state == "VICTORY":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.current_level = 1
                        self.game_state = "PLAYING"
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "MENU"
                        return True

            # Dibujar pantalla de victoria
            self.screen.fill((0, 0, 0))
            draw_text(
                self.screen,
                "¡VICTORIA!",
                (300, 200),
                font_size=60,
                color=(255, 215, 0)
            )
            draw_text(
                self.screen,
                "Has derrotado a la oscuridad",
                (200, 280),
                font_size=30
            )
            draw_text(
                self.screen,
                "Presiona R para jugar de nuevo",
                (250, 350)
            )
            draw_text(
                self.screen,
                "Presiona ESC para volver al menú",
                (200, 400)
            )
            
            pygame.display.flip()
            self.clock.tick(60)

    def run_level(self):
        """Ejecuta el nivel actual."""
        level_map = {
            1: Level1,
            2: Level2,
            3: Level3,
            4: Level4
        }
        
        if self.current_level in level_map:
            level = level_map[self.current_level](self.screen)
            victory = level.run()
            
            if victory:
                if self.current_level < 4:
                    self.current_level += 1
                    return True
                else:
                    self.game_state = "VICTORY"
            else:
                self.game_state = "GAME_OVER"
        
        return False

    def run(self):
        """Loop principal del juego."""
        running = True
        
        while running:
            if self.game_state == "MENU":
                running = self.main_menu()
            elif self.game_state == "PLAYING":
                continue_playing = self.run_level()
                if not continue_playing:
                    running = False
            elif self.game_state == "GAME_OVER":
                running = self.game_over_screen()
            elif self.game_state == "VICTORY":
                running = self.victory_screen()
            
            self.clock.tick(60)

        # Limpieza final
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # Crear y ejecutar el juego
    game = Game()
    game.run()