# coding:utf-8
import pygame
import random
from funcoes import *

pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])
lista_casas = gerar_casas()
lista_pedras = gerar_pedras(lista_casas)

lista_completa = pygame.sprite.Group()

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
            clicked_sprites = [s.pedra for s in lista_casas if s.rect.collidepoint(pos)]
            print clicked_sprites


    screen.fill(WHITE)

    lista_casas.draw(screen)
    lista_pedras.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
