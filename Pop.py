from random import randint
import pygame
pygame.init()
pygame.display.set_mode([1000, 1000])

pops = []


class Pop(pygame.sprite.Sprite):
    image = pygame.image.load("data/pop.png").convert_alpha()

    def __init__(self, group, group1, x, y):
        super().__init__(group, group1)

        self.image = Pop.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.rotate(self.image, randint(0, 360))
        self.time = 0

    def update(self):
        self.time += 1
        if self.time == 30:
            self.kill()
