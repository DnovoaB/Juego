import pygame
import random
from src.utils import load_character_animations
from typing import Tuple

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, size: Tuple[int, int] = (64, 64)):
        super().__init__()
        self.size = size
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.velocity_x = 0
        self.velocity_y = 0
        self.facing_right = False
        self.current_animation = 'idle'
        self.is_attacking = False
        self.is_dying = False
        self.attack_cooldown = 0
        self.attack_range = 100
        self.detection_range = 300
        
    def update_animation(self):
        self.animations[self.current_animation].update()
        new_image = self.animations[self.current_animation].get_current_frame()
        if not self.facing_right:
            new_image = pygame.transform.flip(new_image, True, False)
        self.image = new_image
        
    def move_towards_player(self, player_pos: Tuple[int, int], speed: float):
        if not self.is_dying and not self.is_attacking:
            dx = player_pos[0] - self.rect.x
            self.facing_right = dx > 0
            distance = abs(dx)
            
            if distance > 50:  # Mantener distancia mínima
                self.rect.x += speed if dx > 0 else -speed
                self.current_animation = 'walk'
            else:
                self.current_animation = 'idle'

class BlackMage(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "assets/images/characters/dark_mage/idle/DarkMage_01.png", health=50, speed=2)
        self.spell_damage = 15
        self.spell_cooldown = 1500  # 1.5 segundos
        self.last_spell = 0

    def cast_spell(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spell >= self.spell_cooldown:
            self.last_spell = current_time
            return self.spell_damage
        return 0

class Dragon(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, (120, 120))
        self.animations = load_character_animations("Dragon", {
            'idle': ('Walk', 5),  # Usar walk como idle
            'walk': ('Walk', 5),
            'attack': ('Attack', 4),
            'fire_attack': ('Fire_Attack', 6),
            'death': ('Death', 5)
        }, self.size)
        self.health = 300
        self.attack_damage = 40
        self.speed = 3
        self.attack_cooldown_max = 150
        self.image = self.animations['idle'].get_current_frame()
        self.can_fly = True
        self.flying_height = random.randint(50, 150)

class Ghost1(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, (70, 70))
        self.animations = load_character_animations("Ghost1", {
            'idle': ('Wraith_01_Idle', 11),
            'idle_blink': ('Wraith_01_Idle Blinking', 11),
            'walk': ('Wraith_01_Moving Forward', 11),
            'attack': ('Wraith_01_Attack', 11),
            'cast': ('Wraith_01_Casting Spells', 17),
            'taunt': ('Wraith_01_Taunt', 17),
            'death': ('Wraith_01_Dying', 14)
        }, self.size)
        self.health = 100
        self.attack_damage = 15
        self.speed = 4
        self.attack_cooldown_max = 90
        self.image = self.animations['idle'].get_current_frame()

class Ghost2(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, (70, 70))
        self.animations = load_character_animations("Ghost2", {
            'idle': ('Wraith_02_Idle', 11),
            'idle_blink': ('Wraith_02_Idle Blinking', 11),
            'walk': ('Wraith_02_Moving Forward', 11),
            'attack': ('Wraith_02_Attack', 11),
            'cast': ('Wraith_02_Casting Spells', 17),
            'taunt': ('Wraith_02_Taunt', 17),
            'death': ('Wraith_02_Dying', 14)
        }, self.size)
        self.health = 120
        self.attack_damage = 20
        self.speed = 3.5
        self.attack_cooldown_max = 100
        self.image = self.animations['idle'].get_current_frame()

class Golem1(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, (90, 90))
        self.animations = load_character_animations("Golem1", {
            'idle': ('Golem_03_Idle', 12),
            'idle_blink': ('Golem_03_Idle_Blink', 12),
            'walking': ('Golem_03_Walking', 18),
            'attacking': ('Golem_03_Attacking', 12),
            'jump_start': ('Golem_03_Jump_Start', 6),
            'jump_loop': ('Golem_03_Jump_Loop', 6),
            'taunt': ('Golem_03_Taunt', 18),
            'dying': ('Golem_03_Dying', 15)
        }, self.size)

        # Atributos base
        self.max_health = 200
        self.health = self.max_health
        self.attack_damage = 30
        self.speed = 2
        self.attack_cooldown_max = 120
        self.attack_cooldown = 0
        
        # Estados
        self.current_animation = 'idle'
        self.is_attacking = False
        self.is_dying = False
        self.facing_right = False
        
        # Configuración de combate
        self.attack_range = 60
        self.detection_range = 300
        self.attack_rect = None  # Añadido para detección de colisión de ataque
        
        # Inicialización
        self.image = self.animations[self.current_animation].get_current_frame()
        self.rect = self.image.get_rect(x=x, y=y)
        self.player = None
        
        # Hitbox para colisiones
        self.hitbox = self.rect.inflate(-20, -10)  # Hitbox más pequeña que el rect

    def set_player(self, player):
        """Establece el jugador como objetivo."""
        self.player = player

    def update(self):
        """Actualiza el estado del Golem."""
        if not self.player:
            return

        if self.is_dying:
            self.handle_death()
            return

        # Actualizar cooldown de ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Calcular distancia al jugador
        to_player = self.player.rect.centerx - self.rect.centerx
        distance = abs(to_player)
        
        # Actualizar la dirección a la que mira
        self.facing_right = to_player < 0

        # Si no está atacando, actualizar el estado de movimiento
        if not self.is_attacking:
            # Comportamiento basado en la distancia
            if distance < self.attack_range and self.attack_cooldown <= 0:
                self.start_attack()
            elif distance < self.detection_range:
                # Movimiento hacia el jugador
                direction = -1 if self.facing_right else 1
                self.rect.x += self.speed * direction
                self.current_animation = 'walking'
            else:
                self.idle()
        
        # Actualizar animación actual
        self.update_animation()

        # Actualizar el rectángulo de ataque si está atacando
        if self.is_attacking:
            self.attack_rect = self.rect.copy()
            if self.facing_right:
                self.attack_rect.right = self.rect.left
                self.attack_rect.width = self.attack_range
            else:
                self.attack_rect.left = self.rect.right
                self.attack_rect.width = self.attack_range
        else:
            self.attack_rect = None

    def move_towards_player(self, to_player):
        """Mueve el Golem hacia el jugador."""
        if to_player > 0:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
    
        self.current_animation = 'walking'
        self.animations['walking'].update()

    def start_attack(self):
        """Inicia un ataque."""
        self.is_attacking = True
        self.current_animation = 'attacking'
        self.animations['attacking'].reset()
        self.attack_cooldown = self.attack_cooldown_max
        
        # Crear rectángulo de ataque
        self.attack_rect = self.hitbox.copy()
        if self.facing_right:
            self.attack_rect.right = self.hitbox.left
            self.attack_rect.width = self.attack_range
        else:
            self.attack_rect.left = self.hitbox.right
            self.attack_rect.width = self.attack_range

    def check_collision_with_player(self):
        """Verifica la colisión con el jugador y determina si debe hacer daño."""
        if not self.player or self.is_dying:
            return False

        # Obtener las posiciones relativas
        player_bottom = self.player.rect.bottom
        enemy_top = self.hitbox.top
        
        # Si el jugador está encima del enemigo
        if player_bottom <= enemy_top + 10:  # 10 píxeles de margen
            return False
            
        # Si el enemigo está atacando y el jugador está en el área de ataque
        if self.is_attacking and self.attack_rect and self.attack_rect.colliderect(self.player.rect):
            return True
            
        # Si hay colisión lateral
        if self.hitbox.colliderect(self.player.rect):
            player_center_y = self.player.rect.centery
            enemy_center_y = self.hitbox.centery
            # Si la colisión es más horizontal que vertical
            return abs(player_center_y - enemy_center_y) < 30
            
        return False

    def idle(self):
        """Estado de reposo."""
        if not self.is_attacking:
            if random.random() < 0.01 and self.current_animation == 'idle':
                self.current_animation = 'idle_blink'
                self.animations['idle_blink'].reset()
            elif self.current_animation != 'idle_blink':
                self.current_animation = 'idle'

    def update_animation(self):
        """Actualiza la animación actual."""
        self.animations[self.current_animation].update()
        self.image = self.animations[self.current_animation].get_current_frame()
        
        if self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        
        if self.is_attacking:
            current_frame = self.animations['attacking'].current_frame
            total_frames = len(self.animations['attacking'].frames)
            if current_frame >= total_frames - 1:
                self.is_attacking = False
                self.current_animation = 'idle'
                self.animations['attacking'].reset()
                self.attack_rect = None  # Limpiar el rectángulo de ataque

    def take_damage(self, damage):
        """Recibe daño."""
        if not self.is_dying:
            self.health -= damage
            if self.health <= 0:
                self.start_death()
            else:
                self.current_animation = 'taunt'
                self.animations['taunt'].reset()

    def start_death(self):
        """Inicia la animación de muerte."""
        self.is_dying = True
        self.current_animation = 'dying'
        self.animations['dying'].reset()

    def handle_death(self):
        """Maneja la animación de muerte."""
        self.animations['dying'].update()
        current_frame = self.animations['dying'].current_frame
        total_frames = len(self.animations['dying'].frames)
        if current_frame >= total_frames - 1:
            self.kill()

class Golem2(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, (90, 90))
        self.animations = load_character_animations("Golem2", {
            'idle': ('Golem_01_Idle', 11),
            'idle_blink': ('Golem_01_Idle_Blink', 12),
            'walking': ('Golem_01_Walking', 17),
            'attacking': ('Golem_01_Attacking', 11),
            'jump_start': ('Golem_01_Jump_Start', 6),
            'jump_loop': ('Golem_01_Jump_Loop', 5),
            'taunt': ('Golem_01_Taunt', 17),
            'dying': ('Golem_01_Dying', 14)
        }, self.size)

        # Atributos base (más fuertes que Golem1)
        self.max_health = 250
        self.health = self.max_health
        self.attack_damage = 35
        self.speed = 1.5
        self.attack_cooldown_max = 140
        self.attack_cooldown = 0
        
        # Estados y cooldowns
        self.can_jump = True
        self.jump_cooldown = 0
        self.jump_cooldown_max = 200
        self.is_jumping = False
        self.is_attacking = False
        self.is_dying = False
        self.current_animation = 'idle'
        self.animation_timer = 0
        self.attack_frame = 0
        
        # Física
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_force = -12
        
        # Inicialización
        self.image = self.animations[self.current_animation].get_current_frame()
        self.direction = -1  # -1 izquierda, 1 derecha
        self.attack_range = 70
        self.detection_range = 250
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Estado de IA
        self.state = 'idle'
        self.target = None
        self.last_attack_time = 0
        self.attack_delay = 1000  # milisegundos

    def update(self):
        """Actualiza el estado del Golem."""
        if not self.player:
            return

        if self.is_dying:
            self.handle_death()
            return

        # Actualizar cooldown de ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Calcular distancia al jugador
        to_player = self.player.rect.centerx - self.rect.centerx
        distance = abs(to_player)
        # La dirección visual es correcta
        self.facing_right = to_player < 0

        # Comportamiento basado en la distancia
        if distance < self.attack_range and not self.is_attacking and self.attack_cooldown <= 0:
            # Atacar si está en rango
            self.start_attack()
        elif distance < self.detection_range and not self.is_attacking:
            # Caminar hacia el jugador
            self.move_towards_player(to_player)
        else:
            # Idle si está fuera de rango
            self.idle()

        # Actualizar animación actual
        self.update_animation()

    def update_ai(self):
        """Actualiza la IA del Golem."""
        if not hasattr(self, 'player'):
            return

        # Calcular distancia al jugador
        distance_to_player = self.player.rect.centerx - self.rect.centerx
        abs_distance = abs(distance_to_player)
        
        # Actualizar dirección
        self.direction = 1 if distance_to_player > 0 else -1

        # Comportamiento basado en la distancia
        if abs_distance < self.attack_range and self.attack_cooldown <= 0:
            self.start_attack()
        elif abs_distance < self.detection_range:
            self.move_towards_player()
        else:
            self.idle()

    def update_animation(self):
        """Actualiza la animación actual."""
        self.animation_timer += 1
        
        # Manejar la finalización de las animaciones
        if self.is_attacking:
            if self.animations['attacking'].is_complete():
                self.is_attacking = False
                self.current_animation = 'idle'
                self.animations['attacking'].reset()
        
        # Actualizar la animación actual
        self.animations[self.current_animation].update()

    def move_towards_player(self):
        """Mueve el Golem hacia el jugador."""
        if not self.is_attacking:
            self.rect.x += self.speed * self.direction
            if self.current_animation != 'walking':
                self.current_animation = 'walking'
                self.animations['walking'].reset()

    def start_attack(self):
        """Inicia un ataque."""
        if not self.is_attacking:
            self.is_attacking = True
            self.current_animation = 'attacking'
            self.animations['attacking'].reset()
            self.attack_cooldown = self.attack_cooldown_max
            self.attack_frame = 0

    def attack(self):
        """Realiza el ataque."""
        # La lógica de daño se maneja en el nivel
        self.is_attacking = True
        self.current_animation = 'attacking'
        self.attack_cooldown = self.attack_cooldown_max

    def idle(self):
        """Estado de reposo."""
        if not self.is_attacking:
            if self.current_animation != 'idle' and self.current_animation != 'idle_blink':
                self.current_animation = 'idle'
                self.animations['idle'].reset()
            
            # Probabilidad de parpadear
            if self.current_animation == 'idle' and random.random() < 0.01:
                self.current_animation = 'idle_blink'
                self.animations['idle_blink'].reset()

    def take_damage(self, damage):
        """Recibe daño y actualiza el estado."""
        if not self.is_dying:
            self.health -= damage
            if self.health <= 0:
                self.start_death()
            else:
                self.current_animation = 'taunt'
                self.animations['taunt'].reset()

    def start_death(self):
        """Inicia la animación de muerte."""
        self.is_dying = True
        self.current_animation = 'dying'
        self.animations['dying'].reset()

    def handle_death(self):
        """Maneja la animación de muerte."""
        if self.animations['dying'].is_complete():
            self.kill()

    def jump(self):
        """Realiza un salto."""
        if not self.is_jumping and self.jump_cooldown <= 0:
            self.is_jumping = True
            self.velocity_y = self.jump_force
            self.current_animation = 'jump_start'
            self.animations['jump_start'].reset()
            self.jump_cooldown = self.jump_cooldown_max

    def reset_animation(self):
        """Reinicia la animación actual."""
        self.animations[self.current_animation].reset()

    def get_rect(self):
        """Obtiene el rectángulo de colisión."""
        return self.rect

    def set_player(self, player):
        """Establece el jugador como objetivo."""
        self.player = player