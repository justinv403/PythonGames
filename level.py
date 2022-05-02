import pygame
from support import import_csv_layout, import_cut_graphic
from settings import tile_size
from tiles import AnimatedTile, Tile, StaticTile, Coin
from enemy import Enemy

class Level:
    def __init__(self, level_data, surface):
        """
        Creation of the level class
        """
        
        # general setup
        self.display_surface = surface
        self.world_shift = -9

        # player setup
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # coins
        coin_layout = import_csv_layout(level_data["coins"])
        self.coin_sprites = self.create_tile_group(coin_layout, "coins")
    
        # enemy
        enemy_layout = import_csv_layout(level_data["enemies"])
        self.enemy_sprites = self.create_tile_group(enemy_layout, "enemies")

        # constraints 
        # hidden constraint boxes for enemy movement
        constraint_layout = import_csv_layout(level_data["constraints"])
        self.constraint_sprites = self.create_tile_group(constraint_layout, "constraint")


    def create_tile_group(self, layout, type):
        """
        Creates a tile group to render
        
        :param1 layout: list from the csv interpreter (import_csv_layout) for each group
        :param2 type: string containing the name of the type of sprite group to create
        """
        
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
                    
                    if type == "enemies":
                        sprite = Enemy(tile_size, x, y)

                    if type == "constraint":
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    
    def player_setup(self, layout):
        """
        Sets up the player
        """
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size - (3*tile_size)
                if val != "0": # csv is in terms of strings
                    pass
                    print("player goes here")
                if val != "1": # csv is in terms of strings
                    hat_surface = pygame.image.load("./graphics/character/hat/wizhat-blue-72x72-2.png")
                    hat_surface = pygame.transform.scale(hat_surface, (48,48)).convert_alpha()
                    sprite = StaticTile(tile_size, x+8, y+8, hat_surface)
                    self.goal.add(sprite)


    def enemy_collision_reverse(self):
        """
        Flips the enemy direction if they collide with a constraint
        """
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False): # false means it doesn't destroy the constraint
                enemy.reverse()


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

        # enemy sprites
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # player sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)