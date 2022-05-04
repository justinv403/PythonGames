from csv import reader
import pygame
from settings import tile_size
from os import walk

def import_folder(path):
    """
    Imports a folder (of images) [used for animations]

    :param path: takes the path of the folder to be read
    :return: list of image surfaces
    """
    surface_list = []
    
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    
    return surface_list

def import_csv_layout(path):
    """
    Imports the level layout of the map for use in the other programs

    :param path: takes the path of the csv to be interpreted
    :return: interpreted terrain map
    """

    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=",")
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
    
def import_cut_graphic(path):
    """
    Converts the tileset images to something that pygame can use

    :param path: path of the image to be converted
    :return: cut tiles for use in rendering
    """
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, tile_size, tile_size)) # finds the correct part of the image to get
            cut_tiles.append(new_surf)

    return cut_tiles