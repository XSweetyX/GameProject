import math

import pygame

import settings
from settings import player_coordinates, hands_coordinates


class PlayerHands(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/tile_images/hands.png").convert_alpha()

        self.sprite_type = "visible"

        # выделяем прямоугольную область у картинки, чтобы позиционировать её на экране
        self.rect = self.image.get_rect(center=pos)

        self.hitbox = self.rect.inflate(-100, -100)

        self.pos_p = pos
        # управление
        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.x = pos[0]
        self.y = pos[1]

    def controllers(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * self.speed
        self.hitbox.y += self.direction.y * self.speed
        self.rect.center = self.hitbox.center

    def rotate(self,offset):

        #offset -это offset_pos в отрисовке спайтов(т.е. их смещение при отрисовке)но сами руки рисуются относительно середины экрана (hand_x,hand_y)
        player_rect = self.image.get_rect(center=self.rect.center)

        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - player_rect.x, -(my - player_rect.y)
        angle = math.degrees(math.atan2(dy, dx))
        #корректировка координат области вращения
        offset.x+=12
        offset.y+=35

        settings.player_status = "right"
        if 90<angle or angle<-80:
            offset.x +=7

            self.image = pygame.transform.flip(self.image, False, True)




        # при вращении важно менять область (rect)самого спрайта иначеон будет вращаться относительно старой области
        r_image = pygame.transform.rotozoom(self.image, angle, 0.7)
        #смещение точки вращения
        v = pygame.math.Vector2(25,0)
        r_v =v.rotate(-angle)
        rot_image_rect = r_image.get_rect(center=offset+r_v)#это область именно уже повёрнутого изображения!!!!(это очень важно)

        return [r_image,rot_image_rect ]



def update(self):
    self.controllers()
    self.move()
"""
Рабочий поворот!!!! НЕ УДАЛЯТЬ
    def rotate(self,offset):


        player_rect = self.image.get_rect(center=self.rect.center)

        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - player_rect.x, -(my - player_rect.y)
        angle = math.degrees(math.atan2(dy, dx))
        offset_vector = pygame.math.Vector2(50,0)

        roteted_offset_vector = offset_vector.rotate(angle)
        r_image = pygame.transform.rotozoom(self.image, angle,1)

        rot_image_rect = r_image.get_rect(center=offset)


        return [r_image,rot_image_rect ]
"""