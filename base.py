# coding:utf-8
import pygame
import random
from funcoes import *
from itertools import cycle
from random import choice as escolha_aleatoria
from time import sleep as esperar

pygame.init()

"""ENVIRONMENT"""
screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()
lista_casas = gerar_casas()
lista_pedras = gerar_pedras(lista_casas)
lista_inicio = gerar_coisas_do_inicio()

"""VARIÁVEIS DE CONTROLE"""
done = False
tela = inicio

vez = cycle([S_PEDRA_ROSA, S_PEDRA_VERDE])
turno = vez.next()

qtd = {S_PEDRA_ROSA: 12, S_PEDRA_VERDE:12}
casa_atual = None
casas_pintadas = []

myfont = pygame.font.SysFont("monospace", 15)
label = myfont.render("Comecou", 1, VERMELHO)

# ver:
# https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
# http://samwize.com/2012/09/19/how-you-should-write-getter-slash-setter-for-python/
while not done:

    screen.fill(BRANCO)

    if tela == inicio:
        # EVENTOS QUE ACONTECEM NA TELA DE INICIO
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()

                botoes_clicados = [s for s in lista_inicio if s.rect.collidepoint(mouse)]
                for botao in botoes_clicados:
                    if botao.text == texto_1x1:
                        label = myfont.render("Comecou 1x1", 1, VERMELHO)
                        tela = jogo_1x1

                    if botao.text == texto_1xPC:
                        label = myfont.render("Comecou 1xPC", 1, VERMELHO)
                        tela = jogo_1xPC

                    if botao.text == texto_sair:
                        done = True

        lista_inicio.draw(screen)

        # FIM EVENTOS DA TELA DE INICIO


    elif tela == jogo_1xPC:
        # EVENTOS QUE ACONTECEM DURANTE A PARTIDA 1xPC

        if turno == S_PEDRA_ROSA:
            # VEZ DO PC
            pedra_pc = escolha_aleatoria(lista_pedras.sprites())

            if pedra_pc.sprite == S_PEDRA_ROSA:
                if len(movimentos_possiveis(pedra_pc)[0]) > 0:
                    esperar(1)
                    # SELEÇÃO
                    movimentos = movimentos_possiveis(pedra_pc)
                    # MOVIMENTO DE PEÇA
                    # PRÉ-MOVIMENTO
                    casa_atual = pedra_pc.casa
                    casa_atual.pedra = None

                    # MOVIMENTO
                    casa_clique = escolha_aleatoria(movimentos[0])
                    casa_clique.pedra = pedra_pc
                    pedra_pc.casa = casa_clique
                    pedra_pc.rect = casa_clique.rect
                    pedra_pc.pos = casa_clique.pos

                    print '                            ',casa_atual,' > ', pedra_pc, ' < ', casa_clique

                    try:
                        if movimentos[1][0]:
                            casa_comida = movimentos[1][movimentos[0].index(casa_clique)]
                            for c in casa_comida:
                                pedra_comida = c.pedra
                                c.pedra = None
                                lista_pedras.remove(pedra_comida)
                                qtd[pedra_comida.sprite]-=1
                            if qtd[pedra_comida.sprite] == 0:
                                label = myfont.render("Vencedor: %s"%pedra_comida.sprite, 1, (255,0,0))
                                done = True
                            print "comeu"
                    except Exception as e:
                        print 1,e

                    # PÓS-MOVIMENTO
                    turno = vez.next()
                    label = myfont.render("Vez de %s" %turno, 1, (255,0,0))



            # FIM VEZ DO PC

        else:
            # VEZ DO JOGADOR
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
                        print 2,e

                    if casa_clique:
                        # CLIQUE NO TABULEIRO
                        if not casa_atual:
                            if casa_clique.pedra:
                                # SELEÇÃO DE CASA
                                for casa in lista_casas:
                                    if casa.pedra:
                                        if casa.pedra.sprite == turno:
                                            movimentos = movimentos_possiveis(casa.pedra)
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

                                        try:
                                            if movimentos[1][0]:
                                                casa_comida = movimentos[1][movimentos[0].index(casa_clique)]
                                                for c in casa_comida:
                                                    pedra_comida = c.pedra
                                                    c.pedra = None
                                                    lista_pedras.remove(pedra_comida)
                                                    qtd[pedra_comida.sprite]-=1
                                                if qtd[pedra_comida.sprite] == 0:
                                                    label = myfont.render("Vencedor: %s"%pedra_comida.sprite, 1, (255,0,0))
                                                    done = True
                                                print "comeu"
                                        except Exception as e:
                                            print 3,e

                                        # PÓS-MOVIMENTO
                                        turno = vez.next()
                                        label = myfont.render("Vez de %s" %turno, 1, (255,0,0))

                            # DE-SELEÇÃO DE CASA
                            casa_atual = None

                            # RESETAR AS CORES DAS CASAS
                            try:
                                map(pintar_neutralidade, casas_possiveis)
                                casas_pintadas = []
                            except Exception as e:
                                print 4,e
            # FIM VEZ DO JOGADOR

        lista_casas.draw(screen)
        lista_pedras.draw(screen)
        screen.blit(label, (0, 0))

        # FIM EVENTOS DA TELA DE PARTIDA 1xPC


    elif tela == jogo_1x1:
        # EVENTOS QUE ACONTECEM DURANTE A PARTIDA 1x1
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
                    print 5,e

                if casa_clique:
                    # CLIQUE NO TABULEIRO
                    if not casa_atual:
                        if casa_clique.pedra:
                            # SELEÇÃO DE CASA
                            for casa in lista_casas:
                                if casa.pedra:
                                    if casa.pedra.sprite == turno:
                                        movimentos = movimentos_possiveis(casa.pedra)
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

                                    try:
                                        if movimentos[1][0]:
                                            casa_comida = movimentos[1][movimentos[0].index(casa_clique)]
                                            for c in casa_comida:
                                                pedra_comida = c.pedra
                                                c.pedra = None
                                                lista_pedras.remove(pedra_comida)
                                                qtd[pedra_comida.sprite]-=1
                                            if qtd[pedra_comida.sprite] == 0:
                                                label = myfont.render("Vencedor: %s"%pedra_comida.sprite, 1, (255,0,0))
                                                done = True
                                            print "comeu"
                                    except Exception as e:
                                        print movimentos
                                        print 6,e

                                    # PÓS-MOVIMENTO
                                    turno = vez.next()
                                    label = myfont.render("Vez de %s" %turno, 1, (255,0,0))

                        # DE-SELEÇÃO DE CASA
                        casa_atual = None

                        # RESETAR AS CORES DAS CASAS
                        map(pintar_neutralidade, casas_possiveis)
                        casas_pintadas = []

        lista_casas.draw(screen)
        lista_pedras.draw(screen)
        screen.blit(label, (0, 0))

        # FIM EVENTOS DA TELA DE PARTIDA 1x1


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
