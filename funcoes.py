# coding:utf-8
import pygame
from itertools import cycle

"""CONSTANTES"""
# CORES FLAT
BRANCO = (255, 255, 255)
AZUL  = (150, 206, 180)
BEGE  = (255, 238, 173)

# TIPOS DE PEÇA (COR DA PEÇA OU TIME)
S_PEDRA_ROSA = "sprites/pedra_rosa.png"
S_PEDRA_VERDE = "sprites/pedra_verde.png"

# SPRITES
S_CASA_BRANCA = "sprites/casa_branca.jpg"
S_CASA_PRETA = "sprites/casa_preta.jpg"

# ENVIRONMENT
screen_width = 520
screen_height = 520

posx_tabuleiro = 20
posy_tabuleiro = 20

tamanho_casas = (60,60)

"""CLASSES"""
class Cor(pygame.sprite.Sprite):

    def __init__(self, cor, tamanho, pos):
        super(Cor, self).__init__()
        self.image = pygame.Surface([tamanho[0], tamanho[1]])
        self.image.fill(cor)
        self.pos = pos
        self.rect = self.image.get_rect()
        em_pixels = pos_tabuleiro(pos[0],pos[1])
        self.rect.x = em_pixels[0]
        self.rect.y = em_pixels[1]

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

class Casa(Cor):
    def __init__(self, cor, tamanho, pos):
        super(Casa, self).__init__(cor, tamanho, pos)
        self.pedra = None

class Pedra(Botao):
    def __init__(self, pos, sprite):
        super(Pedra, self).__init__(sprite)
        self.pos = pos
        em_pixels = pos_tabuleiro(pos[0],pos[1])
        self.rect.x = em_pixels[0]
        self.rect.y = em_pixels[1]
        self.sprite = sprite


"""FUNÇÕES"""
def gerar_casas():
    lista_casas = pygame.sprite.Group()

    cores_alternadas = cycle([BEGE, AZUL])

    for i in range(8):
        for j in range(8):
            casa = Casa(cores_alternadas.next(), tamanho_casas, [i,j])
            lista_casas.add(casa)

        cores_alternadas.next()

    return lista_casas

def gerar_pedras(lista_casas):
    lista_pedras = pygame.sprite.Group()

    cores_alternadas = cycle([S_CASA_BRANCA,S_CASA_PRETA])

    for i in range(3):
        for j in range(8):
            casa = cores_alternadas.next()
            if casa == S_CASA_PRETA:
                pedra = Pedra([i,j], S_PEDRA_ROSA)
                casas_encontradas = pygame.sprite.spritecollide(pedra, lista_casas, False)
                lista_pedras.add(pedra)
                casas_encontradas[0].pedra = pedra

        cores_alternadas.next()

    for i in range(5,8):
        for j in range(8):
            casa = cores_alternadas.next()
            if casa == S_CASA_PRETA:
                pedra = Pedra([i,j], S_PEDRA_VERDE)
                casas_encontradas = pygame.sprite.spritecollide(pedra, lista_casas, False)
                lista_pedras.add(pedra)
                casas_encontradas[0].pedra = pedra

        cores_alternadas.next()

    return lista_pedras

def pos_tabuleiro(i,j):
    coluna = posx_tabuleiro + tamanho_casas[0] * i
    linha = posx_tabuleiro + tamanho_casas[1] * j

    return (linha,coluna)
