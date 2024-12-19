import pygame as pg
from pngs import player_png, rectangle_png

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # --- Image stuff
        self.image = player_png
        self.rect = self.image.get_rect()
        
        # --- Positional stuff
        self.x = x
        self.y = y
        self.rect.topleft = (self.x, self.y)


    def update_position(self):
        self.rect.topleft = (self.x, self.y)


class Object():
    def __init__(self, x, y):
        self.image = rectangle_png
        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)
        

