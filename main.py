import pygame as pg
from classes import Player, Object, Camera
from lvl_1 import Entrance, Entrance_bg

pg.init()

size = (750, 750)
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
object = Object(100, 630)


# --- Camera
camera = Camera(player, size[0], size[1])

# --- Levels
entrance = Entrance()
entrance_bg = Entrance_bg()

# --- Main loop
running = True
while running:
    # --- Events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # --- Collision logic
    colliding = player.rect.colliderect(entrance.rect)
    if colliding:
        player.vertical_speed = 0

############################################### INPUT ###############################################
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        player.x -= player.horizontal_speed
        moving = True
    if keys[pg.K_RIGHT]:
        player.x += player.horizontal_speed
        moving = True
    else:
        moving = False

############################################### LOGIC ###############################################
    # --- Jumping logic
    if colliding:
        if not player.isJump:
            if keys[pg.K_UP]:
                player.isJump = True
    if player.isJump:
        player.jump()


    # --- Gravity logic
    if not colliding:
        player.vertical_speed += player.vertical_acc
        player.y += player.vertical_speed


    player.update_position()
    camera.update()


############################################### RENDERS ###############################################
    # --- BACKGROUND --- 
    entrance_bg.render(screen, camera)

    # --- PLAYER AND OBJECTS ---
    entrance.render(screen, camera)
    player.render(screen, camera)


    pg.display.flip()
    clock.tick(60)


pg.quit()