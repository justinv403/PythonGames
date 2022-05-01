import pygame, sys
from settings import *
from level import Level
from game_data import level_1

# sets the fps for the game
# anything other than 60 is not recommended - game speed is tied to fps
window_size = (screen_width, screen_height)
fps = 60

# Pygame
pygame.init()
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Wizard Quest")
clock = pygame.time.Clock() # sets the game clock
level = Level(level_1, screen)

while True: # rendering pipeline (keep as fast as possible)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        

    screen.fill(background_color) # background color
    level.run()

    pygame.display.update()
 
    
    clock.tick(fps)