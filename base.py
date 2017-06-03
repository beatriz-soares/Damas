# coding:utf-8
import pygame
import random
from funcoes import *

pygame.init()

"""ENVIRONMENT"""
screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()
tabuleiro, lista_casas = gerar_casas()
lista_pedras = gerar_pedras(lista_casas)

def movimentos_possiveis(pedra):
    # FOI NECESSÁRIO DECLARAR ESSA FUNÇÃO AQUI PARA ACESSAR A VARIÁVEL tabuleiro
    global tabuleiro
    casas = []

    for direcao in pedra.direcoes:
        x, y = pedra.pos[0] + direcao[0], pedra.pos[1] + direcao[1]
        if x*y >= 0:
            try:
                casa = tabuleiro[x][y]
                if not casa.pedra:
                    casas.append(casa)
            except Exception:
                pass

    return casas


"""VARIÁVEIS DE CONTROLE"""
done = False
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
                        # MOVIMENTO DE PEÇA
                        pedra = casa_atual.pedra
                        if casa_clique in movimentos_possiveis(pedra):
                            casa_atual.pedra = None
                            casa_atual = None
                            casa_clique.pedra = pedra
                            pedra.rect = casa_clique.rect
                            map(pintar_neutralidade, casas_pintadas)
                    else:
                        # DE-SELEÇÃO DE CASA
                        map(pintar_neutralidade, casas_pintadas)
                        casa_atual = None
                        casas_pintadas = []


    screen.fill(BRANCO)

    lista_casas.draw(screen)
    lista_pedras.draw(screen)


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
