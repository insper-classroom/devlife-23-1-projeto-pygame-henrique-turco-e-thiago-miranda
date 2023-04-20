import pygame

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
    
    def desenha(self):
        for i in range(len(self.lista_cores)):
            pygame.draw.circle(self.window, self.lista_cores[i], self.posicoes[i], self.raio)