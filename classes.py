import pygame as pg
from pngs import player_png, rectangle_png

size = (1000, 500)
screen = pg.display.set_mode(size)

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
    
    def render(self, screen, camera):
        render_rect = camera.apply(self.rect)
        screen.blit(self.image, self.rect.topleft)


class Object():
    def __init__(self, x, y):
        self.image = rectangle_png
        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)

    def render(self, screen, camera):
        render_rect = camera.apply(self.rect)
        screen.blit(self.image, self.rect.topleft)
        
class Camera:
    def __init__(self, target, screen_width, screen_height):
        self.target = target
        self.offset_x = 0
        self.offset_y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.offset_x = self.target.x - self.screen_width // 2
        self.offset_y = self.target.y - self.screen_height // 2

    def apply(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)

