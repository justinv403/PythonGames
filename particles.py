import pygame
from support import import_folder

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,type):
        """
        Initialization of the ParticleEffect object
        """
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        if type == "jump":
            self.frames = import_folder("./graphics/character/dust_particles/jump")
        if type == "land":
            self.frames = import_folder("./graphics/character/dust_particles/land")
        if type == "explosion":
            self.frames = import_folder("./graphics/enemy/explosion")
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        """
        Animates the particle effects
        """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill() # destroys the sprite after the animation is over
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        """
        Updates the particle effects and position

        :param1 x_shift: takes the shift in the x axis to update the position
        """
        self.animate()
        self.rect.x += x_shift
