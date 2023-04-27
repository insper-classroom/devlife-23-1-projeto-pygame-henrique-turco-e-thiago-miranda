import pygame
from constantes import *

# MUDEI DE CÍRCULO PARA QUADRADOS

class Quadrado:
    def __init__(self, x, y, largura_rect, altura_rect, cor):
        self.x = x
        self.y = y
        self.largura_rect = largura_rect
        self.altura_rect = altura_rect
        self.cor = cor

    def desenha(self, window): # Desenha os círculos 
        pygame.draw.rect(window, self.cor, (self.x, self.y, self.largura_rect, self.altura_rect))

    # def clicou(self, mouse_x, mouse_y): # Retorna True ou False se o mouse clicou no círculo
    #     return ((mouse_x - self.x) ** 2 + (mouse_y - self.y) **2 ) ** 0.5 <= RAIO
    

class QuadradoClaro:
    def __init__(self, x, y, largura_rect, altura_rect, cor):
        self.x = x
        self.y = y
        self.largura_rect = largura_rect
        self.altura_rect = altura_rect
        self.cor = cor

    def desenha(self, window): 
        pygame.draw.rect(window, self.cor, (self.x, self.y, self.largura_rect, self.altura_rect))