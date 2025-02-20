import pygame
import os
import random
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path

# Inicializar pygame si no está inicializado
if not pygame.get_init():
    pygame.init()

# Constantes
BASE_DIR = Path(os.getcwd())
ASSETS_DIR = BASE_DIR / "assets"
DEFAULT_SIZE = (64, 64)

class Animation:
    def __init__(self, frames: List[pygame.Surface], frame_duration: int = 100):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.finished = False
        
    def update(self) -> pygame.Surface:
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = current_time
            if self.current_frame == 0:
                self.finished = True
        return self.frames[self.current_frame]
    
    def get_current_frame(self) -> pygame.Surface:
        return self.frames[self.current_frame]
    
    def reset(self):
        self.current_frame = 0
        self.finished = False

def create_placeholder_animations(animations_config: Dict[str, Tuple[str, int]], 
                               size: Optional[Tuple[int, int]] = None) -> Dict[str, Animation]:
    """Crea animaciones placeholder cuando no se encuentra el directorio del personaje."""
    animations = {}
    for anim_name, (_, frame_count) in animations_config.items():
        frames = [create_placeholder_image(size or DEFAULT_SIZE) for _ in range(frame_count)]
        animations[anim_name] = Animation(frames)
    return animations

def create_placeholder_image(size: Tuple[int, int]) -> pygame.Surface:
    """Crea una imagen placeholder cuando no se encuentra el archivo."""
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Color base magenta semi-transparente
    pygame.draw.rect(surface, (255, 0, 255, 128), surface.get_rect())
    
    # Patrón de cuadrícula
    cell_size = min(size[0], size[1]) // 8
    for x in range(0, size[0], cell_size):
        for y in range(0, size[1], cell_size):
            if (x + y) // cell_size % 2 == 0:
                pygame.draw.rect(surface, (255, 0, 255, 64), 
                               (x, y, cell_size, cell_size))
    
    # Marco
    pygame.draw.rect(surface, (255, 0, 255), surface.get_rect(), 2)
    
    # Texto informativo
    try:
        font_size = min(size[0]//4, 20)
        font = pygame.font.SysFont('arial', font_size)
        text = font.render(f"{size[0]}x{size[1]}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(size[0]/2, size[1]/2))
        surface.blit(text, text_rect)
    except:
        pass
    
    return surface

def load_image(path: str, size: Optional[Tuple[int, int]] = None) -> pygame.Surface:
    """Carga una imagen y la escala si es necesario."""
    try:
        full_path = ASSETS_DIR / path
        if not full_path.exists():
            print(f"⚠️ Imagen no encontrada: {full_path}")
            return create_placeholder_image(size or DEFAULT_SIZE)
        
        image = pygame.image.load(str(full_path)).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except Exception as e:
        print(f"❌ Error cargando imagen {path}: {e}")
        return create_placeholder_image(size or DEFAULT_SIZE)

def load_sound(filename: str, volume: float = 1.0) -> Optional[pygame.mixer.Sound]:
    """Carga un archivo de sonido."""
    try:
        path = ASSETS_DIR / "sounds" / filename
        if not path.exists():
            print(f"⚠️ Sonido no encontrado: {path}")
            return None
            
        sound = pygame.mixer.Sound(str(path))
        sound.set_volume(volume)
        return sound
    except pygame.error as e:
        print(f"❌ Error cargando sonido {filename}: {e}")
        return None

def play_music(filename: str, loop: bool = True, volume: float = 0.7, fade_ms: int = 1000):
    """Reproduce música de fondo con fade in/out."""
    try:
        path = ASSETS_DIR / "sounds" / filename
        if not path.exists():
            print(f"⚠️ Música no encontrada: {path}")
            return
            
        pygame.mixer.music.fadeout(fade_ms)
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1 if loop else 0, fade_ms=fade_ms)
    except pygame.error as e:
        print(f"❌ Error reproduciendo música {filename}: {e}")

def stop_music(fade_ms: int = 1000):
    """Detiene la música con fade out."""
    pygame.mixer.music.fadeout(fade_ms)

def create_temporary_background(width: int = 800, height: int = 600, 
                              color: Tuple[int, int, int] = (50, 50, 50)) -> pygame.Surface:
    """Crea un fondo temporal cuando no se encuentra la imagen."""
    surface = pygame.Surface((width, height))
    surface.fill(color)
    
    # Agregar un patrón de cuadrícula
    for x in range(0, width, 32):
        pygame.draw.line(surface, (70, 70, 70), (x, 0), (x, height))
    for y in range(0, height, 32):
        pygame.draw.line(surface, (70, 70, 70), (0, y), (width, y))
    
    # Agregar texto de placeholder
    font = pygame.font.Font(None, 36)
    text = font.render("Fondo Temporal", True, (100, 100, 100))
    text_rect = text.get_rect(center=(width/2, height/2))
    surface.blit(text, text_rect)
    
    return surface

def load_background(image_name: str) -> pygame.Surface:
    """Carga una imagen de fondo desde 'assets/images/backgrounds/'."""
    try:
        path = ASSETS_DIR / "images" / "backgrounds" / image_name
        if not path.exists():
            print(f"⚠️ Fondo no encontrado: {path}")
            return create_temporary_background()
            
        background = pygame.image.load(str(path)).convert()
        return pygame.transform.scale(background, (800, 600))
    except Exception as e:
        print(f"❌ Error cargando el fondo {image_name}: {e}")
        return create_temporary_background()

def draw_text(surface: pygame.Surface, text: str, position: Tuple[int, int], 
              font_size: int = 30, color: Tuple[int, int, int] = (255, 255, 255), 
              shadow: bool = True, shadow_color: Tuple[int, int, int] = (0, 0, 0)):
    """Dibuja texto con sombra opcional."""
    try:
        font = pygame.font.SysFont('arial', font_size)
        
        if shadow:
            shadow_surface = font.render(str(text), True, shadow_color)
            surface.blit(shadow_surface, (position[0] + 2, position[1] + 2))
        
        text_surface = font.render(str(text), True, color)
        surface.blit(text_surface, position)
    except Exception as e:
        print(f"⚠️ Error dibujando texto: {e}")

def show_floating_text(screen: pygame.Surface, 
                      text: str, 
                      position: Tuple[int, int], 
                      color: Tuple[int, int, int] = (255, 255, 255), 
                      duration: int = 1000,
                      font_size: int = 24,
                      rise_speed: float = 1.0) -> int:
    """
    Muestra texto flotante temporal en la pantalla y retorna el tiempo de finalización.
    
    Args:
        screen: Superficie donde dibujar el texto
        text: Texto a mostrar
        position: Posición (x, y) donde mostrar el texto
        color: Color del texto en RGB
        duration: Duración en milisegundos
        font_size: Tamaño de la fuente
        rise_speed: Velocidad a la que el texto sube
    
    Returns:
        Tiempo (en ms) cuando el texto debe desaparecer
    """
    try:
        font = pygame.font.SysFont('arial', font_size)
        text_surface = font.render(str(text), True, color)
        
        # Añadir efecto de sombra
        shadow_surface = font.render(str(text), True, (0, 0, 0))
        screen.blit(shadow_surface, (position[0] + 2, position[1] + 2))
        
        # Dibujar texto principal
        screen.blit(text_surface, position)
        
        return pygame.time.get_ticks() + duration
    except Exception as e:
        print(f"⚠️ Error mostrando texto flotante: {e}")
        return pygame.time.get_ticks()

def draw_game_ui(screen: pygame.Surface, player, level_name: str, score: int, wave: int):
    """Dibuja la interfaz del juego."""
    # Barras de estado
    bar_width = 200
    bar_height = 20
    padding = 10
    
    # Fondo de las barras
    pygame.draw.rect(screen, (100, 0, 0), (padding, padding, bar_width, bar_height))
    pygame.draw.rect(screen, (0, 0, 100), (padding, padding * 2 + bar_height, bar_width, bar_height))
    
    # Barra de HP
    hp_width = int(bar_width * (player.health/player.max_health))
    pygame.draw.rect(screen, (255, 0, 0), (padding, padding, hp_width, bar_height))
    
    # Barra de MP
    mp_width = int(bar_width * (player.mana/player.max_mana))
    pygame.draw.rect(screen, (0, 0, 255), 
                    (padding, padding * 2 + bar_height, mp_width, bar_height))
    
    # Textos
    draw_text(screen, f"HP: {int(player.health)}%", (padding + 5, padding), 16)
    draw_text(screen, f"MP: {int(player.mana)}%", (padding + 5, padding * 2 + bar_height), 16)
    draw_text(screen, level_name, (padding, padding * 4 + bar_height * 2), 24)
    draw_text(screen, f"Puntuación: {score}", (padding, padding * 6 + bar_height * 2), 20)
    draw_text(screen, f"Oleada: {wave}", (padding, padding * 8 + bar_height * 2), 20)

def create_particle_effect(position: Tuple[int, int], 
                         color: Tuple[int, int, int], 
                         particle_count: int = 10) -> List[Dict]:
    """Crea un efecto de partículas."""
    return [{
        'pos': [position[0], position[1]],
        'vel': [random.uniform(-2, 2), random.uniform(-2, 2)],
        'timer': 255,
        'color': color
    } for _ in range(particle_count)]

def update_particles(particles: List[Dict]) -> List[Dict]:
    """Actualiza y filtra las partículas activas."""
    return [p for p in particles if update_particle(p)]

def update_particle(particle: Dict) -> bool:
    """Actualiza una partícula individual y retorna si sigue activa."""
    particle['pos'][0] += particle['vel'][0]
    particle['pos'][1] += particle['vel'][1]
    particle['timer'] -= 5
    return particle['timer'] > 0

def draw_particles(screen: pygame.Surface, particles: List[Dict]):
    """Dibuja las partículas en la pantalla."""
    for particle in particles:
        color = (*particle['color'], particle['timer'])
        pos = [int(particle['pos'][0]), int(particle['pos'][1])]
        surface = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, (2, 2), 2)
        screen.blit(surface, pos)

def load_character_animations(character_name: str, 
                           animations_config: Dict[str, Tuple[str, int]], 
                           size: Optional[Tuple[int, int]] = None) -> Dict[str, Animation]:
    """
    Carga todas las animaciones de un personaje.
    Args:
        character_name: Nombre de la carpeta del personaje
        animations_config: Diccionario con {nombre_animacion: (prefijo_archivo, num_frames)}
        size: Tamaño opcional para escalar los sprites
    """
    animations = {}
    
    for anim_name, (prefix, frame_count) in animations_config.items():
        # Usar el formato correcto de carpeta (ej: 'Geralt/Idle' para animación 'idle')
        folder = f"{character_name}/{anim_name.capitalize()}"
        frames = load_animation(folder, prefix, frame_count, size)
        animations[anim_name] = Animation(frames)
    
    return animations
        
def load_animation(folder: str, prefix: str, frame_count: int, size: Optional[Tuple[int, int]] = None) -> List[pygame.Surface]:
    """
    Carga una secuencia de imágenes para animación.
    Args:
        folder: Carpeta del personaje (ej: 'Geralt/Idle')
        prefix: Prefijo del archivo (ej: 'geralt_idle')
        frame_count: Número de frames
        size: Tamaño opcional para escalar los sprites
    """
    frames = []
    base_path = ASSETS_DIR / "images" / "characters"
    
    for i in range(frame_count):  # Cambiado para empezar desde 0
        # Intentar diferentes formatos de nombre de archivo
        possible_names = [
            f"{prefix}_{i:03d}.png",       # formato 3 dígitos: prefix_000.png
            f"{prefix}_{i + 1}.png",        # formato normal: prefix_1.png (para Geralt)
        ]
        
        frame_loaded = False
        for frame_name in possible_names:
            frame_path = base_path / folder / frame_name
            
            try:
                if frame_path.exists():
                    frame = pygame.image.load(str(frame_path)).convert_alpha()
                    if size:
                        frame = pygame.transform.scale(frame, size)
                    frames.append(frame)
                    frame_loaded = True
                    break
            except Exception as e:
                continue
        
        if not frame_loaded:
            print(f"⚠️ No se encontró el archivo: {frame_path}")
            frames.append(create_placeholder_image(size or DEFAULT_SIZE))
    
    return frames if frames else [create_placeholder_image(size or DEFAULT_SIZE)]