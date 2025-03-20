import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Zelda")

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Cargar imágenes
player_image = pygame.Surface((50, 50))
player_image.fill(GREEN)
sword_image = pygame.Surface((10, 30))
sword_image.fill(RED)

# Clase del jugador
class Player:
    def __init__(self):
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
        self.sword = None

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.sword:
            surface.blit(self.sword.image, self.sword.rect)

    def attack(self):
        if not self.sword:  # Si no hay espada activa
            self.sword = Sword(self.rect.center)

# Clase de la espada
class Sword:
    def __init__(self, position):
        self.image = sword_image
        self.rect = self.image.get_rect(center=position)
        self.active = True

    def update(self):
        if self.active:
            self.rect.x += 10  # Mueve la espada hacia adelante
            if self.rect.x > WIDTH:  # Desactiva la espada si sale de la pantalla
                self.active = False

# Crear el jugador
player = Player()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Manejo de teclas
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -1
    if keys[pygame.K_RIGHT]:
        dx = 1
    if keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_DOWN]:
        dy = 1
    if keys[pygame.K_SPACE]:  # Presiona espacio para atacar
        player.attack()

    # Mover al jugador
    player.move(dx, dy)

    # Actualizar la espada
    if player.sword:
        player.sword.update()
        if not player.sword.active:
            player.sword = None  # Desactiva la espada si ya no está activa

    # Dibujar en la pantalla
    screen.fill(WHITE)
    player.draw(screen)
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    pygame.time.Clock().tick(60)