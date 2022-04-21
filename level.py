import pygame
from tiles import Tile

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.create_level(level_data)

    def create_level(self, layout):
        self.tiles = pygame.sprite.Group()

        for row in layout:
            print(row)

    def draw(self):
        self.tiles.draw(self.display_surface)