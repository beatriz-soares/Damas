# coding:utf-8
import pygame
import random
from funcoes import *

pygame.init()

"""ENVIRONMENT"""
screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()
lista_casas = gerar_casas()
lista_pedras = gerar_pedras(lista_casas)
lista_completa = pygame.sprite.Group()

"""VARIÁVEIS DE CONTROLE"""
done = False
casa_selecionada = None

# ver:
# https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
# http://samwize.com/2012/09/19/how-you-should-write-getter-slash-setter-for-python/
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()


            casas_clicadas = [s for s in lista_casas if s.rect.collidepoint(pos)]
            if casas_clicadas:
                if not casa_selecionada:
                    casa_selecionada = casas_clicadas[0]
                else:
                    pedra = casa_selecionada.pedra
                    casa_selecionada.pedra = None
                    casas_clicadas[0].pedra = pedra
                    pedra.rect = casas_clicadas[0].rect
            print casa_selecionada


    screen.fill(BRANCO)

    lista_casas.draw(screen)
    lista_pedras.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
