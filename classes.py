import pygame

cores = [
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 0),
    (255, 0, 0)
]

class Circulo:
    def __init__(self, x, y, raio):
        self.x = x
        self.y = y
        self.raio = raio
        self.lista_cores = cores

    def verifica_clique(self, x, y):
        self.x = x
        self.y = y
        self.distancia_ponto_centro = ((self.cx - self.x)**2 + (self.cy - self.y)**2)**0.5
        if self.distancia_ponto_centro <= self.raio:
            return True
        else:    
            return False
        
    def desenha(self, window):
        for i in range(len(self.lista_cores)):
            pygame.draw.circle(window, self.lista_cores[i], (self.x, self.y), self.raio)