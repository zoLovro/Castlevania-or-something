import pygame as pg
from classes import Player, Camera
from levels import Floor, Level1
from levelmechanics import BreakableTile

pg.init()

size = (600, 600)
screen = pg.display.set_mode(size)
lvl_width = 3075

BLACK = (0, 0, 0)

pg.display.set_caption("Castlevania but better")

# --- Used to manage how fast the screen updates
clock = pg.time.Clock()

# --- Global gravity
gravity = 0.8

# --- Player
player = Player(100, 400)
player_collision = False
moving = False
jumpCheck = False

# --- Floor --- 
exclusions = []
lvlFloorPos = [(x, 510) for x in range(0, 1920, 60)
                if not any(start <= x <= end for start, end in exclusions)]
floor_group = pg.sprite.Group()
for pos in lvlFloorPos:
    floor = Floor(pos[0], pos[1])
    floor_group.add(floor)

# --- Breakable tiles ---
breakablePos = [(2028, 458), (2078, 458), (2128, 458), (2178, 458)]
breakableTiles_group = pg.sprite.Group()
for pos in breakablePos:
    breakableTile = BreakableTile(pos[0], pos[1])
    breakableTiles_group.add(breakableTile)

# --- Stairs ---


# --- Groups ---
player_group = pg.sprite.Group()

# --- Camera ---
camera = Camera(player, size[0], size[1], boundaries=(0, lvl_width))

# --- Levels ---
level1 = Level1(0, 0)
##################################################### MAIN LOOP ######################################
running = True
while running:
    # --- Events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

############################################### LOGIC ###############################################
    # --- Collision logic
    collided_floor = pg.sprite.spritecollide(player, floor_group, False)
    closest_floor = min(floor_group, key=lambda tile: abs(tile.rect.centerx - player.rect.centerx))
    if player.rect.colliderect(closest_floor.rect):
        player.vertical_velocity = 0
        player.y = closest_floor.rect.top - player.rect.height
        player.jumpCheck = False
    else:
        # Apply gravity if no collision
        player.vertical_velocity += gravity
        player.y += player.vertical_velocity
    # Prevent overshooting the floor during collision
    if collided_floor:
        for floor in collided_floor:
            player.y = min(player.y, floor.rect.top - player.rect.height)

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

    # --- Jumping logic
    if collided_floor and not player.canJump:
        if keys[pg.K_UP]:
            player.canJump = True
    if player.canJump:
        player.jump()
        jumpCheck = True
    if player.rect.colliderect(closest_floor.rect) and jumpCheck:
        jumpCheck = False

    print(player.canJump)
    player.update_position()
    camera.update()

############################################### RENDERS ###############################################
    # --- BACKGROUND --- 
    screen.fill(BLACK)

    # # --- PLAYMAPS ---
    # level1.render(screen, camera)

    # --- PLAYER AND OBJECTS ---
    for tile in breakableTiles_group:
        adjusted_btile_rect = camera.apply(tile.rect)
        screen.blit(tile.image, adjusted_btile_rect.topleft)
    for floor in floor_group:
        adjusted_floor_rect = camera.apply(floor.rect)
        screen.blit(floor.image, adjusted_floor_rect.topleft)

# --- PLAYMAPS ---
    level1.render(screen, camera)
    
    player.render(screen, camera)

    pg.display.flip()
    clock.tick(60)


pg.quit()