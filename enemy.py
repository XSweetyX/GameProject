import pygame

import character_preset
import settings
from character_preset import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("assets/sprite_images/Jackl1.png").convert_alpha( )

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

        # характеристики персонажа(присовение значений объекту)
        self.hp = jack_hp


    def take_damage(self):
        self.hp-=character_preset.p_damage

    def draw(self,surf):
        enemy_rect = self.image.get_rect(center=self.pos_p)
        surf.blit(self.image, enemy_rect)

    def enemy_die(self,en):

        print(en)
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
