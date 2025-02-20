import pygame
import random
from src.player import Player
from src.enemies import Ghost1, Ghost2
from src.utils import (
    load_background, 
    draw_text, 
    draw_game_ui, 
    play_music, 
    show_floating_text,
    create_placeholder_image
)

class Level2:
    def __init__(self, screen):
        self.screen = screen
        self.background = load_background("shadow_mountains.png")
        self.player = Player(50, 300)
        self.enemies = pygame.sprite.Group()
        
        # Sistema de spawn y puntuación
        self.score = 0
        self.spawn_timer = 0
        self.spawn_delay = 3500
        self.max_enemies = 4
        self.victory_score = 1500
        self.wave_number = 1
        self.enemies_defeated = 0
        
        # Estado del nivel
        self.running = True
        self.victory = False
        self.game_over = False
        self.paused = False
        self.game_started = False
        
        # Efectos visuales
        self.floating_texts = []
        
        # Música y sonidos
        play_music("level2_background.mp3", volume=0.6)

    def spawn_enemy(self):
        """Sistema de spawn de enemigos."""
        if len(self.enemies) < self.max_enemies:
            # Posiciones de spawn en diferentes alturas
            spawn_positions = [
                (800, 200),  # Altura alta
                (850, 300),  # Altura media
                (900, 400)   # Altura baja
            ]
            
            # Seleccionar posición aleatoria
            pos = random.choice(spawn_positions)
            
            # Probabilidad de spawn basada en la oleada
            if self.wave_number >= 3:
                # Más probabilidad de Ghost2 en oleadas avanzadas
                enemy_type = Ghost2 if random.random() < 0.4 else Ghost1
            else:
                # Mayormente Ghost1 en oleadas iniciales
                enemy_type = Ghost2 if random.random() < 0.2 else Ghost1
            
            # Crear y añadir el enemigo
            enemy = enemy_type(*pos)
            self.enemies.add(enemy)

    def handle_wave(self):
        """Maneja el sistema de oleadas."""
        if len(self.enemies) == 0 and self.enemies_defeated >= self.wave_number * 4:
            self.wave_number += 1
            self.enemies_defeated = 0
            self.spawn_delay = max(2000, self.spawn_delay - 200)
            self.max_enemies = min(6, self.max_enemies + 1)
            
            # Mostrar texto de nueva oleada
            self.floating_texts.append({
                'text': f"¡Oleada {self.wave_number}!",
                'position': (400, 300),
                'color': (255, 215, 0),
                'end_time': show_floating_text(
                    self.screen,
                    f"¡Oleada {self.wave_number}!",
                    (400, 300),
                    (255, 215, 0)
                )
            })
            
            # Spawn especial para nuevas oleadas
            if self.wave_number % 2 == 0:
                self.enemies.add(Ghost2(800, 200))
                self.enemies.add(Ghost2(850, 300))

    def run(self):
        """Loop principal del nivel."""
        clock = pygame.time.Clock()
        
        # Pantalla de inicio del nivel
        while not self.game_started and self.running:
            self.handle_start_screen()
            clock.tick(60)
        
        # Loop principal del juego
        while self.running:
            if not self.paused:
                self.handle_events()
                self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return self.victory

    def handle_start_screen(self):
        """Maneja la pantalla de inicio del nivel."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_started = True
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
        
        # Dibujar pantalla de inicio
        self.screen.fill((0, 0, 0))
        draw_text(
            self.screen,
            "Nivel 2 - Montañas Sombrías",
            (250, 200),
            font_size=40
        )
        draw_text(
            self.screen,
            "Los fantasmas acechan en las sombras...",
            (200, 260),
            font_size=24,
            color=(150, 150, 255)
        )
        draw_text(
            self.screen,
            "Presiona ENTER para comenzar",
            (300, 350)
        )
        draw_text(
            self.screen,
            "Presiona ESC para salir",
            (350, 400)
        )
        pygame.display.flip()

    def handle_events(self):
        """Maneja los eventos del nivel."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
            
            if not self.paused:
                self.player.handle_event(event)

    def update(self):
        """Actualiza el estado del nivel."""
        current_time = pygame.time.get_ticks()
        
        # Actualizar jugador y enemigos
        self.player.update()
        self.enemies.update()

        # Sistema de spawn
        if current_time - self.spawn_timer > self.spawn_delay:
            self.spawn_enemy()
            self.spawn_timer = current_time

        self.handle_wave()

        # Actualizar textos flotantes
        self.floating_texts = [
            text for text in self.floating_texts 
            if current_time < text['end_time']
        ]

        # Colisiones y combate
        for enemy in list(self.enemies):
            # Colisión jugador-enemigo
            if self.player.rect.colliderect(enemy.rect):
                damage = 20 if isinstance(enemy, Ghost2) else 15
                self.player.take_damage(damage)
                if self.player.health <= 0:
                    self.game_over = True
                    self.running = False

            # Verificar si el enemigo murió
            if enemy.health <= 0:
                score_value = 150 if isinstance(enemy, Ghost2) else 100
                self.score += score_value
                self.enemies_defeated += 1
                self.player.add_experience(25)
                
                # Mostrar texto de puntuación
                self.floating_texts.append({
                    'text': f"+{score_value}",
                    'position': enemy.rect.topleft,
                    'color': (255, 215, 0),
                    'end_time': show_floating_text(
                        self.screen,
                        f"+{score_value}",
                        enemy.rect.topleft,
                        (255, 215, 0)
                    )
                })
                
                enemy.kill()

        # Victoria
        if self.score >= self.victory_score:
            self.victory = True
            self.running = False

    def draw(self):
        """Dibuja todos los elementos del nivel."""
        # Dibujar fondo
        self.screen.blit(self.background, (0, 0))
        
        # Dibujar sprites
        self.enemies.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect.topleft)
        
        # Dibujar textos flotantes
        current_time = pygame.time.get_ticks()
        for text in self.floating_texts:
            if current_time < text['end_time']:
                show_floating_text(
                    self.screen,
                    text['text'],
                    text['position'],
                    text['color']
                )
        
        # UI
        draw_game_ui(
            self.screen,
            self.player,
            "Montañas Sombrías - Nivel 2",
            self.score,
            self.wave_number
        )
        
        # Menú de pausa
        if self.paused:
            # Overlay semitransparente
            s = pygame.Surface((800, 600))
            s.set_alpha(128)
            s.fill((0, 0, 0))
            self.screen.blit(s, (0, 0))
            
            # Textos del menú
            draw_text(
                self.screen,
                "PAUSA",
                (350, 250),
                font_size=50
            )
            draw_text(
                self.screen,
                "Presiona P para continuar",
                (300, 320)
            )
            draw_text(
                self.screen,
                "ESC para salir",
                (350, 360)
            )