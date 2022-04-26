import pygame, sys
from settings import *
from level import Level

# sets the fps for the game
# anything other than 60 is not recommended - game speed is tied to fps
window_size = (screen_width, screen_height)
fps = 60

# Pygame
pygame.init()
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Wizard Quest")
clock = pygame.time.Clock() # sets the game clock
level = Level(level_map, screen)

while True: # rendering pipeline (keep as fast as possible)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        

    screen.fill(background_color) # background color
    level.draw()


    pygame.display.update()
 
    
    clock.tick(fps)