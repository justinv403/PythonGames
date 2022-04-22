import pygame
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos): # initialization of the player
        super().__init__()
        # character animation and assets
        self.character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15

        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        # player movement
        self.direction = pygame.math.Vector2(0,0) # 2d vector on a player's movement
        self.speed = 8 # speed multiplier for the player
        self.gravity = 0.8
        self.jump_height = -16 # vertical height is backwards

        # player state
        self.status = "idle"
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def character_assets(self):
        character_data = "./graphics/character/"
        self.animations = {"idle":[],"running":[],"jump":[],"falling":[]}

        for animation in self.animations.keys():
            full_path = character_data + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image
        
        # set the rectangle positions
        if self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)


    def get_input(self):
        # gets the keys pressed by the user
        keys = pygame.key.get_pressed()
        
        # gives the user velocity in a direction
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 1:
            self.status = "falling"
        else:
            if self.direction.x > 0 or self.direction.x < 0:
                self.status = "running"
            else:
                self.status = "idle"

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_height

    def update(self): # the second variable is not needed, so it is given a null value
        self.get_input()
        self.get_status()
        self.animate()