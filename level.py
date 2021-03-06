import pygame 
from support import import_csv_layout, import_cut_graphic
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Coin
from enemy import Enemy
from decoration import Skybox, Water
from player import Player
from particles import ParticleEffect
from game_data import levels

class Level:
	def __init__(self, current_level, surface, create_overworld, change_coins, change_health):
		"""
		Initialization of the level class
		"""
		
		# level setup
		self.display_surface = surface
		self.world_shift = 0 # player movement
		self.current_x = None

		# overworld connection 
		self.create_overworld = create_overworld
		self.current_level = current_level
		level_data = levels[self.current_level]
		self.new_max_level = level_data["unlock"]

		# player 
		player_layout = import_csv_layout(level_data["player"])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout, change_health)

		# UI
		self.change_coins = change_coins

		# dust particle
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		# explosion particle
		self.explosion_sprites = pygame.sprite.Group()

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
		constraint_layout = import_csv_layout(level_data["constraints"])
		self.constraint_sprites = self.create_tile_group(constraint_layout, "constraint")

		# decoration 
		self.sky = Skybox(8)
		level_width = len(terrain_layout[0]) * tile_size
		self.water = Water(screen_height - 50, level_width)


	def create_tile_group(self, layout, type):
		"""
		Creates each group of tiles for the level
		E.g. terrain, coins, enemies, etc...
		"""
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index, val in enumerate(row):
				if val != "-1":
					x = col_index * tile_size
					y = row_index * tile_size

					if type == "terrain":
						terrain_tile_list = import_cut_graphic("./graphics/Terrain/Mossy Tileset/MossyTileSet.png")
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)

					if type == "coins":
						if val == "0": sprite = Coin(tile_size, x, y,"./graphics/coins/gold/anim", 5)
						if val == "1": sprite = Coin(tile_size, x, y,"./graphics/coins/silver/anim", 1)

					if type == "enemies":
						sprite = Enemy(tile_size, x, y)

					if type == "constraint":
						sprite = Tile(tile_size, x, y)

					sprite_group.add(sprite)
		
		return sprite_group


	def player_setup(self, layout, change_health):
		"""
		Sets up the player based on the position in the csv files
		"""
		for row_index, row in enumerate(layout):
			for col_index, val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == "0":
					sprite = Player((x,y), self.display_surface, self.create_jump_particles, change_health)
					self.player.add(sprite)
				if val == "1":
					hat_surface = pygame.image.load("./graphics/character/hat.png").convert_alpha()
					sprite = StaticTile(tile_size, x, y, hat_surface)
					self.goal.add(sprite)


	def enemy_collision_reverse(self):
		"""
        Reverses the enemy direction when they hit a collider box
        """
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
				enemy.reverse()


	def create_jump_particles(self, pos):
		"""
        Creates the jump particles for the player animations
        """
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos, "jump")
		self.dust_sprite.add(jump_particle_sprite)


	def horizontal_collision(self):
		"""
        Handles horizontal collision with static sprites
        """
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		collidable_sprites = self.terrain_sprites.sprites()
		for sprite in collidable_sprites:
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


	def vertical_collision(self):
		"""
        Handles vertical collision with static sprites
        - also applies gravity to the player
        """
		player = self.player.sprite
		player.apply_gravity()
		collidable_sprites = self.terrain_sprites.sprites()

		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False


	def scroll_x(self):
		"""
		Scrolling information for other objects - detects if the player is a certain distance
		to a side of the screen then applies a world shift
		"""
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8


	def get_player_on_ground(self):
		"""
		Detects if the player has hit the ground
		"""
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False


	def create_landing_dust(self):
		"""
		Creates landing dust if the player hits the ground
		"""
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
			self.dust_sprite.add(fall_dust_particle)


	def check_death(self):
		"""
		Checks if the player has died
		"""
		if self.player.sprite.rect.top > screen_height:
			self.create_overworld(self.current_level, 0)


	def check_win(self):
		"""
		Sees if the player wins by colliding with the end sprite
		"""
		if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
			self.create_overworld(self.current_level, self.new_max_level)


	def check_coin_collisions(self):
		"""
		Detects if the player collides with a coin
		"""
		collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
		if collided_coins:
			for coin in collided_coins:
				self.change_coins(coin.value)


	def check_enemy_collisions(self):
		enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

		if enemy_collisions:
			for enemy in enemy_collisions:
				enemy_center = enemy.rect.centery
				enemy_top = enemy.rect.top
				player_bottom = self.player.sprite.rect.bottom
				if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
					self.player.sprite.direction.y = -15
					explosion_sprite = ParticleEffect(enemy.rect.center, "explosion")
					self.explosion_sprites.add(explosion_sprite)
					enemy.kill()
				else:
					self.player.sprite.get_damage()


	def run(self):
		"""
		Runs the entire level class
		"""
		
		# The order that these are done is VERY important -
        # objects rendered after will be in front, and those rendered before will be behind
		

		# skybox
		self.sky.draw(self.display_surface)

		# water 
		self.water.draw(self.display_surface, self.world_shift)
		
		# terrain 
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)
		
		# enemy 
		self.enemy_sprites.update(self.world_shift)
		self.constraint_sprites.update(self.world_shift)
		self.enemy_collision_reverse()
		self.enemy_sprites.draw(self.display_surface)
		self.explosion_sprites.update(self.world_shift)
		self.explosion_sprites.draw(self.display_surface)

		# coins 
		self.coin_sprites.update(self.world_shift)
		self.coin_sprites.draw(self.display_surface)

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

		self.check_death()
		self.check_win()

		self.check_coin_collisions()
		self.check_enemy_collisions()
