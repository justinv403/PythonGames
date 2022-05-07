import pygame, sys
from settings import *
from overworld import Overworld
from level import Level
from ui import UI

# game object
class Game:
    def __init__(self):
        
        # game variables
        self.max_level = 2
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        # overworld
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = "overworld"

        # user interface
        self.ui = UI(screen)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = "overworld"

    def create_level(self, current_level):
        self.level = Level(current_level + 1, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = "level"

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.cur_health += amount
    
    def check_game_over(self):
        if self.cur_health <= 0:
            self.cur_health = 100
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = "overworld"

    def run(self):
        if self.status == "overworld":
            self.overworld.run()
        else:
            self.level.draw()
            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()

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