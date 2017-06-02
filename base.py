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
casa_atual = None

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

            print casa_atual,' > ',
            casa_clique = [s for s in lista_casas if s.rect.collidepoint(pos)][0]
            if casa_clique:
                # CLIQUE NO TABULEIRO
                if not casa_atual:
                    if casa_clique.pedra:
                        # SELEÇÃO DE CASA
                        print casa_clique
                        casa_atual = casa_clique
                else:
                    if casa_clique.ocupavel:
                        # MOVIMENTO DE PEÇA
                        pedra = casa_atual.pedra
                        casa_atual.pedra = None
                        casa_atual = None
                        casa_clique.pedra = pedra
                        pedra.rect = casa_clique.rect
                    else:
                        # DE-SELEÇÃO DE CASA
                        casa_atual = None
            print casa_atual


    screen.fill(BRANCO)

    lista_casas.draw(screen)
    lista_pedras.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
