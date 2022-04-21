import pygame

class Tile(pygame.sprite.Sprite):
    
    def __init__(self, pos, size):
        super().__init__() # python magic

        self.image = pygame.Surface((size,size)) # makes a square tile
        self.image.fill("red") # sets the color of the tile
        self.rect = self.image.get_rect(topleft = pos) # puts the tile in the right spot