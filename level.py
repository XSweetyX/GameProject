import pygame
from enemy import Enemy

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
        self.visibles = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.p_tile_objects = []

        # вызов метода загрузки карты
        self.load_map()
        self.hand_x = pygame.display.get_window_size()[0] / 2
        self.hand_y = pygame.display.get_window_size()[1] / 2

    def load_map(self):
        layouts = {
            "boundary": import_csv_layout("assets/csv/_collision_layer.csv"),  # граница
            "planting": import_csv_layout("assets/csv/_plant_zone.csv"),  # зона посадки
            "enemies": import_csv_layout("assets/csv/_enemy_positions.csv"),  # зона посадки
        }
        en_count = 0
        i = 0
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * tile_size
                        y = row_index * tile_size
                        if style == "boundary":
                            Tile((x, y), [self.obstacles_sprites], "invisable")
                        if style == "planting":

                            p_image = pygame.image.load(
                                f"assets/sprite_images/{settings.planting_tiles[i][4]}").convert_alpha()
                            PlantingTile((x, y), [self.visible_sprites], "visable", p_image)
                            planting_tiles_coords.append((x, y))

                            self.p_tile_objects.append(PlantingTile((x, y), [self.visibles], "visable", p_image))
                            if i < len(settings.planting_tiles) - 1:
                                i += 1
                        if style =="enemies":

                            settings.enemies.append(Enemy((x, y), [self.visible_sprites], obstacle_sprites=self.obstacles_sprites))
                            settings.enemies[en_count]
                            en_count+=1
        settings.p_tile_obljects = self.p_tile_objects

        # начальные координаты игрока

        self.player = Player(player_coordinates, [self.visible_sprites], obstacle_sprites=self.obstacles_sprites)

        print(settings.enemies_pos)

    def run(self):
        # обновление экрана и отрисовка спрайтов
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visibles.update()



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.bullets = []
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.hand_x = self.half_width
        self.hand_y = self.half_height
        self.offset = pygame.math.Vector2()
        # Делаем отрисовку карты заранее
        self.floor_surface = pygame.image.load("assets/tile_images/Atomic Harvest Map Repaired.png").convert()
        # self.floor_surface = pygame.transform.scale(self.floor_surface, (self.floor_surface.get_width()*scale_factor, self.floor_surface.get_height()*scale_factor))
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def redraw_planting_tile(self):
        for i in settings.planting_tiles:
            image = pygame.image.load(f"assets/sprite_images/{i[4]}")
            rect = image.get_rect(topleft=i[1])
            self.display_surface.blit(image, rect)

    def custom_draw(self, player):

        self.hands = PlayerHands((self.hand_x, self.hand_y))
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
        settings.sprite_offset =self.offset
        # отрисовка карты
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        for i in settings.planting_tiles:
            image = pygame.image.load(f"assets/sprite_images/{i[4]}").convert_alpha()
            rect = image.get_rect(topleft=i[1])
            rect.topleft -= self.offset

            self.display_surface.blit(image, rect)
        # отрисовка рук игрока
        # важно! - player.rect.topleft  - именно его мы передаём , чтобы определить смещение относительно игрока
        self.display_surface.blit(player.image, player.rect)
        hands_offset_pos = player.rect.topleft - self.offset
        rot_img = self.hands.rotate(hands_offset_pos)[0]

        rot_rect = self.hands.rotate(hands_offset_pos)[1]
        self.display_surface.blit(rot_img, rot_rect)

        offset_pos = self.sprites()[0].rect.topleft - self.offset
        self.display_surface.blit(self.sprites()[0].image, offset_pos)





        # отрисовка пуль
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.bullets.append(Bullet(*hands_offset_pos))

        for bullet in self.bullets[:]:
            bullet.update()
            if not self.display_surface.get_rect().collidepoint(bullet.pos):
                self.bullets.remove(bullet)

            died_enemy = ""
            died = False
            for en in settings.enemies:
                #находим глобальные(относительно холста) координаты пули
                pos = (bullet.pos[0]-hands_offset_pos.x+settings.player_current_x, bullet.pos[1]-hands_offset_pos.y+settings.player_current_y)
               # print("pos",bullet.pos[0],bullet.pos[1])
                #print("hands_offset",hands_offset_pos.x,hands_offset_pos.y)
               # print("pc.x pc.y",settings.player_current_x,settings.player_current_y)
                b_rect = bullet.bullet.get_rect(center=pos)
                if en.rect.colliderect(b_rect):
                    bullet.bullet.fill((255, 0, 0))
                    print(pos)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                        died_enemy = en
                        img = pygame.image.load(f"assets/sprite_images/pz0.png").convert_alpha()
                        en.image = img
                        rect = img.get_rect(center=en.pos_p)
                        self.display_surface.blit(img,rect)
                        died = True
            if died:
                settings.enemies.remove(died_enemy)
                print(settings.enemies)

        for bullet in self.bullets:
            bullet.draw(self.display_surface)

        for enemy in settings.enemies :
            enemy.draw(self.display_surface)



        self.cursor = Cursor()
        pygame.mouse.set_visible(False)
        self.display_surface.blit(self.cursor.image, self.cursor.cursor_img_rect)

        settings.player_current_y = player.rect.centerx
        settings.player_current_y = player.rect.centery
