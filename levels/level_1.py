import pygame
from src.player import Player
from src.enemies import Golem1, Golem2
from src.utils import (
    load_background, 
    draw_text, 
    draw_game_ui, 
    play_music, 
    show_floating_text,
    create_placeholder_image
)

class Level1:
    def __init__(self, screen):
        self.screen = screen
        self.background = load_background("corrupted_forest.png")
        self.player = Player(50, 450)
        self.enemies = pygame.sprite.Group()
        
        # Sistema de spawn y progresión
        self.score = 0
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_delay = 2000
        self.enemies_defeated = 0
        self.required_kills = 4  # Número de Golems que hay que derrotar
        
        # Control de oleadas
        self.wave_number = 1
        self.wave_enemies = [
            (Golem1, 700, 450),  # Primer Golem
            (Golem2, 700, 450),  # Segundo Golem
            (Golem1, 700, 450),  # Tercer Golem
            (Golem2, 700, 450)   # Cuarto Golem
        ]
        self.current_enemy_index = 0
        
        # Estado del nivel
        self.running = True
        self.victory = False
        self.game_over = False
        self.paused = False
        self.game_started = False
        
        # Efectos visuales
        self.floating_texts = []
        
        # Música y sonidos
        play_music("level1_background.mp3", volume=0.6)

    def spawn_enemy(self):
        """Sistema de spawn de enemigos."""
        current_time = pygame.time.get_ticks()
        
        # Solo spawner si no hay enemigos y aún quedan enemigos por spawner
        if (len(self.enemies) == 0 and 
            self.current_enemy_index < len(self.wave_enemies) and 
            current_time - self.spawn_timer >= self.spawn_delay):
            
            # Obtener el siguiente enemigo de la lista
            enemy_class, x, y = self.wave_enemies[self.current_enemy_index]
            enemy = enemy_class(x, y)
            # Establecer el jugador como objetivo del enemigo
            enemy.set_player(self.player)  # Añadir esta línea
            self.enemies.add(enemy)
            print(f"Spawneando {enemy_class.__name__} en ({x}, {y})")
            
            self.spawn_timer = current_time

    def draw_enemy_health(self, enemy):
        """Dibuja la barra de vida del enemigo."""
        # Barra de vida
        bar_width = 50
        bar_height = 5
        bar_position = (enemy.rect.x, enemy.rect.y - 10)
        
        # Fondo de la barra (rojo)
        pygame.draw.rect(self.screen, (255, 0, 0),
                        (bar_position[0], bar_position[1], bar_width, bar_height))
        
        # Vida actual (verde)
        health_width = (enemy.health / enemy.max_health) * bar_width
        pygame.draw.rect(self.screen, (0, 255, 0),
                        (bar_position[0], bar_position[1], health_width, bar_height))

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
            "Geralt: La Sombra del Abismo",
            (250, 200),
            font_size=40
        )
        draw_text(
            self.screen,
            "Presiona ENTER para comenzar",
            (300, 300)
        )
        draw_text(
            self.screen,
            "Presiona ESC para salir",
            (350, 350)
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
        
        # Actualizar jugador
        self.player.update()
        
        # Mantener al jugador dentro de los límites de la pantalla
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.rect.right > 800:
            self.player.rect.right = 800
        
        # Actualizar y verificar enemigos
        for enemy in list(self.enemies):
            # Asegurar que el enemigo tenga referencia al jugador
            enemy.set_player(self.player)
            enemy.update()
            
            # Verificar colisión con el jugador
            if self.player.rect.colliderect(enemy.rect):
                # Verificar si el jugador está cayendo sobre el enemigo
                player_falling = self.player.velocity_y > 0
                player_above = self.player.rect.bottom < enemy.rect.centery
                
                if player_falling and player_above:
                    # El jugador está cayendo sobre el enemigo
                    # Solo ajustamos la posición del jugador sin hacer daño
                    self.player.rect.bottom = enemy.rect.top
                    self.player.velocity_y = self.player.jump_speed * 0.5  # Rebote pequeño
                else:
                    # Solo recibe daño si el enemigo está atacando
                    if enemy.is_attacking:
                        # Verificar si el jugador está en el área de ataque del enemigo
                        if enemy.attack_rect and enemy.attack_rect.colliderect(self.player.rect):
                            self.player.take_damage(enemy.attack_damage)
                            if self.player.health <= 0:
                                self.game_over = True
                                self.running = False
            
            # Verificar si el jugador está atacando y golpea al enemigo
            if self.player.is_attacking and self.player.attack_rect:
                if self.player.attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.player.attack_damage)
            
            # Verificar si el enemigo murió
            if enemy.health <= 0:
                score_value = 150 if isinstance(enemy, Golem2) else 100
                self.score += score_value
                self.enemies_defeated += 1
                self.current_enemy_index += 1
                enemy.kill()
                
                # Mostrar texto de puntuación
                self.floating_texts.append({
                    'text': f"+{score_value}",
                    'position': enemy.rect.topleft,
                    'color': (255, 215, 0),
                    'end_time': current_time + 1000
                })
                
                # Mostrar texto de progreso
                enemies_left = self.required_kills - self.enemies_defeated
                if enemies_left > 0:
                    self.floating_texts.append({
                        'text': f"¡Faltan {enemies_left} enemigos!",
                        'position': (400, 300),
                        'color': (255, 255, 255),
                        'end_time': current_time + 2000
                    })
                
                # Verificar victoria
                if self.enemies_defeated >= self.required_kills:
                    self.victory = True
                    self.running = False
                    # Mostrar mensaje de victoria
                    self.floating_texts.append({
                        'text': "¡Nivel Completado!",
                        'position': (400, 300),
                        'color': (255, 215, 0),
                        'end_time': current_time + 3000
                    })

        # Spawn de enemigos
        self.spawn_enemy()
        
        # Actualizar textos flotantes
        self.floating_texts = [
            text for text in self.floating_texts 
            if current_time < text['end_time']
        ]
        
    def get_collision_side(self, rect1, rect2):
        """
        Determina el lado de la colisión entre dos rectángulos.
        Retorna: "top", "bottom", "left", o "right"
        """
        # Calcular la intersección
        overlap = rect1.clip(rect2)
        
        if overlap.width == 0 or overlap.height == 0:
            return None
            
        # Calcular las distancias de penetración
        left = rect1.right - rect2.left
        right = rect2.right - rect1.left
        top = rect1.bottom - rect2.top
        bottom = rect2.bottom - rect1.top
        
        # Encontrar la menor penetración
        min_distance = min(left, right, top, bottom)
        
        if min_distance == top:
            return "top"
        elif min_distance == bottom:
            return "bottom"
        elif min_distance == left:
            return "left"
        else:
            return "right"

    def draw(self):
        """Dibuja todos los elementos del nivel."""
        # Dibujar fondo
        self.screen.blit(self.background, (0, 0))
        
        # Dibujar jugador
        self.screen.blit(self.player.image, self.player.rect)
        
        # Dibujar enemigos y sus barras de vida
        for enemy in self.enemies:
            self.screen.blit(enemy.image, enemy.rect)
            self.draw_enemy_health(enemy)
        
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
            "Bosque Corrupto - Nivel 1",
            self.score,
            self.wave_number
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

    def show_game_over_screen(self):
        """Muestra la pantalla de Game Over."""
        s = pygame.Surface((800, 600))
        s.set_alpha(192)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        draw_text(
            self.screen,
            "GAME OVER",
            (400, 250),
            font_size=60,
            color=(255, 0, 0)
        )
        draw_text(
            self.screen,
            f"Puntuación: {self.score}",
            (400, 320),
            font_size=30
        )
        draw_text(
            self.screen,
            "Presiona ESC para salir",
            (400, 380)
        )
        pygame.display.flip()