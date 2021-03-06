from settings import vertical_tile_number, tile_size, screen_width
import pygame
from tiles import AnimatedTile
from support import import_folder
from random import choice, randint

class Skybox:
    def __init__(self, horizon, style = "level"):
        self.top = pygame.image.load("./graphics/decoration/sky_box/top.png").convert()
        self.middle = pygame.image.load("./graphics/decoration/sky_box/middle.png").convert()
        self.bottom = pygame.image.load("./graphics/decoration/sky_box/bottom.png").convert()

        self.horizon = horizon

        # stretch
        self.top = pygame.transform.scale(self.top,(screen_width, tile_size))
        self.middle = pygame.transform.scale(self.top,(screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.top,(screen_width, tile_size))
    
        self.style = style
        if self.style == "overworld":
            background_surfaces = import_folder("./graphics/overworld/background")
            self.back = []

            for surface in [choice(background_surfaces) for image in range(10)]:
                x = randint(0, screen_width)
                y = (self.horizon * tile_size) + randint(50, 100)
                rect = surface.get_rect(midbottom = (x, y))
                self.back.append((surface, rect))
            

    def draw(self, surface):
        x = 0 # is always 0 for a level
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (x, y))
            elif row == self.horizon:
                surface.blit(self.middle,(x, y))
            else:
                surface.blit(self.bottom, (x, y))
        
        if self.style == "overworld":
            for bg in self.back:
                surface.blit(bg[0], bg[1])

class Water:
    def __init__(self, top, level_width):
        water_start = -screen_width
        water_tile_width = 192/2 # width of the water tile image
        tile_x_amount = int((level_width + screen_width * 2) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192/2, x, y, "./graphics/decoration/water")
            self.water_sprites.add(sprite)
        
    
    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)

