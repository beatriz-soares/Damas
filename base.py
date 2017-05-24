import pygame
import random
from funcoes import *

pygame.init()

screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

block_list, all_sprites_list = desenha_tela()

player = Block(RED, 20, 15)
all_sprites_list.add(player)

done = False

clock = pygame.time.Clock()

score = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(WHITE)
    pos = pygame.mouse.get_pos()

    player.rect.x = pos[0]
    player.rect.y = pos[1]

    """blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False)

    for block in blocks_hit_list:
        score += 1
        print(score)"""

    all_sprites_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
