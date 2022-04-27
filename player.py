import pygame
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles): # initialization of the player
        super().__init__()
        # character animation and assets
        self.character_assets()
        self.frame_index = 0
        self.animation_speed = 0.4

        self.image = self.animations["idle"][self.frame_index]
        self.image = pygame.transform.scale(self.image, (154/4.5,278/4.5))
        self.rect = self.image.get_rect(topleft = pos)
        
        # dust particles
        self.import_dust_particles_run()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # player movement
        self.direction = pygame.math.Vector2(0,0) # 2d vector on a player's movement
        self.speed = 8 # speed multiplier for the player
        self.gravity = .8
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


    def import_dust_particles_run(self):
        self.dust_particles_run = import_folder("./graphics/character/dust_particles/run")


    def animate(self): # animation logic
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        image = pygame.transform.scale(image,(154/4.5,278/4.5))
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image
        
        # set the rectangle positions
        # collision scenarios for ground
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        # collision scenarios for the ceiling
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    
    def run_dust_animate(self): # renders the dust particles from player run if the player is running and on the ground
        if self.status == "running" and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_particles_run):
                self.dust_frame_index = 0
            
            dust_particle = self.dust_particles_run[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle,pos)
            elif not self.facing_right:
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                flipped_dust = pygame.transform.flip(dust_particle,True,False)
                self.display_surface.blit(flipped_dust,pos)


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
            self.create_jump_particles(self.rect.midbottom)


    def get_status(self):
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 1 or self.on_ground == False:
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


    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animate()