import pygame

largura_janela = 900
altura_janela = 600
cores = [
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 0),
    (255, 0, 0)
]

posicoes = [
    (340, 270),
    (560, 270),
    (340, 450),
    (560, 450)
]
raio = 55

#class Circulo:
#    def __init__(self, x, y, raio):
#        self.x = x
#        self.y = y
#        self.raio = raio
#        self.lista_cores = cores
#        self.lista_posicoes = posicoes
#        self.circulos = []
#    
#    def desenha(self, window):
#        for i in range(len(self.lista_cores)):
#            self.circulos.append((window, self.lista_cores[i], (self.lista_posicoes[i]), self.raio))
#    
#    def verifica_clique(self, x, y):
#        self.x = x
#        self.y = y
#        self.distancia_ponto_centro = ((self.cx - self.x)**2 + (self.cy - self.y)**2)**0.5
#        if self.distancia_ponto_centro <= self.raio:
#            return True
#        else:    
#            return False

class Jogo:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((largura_janela, altura_janela))
        pygame.display.set_caption('Pattern Pursuit')
        self.lista_cores = cores
        self.lista_posicoes = posicoes

    def desenha(self):
        self.window.fill((0, 0, 0))
        for i in range(len(self.lista_cores)):
            pygame.draw.circle(self.window, self.lista_cores[i], self.lista_posicoes[i], raio)
        pygame.display.update()
    
    def atualiza_estado(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def game_loop(self):
        while self.atualiza_estado():
            self.desenha()
