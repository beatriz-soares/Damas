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

"""VARIÁVEIS DE CONTROLE"""
done = False
vez = cycle([S_PEDRA_ROSA, S_PEDRA_VERDE])
turno = vez.next()
qtd = {S_PEDRA_ROSA: 12, S_PEDRA_VERDE:12}
casa_atual = None
casas_pintadas = []
myfont = pygame.font.SysFont("monospace", 15)
label = myfont.render("Comecou", 1, (255,0,0))

# ver:
# https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
# http://samwize.com/2012/09/19/how-you-should-write-getter-slash-setter-for-python/
while not done:
    casa_clique = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            pedras_clicadas = [s for s in lista_pedras if s.rect.collidepoint(pos)]

            try:
                casa_clique = [s for s in lista_casas if s.rect.collidepoint(pos)][0]
            except Exception as e:
                casa_clique = None
                pass

            if casa_clique:
                # CLIQUE NO TABULEIRO
                if not casa_atual:
                    if casa_clique.pedra:
                        # SELEÇÃO DE CASA
                        for casa in lista_casas:
                            if casa.pedra:
                                if casa.pedra.sprite == turno:
                                    movimentos = movimentos_possiveis(casa.pedra)
                                    if movimentos[1]:
                                        casa_clique = casa
                                        break
                        movimentos = movimentos_possiveis(casa_clique.pedra)
                        casa_atual, casas_possiveis = casa_clique, movimentos[0]

                        map(pintar_selecionavel, casas_possiveis)

                else:
                    if casa_clique.ocupavel and not casa_clique.pedra:
                        if not casa_atual.pedra.sprite == turno:
                            print "nao eh sua vez"
                            label = myfont.render("Nao eh sua vez", 1, (255,0,0))

                        else:
                            pedra = casa_atual.pedra
                            if casa_clique in movimentos_possiveis(pedra)[0]:
                                # MOVIMENTO DE PEÇA
                                # PRÉ-MOVIMENTO
                                casa_atual.pedra = None

                                # MOVIMENTO
                                casa_clique.pedra = pedra
                                pedra.rect = casa_clique.rect
                                pedra.pos = casa_clique.pos

                                if movimentos[1]:
                                    casa_comida = movimentos[1]
                                    pedra_comida = casa_comida.pedra
                                    casa_comida.pedra = None
                                    lista_pedras.remove(pedra_comida)
                                    qtd[pedra_comida.sprite]-=1
                                    if qtd[pedra_comida.sprite] == 0:
                                        label = myfont.render("Vencedor: %s"%pedra_comida.sprite, 1, (255,0,0))
                                        done = True
                                    print "comeu"

                                # PÓS-MOVIMENTO
                                turno = vez.next()
                                label = myfont.render("Vez de %s" %turno, 1, (255,0,0))

                    # DE-SELEÇÃO DE CASA
                    casa_atual = None

                    # RESETAR AS CORES DAS CASAS
                    map(pintar_neutralidade, casas_possiveis)
                    casas_pintadas = []


    screen.fill(BRANCO)

    lista_casas.draw(screen)
    lista_pedras.draw(screen)
    screen.blit(label, (0, 0))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
