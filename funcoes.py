import pygame
from itertools import cycle

class Block(pygame.sprite.Sprite):

    def __init__(self, sprite):
        super(Block, self).__init__()
        self.image = pygame.image.load(sprite)
        self.sprite = sprite
        self.rect = self.image.get_rect()



BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

BRANCO = "sprites/branco.jpg"
PRETO = "sprites/preto.jpg"


def desenha_tela():
    block_list = pygame.sprite.Group()

    all_sprites_list = pygame.sprite.Group()

    cores_alternadas = cycle([BRANCO,PRETO])

    pos_x=0
    pos_y=0

    for i in range(8):
        block = Block(cores_alternadas.next())

        block.rect.x = pos_x
        block.rect.y = pos_y
        pos_x+=56

        block_list.add(block)
        all_sprites_list.add(block)

    return[block_list, all_sprites_list]
