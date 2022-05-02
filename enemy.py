import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        """
        Initialization of the enemy class

        :param1 size: takes the size of the enemy sprite
        :param2 x: takes the x position of the enemy
        :param3 y: takes the y postition of the enemy
        """
        super().__init__(size, x, y, "./graphics/enemy/anim")
        self.rect.y += size - self.image.get_size()[1] + 14 # 12 is offset to make it look better
        self.speed = randint(2,3)


    def move(self):
        """
        Movement for the enemy
        """
        self.rect.x += self.speed


    def reverse_image(self):
        """
        Flips the image to ensure the
        """
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        """
        Flips the movement direction when called
        """
        self.speed *= -1

    def update(self, shift):
        """
        Updates the enemy object

        :param1 shift: Takes the world shift to update the enemy properly even if the world is moving
        """
        self.rect.x += shift
        self.animate() # inherited from animated tile
        self.move()
        self.reverse_image()