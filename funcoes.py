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
S_BRANCO = "sprites/branco.jpg"
S_PRETO = "sprites/preto.jpg"
S_ROSA = "sprites/rosa.png"
S_VERDE = "sprites/verde.png"

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

    pos = [posx_tabuleiro, posy_tabuleiro]

    for i in range(8):
        for j in range(8):

            cor = Cor(cores_alternadas.next(), tamanho_casas, pos)
            # cor = Casa(i+j, (pos_x,pos_y),cores_alternadas.next())

            pos[0]+= tamanho_casas[0]

            lista_casas.add(cor)
            all_sprites_list.add(cor)

        pos[0] = posx_tabuleiro
        pos[1]+= tamanho_casas[1]
        cores_alternadas.next()

    return[lista_casas, all_sprites_list]

def desenha_pedras():
    lista_pedras = pygame.sprite.Group()

    all_pedras_list = pygame.sprite.Group()

    cor = S_VERDE
    cores_alternadas = cycle([S_BRANCO,S_PRETO])

    pos = [posx_pedra, posy_pedra]

    for i in range(3):
        for j in range(8):
            casa = cores_alternadas.next()
            pedra = Pedra(pos, casa, cor)

            pos[0]+= tamanho_casas[0]
            if casa == S_PRETO:
                lista_pedras.add(pedra)
                all_pedras_list.add(pedra)

        pos[0] = posx_tabuleiro
        pos[1] += tamanho_casas[1]
        cores_alternadas.next()

    return[lista_pedras, all_pedras_list]
