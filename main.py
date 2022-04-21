import pygame, sys
from settings import *
from tiles import Tile
from level import Level

# sets the fps for the game
fps = 60

# Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock() # sets the game clock
level = Level(level_map, screen)

while True: # rendering pipeline (keep as fast as possible)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    screen.fill("black")
    level.draw

    pygame.display.update()
    
    clock.tick(fps)