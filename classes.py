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
        self.largura_janela = 900
        self.altura_janela = 600
        self.lista_cores = cores
        
        self.window = pygame.display.set_mode((self.largura_janela, self.altura_janela))
        pygame.display.set_caption('Pattern Pursuit')
        self.circulos = Circulo(self.window)
        self.retangulo = self.circulos.retangulo
        self.jogadas_player = []
        self.rect_sorteados = self.circulos.rect_sorteados
        self.validacao = True
        self.cores_sorteadas = self.circulos.cores_sorteadas
        self.rodada = 1
        


    def desenha(self, window):
        self.window.fill((0, 0, 0))
        self.circulos.desenha()
        
        pygame.display.update()
    
    def atualiza_estado(self):
        self.circulos.atualiza()
        if self.validacao:
            self.circulos.sorteia_circulos()
            self.validacao = False
        
        for event in pygame.event.get():
            self.x, self.y = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(self.x, self.y, 1, 1)
            
            if event.type == pygame.MOUSEBUTTONUP:
                
                if mouse_rect.colliderect(self.retangulo[0]):
                    
                    self.jogadas_player.append(self.lista_cores[0])
                
                elif mouse_rect.colliderect(self.retangulo[1]):
                    
                    self.jogadas_player.append(self.lista_cores[1])
                
                elif mouse_rect.colliderect(self.retangulo[2]):
                    
                    self.jogadas_player.append(self.lista_cores[2])
                
                elif mouse_rect.colliderect(self.retangulo[3]):
                    
                    self.jogadas_player.append(self.lista_cores[3])
                
                print(self.jogadas_player)
                print(self.cores_sorteadas)
                
                if self.jogadas_player == self.cores_sorteadas:
                    print('validou')
                    self.circulos.indice_circulo = 0
                    self.validacao = True
            
            if len(self.jogadas_player) == len(self.cores_sorteadas):
                self.jogadas_player = []
            
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
        self.rect_sorteados = []
        self.retangulo = []
        self.indice_circulo = 0
        self.tempo_start = pygame.time.get_ticks()
        self.mostra_circulo = True
    
    def sorteia_circulos(self):
        circulo_sorteado = random.choice(self.circulos)
        self.cores_sorteadas.append(circulo_sorteado[1])
        self.rect_sorteados.append(pygame.Rect(circulo_sorteado[2][0]-self.raio, circulo_sorteado[2][1]-self.raio, self.raio*2, self.raio*2))
    
    def desenha(self):
        
        for i in range(len(self.lista_cores)):
            r = pygame.Rect(self.posicoes[i][0] - self.raio, self.posicoes[i][1] - self.raio, self.raio*2, self.raio*2)
            self.retangulo.append(r) 
    
            if self.mostra_circulo or self.indice_circulo >= len(self.cores_sorteadas) or self.lista_cores[i] != self.cores_sorteadas[self.indice_circulo]:
                pygame.draw.circle(self.window, self.lista_cores[i], self.posicoes[i], self.raio)
            
    
            
    
    def atualiza(self):
        
        self.tempo_passado = pygame.time.get_ticks() - self.tempo_start
        print(self.tempo_passado)
            
        if self.tempo_passado > 1000:
            self.mostra_circulo = not self.mostra_circulo
            self.tempo_start = pygame.time.get_ticks()
            if self.mostra_circulo:
                self.indice_circulo+=1
        
                
            
        
        
        
        # # for cor in self.cores_sorteadas:   
        #    for circulos in self.circulos:     
        #         if circulos[1] == cor:
                
        #             pygame.draw.circle(self.window, (0, 0, 0), circulos[2], self.raio)
        #             pygame.display.update()
                    
                    
        #             pygame.draw.circle(self.window, cor, circulos[2], self.raio)
        #             pygame.display.update()
                    
                    
                       

                
                            
        
       
                            
        
                        




            

