import pygame
from Dart import darts
from Pop import pops, Pop
pygame.init()
pygame.display.set_mode([1000, 1000])

bloons = []


class Bloon(pygame.sprite.Sprite):
    image_1 = pygame.image.load("data/Bloon_1.png").convert_alpha()
    image_2 = pygame.image.load("data/Bloon_2.png").convert_alpha()
    image_3 = pygame.image.load("data/Bloon_3.png").convert_alpha()

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
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.alive = True
        self.rx = self.rect.x
        self.ry = self.rect.y
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if not self.alive:
            return
        for dart in darts:
            if pygame.sprite.collide_mask(self, dart):
                dart.shoot(self)
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

            self.rx += dx * self.speed
            self.ry += dy * self.speed

            self.rect.x = int(self.rx)
            self.rect.y = int(self.ry)
