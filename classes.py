import pygame
import random

cores = [
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 0),
    (255, 0, 0)
]

class Jogo:
    def __init__(self):
        pygame.init()
        self.largura_janela = 1000
        self.altura_janela = 600
        self.lista_cores = cores
        
        self.raio = 55
        self.window = pygame.display.set_mode((self.largura_janela, self.altura_janela))
        pygame.display.set_caption('Pattern Pursuit')
        self.circulos = Circulo(self.window)

    def desenha(self, window):
        self.window.fill((0, 0, 0))
        self.circulos.desenha()
        if self.circulos.verifica_clique():
            self.circulos.sorteia_cores()

        pygame.display.update()
    
    def atualiza_estado(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def game_loop(self):
        while self.atualiza_estado():
            self.desenha(self.window)

class Circulo:
    def __init__(self, window):
        self.window = window
        self.posicoes = [
        (340, 270),
        (560, 270),
        (340, 450),
        (560, 450)
        ]
        self.lista_cores = cores
        self.raio = 60
        self.circulos = []
        
        for i in range(len(self.lista_cores)):
            self.circulos.append((window, self.lista_cores[i], (self.posicoes[i]), self.raio))
        
        self.cores_sorteadas = []
        self.jogadas_player = []
    
    def desenha(self):
        for i in range(len(self.lista_cores)):
            pygame.draw.circle(self.window, self.lista_cores[i], self.posicoes[i], self.raio)
    
    def verifica_clique(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.distancia_ponto_centro = ((self.x - self.posicoes[0][0])**2 + (self.y - self.posicoes[0][1])**2)**(1/2)
        
        if self.distancia_ponto_centro <= self.raio:
            for circulos in self.circulos:
                if self.x == circulos[2][0] and self.y == circulos[2][1] and pygame.MOUSEBUTTONDOWN:
                    self.jogadas_player.append(circulos[1])
        
        if self.jogadas_player == self.cores_sorteadas:
            return True

    def sorteia_cores(self):
            
            cor_sorteada = random.choice(self.lista_cores)
            self.cores_sorteadas.append(cor_sorteada)
        
            for circulos in self.circulos:
                if circulos[1] == cor_sorteada:
                    pygame.draw.circle(self.window, cor_sorteada, circulos[2], self.raio)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    pygame.draw.circle(self.window, (0, 0, 0), circulos[2], self.raio)
                    pygame.display.update()
                    pygame.time.wait(1000)




            

