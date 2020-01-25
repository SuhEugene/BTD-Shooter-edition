import pygame
import pygame.gfxdraw

import math
from random import randint

from Bloon import Bloon, bloons
from Pop import Pop, pops
from Dart import Dart, darts
from DartMonkey import DartMonkey
from Plains import Map


pygame.init()

pygame.font.init()
myfont = pygame.font.SysFont('Consolas', 20)

size = [800, 600]
screen_rect = (0, 0, 800, 600)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()


def draw_arc(screen, color, center, radius, startDeg, endDeg, thickness):
    (x, y) = center
    rect = (x-radius, y-radius, radius*2, radius*2)
    startRad = startDeg
    endRad = endDeg
    if pygame.mouse.get_focused():
        pygame.draw.arc(screen, color, rect, startRad, endRad, thickness)


all_sprites = pygame.sprite.Group()
bg_group = pygame.sprite.Group()
darts_group = pygame.sprite.Group()
bloons_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
main_map = Map(bg_group, all_sprites)
bloons = []  # Все шарики хранятся тут

counter = 0

mainMonkey = DartMonkey(player_group, all_sprites)

cursor = pygame.transform.scale(pygame.image.load(
    'data/crosshair.png').convert_alpha(), (20, 20))


# Спавнит шары такой сложности, как долго жив игрок
spawnrate = 60
spawnrate_counter = 0


def spawn():
    global spawnrate
    if (not (spawnrate_counter % int(spawnrate))):
        random = randint(0, 1000)
        btype = 1
        if (random > 100 and random < 125):
            btype = 10
        elif (random > 125 and random < 175):
            btype = 9
        elif (random > 175 and random < 225):
            btype = 8
        elif (random > 225 and random < 350):
            btype = 7
        elif (random > 350 and random < 550):
            btype = 6
        elif random <= 100:
            btype = 2
        elif random <= 650:
            btype = 3
        elif random <= 700:
            btype = 4
        elif random <= 750:
            btype = 5
        bloons.append(Bloon(bloons_group, all_sprites, -100, 170, main_map, btype))
        if (spawnrate > 5):
            spawnrate -= 0.01


# Перекрестие рисует
def draw_cursor(screen, x, y):
    if pygame.mouse.get_focused():
        screen.blit(cursor, (x, y))


def draw_upgrades(screen):
    m = myfont.render(f'Деняк: {points}$', True, (0, 0, 0))
    s = myfont.render(f'Скорость: {int(speed*10) - 49} lvl (2$)[Z]', True, (0, 0, 0))
    d = myfont.render(f'Стрельба: {int(cpp * 1000)//2 - 4} lvl (3$)[X]', True, (0, 0, 0))
    l = myfont.render(f'Жизни: {life} hp (5$)[C]', True, (0, 0, 0))
    screen.blit(m, (1, 1))
    screen.blit(s, (1, 22))
    screen.blit(d, (1, 43))
    screen.blit(l, (1, 65))


points = 0  # Деняки
spend = 0  # Потрачено деняк
speed = 5  # Скорость игрока
life = 100  # Жизни
additional_lives = 0  # Дополнительные жизни, за деняки
cooldown = 0  # Для стрельбы
cpp = 0.01  # [cooldown += cpp] далее есть
while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Пиу-пиу по cooldown'у при клике ЛКМ
        if event.type == pygame.MOUSEBUTTONDOWN and life + additional_lives > 0:
            if event.button == 1 and cooldown >= 1:
                cooldown = 0
                darts.append(Dart(darts_group, all_sprites,
                                  mainMonkey.rect.x, mainMonkey.rect.y))
    if (cooldown <= 1):
        cooldown += cpp

    # Двигаем всё, что должно двигаться
    for dart in darts:
        dart.move()

    for bloon in bloons:
        bloon.move()

    for pop in pops:
        pop.update()

    # Пересчёт по убитым шарам жизней и деняк
    life = 30 - sum([b.over for b in bloons]) + additional_lives
    points = int(sum([0.3 for b in bloons if ((not b.alive) and b.over == 0)])) - spend

    # [W][A][S][D]
    if life + additional_lives > 0:
        if pygame.key.get_pressed()[pygame.K_w]:
            mainMonkey.move(0, -speed)
        if pygame.key.get_pressed()[pygame.K_s]:
            mainMonkey.move(0, speed)
        if pygame.key.get_pressed()[pygame.K_d]:
            mainMonkey.move(speed, 0)
        if pygame.key.get_pressed()[pygame.K_a]:
            mainMonkey.move(-speed, 0)

    # Бусты
    if life + additional_lives > 0:
        if pygame.key.get_pressed()[pygame.K_z] and points >= 2:
            spend += 2
            speed += 0.1
        if pygame.key.get_pressed()[pygame.K_x] and points >= 3:
            spend += 3
            cpp += 0.002
        if pygame.key.get_pressed()[pygame.K_c] and points >= 5:
            spend += 5
            additional_lives += 1

    # Крутим бибизяну за курсором
    if life + additional_lives > 0:
        mainMonkey.angle_rot()

    # Задний фон белый
    screen.fill(pygame.Color("white"))

    # Позиция мышки для отрисовки курсора и cooldown'a
    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]

    # Рисуем всё, что можно нарисовать
    bg_group.draw(screen)
    darts_group.draw(screen)
    player_group.draw(screen)
    bloons_group.draw(screen)
    if life + additional_lives > 0:
        draw_upgrades(screen)

    spawnrate_counter += 1
    spawn()

    if life + additional_lives > 0:
        pygame.mouse.set_visible(0)
        draw_cursor(screen, x - 10, y - 10)
        draw_arc(screen, pygame.Color("black"), (x, y), 17,
                 3.15/2, 3.15 * 2 * cooldown + 3.15/2, 2)
    else:
        # Если сдох, то выводим тексты + очки
        pygame.mouse.set_visible(1)
        pnts = sum([1 for b in bloons if ((not b.alive) and b.over == 0)])
        killed = myfont.render('Вы проиграли', True, (255, 255, 255))
        killed2 = myfont.render('Перезапустите игру', True, (255, 255, 255))
        killed3 = myfont.render(f'Ваши очки: ' + str(pnts), True, (255, 255, 255))
        screen.blit(killed, (310, 230))
        screen.blit(killed2, (310, 252))
        screen.blit(killed3, (310, 274))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
