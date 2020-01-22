import pygame
import pygame.gfxdraw

import math

from Bloon import Bloon, bloons
from Pop import Pop, pops
from Dart import Dart, darts
from DartMonkey import DartMonkey

from Plains import Map


pygame.init()

pygame.font.init()
myfont = pygame.font.SysFont('Calibri', 15)

size = [800, 600]
screen_rect = (0, 0, 800, 600)
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(0)
done = False
clock = pygame.time.Clock()


def draw_arc(screen, color, center, radius, startDeg, endDeg, thickness):
    (x, y) = center
    rect = (x-radius, y-radius, radius*2, radius*2)
    startRad = startDeg
    endRad = endDeg

    pygame.draw.arc(screen, color, rect, startRad, endRad, thickness)


all_sprites = pygame.sprite.Group()
bg_group = pygame.sprite.Group()
darts_group = pygame.sprite.Group()
bloons_group = pygame.sprite.Group()
boxes = []
player_group = pygame.sprite.Group()

main_map = Map(bg_group, all_sprites)

bloons = [Bloon(bloons_group, all_sprites, -100, 172, main_map, 1), Bloon(bloons_group, all_sprites, -150, 175, main_map, 3), Bloon(bloons_group,
                                                                                                                                    all_sprites, -200, 180, main_map, 1), Bloon(bloons_group, all_sprites, -250, 185, main_map, 2), Bloon(bloons_group, all_sprites, -300, 190, main_map)]

counter = 0

mainMonkey = DartMonkey(player_group, all_sprites)
speed = 5

cursor = pygame.transform.scale(pygame.image.load(
    'data/crosshair.png').convert_alpha(), (20, 20))


def draw_cursor(screen, x, y):
    if pygame.mouse.get_focused():
        screen.blit(cursor, (x, y))


while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and counter <= 0:
                counter = 60 * 1
                darts.append(Dart(darts_group, all_sprites,
                                  mainMonkey.rect.x, mainMonkey.rect.y))

    for dart in darts:
        dart.move()

    for bloon in bloons:
        bloon.move()

    for pop in pops:
        pop.update()

    if pygame.key.get_pressed()[pygame.K_w]:
        mainMonkey.move(0, -speed)
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

    bg_group.draw(screen)
    darts_group.draw(screen)
    player_group.draw(screen)
    bloons_group.draw(screen)

    counter -= 1

    # textsurface = myfont.render(f'x: {x}, y: {y}', False, (0, 0, 0))
    # screen.blit(textsurface, (0, 0))

    draw_cursor(screen, x - 10, y - 10)

    draw_arc(screen, pygame.Color("black"), (200, 200), 20, 0, 120, 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
