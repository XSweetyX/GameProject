import pygame,sys
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900,800))
        pygame.event.set_grab(True)
        #название
        pygame.display.set_caption("Nuka Harvest")
        #счётчик кадров
        self.clock =  pygame.time.Clock()

        #объявление объектов
        self.level = Level()

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

            self.screen.fill("grey")

            # запуск нашего уровня
            self.level.run()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()