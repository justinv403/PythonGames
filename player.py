import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        # initialization of the player
        super().__init__()
        self.image = pygame.Surface((32,64)) # must be a tuple
        self.image.fill("white") # player color
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direction = pygame.math.Vector2(0,0) # 2d vector on a player's movement
        self.speed = 8 # speed multiplier for the player
    
    def get_input(self):
        # gets the keys pressed by the user
        keys = pygame.key.get_pressed()
        
        # gives the user velocity in a direction
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def update(self, null): # the second variable is not needed, so it is given a null value
        self.get_input()
        self.rect.x += self.direction.x * self.speed