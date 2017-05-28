# coding:utf-8
import pygame
import random
from funcoes import *

pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])

block_list, all_sprites_list = desenha_tela()

pedra_list, all_pedras_list = desenha_pedras()
done = False

clock = pygame.time.Clock()

score = 0
# ver:
# https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
# http://samwize.com/2012/09/19/how-you-should-write-getter-slash-setter-for-python/
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print matriz_pos_mouse(pos)


    screen.fill(WHITE)
    pos = pygame.mouse.get_pos()
    all_sprites_list.draw(screen)
    all_pedras_list.draw(screen)
    pygame.display.flip()

    clock.tick(30)

pygame.quit()
