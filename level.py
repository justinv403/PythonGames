import pygame
from tiles import Tile
from settings import tile_size

class Level:
    def __init__(self, level_data, surface):
        # level setup
        self.display_surface = surface
        self.create_level(level_data)
        self.world_shift = 0 # player movement

    def create_level(self, layout):
        self.tiles = pygame.sprite.Group()

        for h_index,row in enumerate(layout): # interprets the level to be displayed from the "text" file
            for v_index,col in enumerate(row):
                if col == "X": # ground tile
                    h_pos = v_index * tile_size
                    v_pos = h_index * tile_size
                    tile = Tile((h_pos, v_pos), tile_size)
                    self.tiles.add(tile)

    def draw(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)