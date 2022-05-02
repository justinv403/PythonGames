import pygame
from support import import_csv_layout, import_cut_graphic
from settings import tile_size
from tiles import AnimatedTile, Tile, StaticTile, Coin

class Level:
    def __init__(self, level_data, surface):
        """
        Creation of the level class
        """
        
        # general setup
        self.display_surface = surface
        self.world_shift = 0

        # terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # coins
        coin_layout = import_csv_layout(level_data["coins"])
        self.coin_sprites = self.create_tile_group(coin_layout, "coins")
    
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1": # csv is in terms of strings
                    x = col_index * tile_size
                    y = row_index * tile_size

                    # handles the different types of objects to render
                    if type == "terrain":
                        terrain_tile_list = import_cut_graphic("./graphics/terrain/Mossy Tileset/Mossy - TileSet.png")
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    
                    if type == "coins":
                        if val == "0":
                            sprite = Coin(tile_size, x, y, "./graphics/coins/gold/anim")
                        #if val == "1": FIXME: Error out of range for silver coins
                        #    sprite = Coin(tile_size, x, y, "./grahpics/coins/silver/anim")
                    
                    sprite_group.add(sprite)

        return sprite_group


    
    def run(self):
        """
        Runs the entire game/level
        Rendering order - things rendered after render on top
        """

        # terrain sprites
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        # coin sprites
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)