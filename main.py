import pygame as pg
from classes import Player, Camera
from levels import Level1
from levelmechanics import BreakableTile, Floor
from pngs import idle_png

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
moving_right = False
moving_left = False
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
breakablePos = [(2028, 460), (2078, 460), (2128, 460), (2178, 460)]
breakableTiles_group = pg.sprite.Group()
for pos in breakablePos:
    breakableTile = BreakableTile(pos[0], pos[1])
    breakableTiles_group.add(breakableTile)

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

############################################### COLLISION LOGIC ###############################################
    # --- FLOOR ---
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

    # --- BREAKABLE TILES ---
    if 2000 < player.x < 2200:
        collided_breakableTile = pg.sprite.spritecollide(player, breakableTiles_group, False)
        closest_breakableTile = min(breakableTiles_group, key=lambda tile: abs(tile.rect.centerx - player.rect.centerx))
        if player.rect.colliderect(closest_breakableTile.rect):
            player.vertical_velocity = 0
            player.y = closest_breakableTIle.rect.top - player.rect.height
            player.jumpCheck = False
        else:
            # Apply gravity if no collision
            player.vertical_velocity += gravity
            player.y += player.vertical_velocity
        # Prevent overshooting the floor during collision
        if collided_breakableTile:
            for floor in collided_breakableTile:
                player.y = min(player.y, floor.rect.top - player.rect.height)
############################################### INPUT ###############################################
    # --- Timer for animation handling ---
    dt = clock.get_time() / 1000
    print(player.x)
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        player.x -= player.horizontal_speed
        moving = True
        player.walk_left_animate(dt)
    elif keys[pg.K_RIGHT]:
        player.x += player.horizontal_speed
        moving = True
        player.walk_right_animate(dt)
    else:
        player.stop_animation()

    # --- Jumping logic
    if collided_floor or collided_breakableTile and not player.canJump:
        if keys[pg.K_x]:
            player.canJump = True
    if player.canJump:
        player.jump()
        jumpCheck = True
    if player.rect.colliderect(closest_floor.rect) and jumpCheck:
        jumpCheck = False

    player.update_position()
    camera.update()

############################################### RENDERS ###############################################
    # --- BACKGROUND --- 
    screen.fill(BLACK)

        # --- PLAYMAPS ---
    level1.render(screen, camera)

    # --- PLAYER AND OBJECTS ---
    for tile in breakableTiles_group:
        adjusted_btile_rect = camera.apply(tile.rect)
        screen.blit(tile.image, adjusted_btile_rect.topleft)
    for floor in floor_group:
        adjusted_floor_rect = camera.apply(floor.rect)
        screen.blit(floor.image, adjusted_floor_rect.topleft)

    
    # --- PLAYER ---
    player.render(screen, camera)

    pg.display.flip()
    clock.tick(60)


pg.quit()