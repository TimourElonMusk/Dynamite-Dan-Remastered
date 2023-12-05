import pygame, sys # import pygame and sys
from map import game_map, bg
from player import player_image, player_y_momentum, air_timer, test_rect, player_rect, player_speed, playerImageList
clock = pygame.time.Clock() # set up the clock
from pygame import mixer

from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame
pygame.mixer.init()

# initialisation
pygame.display.set_caption('Super Map.') # set the window name
WINDOW_SIZE = (800,600) # set up window size
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen
display = pygame.Surface((800, 600))
TILE_SIZE = 32

# assets import
grass_image = pygame.image.load('brick3.png')
dirt_image = pygame.image.load('brick.png')
stone_image = pygame.image.load('brick2.png')
musicplaying = pygame.mixer.music.load('music.mp3')

# scrolling
display_scroll = 0

# musicking
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()

# collisions
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

# movement
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

# moving or not
moving_right = False
moving_left = False

def getPlayerImage(x):
    if x%3 == 0:
        player_image = pygame.image.load(playerImageList[0])
    elif x%2 == 0:
        player_image = pygame.image.load(playerImageList[1])
    else:
        player_image = pygame.image.load(playerImageList[2])
    return player_image

# game loop
while True:

    display.fill((146, 244, 255))
    display.blit(bg, (0, 0))

    tile_rects = []

    player_falling = False

    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '3':
                display.blit(stone_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]

    if moving_right:
        if player_rect.x < 680:
            player_movement[0] += player_speed
            dir = 'RIGHTdir'

    if moving_left:
        if player_rect.x > 0:
            player_movement[0] -= player_speed
            dir = 'LEFTdir'

    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 2:
        player_y_momentum = 8
        player_falling = False
    else:
        player_falling = True

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    elif collisions['top']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1


    if dir == 'LEFTdir':
        display.blit(getPlayerImage(player_movement[0]), (player_rect.x, player_rect.y))
    else:
        display.blit(pygame.transform.flip(getPlayerImage(player_movement[0]), True, False), (player_rect.x, player_rect.y))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    display.scroll(display_scroll)
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()  # update display
    clock.tick(60)  # maintain 60 fps
