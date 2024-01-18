import time

import pygame

import character_preset
import settings
from character_preset import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("assets/sprite_images/Jackl1.png").convert_alpha()

        self.sprite_type = "enemy"

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
        self.status = "idle"

        # характеристики персонажа(присовение значений объекту)
        self.hp = settings.monster_data["jack"]["health"]
        self.damage = settings.monster_data["jack"]["damage"]
        self.speed = settings.monster_data["jack"]["speed"]
        self.attack_radius = settings.monster_data["jack"]["attack_radius"]
        self.notice_radius = settings.monster_data["jack"]["notice_radius"]


    def take_damage(self):
        self.hp -= character_preset.p_damage

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x
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

    def draw(self, surf):
        enemy_rect = self.image.get_rect(center=self.pos_p)
        surf.blit(self.image, enemy_rect)

    def animate(self):

        self.animations = {"right": f"assets/animations/MC_R/r_{int(self.animation_count)}.png",
                           "left": f"assets/animations/MC_L/l_{int(self.animation_count)}.png"}
        self.animation_count += self.animation_speed
        mx, my = pygame.mouse.get_pos()
        if 0 < mx < 480:
            self.status = "left"
        else:
            self.status = "right"
        if self.animation_count >= 5:
            self.animation_count = 1
        self.image = pygame.image.load(self.animations[self.status]).convert_alpha()

        self.rect = self.image.get_rect(center=self.hitbox.center)

    def get_player_distance_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius:
            self.status = "attack"

        elif distance <= self.notice_radius:

            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player):
        if self.status == "attack":

            player.get_damage(self)

        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def update(self):
        self.move()
    def get_damage(self):
        self.hp-=p_damage

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
