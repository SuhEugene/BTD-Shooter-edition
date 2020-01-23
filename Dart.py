import pygame
import math

screen_rect = (0, 0, 800, 600)

pygame.init()
pygame.display.set_mode([1000, 1000])

darts = []


class Dart(pygame.sprite.Sprite):
    image = pygame.image.load("data/dart.png").convert_alpha()

    def __init__(self, group, group1, x, y):
        super().__init__(group, group1)

        self.main_image = Dart.image
        self.image = self.main_image
        self.rect = self.image.get_rect()
        self.rect.x = x + 25
        self.rect.y = y + 25
        self.alive = True
        self.speed = 10
        self.counter = set()
        angle = math.atan2(pygame.mouse.get_pos()[0] - self.rect.x + 1.5,
                           pygame.mouse.get_pos()[1] - self.rect.y + 5) + 1.570796327

        dx = math.sin(angle) * -17
        dy = math.cos(angle) * -17

        self.rect.x = self.rect.x + dx
        self.rect.y = self.rect.y + dy

        self.angle = math.atan2(pygame.mouse.get_pos()[0] - self.rect.x + 1.5,
                                pygame.mouse.get_pos()[1] - self.rect.y + 5)

        self.dx = math.sin(self.angle) * self.speed
        self.dy = math.cos(self.angle) * self.speed

        self.rx, self.ry = self.rect.x, self.rect.y

        self.image = pygame.transform.rotate(
            self.main_image, math.degrees(self.angle))
        rect = self.rect
        self.rect = self.image.get_rect(center=rect.center)

    def move(self):
        self.rx += self.dx
        self.ry += self.dy

        self.rect.x = int(self.rx)
        self.rect.y = int(self.ry)

        if not self.rect.colliderect(screen_rect):
            self.alive = False
            self.kill()
        # print(darts)

    def shoot(self, kill):
        self.counter.add(kill)
        if len(self.counter) == 3:
            self.alive = False
            self.kill()
