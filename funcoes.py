import pygame

class Block(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super(Block, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()



BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)


def desenha_tela():
    block_list = pygame.sprite.Group()

    all_sprites_list = pygame.sprite.Group()

    pos_x=0
    pos_y=0

    for i in range(8):
        block = Block(BLACK, 20, 15)

        block.rect.x = pos_x
        block.rect.y = pos_y
        pos_x+=56
        block.image = pygame.image.load("branco.jpg")

        block_list.add(block)
        all_sprites_list.add(block)

    return[block_list, all_sprites_list]
