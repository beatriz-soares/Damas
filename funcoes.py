# coding:utf-8
import pygame
from itertools import cycle

"""CONSTANTES"""
# CORES FLAT
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

# TIPOS DE PEÇA (COR DA PEÇA OU TIME)
P_PRETA = 0
P_BRANCA = 1

# SPRITES
S_BRANCO = "sprites/branco.jpg"
S_PRETO = "sprites/preto.jpg"

# ENVIRONMENT
posx_tabuleiro = 20
posy_tabuleiro = 20

tile_x_tam = 56
tile_y_tam = 56

"""CLASSES"""
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

class Casa(Botao):
    def __init__(self, id, pos, sprite):
        super(Casa, self).__init__(sprite)
        self.id = id
        self.preenchida = False
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pedra = None

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

    cores_alternadas = cycle([S_BRANCO,S_PRETO])

    pos_x = posx_tabuleiro
    pos_y = posy_tabuleiro

    for i in range(8):
        for j in range(8):
            casa = Casa(i+j, (pos_x,pos_y),cores_alternadas.next())

            pos_x+= tile_x_tam

            lista_casas.add(casa)
            all_sprites_list.add(casa)

        pos_x = posx_tabuleiro
        pos_y += tile_y_tam
        cores_alternadas.next()

    return[lista_casas, all_sprites_list]
