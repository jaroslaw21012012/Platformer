import math, pickle

import pygame, sys, os
from pygame.locals import *
pygame.init()
# width = 71
# height = 53

WIDTH = 640 * 2 + 108 + 60
HEIGHT = 480 * 2 + 40
FPS = 30
clock = pygame.time.Clock()
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MAP GENERATOR")
# ============== RUS INSTRUCTIONS ============== #
# пока лкм зажата, то блок будет ставиться
# пока пкм зажата, то блок будет стираться
# если нажать на p - стирается ВСЁ!! БУДЬ ОСТОРОЖНЕЙ
# если нажать на s - сохранить карту

# ============== ENG INSTRUCTIONS ============== #
# while left mouse button pressed, block adding in mouse position
# while right mouse button pressed, block destroys in mouse position
# if you press "p" - it will be erase ALL MAP!! BE CAREFUL
# if you press "s" - it will be save map
draw_active = False
clear_active = False

def for_zero(count):
    s = str(count)
    if len(s) == 1:
        s = '000' + s
    elif len(s) == 2:
        s = '00' + s
    elif len(s) == 3:
        s = '0' + s
    elif len(s) == 4:
        s = '0' + s
    return s


with open("../game/levels/level.lvl", "rb") as f:
    level = pickle.load(f)
count = 0
# level = []
# for y in range(53):
#     row = []
#     for x in range(71):
#         row.append(-1)
#     level.append(row)
asset = []
count = 0
for y in range(30):
    row = []
    for x in range(6):
        row.append(f"tile_{for_zero(count)}.png")
        count += 1
    asset.append(row)
print(asset)

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
panel_rect = []




def draw_board(level):
    for y in range(53):
        for x in range(71):
            value_box = level[y][x]
            left = x * 18
            top = y * 18
            if value_box != -1:
                name = f"tile_{for_zero(value_box)}.png"
                image = pygame.image.load(os.path.join(f"assets/{name}"))
                rect = image.get_rect()
                rect.topleft = (left, top)
                DISPLAY.blit(image, rect.topleft)

def create_board():
    board = []
    for y in range(53):
        row = []
        for x in range(71):
            left = x * 18 + 10
            top = y * 18 + 20
            block = pygame.Rect(left, top, 18, 18)
            row.append(block)
        board.append(row)
    return board

def create_blocks_board():
    for y in range(30):
        for x in range(6):
            left = x * (18 + 4) + 1298
            top = y * (18 + 13) + 5
            panel_rect.append(pygame.Rect(left, top, 18, 18))

def draw_panel(asset):
    for y in range(30):
        for x in range(6):
            value_box = asset[y][x]
            left = x * (18 + 4) + 1298
            top = y * (18 + 13) + 5
            image = pygame.image.load(os.path.join(f"assets/{value_box}"))
            rect = image.get_rect()
            rect.topleft = (left, top)
            DISPLAY.blit(image, rect.topleft)




create_blocks_board()
mx = 0
my = 0
choiced_asset = 0
DISPLAY.fill((255, 224, 179))
draw_board(level)
while True:
    draw_panel(asset)
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            mx, my = event.pos
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                draw_active = True
            elif event.button == 3:
                clear_active = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                draw_active = False
                index = pygame.Rect(mx, my, 1, 1).collidelist(panel_rect)
                if index != -1:
                    choiced_asset = index
            elif event.button == 3:
                clear_active = False
        elif event.type == KEYDOWN:
            if event.key == K_s:
                with open("../game/levels/level.lvl", "wb") as f:
                    pickle.dump(level, f)

            if event.key == K_p:
                level = []
                for y in range(53):
                    row = []
                    for x in range(71):
                        row.append(-1)
                    level.append(row)
                DISPLAY.fill((255, 224, 179))
    if draw_active:
        x = (mx - mx % 18) // 18
        y = (my - my % 18) // 18
        try:
            level[y][x] = choiced_asset
            name = f"tile_{for_zero(level[y][x])}.png"
            image = pygame.image.load(os.path.join(f"assets/{name}"))
            rect = image.get_rect()
            rect.topleft = (x * 18, y * 18)
            pygame.draw.rect(DISPLAY, (255, 224, 179), (x * 18, y * 18, 18, 18))
            DISPLAY.blit(image, rect.topleft)
        except IndexError:
            pass
    if clear_active:
        x = (mx - mx % 18) // 18
        y = (my - my % 18) // 18
        level[y][x] = -1
        pygame.draw.rect(DISPLAY, (255, 224, 179), (x * 18, y * 18, 18, 18))
    pygame.display.update()
    clock.tick(FPS)
