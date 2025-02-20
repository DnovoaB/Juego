import pygame
import random
from src.player import Player
from src.enemies import Dragon, Ghost1, Ghost2
from src.utils import load_background, draw_text, load_sound

class Level3:
    def __init__(self, screen):
        self.screen = screen
        self.background = load_background("assets/images/backgrounds/dungeon.png")
        self.player = Player(50, 300)
        
        # Música y efectos de sonido
        self.background_music = load_sound("level3_theme.mp3")
        if self.background_music:
            self.background_music.play(-1)
        
        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
        # Añadir enemigos
        self.dragon = Dragon(600, 200)
        self.enemies.add(self.dragon)
        self.all_sprites.add(self.dragon)
        
        # Añadir fantasmas
        ghost_positions = [(400, 100), (200, 400), (700, 300)]
        for x, y in ghost_positions:
            ghost = Ghost1(x, y) if random.random() < 0.5 else Ghost2(x, y)
            self.enemies.add(ghost)
            self.all_sprites.add(ghost)
        
        self.running = True
        self.score = 0
        self.wave = 1
        self.max_waves = 3
        
    def spawn_wave(self):
        if self.wave < self.max_waves:
            self.wave += 1
            # Spawn más enemigos según la oleada
            num_ghosts = 2 + self.wave
            for _ in range(num_ghosts):
                x = random.randint(100, 700)
                y = random.randint(100, 500)
                ghost = Ghost1(x, y) if random.random() < 0.5 else Ghost2(x, y)
                self.enemies.add(ghost)
                self.all_sprites.add(ghost)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)

        # Limpiar recursos
        if self.background_music:
            self.background_music.stop()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.player.handle_event(event)

    def update(self):
        # Actualizar jugador
        self.player.update()
        
        # Actualizar enemigos
        self.enemies.update()
        
        # Colisiones con enemigos
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                if isinstance(enemy, Dragon):
                    self.player.take_damage(enemy.damage * 2)  # El dragón hace más daño por contacto
                else:
                    self.player.take_damage(enemy.damage)
            
            # Lógica de ataque de enemigos
            if isinstance(enemy, Dragon):
                if abs(self.player.rect.centerx - enemy.rect.centerx) < 200:
                    damage = enemy.fire_attack()
                    if damage > 0:
                        self.player.take_damage(damage)
        
        # Verificar condiciones de victoria/derrota
        if self.player.health <= 0:
            self.running = False
        elif len(self.enemies) == 0:
            if self.wave < self.max_waves:
                self.spawn_wave()
            else:
                self.running = False  # Victoria

    def draw(self):
        # Dibujar fondo
        self.screen.blit(self.background, (0, 0))
        
        # Dibujar sprites
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        
        # Dibujar UI
        draw_text(self.screen, f"Mazmorras Oscuras - Oleada {self.wave}/{self.max_waves}", (20, 20))
        draw_text(self.screen, f"Puntuación: {self.score}", (20, 50))
        
        # Barras de vida y maná del jugador
        pygame.draw.rect(self.screen, (255, 0, 0), (10, 80, 200 * (self.player.health/self.player.max_health), 20))
        pygame.draw.rect(self.screen, (0, 0, 255), (10, 110, 200 * (self.player.mana/self.player.max_mana), 20))
        
        # Barras de vida de enemigos
        for enemy in self.enemies:
            health_percentage = enemy.health / enemy.max_health
            bar_width = 50
            bar_height = 5
            bar_x = enemy.rect.centerx - bar_width // 2
            bar_y = enemy.rect.top - 10
            pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, bar_width * health_percentage, bar_height))