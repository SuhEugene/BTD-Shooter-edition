import pygame

from Bloon import Bloon, bloons 
from Pop import Pop, pops 
from Dart import Dart, darts
from DartMonkey import DartMonkey

from Plains import Map


pygame.init()
size = [800, 600]
screen_rect = (0, 0, 800, 600)
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(0)
done = False
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
darts_group = pygame.sprite.Group()
bloons_group = pygame.sprite.Group()
boxes = []
player_group = pygame.sprite.Group()

bloons = [Bloon(bloons_group, all_sprites, 150, 50, Map), Bloon(
    bloons_group, all_sprites, 195, 50, Map), Bloon(bloons_group, all_sprites, 240, 50, Map)]



mainMonkey = DartMonkey(player_group, all_sprites)
speed = 5

cursor = pygame.transform.scale(pygame.image.load('data/crosshair.png').convert_alpha(), (20, 20))


def draw_cursor(screen, x, y):
    if pygame.mouse.get_focused():
        screen.blit(cursor, (x, y))


while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                darts.append(Dart(darts_group, all_sprites, mainMonkey.rect.x, mainMonkey.rect.y))

    for dart in darts:
        dart.move()

    for bloon in bloons:
        bloon.move()

    for pop in pops:
        pop.update()

    if pygame.key.get_pressed()[pygame.K_w]:
        mainMonkey.move(0, -speed)
        darts.append(Dart(all_sprites, darts_group, mainMonkey.rect.x, mainMonkey.rect.y))
    if pygame.key.get_pressed()[pygame.K_s]:
        mainMonkey.move(0, speed)
    if pygame.key.get_pressed()[pygame.K_d]:
        mainMonkey.move(speed, 0)
    if pygame.key.get_pressed()[pygame.K_a]:
        mainMonkey.move(-speed, 0)

    mainMonkey.angle_rot()

    screen.fill(pygame.Color("white"))
    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]

    darts_group.draw(screen)
    player_group.draw(screen)
    bloons_group.draw(screen)

    draw_cursor(screen, x - 10, y - 10)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
