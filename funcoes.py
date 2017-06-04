# coding:utf-8
import pygame
from itertools import cycle

"""CONSTANTES"""
# CORES FLAT
BRANCO = (255, 255, 255)
AZUL  = (150, 206, 180)
BEGE  = (255, 238, 173)
VERMELHO_ESCURO = (197, 81, 68)

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
comiveis = (((1,1),(2,2)), ((1,-1),(2,-2)), ((-1,-1),(-2,-2)),((-1,1),(-2,2)))
tamanho_casas = (60,60)

# DECLARAÇÃO DE TABULEIRO
# O tabuleiro foi declarado aqui para que ele possa ser acessado
# globalmente pelas funções definidas abaixo e em seguida
# ser importado no arquivo base.py
tabuleiro = []

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
    def __init__(self, cor, tamanho, pos, ocupavel=False):
        super(Casa, self).__init__(cor, tamanho, pos)
        self.pedra = None
        self.ocupavel = ocupavel
        self.cor = cor
        self.id = None

    def __repr__(self):
        return '#%d @%d,%d' % (self.id, self.pos[0], self.pos[1])

class Pedra(Botao):
    def __init__(self, pos, sprite):
        super(Pedra, self).__init__(sprite)
        self.pos = pos
        em_pixels = pos_tabuleiro(pos[0],pos[1])
        self.rect.x = em_pixels[0]
        self.rect.y = em_pixels[1]
        self.sprite = sprite

        # ESSAS DIREÇÕES SÃO COMO VETORES QUE UTILIZAMOS PARA APONTAR QUE CASA PODE ANDAR
        if sprite == S_PEDRA_ROSA:
            self.direcoes = ((1,1),(1,-1))
        else:
            self.direcoes = ((-1,-1),(-1,1))



"""FUNÇÕES"""
def gerar_casas():
    global tabuleiro
    lista_casas = pygame.sprite.Group()

    cores_alternadas = cycle([BEGE, AZUL])

    for i in range(8):
        linha = []
        for j in range(8):
            casa = Casa(cores_alternadas.next(), tamanho_casas, [i,j])
            if casa.cor == AZUL:
                casa.ocupavel = True
            lista_casas.add(casa)
            linha.append(casa)
            casa.id = len(lista_casas)
        tabuleiro.append(linha)

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
    # CONVERTE COORDENADAS CARTESIANAS EM COORDENADAS DE PIXELS
    coluna = posx_tabuleiro + tamanho_casas[0] * i
    linha = posx_tabuleiro + tamanho_casas[1] * j

    return (linha,coluna)

def pintar_selecionavel(casa):
    casa.image.fill(VERMELHO_ESCURO)
    return casa

def pintar_neutralidade(casa):
    casa.image.fill(AZUL)
    return casa

def movimentos_possiveis(pedra):
    global tabuleiro
    casas = []
    comida = None

    for direcao in pedra.direcoes:
        x, y = pedra.pos[0] + direcao[0], pedra.pos[1] + direcao[1]
        if x*y >= 0:
            try:
                casa = tabuleiro[x][y]
                if not casa.pedra:
                    casas.append(casa)
            except Exception:
                pass

    for possibilidade in comiveis:
        comida_x, comida_y = pedra.pos[0] + possibilidade[0][0], pedra.pos[1] + possibilidade[0][1]
        destino_x, destino_y = pedra.pos[0] + possibilidade[1][0], pedra.pos[1] + possibilidade[1][1]

        if destino_x*destino_y >= 0:
            try:
                casa_comida = tabuleiro[comida_x][comida_y]
                casa_destino = tabuleiro[destino_x][destino_y]
                if casa_comida.pedra and casa_comida.pedra.sprite != pedra.sprite:
                    if not casa_destino.pedra:
                        del casas[:]
                        casas.append(casa_destino)
                        comida = casa_comida
                        return [casas, comida]
            except Exception:
                pass

    return [casas, comida]
