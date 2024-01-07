import math

import pygame

import settings
from cursor import Cursor
from guns import Bullet
from hands import PlayerHands
from player import Player
from config import *
from settings import *
from tile import Tile, PlantingTile


class Level:
    def __init__(self):
        # экран
        self.display_surface = pygame.display.get_surface()
        # подразделяем объекты на 2 группы (видимые и физические)
        self.visible_sprites = YSortCameraGroup()
        self.visibles = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.res = []
        # вызов метода загрузки карты
        self.load_map()
        self.hand_x = pygame.display.get_window_size()[0] / 2
        self.hand_y = pygame.display.get_window_size()[1] / 2
    def load_map(self):
        layouts = {
            "boundary": import_csv_layout("assets/csv/_collision_layer.csv"),#граница
            "planting": import_csv_layout("assets/csv/_plant_zone.csv"),#зона посадки
        }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
               for col_index,col in enumerate(row):
                   if col!= "-1":
                        x = col_index*tile_size
                        y = row_index*tile_size
                        if style=="boundary":
                            Tile((x,y), [self.obstacles_sprites], "invisable")
                        if style=="planting":
                            PlantingTile((x, y), [self.visibles], "visable")
                            planting_tiles_coords.append((x,y))


        #начальные координаты игрока

        self.player = Player(player_coordinates, [self.visible_sprites], obstacle_sprites=self.obstacles_sprites)

        print(planting_tiles_coords)



    def run(self):
        # обновление экрана и отрисовка спрайтов
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visibles.update()



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        super().__init__()



        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.hand_x =self.half_width
        self.hand_y =self.half_height
        self.offset = pygame.math.Vector2()
        # Делаем отрисовку карты заранее
        self.floor_surface = pygame.image.load("assets/tile_images/Atomic Harvest Map Repaired.png").convert()
        #self.floor_surface = pygame.transform.scale(self.floor_surface, (self.floor_surface.get_width()*scale_factor, self.floor_surface.get_height()*scale_factor))
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        self.hands = PlayerHands((self.hand_x,self.hand_y))
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()
        self.camera_borders = {"left": 450, "right": 450, "bottom": 406, "top": 406}
        left_border = self.camera_borders["left"]
        right_border = self.display_surface.get_size()[0] - self.camera_borders["right"]
        top_border = self.camera_borders["top"]
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders["bottom"]

        self.mouse_camera_speed = 0.4

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border

            if mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border

        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, top_border)
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, top_border)

        if left_border < mouse.x < right_border:
            if mouse.y > bottom_border:
                mouse_offset_vector.y = mouse.y - bottom_border

            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border

        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, bottom_border)

            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, bottom_border)


        ####### изначальный код(выставление цетральной позиции игрока)
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # поиграйся с позициями x y чтобы убрать резкий переход
        self.offset.x += mouse_offset_vector.x * self.mouse_camera_speed
        self.offset.y += mouse_offset_vector.y * self.mouse_camera_speed


        # отрисовка карты
        floor_offset_pos = self.floor_rect.topleft - self.offset

        self.display_surface.blit(self.floor_surface, floor_offset_pos)
        for i in settings.planting_tiles:
            p_image = pygame.image.load(f"assets/sprite_images/{i[5]}")
            p_rect = p_image.get_rect(center=i[1])
            self.display_surface.blit(p_image,p_rect)



        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        # отрисовка рук игрока
        # важно! - player.rect.topleft  - именно его мы передаём , чтобы определить смещение относительно игрока
        hands_offset_pos = player.rect.topleft - self.offset
        rot_img = self.hands.rotate(hands_offset_pos)[0]

        rot_rect = self.hands.rotate(hands_offset_pos)[1]
        self.display_surface.blit(rot_img, rot_rect)



        pos =(640,320)
        bullets = []
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullets.append(Bullet(*pos))
                print("fire")
        for bullet in bullets[:]:
            bullet.update()
            if not self.display_surface.get_rect().collidepoint(bullet.pos):
                bullets.remove(bullet)
            print()

        for bullet in bullets:
            bullet.draw( self.display_surface)

        self.cursor = Cursor()
        pygame.mouse.set_visible(False)
        self.display_surface.blit(self.cursor.image, self.cursor.cursor_img_rect)


        settings.player_current_y = player.rect.centerx
        settings.player_current_y = player.rect.centery