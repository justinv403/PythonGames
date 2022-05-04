import pygame
from game_data import levels

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status):
        super().__init__() # python magic
        # creates the sprite for a node
        self.image = pygame.Surface((200, 200))
        if status == "available":
            self.image.fill("red")
        else:
            self.image.fill("grey")
        self.rect = self.image.get_rect(center = pos)

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__() # python magic
        self.image = pygame.Surface((20,20))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center = pos)

class Overworld:
    def __init__(self, start_level, max_level, surface):
        """
        Creates the overworld object
        """

        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level

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
                sprite_node = Node(node["node_pos"], "available")
                self.nodes.add(sprite_node)
            else:
                sprite_node = Node(node["node_pos"], "locked")
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

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.current_level <= self.max_level:
            self.current_level += 1
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.current_level > 0:
            self.current_level -= 1


    def update_icon(self):
        pass
        #self.icon.sprite.rect.center = self.nodes.sprites()[self.current_level].rect.center

    def run(self):
        self.input()
        self.paths()
        self.nodes.draw(self.display_surface)
        self.update_icon()
        self.icon.draw(self.display_surface)