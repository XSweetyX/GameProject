import pygame,sys

import character_preset
import settings
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900,800))
        HEIGHT = 900
        WIDTH =  800
        pygame.event.set_grab(True)
        #название
        pygame.display.set_caption("Nuka Harvest")
        #счётчик кадров
        self.clock =  pygame.time.Clock()

        #объявление объектов
        self.level = Level()




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
        scores = 1223425
        self.level_runnable = False
        self.menu_text = font.render(f'Очки: {character_preset.p_scores}', True, (255, 255, 255))  # белый цвет
        self.menu_text_rect = self.menu_text.get_rect(center=(WIDTH // 2, 100))

        # Кнопка "Играть" (синий текст на красной кнопке)
        self.play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        pygame.draw.rect(self.screen, self.color4, self.play_button)  # желтый цвет
        self.play_text = font.render('Играть', True, self.color3)  # синий цвет для текста
        self.play_text_rect = self.play_text.get_rect(center=self.play_button.center)
        self.screen.fill("grey")

        img = pygame.image.load("assets/sprite_images/bgmain.png").convert_alpha()
        img_rect = img.get_rect(topleft=(0, 0))
        self.screen.blit(img, img_rect)
        self.screen.blit(self.menu_text, self.menu_text_rect)

        pygame.draw.rect(self.screen, self.color4, self.play_button)

        self.screen.blit(self.play_text, self.play_text_rect)
    def run(self):
        while True:

            # обработчик событий
            for event in pygame.event.get():

                #выход из игры
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
                            settings.planted=True
                    if event.key == pygame.K_1:
                        character_preset.write_scores()
                        print("The data has been written")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # запуск нашего уровня
                    if self.play_button.collidepoint(event.pos):
                        self.level_runnable=True



            if self.level_runnable:
                self.level.run()





            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()