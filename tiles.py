import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
    """
    Main Tile class to create each subsequent tile type

    :param1 pygame.sprite.Sprite: takes pygame sprite as inheritance
    """
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x,y))
    
    def update(self, shift):
        self.rect.x += shift


class StaticTile(Tile):
    """
    Handles all types of static tiles (inherited)
    Inherits a lot of info from Tile class, but saves resources
    """
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class AnimatedTile(Tile):
    """
    Important to create a animated tile
    Use inheritance and super() to create a new type if necessary

    :param1 Tile: takes inheritance from the Tile class
    """
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
    
    def animate(self):
        anim_speed = 0.15
        
        self.frame_index += anim_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        #self.image = pygame.transform.scale(self.image, (376/4,256/4))
    
    def update(self, shift):
        self.animate()
        self.rect.x += shift


class Coin(AnimatedTile):
    """
    Creates the "Coin" animated tile type
    """
    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y))
        self.value = value