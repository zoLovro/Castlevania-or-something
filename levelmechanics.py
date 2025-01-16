import pygame as pg
from pngs import rectangle_png
############################################### IMAGES ###############################################
breakable_tile = pg.image.load("data/pngs/objects/breakableTile.png")
floating_tile = pg.image.load("data/pngs/objects/floatingTile.png")
stairs_tile = pg.image.load("data/pngs/objects/stairTile.png") 

############################################### CLASSES ###############################################
class Floor(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = rectangle_png
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def render(self, screen, camera):
        render_rect = camera.apply(self.rect)
        screen.blit(self.image, render_rect.topleft)

class BreakableTile(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = breakable_tile
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

        # For removing tile
        self.timer_start = None
        self.collided_object = None
        self.removal_duration = 3000

    def render(self, screen, camera):
        render_rect = camera.apply(self.rect)
        screen.blit(self.image, render_rect.topleft)

class Stairs(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = stairs_tile
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

        self.active = False # If player is on stairs

    def render(self, screen, camera):
        render_rect = camera.apply(self.rect)
        screen.blit(self.image, render_rect.topleft)

def generate_stair_pattern(start_x, start_y, hx, hy, count):
    coordinates = []
    coordinates.append((start_x,start_y))
    count += (count//3) + 1
    deljeno = 0
    for x in range(1,count):
        if x % 3 == 2:
            coordinates.append((coordinates[x - 1][0], coordinates[x - 1][1] - hy))
            deljeno += 2
        else:
            xcord = start_x + hx * (x - deljeno)
            coordinates.append((xcord, coordinates[x - 1][1]))
    return coordinates

def generate_reverse_stair_pattern(start_x, start_y, hx, hy, count):
    coordinates = []
    coordinates.append((start_x, start_y))
    count += (count // 3) + 1
    deljeno = 0

    for x in range(1, count):
        if x % 3 == 2:
            # Move vertically downwards
            coordinates.append((coordinates[x - 1][0], coordinates[x - 1][1] - hy))
            deljeno += 2
        else:
            # Move horizontally to the left
            xcord = start_x - hx * (x - deljeno)
            coordinates.append((xcord, coordinates[x - 1][1]))

    return coordinates
class FloatingTile(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = floating_tile
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def render(self, screen, camera):
        render_rect = camera.apply(self.rect)
        screen.blit(self.image, render_rect.topleft)