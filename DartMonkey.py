import pygame
import math


pygame.init()
pygame.display.set_mode([1000, 1000])


class DartMonkey(pygame.sprite.Sprite):
    image = pygame.image.load("data/dartmonkey.png").convert_alpha()

    def __init__(self, group, group1):
        super().__init__(group, group1)

        self.main_image = DartMonkey.image
        self.image = self.main_image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.angle = 0

    def move(self, x, y):
        if (self.rect.x + x < -20 or self.rect.y + y < -20 or
                self.rect.x + x + 50 > 820 or self.rect.y + y + 50 > 620):
            return
        self.rect = self.rect.move(x, y)

    def angle_rot(self):
        self.angle = math.degrees(math.atan2(self.rect.x + 25 - pygame.mouse.get_pos()[0],
                                             self.rect.y + 25 - pygame.mouse.get_pos()[1]))

        self.image = pygame.transform.rotate(self.main_image, self.angle)

        rect = self.rect
        self.rect = self.image.get_rect(center=rect.center)
