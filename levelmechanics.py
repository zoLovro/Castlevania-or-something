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

def generate_stair_pattern(start_x, start_y, step_x, step_y, count):
    coordinates = []
    for i in range(count):
        if i % 3 == 2:  # Every third element
            # Place on top of the previous element
            x, y = coordinates[-1][0], coordinates[-1][1] - step_y
        else:
            # For the first two, x is the same; y increases
            x = start_x + (i // 3) * step_x
            y = start_y if i % 3 == 0 else start_y + step_y
        
        coordinates.append((x, y))
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