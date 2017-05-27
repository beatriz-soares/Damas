# coding:utf-8
import pygame
from itertools import cycle

"""CONSTANTES"""
# CORES
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

# SPRITES
BRANCO = "sprites/branco.jpg"
PRETO = "sprites/preto.jpg"

# ENVIRONMENT
posx_tabuleiro = 20
posy_tabuleiro = 20

tile_x_tam = 56
tile_y_tam = 56

"""CLASSES"""
class Block(pygame.sprite.Sprite):

    def __init__(self, sprite):
        super(Block, self).__init__()
        self.image = pygame.image.load(sprite)
        self.sprite = sprite
        self.rect = self.image.get_rect()

"""FUNÇÕES"""
def desenha_tela():
    block_list = pygame.sprite.Group()

    all_sprites_list = pygame.sprite.Group()

    cores_alternadas = cycle([BRANCO,PRETO])

    pos_x = posx_tabuleiro
    pos_y = posy_tabuleiro

    for i in range(8):
        for j in range(8):
            block = Block(cores_alternadas.next())

            block.rect.x = pos_x
            block.rect.y = pos_y
            pos_x+= tile_x_tam

            block_list.add(block)
            all_sprites_list.add(block)

        pos_x = posx_tabuleiro
        pos_y += tile_y_tam
        cores_alternadas.next()

    return[block_list, all_sprites_list]
