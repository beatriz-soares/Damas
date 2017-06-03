# coding:utf-8
import pygame
import random
from funcoes import *
from itertools import cycle

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
vez = cycle([S_PEDRA_ROSA, S_PEDRA_VERDE])
turno = vez.next()
# ver:
# https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
# http://samwize.com/2012/09/19/how-you-should-write-getter-slash-setter-for-python/
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            pedras_clicadas = [s for s in lista_pedras if s.rect.collidepoint(pos)]

            print casa_selecionada,' > ',
            casas_clicadas = [s for s in lista_casas if s.rect.collidepoint(pos)]
            if casas_clicadas:
                if not casa_selecionada:
                    if casas_clicadas[0].pedra:
                        print casas_clicadas
                        casa_selecionada = casas_clicadas[0]
                else:
                    if casa_selecionada and casa_selecionada.ocupavel:
                        if casa_selecionada.pedra.sprite == turno:
                            pedra = casa_selecionada.pedra
                            casa_selecionada.pedra = None
                            casa_selecionada = None
                            casas_clicadas[0].pedra = pedra
                            pedra.rect = casas_clicadas[0].rect
                            turno = vez.next()
                        else:
                            print "nao eh sua vez"
                            casa_selecionada = None

            print casa_selecionada


    screen.fill(BRANCO)

    lista_casas.draw(screen)
    lista_pedras.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
