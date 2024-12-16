import pygame as pg

size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

while True:

    # --- Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # ---Background
    screen.fill(WHITE)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()