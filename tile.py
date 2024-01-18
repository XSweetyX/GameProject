import pygame

import character_preset
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
    def __init__(self, pos, groups, sprite_type, img):
        super().__init__(groups)
        self.sprite_type = sprite_type  # враг,обект и тд
        self.image = img
        # выделяем прямоугольную область у картинки, чтобы позиционировать её на экране
        self.rect = self.image.get_rect(topleft=pos)
        # возможность сажать растения
        self.plantable = False
        self.planted = False
        self.decreased = False
        self.planting_stages = {"seed": [], "sprout": [], "grown_up": [], "without": [], }
        self.plant_types = {"potato": 15}
        self.current_stage = "without"
        # свойтв полей растения

    def find_tile_by_pos(self, pos):
        for i in settings.planting_tiles:
            if i[1][0] == pos[0] and i[1][1] == pos[1]:
                return i[0] - 1

    def run_once(f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)

        wrapper.has_run = False
        return wrapper

    def check_mouse_on_plant(self):

        if planting_tiles_coords[0][0] <= settings.player_current_x <= planting_tiles_coords[-1][0] + 128 \
                and planting_tiles_coords[0][1] <= settings.player_current_y <= planting_tiles_coords[-1][1] + 128:
            self.plantable = True

        else:
            self.plantable = False
        self.last_idx = 17
        if not self.plantable:
            if self.last_idx != 17:
                settings.planting_tiles[self.last_idx][4] = "without.png"
        if self.plantable:
            planting_tile_coords = self.find_planting_tile(settings.player_current_x, settings.player_current_y)
            t_idx = self.find_tile_by_pos(planting_tile_coords)

            if t_idx:
                for i in range(len(settings.planting_tiles)):
                    if i != t_idx and not settings.planting_tiles[i][5]:
                        settings.planting_tiles[i][4] = "without.png"
                if not settings.planting_tiles[t_idx][5]:
                    settings.planting_tiles[t_idx][4] = "plantable.png"
                    if settings.planted:
                        self.plant()
                        self.decrease_seed()
                        settings.planted = False

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
            planting_tile_id = self.find_tile_by_pos(p_coords)
            settings.planting_tiles[planting_tile_id][2] = "potato"
            settings.planting_tiles[planting_tile_id][3] = time.time()
            settings.planting_tiles[planting_tile_id][4] = "seed.png"
            settings.planting_tiles[planting_tile_id][5] = True

    def decrease_seed(self):

        character_preset.p_seeds["potato"] = character_preset.p_seeds["potato"] - 1
        print(character_preset.p_seeds["potato"])

    def grow(self):

        for i in range(1, len(settings.planting_tiles)):
            if settings.planting_tiles[i][3] != 0:
                if time.time() - settings.planting_tiles[i][3] > 3:
                    settings.planting_tiles[i][4] = "sprout.png"
                if time.time() - settings.planting_tiles[i][3] > 6:
                    settings.planting_tiles[i][4] = "grown_up.png"
                if time.time() - settings.planting_tiles[i][3] > 9:
                    settings.planting_tiles[i][4] = "pickable.png"
                    if settings.picked:
                        settings.planting_tiles[i][3] = 0
                        settings.planting_tiles[i][5] = False
                        settings.planting_tiles[i][4] = "without.png"

                        character_preset.p_money += 10
                        character_preset.p_scores += 1000

                        settings.picked = False

                        print(character_preset.p_money)

    def update(self):
        self.check_mouse_on_plant()
        self.grow()
