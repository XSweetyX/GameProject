import pygame

import settings
from cursor import Cursor
from settings import *

import time


# общий класс чанка карты(обекта отрисовки)
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((tile_size, tile_size))):
        super().__init__(groups)
        self.image = surface

        self.image = pygame.transform.scale(self.image, (tile_size, tile_size)).convert_alpha()
        self.sprite_type = sprite_type  # враг,обект и тд
        # выделяем прямоугольную область у картинки, чтобы позиционировать её на экране
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -5)


# класс зоны посадки
class PlantingTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((tile_size, tile_size))):
        super().__init__(groups)
        #self.image = pygame.image.load("assets/sprite_images/without.png")
        #self.position = pos
        # self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.sprite_type = sprite_type  # враг,обект и тд
        # выделяем прямоугольную область у картинки, чтобы позиционировать её на экране
        #self.rect = self.image.get_rect(topleft=pos)
        # возможность сажать растения
        self.plantable = False
        self.planted=False
        self.planting_stages = {"seed": [], "sprout": [], "grown_up": [], "without": [],"seed": []}
        self.plant_types = {"potato": 15}
        self.current_stage = "without"
        # свойтв полей растения



    def find_tile_by_pos(self, pos):
        for i in settings.planting_tiles:
            if i[1][0] == pos[0] and i[1][1] == pos[1]:
                return i[0] - 1

    def check_mouse_on_plant(self):
        keys = pygame.key.get_pressed()

        if planting_tiles_coords[0][0] <= settings.player_current_x <= planting_tiles_coords[-1][0] + 128 \
                and planting_tiles_coords[0][1] <= settings.player_current_y <= planting_tiles_coords[-1][1] + 128:
            planting_tile_coords = self.find_planting_tile(settings.player_current_x, settings.player_current_y)
            t_idx = self.find_tile_by_pos(planting_tile_coords)
            if t_idx:
                if not settings.planting_tiles[t_idx][6]:
                        if planting_tile_coords:
                            settings.planting_tiles[t_idx][5]="plantanble.png"
                            print(settings.planting_tiles)
                            if keys[pygame.K_e]:
                                self.plant()

        #else:
            #self.delete_without()


        #print(settings.planting_tiles)
    def delete_without(self):
        for i in settings.planting_tiles:
            if i[5] =="plantanble.png":
                i[5]="without.png"
        print(settings.planting_tiles)
    def find_planting_tile(self, x, y):
        res = None
        for i in range(len(planting_tiles_coords)):
            if planting_tiles_coords[i][0] - 2 < x < planting_tiles_coords[i][0] + 129 and planting_tiles_coords[i][
                1] - 2 < y < planting_tiles_coords[i][1] + 129:
                res = planting_tiles_coords[i]
            elif planting_tiles_coords[-1][0] - 2 < x < planting_tiles_coords[-1][0] + 128 and \
                    planting_tiles_coords[-1][1] - 2 < y < planting_tiles_coords[-1][1] + 128:
                res = planting_tiles_coords[-1]
        return res

    def plant(self):

        if self.plantable:
            p_coords = self.find_planting_tile(settings.player_current_x, settings.player_current_y)

            self.image = pygame.image.load("assets/sprite_images/pz0.png").convert_alpha()
            self.rect = self.image.get_rect(topleft=p_coords)
            planting_tile_id = self.find_tile_by_pos(p_coords)
            settings.planting_tiles[planting_tile_id][2] = "seed"
            settings.planting_tiles[planting_tile_id][3] = "potato"
            settings.planting_tiles[planting_tile_id][4] = time.time()
            settings.planting_tiles[planting_tile_id][6] = True


    def grow(self):
        pass

    def pick_up_plant(self):
        pass

    def update(self):
        self.check_mouse_on_plant()
