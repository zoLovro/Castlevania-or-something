import pygame as pg
from classes import Player, Object

pg.init()

size = (1000, 500)
screen = pg.display.set_mode(size)

BLACK = (0, 0, 0)

pg.display.set_caption("Castlevania but better")

# --- Used to manage how fast the screen updates
clock = pg.time.Clock()

# --- Global gravity
gravity = 1.01

# --- Player
player = Player(100, 100)
player_collision = False
moving = False


# --- Objects
object = Object(100, 450)

# --- Main loop
running = True
while running:
    # --- Events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # --- Collision logic
    colliding = player.rect.colliderect(object.rect)
    if colliding:
        player.vertical_speed = 0

    # --- Sideways movement logic
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        player.x -= player.horizontal_speed
        moving = True
    if keys[pg.K_RIGHT]:
        player.x += player.horizontal_speed
        moving = True
    else:
        moving = False
    print(player.horizontal_speed)

    # --- Jumping logic
    if colliding:
        if keys[pg.K_UP]:
            player.vertical_speed += player.jumping_acc
            player.y -= player.vertical_speed


    # --- Gravity logic
    if not colliding:
        player.vertical_speed += player.vertical_acc
        player.y += player.vertical_speed


    player.update_position()


    # --- Background
    screen.fill(BLACK)


    # --- Making stuff appear
    screen.blit(object.image, object.rect.topleft)
    screen.blit(player.image, player.rect.topleft)


    pg.display.flip()
    clock.tick(60)


pg.quit()