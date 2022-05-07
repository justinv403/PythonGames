import pygame
from game_data import levels
from support import import_folder
from decoration import Skybox

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed, path):
        super().__init__() # python magic
        # creates the sprite for a node
        self.frames = import_folder(path)
        self.frame_index = 0

        self.image = self.frames[self.frame_index]
        if status == "available":
            self.status = "available"
        else:
            self.status = "locked"
        self.rect = self.image.get_rect(center = pos)

        # collision detection to snap the player to the node
        # also sizes the rectangle to the exact size needed for the specific speed of the player icon
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed/2), self.rect.centery - (icon_speed/2), icon_speed, icon_speed)

    def animate(self):
        """
        Applies animation to overworld
        """
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.status == "available":
            self.animate()
        else:
            tint_surf = self.image.copy()
            tint_surf.fill("black", None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf, (0,0))


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        """
        Initializes the Icon object
        """
        super().__init__() # python magic
        self.pos = pos
        self.image = pygame.image.load("./graphics/overworld/hat.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        """
        Updates the icon object
        """
        self.rect.center = self.pos # fixes for rectangles only being able to use ints


class Overworld:
    def __init__(self, start_level, max_level, surface, create_level):
        """
        Creates the overworld object
        """

        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level + 1
        self.create_level = create_level # create level function passed

        # movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8

        # sprites
        self.setup_nodes()
        self.setup_icon()
        self.skybox = Skybox(8, "overworld")
    
    def setup_nodes(self):
        """
        Gets the nodes and positions of nodes to prep for display
        """
        self.nodes = pygame.sprite.Group()

        for index, node in enumerate(levels.values()):
            if index < self.max_level:
                sprite_node = Node(node["node_pos"], "available", self.speed, node["node_graphics"])
            else:
                sprite_node = Node(node["node_pos"], "locked", self.speed, node["node_graphics"])
            self.nodes.add(sprite_node)
    

    def paths(self):
        """
        Draws the paths between the overworld levels
        """
        if self.max_level > 0:
            points = [node["node_pos"] for index, node in enumerate(levels.values()) if index <= self.max_level]
            
            # this uses the line width and color settings recommended by the tutorial (README)
            pygame.draw.lines(self.display_surface, "#a04f45", False, points, 6)
        

    def setup_icon(self):
        """
        Prepares a icon as a sprite
        """
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)


    def input(self):
        """
        Gets the user input for the overworld screen
        """
        keys = pygame.key.get_pressed()

        if not self.moving:
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data("right")
                self.current_level += 1
                self.moving = True
            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.current_level > 0:
                self.move_direction = self.get_movement_data("left")
                self.current_level -= 1
                self.moving = True
            elif (keys[pygame.K_SPACE] or keys[pygame.K_KP_ENTER]):
                self.create_level(self.current_level)

    def get_movement_data(self, direction):
        # gets the initial position of the player
        start_vector = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        
        # selects the correct direction to move the player
        if direction == "left":
            end_vector = pygame.math.Vector2(self.nodes.sprites()[self.current_level-1].rect.center)
        elif direction == "right":
            end_vector = pygame.math.Vector2(self.nodes.sprites()[self.current_level+1].rect.center)
        else:
            end_vector = start_vector

        return (end_vector - start_vector).normalize() # returns a normalized vector for the direction the player needs to go

    def update_icon(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)

    def run(self):
        self.input()
        self.update_icon()
        self.icon.update()
        self.nodes.update()
        
        self.skybox.draw(self.display_surface)
        
        self.paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)