import pygame
from src.player import Player
from src.enemies import Dragon, DarkMage
from src.utils import load_background, draw_text

class Level4:
    def __init__(self, screen):
        self.screen = screen
        self.background = load_background("assets/images/backgrounds/shadow_castle.png")
        self.player = Player(50, 300)
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Dragon(600, 250))
        self.enemies.add(DarkMage(700, 300))

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
                self.player.take_damage(3)  # El dragón hace mucho daño

        if len(self.enemies) == 0:
            self.running = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.enemies.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect.topleft)
        draw_text(self.screen, "Castillo del Señor Oscuro - Jefe Final", (20, 20))
