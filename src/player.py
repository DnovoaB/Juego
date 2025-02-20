import pygame
from typing import Dict, Optional, List, Tuple
from src.utils import (
    load_animation,
    load_sound,
    create_particle_effect
)

class Animation:
    def __init__(self, frames: List[pygame.Surface], frame_duration: int = 5):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame_index = 0
        self.frame_timer = 0
        
    def update(self):
        """Actualiza el frame actual de la animación."""
        self.frame_timer += 1
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
    
    def get_current_frame(self) -> pygame.Surface:
        """Retorna el frame actual de la animación."""
        return self.frames[self.current_frame_index]
    
    def reset(self):
        """Reinicia la animación al primer frame."""
        self.current_frame_index = 0
        self.frame_timer = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        
        self.size = (96, 96)
        # Cargar SOLO las animaciones que existen en tu estructura
        self.animations = self.load_character_animations("Geralt", {
            'idle': ('geralt_idle', 10),
            'walk': ('geralt_walk', 10),
            'run': ('geralt_run', 10),
            'jump': ('geralt_jump', 10),
            'die': ('geralt_die', 10),
            'fight': ('geralt_fight', 10)
        }, size=self.size)
        
        # Estado inicial
        self.current_animation = 'idle'
        self.image = self.animations['idle'].get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Atributos de movimiento
        self.speed = 5
        self.jump_speed = -15
        self.gravity = 0.8
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.5
        self.friction = 0.85
        self.is_jumping = False
        self.facing_right = True
        self.air_jumps = 1  # Doble salto
        self.air_jumps_left = self.air_jumps
        
        # Estadísticas del jugador
        self.max_health = 100
        self.health = self.max_health
        self.max_mana = 100
        self.mana = self.max_mana
        self.experience = 0
        self.level = 1
        self.mana_regeneration = 0.1
        
        # Combate
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_damage = 20
        self.attack_range = 60  # Añadido el rango de ataque
        self.attack_rect = None  # Añadido el rectángulo de ataque
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 1000
        self.combo_count = 0
        self.combo_timer = 0
        self.combo_window = 500  # ms para continuar el combo
        
        # Habilidades
        self.abilities = {
            'fire': {'mana_cost': 20, 'damage': 30, 'cooldown': 0},
            'ice': {'mana_cost': 30, 'damage': 40, 'cooldown': 0},
            'thunder': {'mana_cost': 50, 'damage': 60, 'cooldown': 0}
        }
        
        # Efectos visuales
        self.particles = []
        self.flash_timer = 0
        self.flash_duration = 100
        
        # Cargar sonidos
        self.sounds = {
            'jump': load_sound('jump.wav', 0.3),
            'attack': load_sound('attack.wav', 0.3),
            'hurt': load_sound('hurt.wav', 0.3),
            'die': load_sound('die.wav', 0.3),
            'spell': load_sound('spell.wav', 0.3)
        }

    def load_character_animations(self, character_name: str, animation_data: Dict[str, Tuple[str, int]], 
                            size: Optional[Tuple[int, int]] = None) -> Dict[str, Animation]:
        """
        Carga todas las animaciones para un personaje.
        Args:
            character_name: Nombre de la carpeta del personaje (ej: 'Geralt')
            animation_data: Diccionario con los datos de animación
            size: Tamaño opcional para escalar los sprites
        """
        animations = {}
        for anim_name, (prefix, frame_count) in animation_data.items():
            # Usar el formato correcto de carpeta (ej: 'Geralt/Idle' para animación 'idle')
            folder = f"{character_name}/{anim_name.capitalize()}"
            frames = load_animation(folder, prefix, frame_count, size)
            animations[anim_name] = Animation(frames)
        return animations

    def update(self):
        """Actualiza el estado del jugador."""
        # Obtener teclas presionadas
        keys = pygame.key.get_pressed()
        
        # Movimiento horizontal con aceleración
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = max(self.velocity_x - self.acceleration, -self.speed)
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = min(self.velocity_x + self.acceleration, self.speed)
            self.facing_right = True
        else:
            self.velocity_x *= self.friction
        
        # Aplicar velocidad
        self.rect.x += self.velocity_x
        
        # Gravedad y salto
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        # Limitar al suelo
        if self.rect.bottom > 550:  # Ajustar según tu nivel
            self.rect.bottom = 550
            self.velocity_y = 0
            self.is_jumping = False
            self.air_jumps_left = self.air_jumps
        
        # Regeneración de mana
        if self.mana < self.max_mana:
            self.mana = min(self.max_mana, self.mana + self.mana_regeneration)
        
        # Actualizar cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        for ability in self.abilities.values():
            if ability['cooldown'] > 0:
                ability['cooldown'] -= 1
        
        # Actualizar combo
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_count = 0
        
        # Actualizar invulnerabilidad
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerable_timer > self.invulnerable_duration:
                self.invulnerable = False
        
        # Actualizar efectos visuales
        if self.flash_timer > 0:
            self.flash_timer -= 1
        self.particles = self.update_particles()
        
        # Determinar animación actual
        self.update_animation()

    def update_animation(self):
        """Actualiza la animación actual del jugador."""
        # Si está atacando, verificar si la animación terminó
        if self.is_attacking:
            self.current_animation = 'fight'
            current_frame = self.animations['fight'].current_frame_index
            total_frames = len(self.animations['fight'].frames)
            
            # Si llegamos al último frame, terminar el ataque
            if current_frame >= total_frames - 1:
                self.is_attacking = False
                self.current_animation = 'idle'
                self.animations['fight'].reset()
        elif self.is_jumping:
            self.current_animation = 'jump'
        elif abs(self.velocity_x) > 0.5:
            self.current_animation = 'run' if abs(self.velocity_x) > 3 else 'walk'
        else:
            self.current_animation = 'idle'
        
        # Actualizar frame de animación
        self.animations[self.current_animation].update()
        new_image = self.animations[self.current_animation].get_current_frame()
        
        # Voltear imagen si es necesario
        if not self.facing_right:
            new_image = pygame.transform.flip(new_image, True, False)
        
        self.image = new_image

    def handle_event(self, event):
        """Maneja eventos de input del jugador."""
        if event.type == pygame.KEYDOWN:
            # Salto
            if event.key in [pygame.K_UP, pygame.K_w]:
                if not self.is_jumping:
                    self.jump()
                elif self.air_jumps_left > 0:
                    self.double_jump()
            
            # Ataque
            elif event.key == pygame.K_SPACE:
                self.attack()
            
            # Habilidades
            elif event.key == pygame.K_1:
                self.cast_spell('fire')
            elif event.key == pygame.K_2:
                self.cast_spell('ice')
            elif event.key == pygame.K_3:
                self.cast_spell('thunder')

    def jump(self):
        """Realiza un salto normal."""
        self.is_jumping = True
        self.velocity_y = self.jump_speed
        self.play_sound('jump')
        self.create_jump_particles()

    def double_jump(self):
        """Realiza un doble salto."""
        self.velocity_y = self.jump_speed * 0.8
        self.air_jumps_left -= 1
        self.play_sound('jump')
        self.create_jump_particles()

    def attack(self):
        """Realiza un ataque melee."""
        current_time = pygame.time.get_ticks()
        if not self.is_attacking and self.attack_cooldown == 0:
            self.is_attacking = True
            self.attack_cooldown = 20
            self.play_sound('attack')
            
            # Sistema de combos
            if self.combo_timer > 0:
                self.combo_count = (self.combo_count + 1) % 3
                self.attack_damage = 20 + (self.combo_count * 10)
            else:
                self.combo_count = 0
                self.attack_damage = 20
            
            # Crear rectángulo de ataque
            self.attack_rect = self.rect.copy()
            if self.facing_right:
                self.attack_rect.left = self.rect.right
                self.attack_rect.width = self.attack_range
            else:
                self.attack_rect.right = self.rect.left
                self.attack_rect.width = self.attack_range
            
            self.combo_timer = self.combo_window
            self.animations['fight'].reset()
            self.create_attack_particles()

    def cast_spell(self, spell_type: str):
        """Lanza un hechizo."""
        if spell_type in self.abilities and self.abilities[spell_type]['cooldown'] == 0:
            ability = self.abilities[spell_type]
            if self.mana >= ability['mana_cost']:
                self.mana -= ability['mana_cost']
                ability['cooldown'] = 60
                self.play_sound('spell')
                self.create_spell_particles(spell_type)
                return True
        return False

    def take_damage(self, amount: int):
        """Recibe daño."""
        if not self.invulnerable:
            self.health = max(0, self.health - amount)
            self.invulnerable = True
            self.invulnerable_timer = pygame.time.get_ticks()
            self.flash_timer = self.flash_duration
            self.play_sound('hurt')
            self.create_damage_particles()
            
            if self.health <= 0:
                self.die()

    def die(self):
        """Maneja la muerte del jugador."""
        self.current_animation = 'die'
        self.animations['die'].reset()
        self.play_sound('die')
        self.create_death_particles()

    def add_experience(self, amount: int):
        """Añade experiencia y maneja el sistema de niveles."""
        self.experience += amount
        if self.experience >= 100 * self.level:
            self.level_up()

    def level_up(self):
        """Sube de nivel y mejora estadísticas."""
        self.level += 1
        self.experience = 0
        self.max_health += 20
        self.health = self.max_health
        self.max_mana += 10
        self.mana = self.max_mana
        self.attack_damage += 5
        self.create_level_up_particles()

    def play_sound(self, sound_name: str):
        """Reproduce un sonido si está disponible."""
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()

    def create_particles(self, position: Tuple[int, int], color: Tuple[int, int, int], 
                        count: int = 10) -> None:
        """Crea partículas en una posición específica."""
        self.particles.extend(create_particle_effect(position, color, count))

    def update_particles(self) -> List[Dict]:
        """Actualiza las partículas existentes."""
        return [p for p in self.particles if p['timer'] > 0]

    def create_jump_particles(self):
        """Crea partículas para el salto."""
        self.create_particles((self.rect.centerx, self.rect.bottom), (200, 200, 255))

    def create_attack_particles(self):
        """Crea partículas para el ataque."""
        x = self.rect.right if self.facing_right else self.rect.left
        self.create_particles((x, self.rect.centery), (255, 200, 200))

    def create_spell_particles(self, spell_type: str):
        """Crea partículas para los hechizos."""
        colors = {
            'fire': (255, 100, 0),
            'ice': (100, 200, 255),
            'thunder': (255, 255, 0)
        }
        self.create_particles((self.rect.centerx, self.rect.centery), 
                            colors.get(spell_type, (255, 255, 255)), 20)

    def create_damage_particles(self):
        """Crea partículas al recibir daño."""
        self.create_particles((self.rect.centerx, self.rect.centery), (255, 0, 0), 15)

    def create_death_particles(self):
        """Crea partículas para la muerte."""
        self.create_particles((self.rect.centerx, self.rect.centery), (100, 0, 0), 30)

    def create_level_up_particles(self):
        """Crea partículas al subir de nivel."""
        self.create_particles((self.rect.centerx, self.rect.centery), (255, 255, 0), 25)