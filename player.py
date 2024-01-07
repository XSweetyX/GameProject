import math

import pygame

import settings
from character_preset import *
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):

        super().__init__(groups)
        self.image = pygame.image.load("assets/animations/MC_R/r_1.png").convert_alpha()

        self.sprite_type = "visible"

        # выделяем прямоугольную область у картинки, чтобы позиционировать её на экране
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-50, -50)
        # коллизия
        self.obstacle_sprites = obstacle_sprites
        self.pos_p = pos
        self.animation_speed = 0.15
        # управление
        self.direction = pygame.math.Vector2()

        self.animation_count = 1
        self.status = "right"

        #характеристики персонажа(присовение значений объекту)
        self.hp = p_hp
        self.value_of_water = p_value_of_water
        self.speed = p_speed
        self.money = p_money
        self.seeds = p_seeds



    def animate(self):
        self.animations = {"right": f"assets/animations/MC_R/r_{int(self.animation_count)}.png",
                           "left": f"assets/animations/MC_L/l_{int(self.animation_count)}.png"}
        self.animation_count += self.animation_speed
        mx,my = pygame.mouse.get_pos()
        if 0<mx<480 :
            self.status = "left"
        else :
            self.status = "right"
        if self.animation_count >=5:
            self.animation_count =1
        self.image = pygame.image.load(self.animations[self.status]).convert_alpha()


        self.rect = self.image.get_rect(center=self.hitbox.center)
    def controllers(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.animate()
            self.animation_speed = 0.075
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.animate()
            self.animation_speed = 0.075
        else:
            self.direction.y = 0
        if keys[pygame.K_a]:
            self.direction.x = -1

            self.animate()
            self.animation_speed = 0.075

        elif keys[pygame.K_d]:
            self.direction.x = 1

            self.animate()
            self.animation_speed = 0.075
        else:

            self.direction.x = 0
        if not  keys[pygame.K_a] and  not keys[pygame.K_d]and not  keys[pygame.K_w] and not  keys[pygame.K_s]:

            self.animation_count = 1
            self.animation_speed = 0

        if (keys[pygame.K_d] and keys[pygame.K_w]) or(keys[pygame.K_d] and keys[pygame.K_s])  or(keys[pygame.K_a] and keys[pygame.K_s])or(keys[pygame.K_a] and keys[pygame.K_w]):
            self.animation_speed = 0.075
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * self.speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * self.speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):

        if direction == "horizontal":

            for sprite in self.obstacle_sprites:

                if self.hitbox.colliderect(sprite.hitbox):

                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left

                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if self.hitbox.colliderect(sprite.rect):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):

        self.animate()
        self.controllers()
        self.move()

        settings.player_current_x=self.hitbox.x
        settings.player_current_y=self.hitbox.y