import pygame

import settings


class Cursor():
    def __init__(self):
        self.image = pygame.image.load("assets/sprite_images/cursor.png").convert_alpha()
        self.cursor_img_rect = self.image.get_rect()
        self.cursor_img_rect.center = pygame.mouse.get_pos()  # update position
