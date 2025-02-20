import pygame
import random
from src.player import Player
from src.enemies import BlackMage
from src.utils import (
    load_background, 
    draw_text, 
    draw_game_ui, 
    play_music, 
    show_floating_text,
    create_placeholder_image
)

class Level4:
    def __init__(self, screen):
        self.screen = screen
        self.background = load_background("shadow_castle.png")
        self.player = Player(50, 300)
        self.enemies = pygame.sprite.Group()
        
        # Configuración del jefe final
        self.boss = BlackMage(600, 250)
        self.enemies.add(self.boss)
        self.boss_phases = 3
        self.current_phase = 1
        self.phase_health_thresholds = [200, 100]  # Puntos de vida para cambios de fase
        
        # Sistema de puntuación
        self.score = 0
        self.victory_score = 1000
        self.boss_defeated = False
        
        # Estado del nivel
        self.running = True
        self.victory = False
        self.game_over = False
        self.paused = False
        self.game_started = False
        
        # Efectos visuales
        self.floating_texts = []
        self.screen_shake = 0
        self.flash_screen = False
        self.flash_duration = 0
        
        # Música y sonidos
        play_music("boss_theme.mp3", volume=0.7)

    def handle_boss_phases(self):
        """Maneja las fases del jefe final."""
        if self.boss.health <= self.phase_health_thresholds[1] and self.current_phase == 1:
            self.current_phase = 2
            self.boss.attack_damage *= 1.5
            self.boss.speed *= 1.2
            self.screen_shake = 20
            self.flash_screen = True
            self.flash_duration = 30
            self.floating_texts.append({
                'text': "¡El poder oscuro se intensifica!",
                'position': (300, 200),
                'color': (255, 0, 0),
                'end_time': show_floating_text(
                    self.screen,
                    "¡El poder oscuro se intensifica!",
                    (300, 200),
                    (255, 0, 0)
                )
            })
        elif self.boss.health <= self.phase_health_thresholds[0] and self.current_phase == 2:
            self.current_phase = 3
            self.boss.attack_damage *= 2
            self.boss.speed *= 1.5
            self.screen_shake = 30
            self.flash_screen = True
            self.flash_duration = 45
            self.floating_texts.append({
                'text': "¡FASE FINAL!",
                'position': (350, 200),
                'color': (255, 0, 0),
                'end_time': show_floating_text(
                    self.screen,
                    "¡FASE FINAL!",
                    (350, 200),
                    (255, 0, 0)
                )
            })

    def run(self):
        """Loop principal del nivel."""
        clock = pygame.time.Clock()
        
        # Pantalla de inicio
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
            "BATALLA FINAL",
            (300, 150),
            font_size=50,
            color=(255, 0, 0)
        )
        draw_text(
            self.screen,
            "El Señor Oscuro te espera...",
            (250, 250),
            font_size=30,
            color=(150, 0, 0)
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
        
        # Actualizar jugador y jefe
        self.player.update()
        self.enemies.update()
        
        # Actualizar efectos visuales
        if self.screen_shake > 0:
            self.screen_shake -= 1
        if self.flash_duration > 0:
            self.flash_duration -= 1
        else:
            self.flash_screen = False

        # Manejar fases del jefe
        self.handle_boss_phases()

        # Actualizar textos flotantes
        self.floating_texts = [
            text for text in self.floating_texts 
            if current_time < text['end_time']
        ]

        # Colisiones y combate
        if self.player.rect.colliderect(self.boss.rect):
            self.player.take_damage(self.boss.attack_damage)
            if self.player.health <= 0:
                self.game_over = True
                self.running = False

        # Verificar si el jefe fue derrotado
        if self.boss.health <= 0 and not self.boss_defeated:
            self.boss_defeated = True
            self.score += 1000
            self.victory = True
            self.running = False
            
            # Efecto de victoria
            self.floating_texts.append({
                'text': "¡Victoria!",
                'position': (350, 200),
                'color': (255, 215, 0),
                'end_time': show_floating_text(
                    self.screen,
                    "¡Victoria!",
                    (350, 200),
                    (255, 215, 0)
                )
            })

    def draw(self):
        """Dibuja todos los elementos del nivel."""
        # Aplicar screen shake
        offset_x = random.randint(-self.screen_shake, self.screen_shake)
        offset_y = random.randint(-self.screen_shake, self.screen_shake)
        
        # Dibujar fondo
        self.screen.blit(self.background, (offset_x, offset_y))
        
        # Flash screen effect
        if self.flash_screen:
            s = pygame.Surface((800, 600))
            s.fill((255, 0, 0))
            s.set_alpha(100)
            self.screen.blit(s, (0, 0))
        
        # Dibujar sprites
        self.enemies.draw(self.screen)
        self.screen.blit(self.player.image, 
                        (self.player.rect.x + offset_x, 
                         self.player.rect.y + offset_y))
        
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
            f"Castillo del Señor Oscuro - Fase {self.current_phase}",
            self.score,
            self.current_phase
        )
        
        # Barra de vida del jefe
        boss_health_width = 400
        boss_health_height = 30
        boss_health_x = (800 - boss_health_width) // 2
        boss_health_y = 550
        
        # Fondo de la barra
        pygame.draw.rect(self.screen, (100, 0, 0), 
                        (boss_health_x, boss_health_y, 
                         boss_health_width, boss_health_height))
        
        # Barra de vida actual
        health_percentage = self.boss.health / 300  # 300 es la vida máxima del jefe
        current_width = int(boss_health_width * health_percentage)
        pygame.draw.rect(self.screen, (200, 0, 0), 
                        (boss_health_x, boss_health_y, 
                         current_width, boss_health_height))
        
        # Nombre del jefe
        draw_text(
            self.screen,
            "El Señor Oscuro",
            (boss_health_x, boss_health_y - 25),
            font_size=20,
            color=(255, 0, 0)
        )
        
        # Menú de pausa
        if self.paused:
            s = pygame.Surface((800, 600))
            s.set_alpha(128)
            s.fill((0, 0, 0))
            self.screen.blit(s, (0, 0))
            
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