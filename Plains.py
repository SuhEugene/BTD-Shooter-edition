import pygame

pygame.init()
pygame.display.set_mode([1000, 1000])


class Map(pygame.sprite.Sprite):
    image = pygame.image.load("data/Plainsmap.png").convert_alpha()

    def __init__(self, group, group1):
        super().__init__(group, group1)

        self.image = Map.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def get(self, pos):
        if (pos[0] < 200):
            #print("pos[0] < 200", flush=True)
            return (1, -0.05)
        elif (pos[0] >= 200 and pos[1] < 330 and pos[0] < 500):
            #print("pos[0] >= 200 and pos[1] < 330", flush=True)
            return (0.1, 1)
        elif (pos[0] <= 490):
            #print("pos[0] <= 490", flush=True)
            return (1, 0.035)
        elif (pos[1] <= 485 and pos[0] < 500):
            #print("pos[1] <= 485", flush=True)
            return (0.05, 1)
        elif (pos[0] <= 700):
            #print("pos[0] <= 700", flush=True)
            return (1, 0.05)
        elif (pos[1] > -45):
            #print("pos[1] > 0", flush=True)
            return (0, -1)
        elif (pos[1] <= -45):
            return "killed"
        return (0, 0)
