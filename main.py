import pygame as pg
from classes import Player, Object

pg.init()

size = (700, 500)
screen = pg.display.set_mode(size)

BLACK = (0, 0, 0)

pg.display.set_caption("Castlevania but better")

# --- Used to manage how fast the screen updates
clock = pg.time.Clock()

# --- Global gravity
gravity = 1.01

# --- Player
player = Player(100, 100)
collision = False


# --- Objects
object = Object(100, 300)

# --- Main loop
running = True
while running:
    # --- Events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    # --- Player logic
    if not collision:
        player.y *= gravity 
    else:
        player.y /= gravity
    player.update_position()

    # --- Collision logic
    colliding = player.rect.colliderect(object.rect)
    if colliding:
        collision = True
    else:
        # --- Background
        screen.fill(BLACK)


    # --- Making stuff appear
    screen.blit(object.image, object.rect.topleft)
    screen.blit(player.image, player.rect.topleft)


    pg.display.flip()
    clock.tick(60)


pg.quit()