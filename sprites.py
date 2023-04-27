import pygame
from constantes import *


class Circulos:
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.cor = cor

    def desenha(self, window): # Desenha os círculos 
        pygame.draw.circle(window, self.cor, (self.x, self.y), RAIO)

    def clicou(self, mouse_x, mouse_y): # Retorna True ou False se o mouse clicou no círculo
        return ((mouse_x - self.x) ** 2 + (mouse_y - self.y) **2 ) ** 0.5 <= RAIO
    

class CirculosClaros:
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.cor = cor

    def desenha(self, window): 
        pygame.draw.circle(window, self.cor, (self.x, self.y), RAIO)