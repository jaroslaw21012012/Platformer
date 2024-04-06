import time

import pygame, sys, os, pickle



# ============== SETTINGS ============== #
clock = pygame.time.Clock()
FPS = 90
pygame.init()
pygame.display.set_caption('Platformer')
WINDOW_SIZE = (640,480)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((320, 240), pygame.SRCALPHA)
TOUCH_BLOCKS = (0, 1, 2, 3, 4, 5, 6, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 47, 48, 49, 50, 51, 52, 56, 57, 58, 59, 60, 61, 62, 63, 76, 77, 78, 79, 80, 81, 82, 83, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 113, 114, 155, 119, 120, 121, 122, 123, 130, 132, 133, 134, 135, 140, 141, 142, 143, 146, 147, 148, 153, 154, 155, 156)
bg_image = pygame.image.load(os.path.join("assets/Backgrounds/bg.jpg"))


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

# ============== SOUNDS ============== #
coin_snd = pygame.mixer.Sound("assets/coin.wav")
tp_snd = pygame.mixer.Sound("assets/teleport.wav")
hit_snd = pygame.mixer.Sound("assets/hit.wav")
pygame.mixer.music.load("assets/music.wav")

# ============== MUSIC ============== #
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)


# ============== GUI COUNTER ============== #
coin_count = 0
COIN_BLOCKS = (151, )
font = pygame.font.Font(os.path.join("assets/pixel.ttf"), 16)

coin_image = pygame.image.load(os.path.join("assets/tile_0151.png"))

# ============== ENEMIES ============== #

ENEMIES_BLOCKS = (68, )

# ============== TELEPORTS ============== #
TELEPORT_BLOCKS = (107, 108, )

# ============== WIN BLOCK ============== #
WIN_BLOCK = (111, 112, )

# ============== ASSETS LOADING ============== #
def load_assets():
    assets = []
    for i in range(180):
        name = f"tile_{for_zero(i)}.png"
        image = pygame.image.load(os.path.join(f"assets/{name}"))
        assets.append(image)
    return assets


assets = load_assets()


def load_player_animation():
    animation_frames = {}
    animation_frames_data = []
    for i in range(1, 9):
        image_name = f"elf_side02_walk{i}.png"
        image = pygame.image.load(os.path.join(f"assets/Characters/run_left/{image_name}"))
        animation_frames_data.append(image)
    animation_frames["run_left"] = animation_frames_data
    animation_frames_data = []
    for i in range(1, 9):
        image_name = f"elf_side01_walk{i}.png"
        image = pygame.image.load(os.path.join(f"assets/Characters/run_right/{image_name}"))
        animation_frames_data.append(image)
    animation_frames["run_right"] = animation_frames_data
    image = pygame.image.load(os.path.join("assets/Characters/idle/elf_front_idle.png"))
    animation_frames["idle"] = [image]
    return animation_frames


animation_frames = load_player_animation()


# ============== MAP ============== #
LEVEL = []
with open("levels/level.lvl", "rb") as f:
    LEVEL = pickle.load(f)
level = LEVEL.copy()

# ============== PLAYER MOVEMENT AND COLLISION CHECK ============== #
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types








player_image = pygame.image.load(os.path.join("assets/Characters/idle/elf_front_idle.png"))
player_rect = player_image.get_rect()
player_rect.left = 180
player_rect.top = 140
moving_right = False
moving_left = False
player_action = "idle"
player_frame = 0

player_y_momentum = 0
air_timer = 0

true_scroll = [0, 0]
camera_speed = 20
flip = True
flag = True


win = False
font_win = pygame.font.Font(os.path.join("assets/pixel.ttf"), 50)
win_text_label = font_win.render("YOU WIN", False, (0, 0, 0))
win_rect = win_text_label.get_rect()
win_rect.center = (160, 120)
win_label_time = time.time()
win_label_direction = "top"



while flag:
    #display.fill((255, 224, 179))
    if win:

        display.fill((244, 244, 244))
        display.blit(win_text_label, win_rect)
        if time.time() - win_label_time < 0.2:
            if win_label_direction == "top":
                win_rect.y -= 1
            else:
                win_rect.y += 1
        else:
            win_label_time = time.time()
            if win_label_direction == "top":
                win_label_direction = "bottom"
            else:
                win_label_direction = "top"





    elif not win:
        # ============== SCROLL ============== #
        true_scroll[0] += (player_rect.x - true_scroll[0] - 167)/camera_speed
        true_scroll[1] += (player_rect.y - true_scroll[1] - 127)/camera_speed*2
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
        display.blit(bg_image, (-300 - scroll[0] / 2, -500 - scroll[1] / 3))

        # ============== PLACEMENT OF BLOCKS ============== #
        tile_rects = []
        coin_rects = []
        enemy_rects = []
        teleport_rects = []
        win_block_rects = []
        for y in range(len(level)):
            for x in range(len(level[y])):
                left = 18 * x - scroll[0]
                top = 18 * y - scroll[1]
                value = level[y][x]
                if value != -1:
                    image = assets[value]
                    rect = image.get_rect()
                    rect.topleft = (left, top)
                    display.blit(image, rect.topleft)
                    if value in TOUCH_BLOCKS:
                        tile_rects.append(pygame.Rect(x * 18, y * 18, 18, 18))
                    elif value in COIN_BLOCKS:
                        coin_rects.append(pygame.Rect(x * 18, y * 18, 18, 18))
                    elif value in ENEMIES_BLOCKS:
                        enemy_rects.append(pygame.Rect(x * 18, y * 18, 18, 18))
                    elif value in TELEPORT_BLOCKS:
                        teleport_rects.append(pygame.Rect(x * 18, y * 18, 18, 18))
                    elif value in WIN_BLOCK:
                        win_block_rects.append(pygame.Rect(x * 18, y * 18, 18, 18))



        # ============== PLAYER MOVEMENT ============== #
        player_movement = [0, 0]
        if moving_right:
            player_movement[0] += 2
        elif moving_left:
            player_movement[0] -= 2
        player_movement[1] += player_y_momentum
        player_y_momentum += 0.2
        if player_y_momentum > 5:
            player_y_momentum = 5

        if player_movement[0] < 0:
            player_action = "run_right"
            if player_frame != 7:
                player_frame += 1
            else:
                player_frame = 0
        if player_movement[0] > 0:
            player_action = "run_left"
            if player_frame != 7:
                player_frame += 1
            else:
                player_frame = 0
        if player_movement[0] == 0:
            player_action = "idle"
            player_frame = 0
        player_rect, collisions = move(player_rect, player_movement, tile_rects) #  player move


        # ============== FOR JUMP ============== #
        if collisions['bottom']:
            player_y_momentum = 0
            air_timer = 0
        else:
            air_timer += 1

        if collisions['top']:
            player_y_momentum = 0

        # ============== COIN AND ENEMY BLOCKS COLLISION AND TELEPORT AND WIN ============== #
        for coin in range(len(coin_rects)):
            if player_rect.colliderect(coin_rects[coin]):
                coin_count += 1
                y = int(coin_rects[coin].y / 18)
                x = int(coin_rects[coin].x / 18)
                LEVEL[y][x] = -1
                coin_snd.play()

        if player_rect.collidelistall(enemy_rects):
            player_rect.y = 140
            player_rect.x = 180
            hit_snd.play()

        if player_rect.colliderect(teleport_rects[-1]):
            player_rect.y = teleport_rects[0].y
            player_rect.x = teleport_rects[0].x
            tp_snd.play()

        if player_rect.collidelistall(win_block_rects):
            win = True
            win_label_time = time.time()
            pygame.mixer.music.stop()



    # ============== EVENTS ============== #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_UP:
                if air_timer < 6:
                    player_y_momentum = -6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                moving_left = False

    if not win:
        # ============== DRAW PLAYER ============== #
        player_image = animation_frames[player_action][player_frame]
        display.blit(pygame.transform.flip(player_image, flip, False),(player_rect.x - scroll[0], player_rect.y - scroll[1]))

        # ============== COIN INDICATOR ============== #

        coin_text = font.render(str(coin_count), False, (255, 255, 255))
        display.blit(coin_text, (20, 1))
        display.blit(coin_image, (2, 0))



    # ============== DISPLAY UPDATE ============== #
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(FPS)


