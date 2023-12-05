import pygame

playerImageList = ['dynamite-dan_walk1.png','dynamite-dan_walk2.png','dynamite-dan_walk3.png']
player_image = pygame.image.load(playerImageList[0])
player_image.set_colorkey((255, 255, 255))

player_y_momentum = 0
air_timer = 0
player_speed = 5

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)