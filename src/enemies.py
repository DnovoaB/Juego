import pygame
import random
import os
from src.utils import load_image, load_animation

# Clase base para los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, health, speed):
        super().__init__()

        # Cargar la imagen usando utils.load_image()
        self.image = load_image(image_path, size=(64, 64))  # Tamaño estándar de enemigos
        self.rect = self.image.get_rect(topleft=(x, y))

        # Atributos del enemigo
        self.health = health
        self.speed = speed
        self.direction = random.choice([-1, 1])

    def update(self):
        """Movimiento y actualización del enemigo"""
        self.rect.x += self.speed * self.direction

        # Cambio de dirección si choca con un borde
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.direction *= -1

    def take_damage(self, amount):
        """Reduce la vida del enemigo"""
        self.health -= amount
        if self.health <= 0:
            self.kill()

# Enemigos específicos con habilidades únicas
class DarkMage(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "characters/dark_mage.png", health=50, speed=2)

    def cast_spell(self):
        """El mago oscuro lanza un hechizo"""
        print("¡El Mago Oscuro lanza un hechizo oscuro!")

class Golem(Enemy):
    def __init__(self, x, y, golem_type="stone"):
        image_path = f"characters/golem_{golem_type}.png"  # Usamos diferentes tipos de golem
        super().__init__(x, y, image_path, health=100, speed=1)

        # Cargar animaciones de golem (para Golem1 y Golem2)
        self.idle_sprites = load_animation(f"{golem_type}/Idle", "Golem_03_Idle", 12)
        self.idle_blinking_sprites = load_animation(f"{golem_type}/Idle Blinking", "Golem_03_Idle Blinking", 12)
        self.walk_sprites = load_animation(f"{golem_type}/Walking", "Golem_03_Walking", 18)
        self.attack_sprites = load_animation(f"{golem_type}/Attacking", "Golem_03_Attacking", 12)
        self.dying_sprites = load_animation(f"{golem_type}/Dying", "Golem_03_Dying", 15)
        self.taunt_sprites = load_animation(f"{golem_type}/Taunt", "Golem_03_Taunt", 18)
        self.jump_loop_sprites = load_animation(f"{golem_type}/Jump Loop", "Golem_03_Jump Loop", 6)
        self.jump_start_sprites = load_animation(f"{golem_type}/Jump Start", "Golem_03_Jump Start", 6)

        # Estado inicial
        self.current_sprites = self.idle_sprites
        self.image = self.current_sprites[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_index = 0
        self.action = "idle"  # Puede ser "idle", "walk", "attack", "casting", "dying", "taunt", "jump"
        self.speed = 3

    def update(self):
        """Actualizar animación y lógica del golem."""
        if isinstance(self.current_sprites, list):  # Solo animaciones tienen múltiples frames
            self.frame_index += 0.1
            if self.frame_index >= len(self.current_sprites):
                self.frame_index = 0
            self.image = self.current_sprites[int(self.frame_index)]

    def move(self, direction):
        """Maneja el movimiento del golem."""
        if direction in ["left", "right"]:
            self.rect.x += -self.speed if direction == "left" else self.speed
            self.action = "walk"
            self.current_sprites = self.walk_sprites

    def stop(self):
        """Detener al golem y cambiar a animación de idle."""
        self.action = "idle"
        self.current_sprites = self.idle_sprites

    def attack(self):
        """Cambia la animación a ataque."""
        self.action = "attack"
        self.current_sprites = self.attack_sprites
        self.frame_index = 0  # Reiniciar la animación de ataque

    def taunt(self):
        """Animación de provocación."""
        self.action = "taunt"
        self.current_sprites = self.taunt_sprites
        self.frame_index = 0

    def die(self):
        """Animación de muerte."""
        self.action = "dying"
        self.current_sprites = self.dying_sprites
        self.frame_index = 0

    def jump(self, start=False):
        """Animación de salto."""
        self.action = "jump"
        self.current_sprites = self.jump_start_sprites if start else self.jump_loop_sprites
        self.frame_index = 0

# Creación de instancias de golem (Golem1 y Golem2)
class Golem1(Golem):
    def __init__(self, x, y):
        super().__init__(x, y, "Golem1")

class Golem2(Golem):
    def __init__(self, x, y):
        super().__init__(x, y, "Golem2")

# Ghost base class for both Ghost1 and Ghost2
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, ghost_type="Ghost1"):
        super().__init__()

        # Cargar animaciones de cada tipo de fantasma (Ghost1 y Ghost2)
        self.color = ghost_type
        self.x, self.y = x, y

        # Cargar animaciones específicas para el fantasma
        self.idle_sprites = load_animation(f"{self.color}/Idle", "Wraith_02_Idle", 12)
        self.idle_blinking_sprites = load_animation(f"{self.color}/Idle Blinking", "Wraith_02_Idle Blinking", 12)
        self.walk_sprites = load_animation(f"{self.color}/Walking", "Wraith_02_Moving Forward", 12)
        self.attack_sprites = load_animation(f"{self.color}/Attacking", "Wraith_02_Attack", 12)
        self.casting_spells_sprites = load_animation(f"{self.color}/Casting Spells", "Wraith_02_Casting Spells", 18)
        self.dying_sprites = load_animation(f"{self.color}/Dying", "Wraith_02_Dying", 15)
        self.taunt_sprites = load_animation(f"{self.color}/Taunt", "Wraith_02_Taunt", 18)

        # Estado inicial
        self.current_sprites = self.idle_sprites
        self.image = self.current_sprites[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_index = 0
        self.action = "idle"  # Puede ser "idle", "walk", "attack", "casting", "dying", "taunt"
        self.speed = 3

    def update(self):
        """Actualizar animación y lógica del fantasma."""
        if isinstance(self.current_sprites, list):  # Solo animaciones tienen múltiples frames
            self.frame_index += 0.1
            if self.frame_index >= len(self.current_sprites):
                self.frame_index = 0
            self.image = self.current_sprites[int(self.frame_index)]

    def move(self, direction):
        """Maneja el movimiento del fantasma."""
        if direction in ["left", "right"]:
            self.rect.x += -self.speed if direction == "left" else self.speed
            self.action = "walk"
            self.current_sprites = self.walk_sprites

    def stop(self):
        """Detener al fantasma y cambiar a animación de idle."""
        self.action = "idle"
        self.current_sprites = self.idle_sprites

    def attack(self):
        """Cambia la animación a ataque."""
        self.action = "attack"
        self.current_sprites = self.attack_sprites
        self.frame_index = 0  # Reiniciar la animación de ataque

    def cast_spell(self):
        """Cambia la animación a lanzamiento de hechizo."""
        self.action = "casting"
        self.current_sprites = self.casting_spells_sprites
        self.frame_index = 0

    def die(self):
        """Animación de muerte."""
        self.action = "dying"
        self.current_sprites = self.dying_sprites
        self.frame_index = 0

    def taunt(self):
        """Animación de provocación."""
        self.action = "taunt"
        self.current_sprites = self.taunt_sprites
        self.frame_index = 0

# Creación de instancias de fantasmas (Ghost1 y Ghost2)
class Ghost1(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, "Ghost1")

class Ghost2(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, "Ghost2")
