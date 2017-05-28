# coding:utf-8
import pygame
from itertools import cycle

"""CONSTANTES"""
# CORES FLAT
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
AZUL  = (150, 206, 180)
BEGE  = (255, 238, 173)

# TIPOS DE PEÇA (COR DA PEÇA OU TIME)
P_PRETA = 0
P_BRANCA = 1

# SPRITES
S_CASA_BRANCA = "sprites/casa_branca.jpg"
S_CASA_PRETA = "sprites/casa_preta.jpg"
S_ROSA = "sprites/pedra_rosa.png"
S_VERDE = "sprites/pedra_verde.png"

# ENVIRONMENT
screen_width = 488
screen_height = 488

posx_tabuleiro = 20
posy_tabuleiro = 20

posx_pedra = 22
posy_pedra = 20

tamanho_casas = (56,56)

dim_pedra = 50

"""CLASSES"""
class Cor(pygame.sprite.Sprite):

    def __init__(self, cor, tamanho, pos):
        super(Cor, self).__init__()
        self.image = pygame.Surface([tamanho[1], tamanho[0]])
        self.image.fill(cor)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class Bloco(pygame.sprite.Sprite):

    def __init__(self, sprite, clicavel=False):
        super(Bloco, self).__init__()
        self.image = pygame.image.load(sprite)
        self.sprite = sprite
        self.clicavel = clicavel
        self.rect = self.image.get_rect()

class Botao(Bloco):
    def __init__(self, sprite):
        super(Botao, self).__init__(sprite, clicavel=True)

# class Casa(Botao):
#     def __init__(self, id, pos, sprite):
#         super(Casa, self).__init__(sprite)
#         self.id = id
#         self.preenchida = False
#         self.rect.x = pos[0]
#         self.rect.y = pos[1]
#         self.pedra = None

class Pedra(Botao):
    def __init__(self, pos, cor, sprite):
        super(Pedra, self).__init__(sprite)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.cor = cor


"""FUNÇÕES"""
def desenha_tela():
    lista_casas = pygame.sprite.Group()

    all_sprites_list = pygame.sprite.Group()

    cores_alternadas = cycle([BEGE, AZUL])

    for i in range(8):
        for j in range(8):

            cor = Cor(cores_alternadas.next(), tamanho_casas, pos(i,j))

            lista_casas.add(cor)
            all_sprites_list.add(cor)

        cores_alternadas.next()

    return[lista_casas, all_sprites_list]

def desenha_pedras():
    lista_pedras = pygame.sprite.Group()

    all_pedras_list = pygame.sprite.Group()

    cor = S_VERDE
    cores_alternadas = cycle([S_CASA_BRANCA,S_CASA_PRETA])

    for linha in range(3):
        for coluna in range(8):
            casa = cores_alternadas.next()

            if casa == S_CASA_PRETA:
                print '%d %d    %s' % (linha,coluna,pos(linha,coluna))
                pedra = Pedra(pos(linha,coluna), P_PRETA, cor)
                lista_pedras.add(pedra)
                all_pedras_list.add(pedra)
        cores_alternadas.next()

    cor = S_ROSA

    for i in range(5,8):
        for j in range(8):
            casa = cores_alternadas.next()
            pedra = Pedra(pos(i,j), casa, cor)

            if casa == S_CASA_PRETA:
                lista_pedras.add(pedra)
                all_pedras_list.add(pedra)

        cores_alternadas.next()

    return[lista_pedras, all_pedras_list]

def pos(i,j):
    coluna = posx_tabuleiro + tamanho_casas[0] * i
    linha = posx_tabuleiro + tamanho_casas[1] * j

    return (linha,coluna)
