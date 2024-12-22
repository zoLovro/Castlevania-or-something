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

        # --- Movement
        self.vertical_speed = 0
        self.horizontal_speed = 2
        self.vertical_acc = 1.1
        self.jumping_acc = 5
        self.max_speed = 3


    def update_position(self):
        self.rect.topleft = (self.x, self.y)


class Object():
    def __init__(self, x, y):
        self.image = rectangle_png
        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)
        

