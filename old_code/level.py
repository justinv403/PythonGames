import pygame
from decoration import Skybox
from support import import_csv_layout, import_cut_graphic
from settings import tile_size, screen_height, screen_width
from tiles import AnimatedTile, Tile, StaticTile, Coin
from enemy import Enemy
from decoration import Skybox, Water
from player import Player
from particles import ParticleEffect
from game_data import levels

class Level:
    def __init__(self, current_level, level_data, surface):
        """
        Creation of the level class
        """
        
        # general setup
        self.display_surface = surface
        self.current_level = current_level
        level_data = levels[current_level]
        level_content = level_data["content"]
        self.new_max_level = level_data["unlock"]
        
        # display
        self.font = pygame.font.Font(None, 40)
        self.text_surface = self.font.render(level_content, True, "White")
        self.text_rect = self.text_surface.get_rect(center = (screen_width / 2, screen_height / 2))

        # world shift
        self.world_shift = 0

        # player setup
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        
        # terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # coins
        coin_layout = import_csv_layout(level_data["coins"])
        self.coin_sprites = self.create_tile_group(coin_layout, "coins")
    
        # enemy
        enemy_layout = import_csv_layout(level_data["enemies"])
        self.enemy_sprites = self.create_tile_group(enemy_layout, "enemies")

        # constraints 
        # hidden constraint boxes for enemy movement
        constraint_layout = import_csv_layout(level_data["constraints"])
        self.constraint_sprites = self.create_tile_group(constraint_layout, "constraint")

        # decoration
        self.sky_box = Skybox(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40, level_width)


    def create_tile_group(self, layout, type):
        """
        Creates a tile group to render
        
        :param1 layout: list from the csv interpreter (import_csv_layout) for each group
        :param2 type: string containing the name of the type of sprite group to create
        """
        
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1": # csv is in terms of strings
                    x = col_index * tile_size
                    y = row_index * tile_size

                    # handles the different types of objects to render
                    if type == "terrain":
                        terrain_tile_list = import_cut_graphic("./graphics/terrain/Mossy Tileset/Mossy - TileSet.png")
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    
                    if type == "coins":
                        if val == "0":
                            sprite = Coin(tile_size, x, y, "./graphics/coins/gold/anim")
                        #if val == "1": FIXME: Error out of range for silver coins
                        #    sprite = Coin(tile_size, x, y, "./grahpics/coins/silver/anim")
                    
                    if type == "enemies":
                        sprite = Enemy(tile_size, x, y)

                    if type == "constraint":
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    
    def player_setup(self, layout):
        """
        Sets up the player
        """
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size - (3*tile_size)
                if val != "0": # csv is in terms of strings
                    sprite = Player((128,y), self.display_surface, self.create_jump_particles) #FIXME: player spawn position should be automatic, instead of manually adding 128 it should be x
                    self.player.add(sprite)
                    pass
                if val != "1": # csv is in terms of strings
                    hat_surface = pygame.image.load("./graphics/character/hat/wizhat-blue-72x72-2.png")
                    hat_surface = pygame.transform.scale(hat_surface, (48,48)).convert_alpha()
                    sprite = StaticTile(tile_size, x+8, y+8, hat_surface)
                    self.goal.add(sprite)


    def enemy_collision_reverse(self):
        """
        Flips the enemy direction if they collide with a constraint
        """
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False): # false means it doesn't destroy the constraint
                enemy.reverse()


    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right: # offset for the jump particles to look better
           pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, "jump")
        self.dust_sprite.add(jump_particle_sprite)

    
    def horizontal_collision(self): # handles horizontal collision of the player
        player = self.player.sprite # gets the player sprite so it doesn't have to be specifically called each time
        player.rect.x += player.direction.x * player.speed

        # sprites the player can collide with
        collidable_sprites = self.terrain_sprites.sprites() + self.enemy_sprites.sprites()

        for sprite in collidable_sprites: # sets the player to the right side of whatever they collide with
            if sprite.rect.colliderect(player.rect):
                
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False


    def vertical_collision(self): # handles vertical collision of the player and some gravity logic
        player = self.player.sprite
        player.apply_gravity()

        # sprites the player can collide with
        collidable_sprites = self.terrain_sprites.sprites() + self.enemy_sprites.sprites()

        # prevents the player from going up through an object or through an object below
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0 # fixes gettings stuck to ceilings
                    player.on_ceiling = True
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0 # fixes infinity gravity glitch on floors
                    player.on_ground = True
        
        # checks for ground and ceiling contact (helps animation quality)
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False
    

    def scroll_x(self): # horizontal level scrolling logic
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        # finds where the player is and determines whether the screen should shift or not
        if player_x < (screen_width / 3)  and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width - (screen_width / 3)) and direction_x > 0:
            self.world_shift = -8
            player.speed = -0
        else:
            self.world_shift = 0
            player.speed = 8

    
    def get_player_on_ground(self): # important for landing particles
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False
    

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,"land")
            self.dust_sprite.add(fall_dust_particle)
    

    def run(self):
        """
        Runs the entire game/level
        Rendering order - things rendered after render on top
        """
        
        # skybox
        self.sky_box.draw(self.display_surface)
        
        # coin sprites
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # enemy sprites
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_collision()
        
        self.get_player_on_ground()
        self.vertical_collision()
        self.create_landing_dust()
        
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)
        
        # terrain sprites
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # text
        self.display_surface.blit(self.text_surface, self.text_rect)