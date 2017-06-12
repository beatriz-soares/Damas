# coding:utf-8
import pygame
from itertools import cycle

"""CONSTANTES"""
# CORES FLAT
BRANCO = (255, 255, 255)
AZUL  = (150, 206, 180)
BEGE  = (255, 238, 173)
VERMELHO = (255,0,0)
VERMELHO_ESCURO = (197, 81, 68)

# TIPOS DE PEÇA (COR DA PEÇA OU TIME)
S_PEDRA_ROSA = "sprites/pedra_rosa.png"
S_PEDRA_VERDE = "sprites/pedra_verde.png"

# SPRITES
S_CASA_BRANCA = "sprites/casa_branca.jpg"
S_CASA_PRETA = "sprites/casa_preta.jpg"

# TELAS
inicio = 1
jogo_1x1 = 2
jogo_1xPC = 3
fim = 4

# TEXTOS
texto_1x1 = 'JOGAR 1x1'
texto_1xPC = 'JOGAR 1xPC'

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

class Texto(pygame.sprite.Sprite):
    def __init__(self, dict_surface, dict_texto):
        super(Texto, self).__init__()

        tamanho = dict_surface['tamanho']
        cor = dict_surface['cor']
        pos = dict_surface['pos']

        self.image = pygame.Surface([tamanho[0], tamanho[1]])
        self.image.fill(cor)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.font = pygame.font.SysFont("Arial", dict_texto['size'])
        self.textSurf = self.font.render(dict_texto['text'], 1, dict_texto['color'])
        self.text = dict_texto['text']
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, (dict_surface['tamanho'][0]/2 - W/2, dict_surface['tamanho'][1]/2 - H/2))

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

def gerar_coisas_do_inicio():
    lista_coisas = pygame.sprite.Group()

    tam_botao = [100,50]

    meio_horizontal = screen_width/2 - tam_botao[0]/2
    meio_vertical = (screen_height/2 - tam_botao[1]/2)/2

    humano_surface = {'cor':BEGE, 'tamanho':tam_botao, 'pos':(meio_horizontal, meio_vertical)}
    humano_texto = {'size':15, 'color':VERMELHO_ESCURO, 'text':texto_1x1}

    maquina_surface = {'cor':BEGE, 'tamanho':tam_botao, 'pos':(meio_horizontal, meio_vertical + tam_botao[1]*1.5)}
    maquina_texto = {'size':15, 'color':VERMELHO_ESCURO, 'text':texto_1xPC}

    botao_humano = Texto(humano_surface, humano_texto)
    botao_maquina = Texto(maquina_surface, maquina_texto)

    lista_coisas.add(botao_humano)
    lista_coisas.add(botao_maquina)

    return lista_coisas

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
    casa_comer = []
    comida = []

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
                        casa_comer.append(casa_destino)
                        comida.append([casa_comida])
                        for possibilidade in comiveis:

                            comida_x, comida_y = destino_x + possibilidade[0][0], destino_y + possibilidade[0][1]
                            destino_x, destino_y = destino_x + possibilidade[1][0], destino_y + possibilidade[1][1]
                            if destino_x*destino_y >= 0:
                                try:
                                    casa_comida_2 = tabuleiro[comida_x][comida_y]
                                    casa_destino_2 = tabuleiro[destino_x][destino_y]
                                    if casa_comida_2.pedra and casa_comida_2.pedra.sprite != pedra.sprite:
                                        if not casa_destino_2.pedra and casa_destino_2 != casa_destino:
                                            casa_comer.remove(casa_destino)
                                            comida.remove([casa_comida])
                                            casa_comer.append(casa_destino_2)
                                            comida.append([casa_comida, casa_comida_2])
                                except Exception:
                                    pass
            except Exception as e:
                pass
    if len(casa_comer) > 0:
        return [casa_comer, comida]
    return [casas, comida]
