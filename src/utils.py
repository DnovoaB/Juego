import pygame
import os

# Obtener ruta absoluta del directorio base
BASE_DIR = os.getcwd()

# Cargar imagen con manejo de errores
def load_image(path, size=None):
    """Carga una imagen desde 'assets/images' y la escala si es necesario."""
    full_path = os.path.join(BASE_DIR, "assets/images", path)  # Asegura la ruta correcta
    
    if not os.path.exists(full_path):
        print(f"⚠️ Advertencia: Imagen no encontrada {full_path}")
        return pygame.Surface((50, 50), pygame.SRCALPHA)  # Imagen vacía como fallback

    try:
        image = pygame.image.load(full_path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"❌ Error cargando la imagen {full_path}: {e}")
        return pygame.Surface((50, 50), pygame.SRCALPHA)

# Cargar fondo de pantalla
def load_background(image_name):
    """Carga una imagen de fondo desde 'assets/images/backgrounds/'."""
    return load_image(f"backgrounds/{image_name}")

# Cargar sonido con manejo de errores
def load_sound(path):
    """Carga un archivo de sonido desde 'assets/sounds/'."""
    full_path = os.path.join(BASE_DIR, "assets/sounds", path)
    
    if not os.path.exists(full_path):
        print(f"⚠️ Advertencia: Sonido no encontrado {full_path}")
        return None
    
    try:
        return pygame.mixer.Sound(full_path)
    except pygame.error as e:
        print(f"❌ Error cargando el sonido {full_path}: {e}")
        return None

# Mostrar texto en la pantalla
def draw_text(surface, text, position, font_size=30, color=(255, 255, 255)):
    """Dibuja texto en la pantalla."""
    font_path = os.path.join(BASE_DIR, "assets/fonts/magical_font.ttf")
    if os.path.exists(font_path):
        font = pygame.font.Font(font_path, font_size)
    else:
        font = pygame.font.Font(None, font_size)

    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

# Verificar colisión entre dos rectángulos
def check_collision(rect1, rect2):
    """Verifica si dos rectángulos colisionan."""
    return rect1.colliderect(rect2)

# Reproducir música de fondo con manejo de errores
def play_music(path, loop=True):
    """Reproduce música de fondo desde 'assets/sounds/'."""
    full_path = os.path.join(BASE_DIR, "assets/sounds", path)
    
    if os.path.exists(full_path):
        try:
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play(-1 if loop else 0)
        except pygame.error as e:
            print(f"❌ Error cargando música {full_path}: {e}")
    else:
        print(f"⚠️ Advertencia: Música no encontrada {full_path}")

# Detener la música de fondo
def stop_music():
    """Detiene la música de fondo."""
    pygame.mixer.music.stop()

# Cargar animaciones desde múltiples imágenes
def load_animation(folder, base_name, frame_count, size=None):
    """Carga una animación desde múltiples imágenes numeradas dentro de 'assets/images/characters/Geralt/'."""
    frames = []
    
    for i in range(1, frame_count + 1):
        frame_path = f"characters/Geralt/{folder}/{base_name}_{i}.png"
        image = load_image(frame_path, size)
        if image:
            frames.append(image)
        else:
            print(f"⚠️ Advertencia: Falta {frame_path}")

    if not frames:
        print(f"❌ Error: No se encontraron imágenes en {folder}")
        return [pygame.Surface((50, 50), pygame.SRCALPHA)]  # Fallback: Un cuadro vacío
    
    return frames