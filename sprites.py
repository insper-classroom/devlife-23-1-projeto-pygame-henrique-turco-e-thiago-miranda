import pygame
from constantes import *


class QuadradoClaro:
    def __init__(self, x, y, largura_rect, altura_rect, cor):
        self.x = x
        self.y = y
        self.largura_rect = largura_rect
        self.altura_rect = altura_rect
        self.cor = cor

    def desenha(self, window): # Desenha os quadrados claros
        pygame.draw.rect(window, self.cor, (self.x, self.y, self.largura_rect, self.altura_rect))


# fonte: tutorial YouTube canal Tech & Gaming
class Pontuacao:
    def __init__(self, x, y, texto):
        self.x, self.y = x, y
        self.texto = texto

    def desenha(self, window):
        fonte = pygame.font.SysFont("Consolas", 16)
        texto = fonte.render(self.texto, True, BRANCO)
        window.blit(texto, (self.x, self.y))