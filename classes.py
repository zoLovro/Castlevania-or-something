import pygame as pg
from pngs import player_png, rectangle_png

size = (1000, 500)
screen = pg.display.set_mode(size)
gravity = 1

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # --- Image stuff
        self.image = player_png
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

        # --- Positional stuff
        self.x = x
        self.y = y
        self.rect.topleft = (self.x, self.y)

        # --- Movement
        self.vertical_speed = 0
        self.horizontal_speed = 5
        self.vertical_acc = 1.1
        self.max_speed = 3

        # --- Jumping
        self.isJump = False
        self.jump_height = 20
        self.y_velocity = self.jump_height

    def jump(self):
        self.y -= self.y_velocity
        self.y_velocity -= gravity
        if self.y_velocity < -self.jump_height:
            self.isJump = False
            self.y_velocity = self.jump_height

    def update_position(self):
        self.rect.topleft = (self.x, self.y)
    
    def render(self, screen, camera):
        render_rect = camera.apply(self.rect)
        screen.blit(self.mask_image, render_rect.topleft)


class Object():
    def __init__(self, x, y):
        self.image = rectangle_png
        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)

    def render(self, screen, camera):
        render_rect = camera.apply(self.rect)
        screen.blit(self.image, render_rect.topleft)
        
class Camera:
    def __init__(self, target, screen_width, screen_height):
        self.target = target
        self.offset_x = 0
        self.offset_y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.offset_x = self.target.x - self.screen_width // 2
        self.offset_y = 0

    def apply(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)