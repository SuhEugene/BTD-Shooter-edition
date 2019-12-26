import pygame
from Dart import darts
from Pop import pops, Pop
pygame.init()
pygame.display.set_mode([1000, 1000])

bloons = []

class Bloon(pygame.sprite.Sprite):
    image = pygame.image.load("data/bloon.png").convert_alpha()

    def __init__(self, group, group1, x, y, map_c):
        super().__init__(group, group1)

        self.group = group
        self.group1 = group1

        self.map = map_c()
        self.image = Bloon.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
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
                pops.append(Pop(self.group, self.group1, self.rect.x, self.rect.y))
                self.kill()

        dx, dy = self.map.get((self.rect.x, self.rect.y))

        self.rx += dx
        self.ry += dy

        self.rect.x = int(self.rx)
        self.rect.y = int(self.ry)