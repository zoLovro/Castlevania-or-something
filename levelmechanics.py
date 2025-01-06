import pygame as pg

############################################### IMAGES ###############################################
breakable_entrance = pg.image.load("data/pngs/lvl1/entrance/breakable_entrance.png")

############################################### CLASSES ###############################################
class BreakableTile(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = breakable_entrance
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def render(self, screen, camera):
        render_rect = camera.apply(self.rect)
        screen.blit(self.image, render_rect.topleft)

class Stairs(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()