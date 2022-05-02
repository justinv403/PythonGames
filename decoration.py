from settings import vertical_tile_number, tile_size, screen_width
import pygame

class Skybox:
    def __init__(self, horizon):
        self.top = pygame.image.load("./graphics/decoration/sky_box/top.png")
        self.middle = pygame.image.load("./graphics/decoration/sky_box/middle.png")
        self.bottom = pygame.image.load("./graphics/decoration/sky_box/bottom.png")

        self.horizon = horizon

        # stretch
        self.top = pygame.transform.scale(self.top,(screen_width, tile_size))
        self.middle = pygame.transform.scale(self.top,(screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.top,(screen_width, tile_size))

    
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