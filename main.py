import pygame, sys

import character_preset
import settings
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 800))
        HEIGHT = 900
        WIDTH = 800
        self.WIDTH = WIDTH
        self.sd = "Нормально"
        self.s_color = (0, 255, 0)
        pygame.event.set_grab(True)
        # название
        pygame.display.set_caption("Nuka Harvest")
        # счётчик кадров
        self.clock = pygame.time.Clock()

        # объявление объектов
        self.level =""
        self.level_initialized = False
        self.color1 = (255, 0, 0)  # красный
        self.color2 = (0, 255, 0)  # зеленый
        self.color3 = (0, 0, 255)  # синий
        self.color4 = (255, 255, 0)  # желтый

        for y in range(HEIGHT):
            color = (
                int(self.color1[0] * (1 - y / HEIGHT) + self.color2[0] * (y / HEIGHT)),
                int(self.color1[1] * (1 - y / HEIGHT) + self.color2[1] * (y / HEIGHT)),
                int(self.color1[2] * (1 - y / HEIGHT) + self.color2[2] * (y / HEIGHT))
            )

        font = pygame.font.Font(None, 36)
        logo_font = pygame.font.Font(None, 72)
        self.level_runnable = False
        self.dufficulty_changed = False
        self.menu_text = font.render(f'Очки: {character_preset.p_scores}', True, (255, 255, 255))  # белый цвет
        self.menu_text_rect = self.menu_text.get_rect(center=(WIDTH // 2 + 50, 100))

        self.menu_text = font.render(f'Очки: {character_preset.p_scores}', True, (255, 255, 255))  # белый цвет
        self.menu_text_rect = self.menu_text.get_rect(center=(WIDTH // 2 + 50, 100))

        self.logo_text = logo_font.render(f'ATOMIC HARVEST', True, (255, 255, 255))  # белый цвет
        self.logo_text_rect = self.logo_text.get_rect(center=(WIDTH // 2 + 50, 200))

        self.play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 , 300, 50)
        pygame.draw.rect(self.screen, self.color4, self.play_button)  # желтый цвет
        self.play_text = font.render('Играть', True, self.color3)  # синий цвет для текста
        self.play_text_rect = self.play_text.get_rect(center=self.play_button.center)

        self.dufficulty_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 300, 50)
        pygame.draw.rect(self.screen, self.color4, self.dufficulty_button)  # желтый цвет
        self.dufficulty_text = font.render('Сложность', True, self.color3)  # синий цвет для текста
        self.dufficulty_text_rect = self.dufficulty_text.get_rect(center=self.dufficulty_button.center)

        self.screen.fill("grey")

    def run(self):
        while True:
            font = pygame.font.Font(None, 36)
            self.current_dufficulty_text = font.render(f'Сложность: {self.sd}', True, self.s_color)
            self.current_dufficulty_text_rect = self.current_dufficulty_text.get_rect(
                center=(self.WIDTH // 2 + 50, 650))

            # обработчик событий
            for event in pygame.event.get():

                # выход из игры
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_e:
                        settings.picked = True
                        if character_preset.get_seed_count() != 0:
                            settings.planted = True
                    if event.key == pygame.K_1:
                        character_preset.write_scores()

                        print("The data has been written")
                    if event.key == pygame.K_2:
                        character_preset.p_scores += 1000
                        print(character_preset.p_scores)
                    if event.key == pygame.K_SPACE:
                        settings.pressed=True

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.play_button.collidepoint(event.pos):
                        self.level_runnable = True
                        self.level_initialized =True
                        character_preset.p_scores = 0

                    if self.dufficulty_text_rect.collidepoint(event.pos):

                        if self.dufficulty_changed:
                            self.sd = "Нормально"
                            self.dufficulty_changed = False
                            self.s_color = (0, 255, 0)
                        else:
                            self.sd = "Сложно"
                            self.dufficulty_changed = True
                            self.s_color = (255, 0, 0)
                        if self.dufficulty_changed:
                            settings.monster_data["jack"]["speed"] = 6
                            settings.monster_data["jack"]["damage"] = 20
                            settings.monster_data["jack"]["health"] = 300
                            font = pygame.font.Font(None, 36)
                            self.current_dufficulty_text = font.render(f'Сложность: {self.sd}', True, self.s_color)
                            self.current_dufficulty_text_rect = self.current_dufficulty_text.get_rect(
                                center=(self.WIDTH // 2 + 50, 650))
                            self.screen.blit(self.current_dufficulty_text, self.current_dufficulty_text_rect)

                        else:
                            settings.monster_data["jack"]["speed"] = 3
                            settings.monster_data["jack"]["damage"] = 5
                            settings.monster_data["jack"]["health"] = 100
            if not self.level_runnable :

                s = pygame.Surface((1000, 750))
                s.set_alpha(128)
                s.fill((255, 255, 255))
                self.screen.blit(s, (0, 0))
                img = pygame.image.load("assets/sprite_images/bgmain.png").convert_alpha()
                img_rect = img.get_rect(topleft=(0, 0))
                self.screen.blit(img, img_rect)
                pygame.draw.rect(self.screen, self.color4, self.dufficulty_button)
                self.screen.blit(self.current_dufficulty_text, self.current_dufficulty_text_rect)

                self.screen.blit(self.menu_text, self.menu_text_rect)

                pygame.draw.rect(self.screen, self.color4, self.play_button)
                pygame.draw.rect(self.screen, self.color4, self.dufficulty_button)

                self.screen.blit(self.play_text, self.play_text_rect)
                self.screen.blit(self.dufficulty_text, self.dufficulty_text_rect)
                self.screen.blit(self.logo_text, self.logo_text_rect)

            # запуск нашего уровня
            if self.level_runnable:
                if self.level_initialized:
                    self.level = Level()
                    self.level_initialized = False
                if settings.win != "lost":

                    self.level.run()
                else:
                    font = pygame.font.Font(None, 54)
                    img = pygame.image.load("assets/sprite_images/bgmain.png").convert_alpha()
                    img_rect = img.get_rect(topleft=(0, 0))
                    self.screen.blit(img, img_rect)
                    self.lose_text = font.render(f'ВЫ ПРОИГРАЛИ', True, (255,255,255))
                    self.lose_text_rect = self.lose_text.get_rect(
                        center=(self.WIDTH // 2+50 , 250))
                    self.w_text = font.render(f'ВАШ СЧЁТ:{character_preset.p_scores}', True, (255, 255, 255))

                    character_preset.write_scores()

                    self.w_text_rect = self.w_text.get_rect(
                        center=(self.WIDTH // 2 + 50, 350))
                    self.screen.blit(self.w_text, self.w_text_rect)
                    self.screen.blit(self.lose_text, self.lose_text_rect)
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
