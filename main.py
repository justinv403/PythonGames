import pygame, sys
from settings import *
from overworld import Overworld
from level import Level

# game object
class Game:
    def __init__(self):
        self.max_level = 2
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = "overworld"

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = "overworld"
    
    def create_level(self, current_level):
        self.level = Level(current_level + 1, screen, self.create_overworld)
        self.status = "level"

    def run(self):
        if self.status == "overworld":
            self.overworld.run()
        else:
            self.level.run()

# sets the fps for the game
# anything other than 60 is not recommended - game speed is tied to fps
window_size = (screen_width, screen_height)
fps = 60

# Pygame
pygame.init()
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Wizard Quest")
clock = pygame.time.Clock() # sets the game clock
game = Game()

while True: # rendering pipeline (keep as fast as possible)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # handles quitting of the game (user presses the x)
            pygame.quit()
            sys.exit()
        

    screen.fill(background_color) # background color
    game.run()

    pygame.display.update()
 
    
    clock.tick(fps)