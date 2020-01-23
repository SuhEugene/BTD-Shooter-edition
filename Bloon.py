from Pop import pops, Pop
from Dart import darts
import pygame
pygame.init()
pygame.display.set_mode([1000, 1000])
bloons = []


class Bloon(pygame.sprite.Sprite):
    image_1 = pygame.image.load("data/Bloon_1.png").convert_alpha()
    image_2 = pygame.image.load("data/Bloon_2.png").convert_alpha()
    image_3 = pygame.image.load("data/Bloon_3.png").convert_alpha()
    image_4 = pygame.image.load("data/Bloon_4.png").convert_alpha()
    image_5 = pygame.image.load("data/Bloon_5.png").convert_alpha()
    image_6 = pygame.image.load("data/HBloon_1.png").convert_alpha()
    image_7 = pygame.image.load("data/HBloon_2.png").convert_alpha()
    image_8 = pygame.image.load("data/HBloon_3.png").convert_alpha()
    image_9 = pygame.image.load("data/HBloon_4.png").convert_alpha()
    image_10 = pygame.image.load("data/HBloon_5.png").convert_alpha()

    def __init__(self, group, group1, x, y, map_c, what_bloon=1):
        super().__init__(group, group1)

        self.group = group
        self.group1 = group1

        self.bloon = what_bloon

        self.map = map_c
        if what_bloon == 1:
            self.image = Bloon.image_1
        elif what_bloon == 2:
            self.image = Bloon.image_2
        elif what_bloon == 3:
            self.image = Bloon.image_3
        elif what_bloon == 4:
            self.image = Bloon.image_4
        elif what_bloon == 5:
            self.image = Bloon.image_5
        elif what_bloon == 6:
            self.image = Bloon.image_6
        elif what_bloon == 7:
            self.image = Bloon.image_7
        elif what_bloon == 8:
            self.image = Bloon.image_8
        elif what_bloon == 9:
            self.image = Bloon.image_9
        elif what_bloon == 10:
            self.image = Bloon.image_10
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.alive = True
        self.rx = self.rect.x
        self.ry = self.rect.y
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if not self.alive:
            return
        for dart in darts:
            if pygame.sprite.collide_mask(self, dart) and dart.alive:
                dart.shoot(self)
                if self.bloon == 3:
                    self.image = Bloon.image_2
                    self.bloon = 2
                elif self.bloon == 2:
                    self.image = Bloon.image_1
                    self.bloon = 1
                else:
                    self.alive = False
                    pops.append(Pop(self.group, self.group1,
                                    self.rect.x, self.rect.y))
                    self.kill()
        response = self.map.get((self.rect.x, self.rect.y))
        if (response == "killed"):
            if self.bloon == 3:
                self.image = Bloon.image_2
                self.bloon = 2
            elif self.bloon == 2:
                self.image = Bloon.image_1
                self.bloon = 1
            else:
                self.alive = False
                self.kill()
        else:
            dx, dy = response

            self.rx += dx * (self.bloon % 5) * 1.1
            self.ry += dy * (self.bloon % 5) * 1.1

            self.rect.x = int(self.rx)
            self.rect.y = int(self.ry)
