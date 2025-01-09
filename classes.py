import pygame as pg
import json
from pngs import idle_png, rectangle_png

size = (600, 600)
screen = pg.display.set_mode(size)
gravity = 1

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # --- Image stuff
        self.idle_image = idle_png
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

        # --- WALKING ANIMATION ---
        # Right
        self.walking_right_spritesheet = Spritesheet("data/pngs/player/spritesheets/walking_right.png",
                                                "data/pngs/player/spritesheets/json_files/walking_right.json")
        self.walking_right_animation = [
                                self.walking_right_spritesheet.parse_sprite('walk1.png'),
                                self.walking_right_spritesheet.parse_sprite('walk2.png'), 
                                self.walking_right_spritesheet.parse_sprite('walk3.png'), 
                                self.walking_right_spritesheet.parse_sprite('walk4.png'), 
                                self.walking_right_spritesheet.parse_sprite('walk5.png'),
                                self.walking_right_spritesheet.parse_sprite('walk6.png')
                                ]

        # Left
        self.walking_left_spritesheet = Spritesheet("data/pngs/player/spritesheets/walking_left.png",
                                                "data/pngs/player/spritesheets/json_files/walking_left.json")
        self.walking_left_animation = [
                                self.walking_left_spritesheet.parse_sprite('walk1.png'),
                                self.walking_left_spritesheet.parse_sprite('walk2.png'), 
                                self.walking_left_spritesheet.parse_sprite('walk3.png'), 
                                self.walking_left_spritesheet.parse_sprite('walk4.png'), 
                                self.walking_left_spritesheet.parse_sprite('walk5.png'),
                                self.walking_left_spritesheet.parse_sprite('walk6.png')
                                ]
        self.index = 0
        self.animation_speed = 0.1
        self.animation_timer = 0

        # --- Positional stuff
        self.x = x
        self.y = y
        self.rect.topleft = (self.x, self.y)
        self.vertical_velocity = 0
        self.horizontal_speed = 5

        # --- Jumping
        self.canJump = False
        self.jump_height = 20
        self.y_velocity = self.jump_height

    # --- Jumping ---
    def jump(self):
        self.y -= self.y_velocity
        self.y_velocity -= gravity
        if self.y_velocity <= 0:
            self.canJump = False
            self.y_velocity = self.jump_height

    ######## WALKING ########
    def walk_right_animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.index = (self.index + 1) % len(self.walking_right_animation)
            self.image = self.walking_right_animation[self.index]
            self.animation_timer = 0
    
    def walk_left_animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.index = (self.index + 1) % len(self.walking_left_animation)
            self.image = self.walking_left_animation[self.index]
            self.animation_timer = 0
    
    def stop_animation(self):
        self.image = idle_png
        self.index = 0

    def update_position(self):
        self.rect.topleft = (self.x, self.y)
    
    def render(self, screen, camera):
        render_rect = camera.apply(self.rect)
        screen.blit(self.image, render_rect.topleft)

class Camera:
    def __init__(self, target, screen_width, screen_height, boundaries):
        self.target = target
        self.offset_x = 0
        self.offset_y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.boundaries = boundaries

    def update(self):
        self.offset_x = self.target.x - self.screen_width // 2
        self.offset_y = 0

        # Boundaries
        min_x, max_x = self.boundaries
        self.offset_x = max(min_x, min(self.offset_x, max_x - self.screen_width))

    def apply(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)

class Spritesheet:
    def __init__(self, filename, meta_data):
        self.filename = filename
        self.sprite_sheet = pg.image.load(filename).convert()
        self.meta_data = meta_data
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):
        sprite = pg.Surface((w, h), pg.SRCALPHA)  # Ensure alpha transparency
        sprite.set_colorkey((0, 0, 0))  # Set transparency color (match your spritesheet background)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
        image = self.get_sprite(x, y, w, h)
        return image