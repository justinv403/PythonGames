import pygame
from game_data import levels

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed):
        super().__init__() # python magic
        # creates the sprite for a node
        self.image = pygame.Surface((200, 200))
        if status == "available":
            self.image.fill("red")
        else:
            self.image.fill("grey")
        self.rect = self.image.get_rect(center = pos)

        # collision detection to snap the player to the node
        # also sizes the rectangle to the exact size needed for the specific speed of the player icon
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed/2), self.rect.centery - (icon_speed/2), icon_speed, icon_speed)

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__() # python magic
        self.pos = pos
        self.image = pygame.Surface((20,20))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center = pos)

    def update(self):
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
    
    def setup_nodes(self):
        """
        Gets the nodes and positions of nodes to prep for display
        """
        self.nodes = pygame.sprite.Group()

        for index, node in enumerate(levels.values()):
            if index < self.max_level:
                sprite_node = Node(node["node_pos"], "available", self.speed)
                self.nodes.add(sprite_node)
            else:
                sprite_node = Node(node["node_pos"], "locked", self.speed)
            self.nodes.add(sprite_node)
    
    def paths(self):
        prev_node = (0,0) # default line position (offscreen)
        for index, node in enumerate(levels.values()):
            if index < self.max_level:
                pygame.draw.line(self.display_surface, "red", prev_node, node["node_pos"], 6)
            else:
                pygame.draw.line(self.display_surface, "grey", prev_node, node["node_pos"], 6)
            prev_node = node["node_pos"]
        
    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)


    def input(self):
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
        self.paths()
        self.nodes.draw(self.display_surface)
        self.update_icon()
        self.icon.update()
        self.icon.draw(self.display_surface)