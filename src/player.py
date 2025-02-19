import pygame
from src.utils import load_animation, load_image

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.direction = "right"  # Direcciones posibles: "left", "right"
        
        # Cargar animaciones con nombres actualizados
        self.idle_sprites = load_animation("Idle", "geralt_idle", 10)
        self.walk_sprites = {
            "left": load_animation("Walk", "geralt_walk", 10),
            "right": load_animation("Walk", "geralt_walk", 10),
        }
        self.fight_sprites = load_animation("Fight", "geralt_fight", 10)
        self.die_sprites = load_animation("Die", "geralt_die", 10)
        self.jump_sprites = load_animation("Jump", "geralt_jump", 10)
        self.run_sprites = load_animation("Run", "geralt_run", 10)

        # Estado inicial
        self.current_sprites = self.idle_sprites
        self.image = self.current_sprites[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_index = 0
        self.action = "idle"  # Puede ser "idle", "walk", "fight", "die", "jump", "run"
        self.speed = 5

    def update(self):
        """Actualizar animación y lógica del jugador."""
        if isinstance(self.current_sprites, list):  # Solo animaciones tienen múltiples frames
            self.frame_index += 0.1
            if self.frame_index >= len(self.current_sprites):
                self.frame_index = 0
            self.image = self.current_sprites[int(self.frame_index)]

    def move(self, direction):
        """Maneja el movimiento del jugador."""
        if direction in self.walk_sprites:
            self.direction = direction
            self.rect.x += -self.speed if "left" in direction else self.speed
            self.action = "walk"
            self.current_sprites = self.walk_sprites[direction]

    def stop(self):
        """Detener al jugador y cambiar a animación de idle."""
        self.action = "idle"
        self.current_sprites = self.idle_sprites

    def attack(self):
        """Cambia la animación a pelea."""
        self.action = "fight"
        self.current_sprites = self.fight_sprites
        self.frame_index = 0  # Reiniciar la animación de ataque

    def die(self):
        """Animación de muerte."""
        self.action = "die"
        self.current_sprites = self.die_sprites
        self.frame_index = 0

    def jump(self):
        """Animación de salto."""
        self.action = "jump"
        self.current_sprites = self.jump_sprites
        self.frame_index = 0

    def run(self):
        """Animación de correr."""
        self.action = "run"
        self.current_sprites = self.run_sprites
        self.frame_index = 0
