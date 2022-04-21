import pygame
from tiles import Tile
from settings import tile_size, screen_width
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
        for row_index,row in enumerate(layout):
            for col_index,col in enumerate(row):
                # gets the position to place (whatever it is to be placed)
                x = col_index * tile_size
                y = row_index * tile_size

                
                if col == "X": # ground tile
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if col == "P": # player spawn position
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)


    def scroll_x(self): # horizontal level scrolling logic
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        # finds where the player is and determines whether the screen should shift or not
        if player_x < (screen_width / 3)  and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width - (screen_width / 3)) and direction_x > 0:
            self.world_shift = -8
            player.speed = -0
        else:
            self.world_shift = 0
            player.speed = 8


    def horizontal_collision(self): # handles horizontal collision of the player
        player = self.player.sprite # gets the player sprite so it doesn't have to be specifically called each time
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites(): # sets the player to the right side of whatever they collide with
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
    

    def vertical_collision(self): # handles vertical collision of the player and some gravity logic
        player = self.player.sprite
        player.apply_gravity()

        # prevents the player from going up through an object or through an object below
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0 # fixes gettings stuck to ceilings
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0 # fixes infinity gravity glitch on floors


    def draw(self): # drawing of the level
        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # player
        self.player.update()
        self.horizontal_collision()
        self.vertical_collision()
        self.player.draw(self.display_surface)