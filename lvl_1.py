import pygame as pg
############################################### IMAGES ###############################################
# --- BACKGROUNDS ---
castle_entrance_bg = pg.image.load("data/pngs/lvl1/entrance/castle_entrance_bg.png")

# --- PLAYMAPS --- 
entrance_playmap = pg.image.load("data/pngs/lvl1/entrance/playmap.png")


############################################### CLASSES ###############################################
class Entrance():
    def __init__(self):
        self.image = entrance_playmap
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

    def render(self, screen, camera):
        render_rect = camera.apply(self.rect)
        screen.blit(self.mask_image, render_rect.topleft)

class Entrance_bg():
    def __init__(self):
        self.image = castle_entrance_bg
        self.rect = self.image.get_rect()

    def render(self, screen, camera):
        render_rect = camera.apply(self.rect)
        screen.blit(self.image, render_rect.topleft)
