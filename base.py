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
print tabuleiro

"""VARIÁVEIS DE CONTROLE"""
done = False
vez = cycle([S_PEDRA_ROSA, S_PEDRA_VERDE])
turno = vez.next()
casa_atual = None
casas_pintadas = []

# ver:
# https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
# http://samwize.com/2012/09/19/how-you-should-write-getter-slash-setter-for-python/
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            print casas_pintadas
            pos = pygame.mouse.get_pos()

            pedras_clicadas = [s for s in lista_pedras if s.rect.collidepoint(pos)]

            try:
                casa_clique = [s for s in lista_casas if s.rect.collidepoint(pos)][0]
            except Exception as e:
                pass
            if casa_clique:
                # CLIQUE NO TABULEIRO
                if not casa_atual:
                    if casa_clique.pedra:
                        # SELEÇÃO DE CASA
                        casa_atual, casas_possiveis = casa_clique, movimentos_possiveis(casa_clique.pedra)
                        casas_pintadas.extend(casas_possiveis + [casa_atual])
                        map(pintar_selecionavel, casas_pintadas)

                else:
                    if casa_clique.ocupavel and not casa_clique.pedra:
                        if not casa_atual.pedra.sprite == turno:
                            print "nao eh sua vez"
                            casa_atual = None

                        else:
                            pedra = casa_atual.pedra
                            if casa_clique in movimentos_possiveis(pedra):
                                # MOVIMENTO DE PEÇA
                                # PRÉ-MOVIMENTO
                                casa_atual.pedra = None
                                casa_atual = None

                                # MOVIMENTO
                                casa_clique.pedra = pedra
                                pedra.rect = casa_clique.rect
                                pedra.pos = casa_clique.pos

                                # PÓS-MOVIMENTO
                                turno = vez.next()
                    else:
                        # DE-SELEÇÃO DE CASA
                        casa_atual = None

                    # RESETAR AS CORES DAS CASAS
                    map(pintar_neutralidade, casas_pintadas)
                    casas_pintadas = []


    screen.fill(BRANCO)

    lista_casas.draw(screen)
    lista_pedras.draw(screen)


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
