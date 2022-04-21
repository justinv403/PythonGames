import pygame
from tiles import Tile
from settings import tile_size
from player import Player

class Level:
    def __init__(self, level_data, surface):
        # level setup
        self.display_surface = surface
        self.create_level(level_data)
        self.world_shift = 0 # player movement

    def create_level(self, layout):
        # creates the different tile categories
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        # interprets the level to be displayed from the "text" file
        for h_index,row in enumerate(layout):
            for v_index,col in enumerate(row):
                # gets the position to place (whatever it is to be placed)
                h_pos = v_index * tile_size
                v_pos = h_index * tile_size

                
                if col == "X": # ground tile
                    tile = Tile((h_pos, v_pos), tile_size)
                    self.tiles.add(tile)
                if col == "P": # player spawn position
                    player_sprite = Player((h_pos, v_pos))
                    self.tiles.add(player_sprite)

    def draw(self):
        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        # player
        self.player.draw(self.display_surface)