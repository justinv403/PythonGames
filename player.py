import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos): # initialization of the player
        super().__init__()
        self.image = pygame.Surface((32,64)) # must be a tuple
        self.image.fill("white") # player color
        self.rect = self.image.get_rect(topleft = pos)
        
        # player movement
        self.direction = pygame.math.Vector2(0,0) # 2d vector on a player's movement
        self.speed = 8 # speed multiplier for the player
        self.gravity = 0.8
        self.jump_height = -16 # vertical height is backwards

    def get_input(self):
        # gets the keys pressed by the user
        keys = pygame.key.get_pressed()
        
        # gives the user velocity in a direction
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        if keys[pygame.K_UP] or keys[pygame.K_SPACE] or keys[pygame.K_w]:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_height

    def update(self): # the second variable is not needed, so it is given a null value
        self.get_input()
        self.apply_gravity()