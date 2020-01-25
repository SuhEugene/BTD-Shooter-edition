from Pop import pops, Pop
from Dart import darts
import pygame
pygame.init()
pygame.display.set_mode([1000, 1000])
bloons = []


class Bloon(pygame.sprite.Sprite):
    # Прямо все шарики
    images = [0, pygame.image.load("data/Bloon_1.png").convert_alpha(),
              pygame.image.load("data/Bloon_2.png").convert_alpha(),
              pygame.image.load("data/Bloon_3.png").convert_alpha(),
              pygame.image.load("data/Bloon_4.png").convert_alpha(),
              pygame.image.load("data/Bloon_5.png").convert_alpha(),
              pygame.image.load("data/HBloon_1.png").convert_alpha(),
              pygame.image.load("data/HBloon_2.png").convert_alpha(),
              pygame.image.load("data/HBloon_3.png").convert_alpha(),
              pygame.image.load("data/HBloon_4.png").convert_alpha(),
              pygame.image.load("data/HBloon_5.png").convert_alpha()]

    def __init__(self, group, group1, x, y, map_c, what_bloon=1):
        super().__init__(group, group1)

        # Pygame требует, лучше не трогать
        self.group = group
        self.group1 = group1

        # Сколько от этого шара ушло за карту
        self.over = 0

        # Цвет и тип шара
        self.bloon = what_bloon

        # Ксласс карты, который возвращает шару куда ему двмгаться
        self.map = map_c

        # Устанавливаем шарику ему соответствующую картинку
        self.image = Bloon.images[self.bloon]

        # Стандартная процедура
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rx = self.rect.x
        self.ry = self.rect.y

        # Жив ли шар, так как self.kill() у спрайта робит через... не так как надо
        self.alive = True

        # Маска шара, чтобы касание дротика работало по ней, а не по прямоугольнику
        self.mask = pygame.mask.from_surface(self.image)

    # Движение шара, и убийство, если вышел за границу или коснулся дротика
    # Также увеличитель счёта
    def move(self):
        if not self.alive:
            return
        for dart in darts:
            if pygame.sprite.collide_mask(self, dart) and dart.alive:
                dart.shoot(self)
                if self.bloon <= 5 and self.bloon > 1:
                    self.bloon -= 1
                    self.image = Bloon.images[self.bloon]
                else:
                    self.alive = False
                    pops.append(Pop(self.group, self.group1,
                                    self.rect.x, self.rect.y))
                    self.kill()
        response = self.map.get((self.rect.x, self.rect.y))
        if (response == "killed"):
            self.alive = False
            self.kill()
            self.over = self.bloon
        else:
            dx, dy = response

            self.rx += dx * (self.bloon % 5) * 1.1
            self.ry += dy * (self.bloon % 5) * 1.1

            self.rect.x = int(self.rx)
            self.rect.y = int(self.ry)
