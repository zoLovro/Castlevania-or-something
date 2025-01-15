import pygame as pg
from classes import Player, Camera
from levels import Level1
from levelmechanics import BreakableTile, Floor, FloatingTile, Stairs, generate_stair_pattern
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
player = Player(900, 0)
player_collision = False
moving_right = False
moving_left = False
jumpCheck = False


# --- FLOOR --- 
exclusions = []
lvlFloorPos = [(x, 510) for x in range(0, 1920, 60)
                if not any(start <= x <= end for start, end in exclusions)]
floor_group = pg.sprite.Group()
for pos in lvlFloorPos:
    floor = Floor(pos[0], pos[1])
    floor_group.add(floor)

# --- BREAKABLE TILES ---
breakablePos = [(2028, 460), (2078, 460), (2128, 460), (2178, 460)]
breakableTiles_group = pg.sprite.Group()
for pos in breakablePos:
    breakableTile = BreakableTile(pos[0], pos[1])
    breakableTiles_group.add(breakableTile)

# --- FLOATING TILES ---
floatingPos = [(965 + i * 50, 220) for i in range(6)]
floatingTiles_group = pg.sprite.Group()
for pos in floatingPos:
    floatingTile = FloatingTile(pos[0], pos[1])
    floatingTiles_group.add(floatingTile)

# --- STAIRS ---
stairsPos = generate_stair_pattern(300, 300, 40, 40, 10)
print(stairsPos)
stairs_group = pg.sprite.Group()
for stair in stairsPos:
    stairs = Stairs(stair[0], stair[1])
    stairs_group.add(stairs)

# --- Camera ---
camera = Camera(player, size[0], size[1], boundaries=(0, lvl_width))

# --- Levels ---
level1 = Level1(0, 0)
##################################################### MAIN LOOP ###############################################
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
    if not 1975 < player.x < 2200 and not player.y < 280:
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

    # --- PLATFORMS --- 
    collided_platform = pg.sprite.spritecollide(player, floatingTiles_group, False)
    closest_platform = min(floatingTiles_group, key=lambda tile: abs(tile.rect.centerx - player.rect.centerx))
    if player.y < 280:
        if player.rect.colliderect(closest_platform.rect):
            player.vertical_velocity = 0
            player.y = closest_platform.rect.top - player.rect.height
            player.jumpCheck = False
        else:
            # Apply gravity if no collision
            player.vertical_velocity += gravity
            player.y += player.vertical_velocity
            # Prevent overshooting the floor during collision
            if collided_platform:
                for platform in collided_platform:
                    player.y = min(player.y, platform.rect.top - player.rect.height)

    # --- BREAKABLE TILES ---
    collided_breakableTile = pg.sprite.spritecollide(player, breakableTiles_group, False)
    closest_breakableTile = min(breakableTiles_group, key=lambda tile: abs(tile.rect.centerx - player.rect.centerx))
    if 1975 < player.x < 2210:
        if player.rect.colliderect(closest_breakableTile.rect):
            player.vertical_velocity = 0
            player.y = closest_breakableTile.rect.top - player.rect.height
            player.jumpCheck = False

            # --- BREAK LOGIC --- 
            if closest_breakableTile.timer_start is None:
                # Start the timer for this tile
                closest_breakableTile.timer_start = pg.time.get_ticks()
            else:
                current_time = pg.time.get_ticks()
                if current_time - closest_breakableTile.timer_start >= closest_breakableTile.removal_duration:
                    # Remove the tile after the timer ends
                    breakableTiles_group.remove(closest_breakableTile)
                    breakableTile.timer_start = None
                    breakableTile.collided_object = None
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
    #print((player.x, player.y))
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

############################################### LOGIC ###############################################
    # --- JUMPING LOGIC ---
    if collided_floor or collided_breakableTile or collided_platform and not player.canJump:
        if keys[pg.K_x]:
            player.canJump = True
    if player.canJump:
        player.jump()
        jumpCheck = True
    if player.rect.colliderect(closest_floor.rect) and jumpCheck:
        jumpCheck = False

    # --- BREAKABLE TILE BREAKING LOGIC ---


    player.update_position()
    camera.update()

############################################### RENDERS ###############################################
    # --- BACKGROUND --- 
    screen.fill(BLACK)

    # --- PLAYMAPS ---
    level1.render(screen, camera)

    # --- OBJECTS ---
    for tile in breakableTiles_group:
        adjusted_btile_rect = camera.apply(tile.rect)
        screen.blit(tile.image, adjusted_btile_rect.topleft)
    for floor in floor_group:
        adjusted_floor_rect = camera.apply(floor.rect)
        screen.blit(floor.image, adjusted_floor_rect.topleft)
    for floatingtile in floatingTiles_group:
        adjusted_ftile_rect = camera.apply(floatingtile.rect)
        screen.blit(floatingtile.image, adjusted_ftile_rect.topleft)
    for stair in stairs_group:
        adjusted_stile_rect = camera.apply(stair.rect)
        screen.blit(stair.image, adjusted_stile_rect.topleft)
    
    # --- PLAYER ---
    player.render(screen, camera)

    pg.display.flip()
    clock.tick(60)

pg.quit()