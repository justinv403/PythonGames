import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        # initialization of the player
        super().__init__()
        self.image = pygame.Surface((32,64)) # must be a tuple
        self.image.fill("white") # player color
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0) # 2d vector on a player's movement
    
    def get_input(self):
        # gets the keys pressed by the user
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_W]:
            pass
        if keys[pygame.K_A]:
            pass
        if keys[pygame.K_D]:
            pass