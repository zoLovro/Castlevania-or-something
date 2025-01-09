import pygame as pg
############################################### IMAGES ###############################################
# --- BACKGROUNDS ---
castle_entrance_bg = pg.image.load("data/pngs/lvl1/entrance/castle_entrance_bg.png")

# --- PLAYMAPS --- 
entrance_playmap = pg.image.load("data/pngs/lvl1/entrance/playmap.png")

############################################### CLASSES ###############################################

class Level1(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = entrance_playmap
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def render(self, screen, camera):
        render_rect = camera.apply(self.rect)
        screen.blit(self.image, render_rect.topleft)

