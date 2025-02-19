import pygame
from src.player import Player
from src.enemies import Ghost1, Ghost2
from src.utils import load_background, draw_text

class Level2:
    def __init__(self, screen):
        self.screen = screen
        self.background = load_background("assets/images/backgrounds/shadow_mountains.png")
        self.player = Player(50, 300)
        self.enemies = pygame.sprite.Group()
        # Añadir Ghost1 y Ghost2 al grupo de enemigos
        self.enemies.add(Ghost1(600, 300))  # Golem1 en la posición (600, 300)
        self.enemies.add(Ghost2(700, 300))  # Golem2 en la posición (700, 300)

        self.running = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.player.handle_event(event)

    def update(self):
        self.player.update()
        self.enemies.update()

        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(2)

        if len(self.enemies) == 0:
            self.running = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.enemies.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect.topleft)
        draw_text(self.screen, "Montañas Sombrías", (20, 20))
