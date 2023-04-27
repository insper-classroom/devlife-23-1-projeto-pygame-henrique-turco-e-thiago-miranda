import pygame
import random
from sprites import *
from constantes import *

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TÍTULO)
        self.window = pygame.display.set_mode((LARGURA, ALTURA))
        self.fundo = pygame.image.load('img/Inicio-Pattern-Pursuit.png')
        self.fundo_modo_classico = pygame.image.load('img/Modo-Classico.png')

    def roda(self):
        self.desenha()
        pygame.display.update()

class TelaInicial(Jogo):
    def __init__(self):
        super().__init__()
        self.rect_modo_classico = pygame.Rect(235, 190, 330, 90)
        self.rect_modo_rapido = pygame.Rect(235, 290, 330, 90)
        self.rect_modo_escuro = pygame.Rect(235, 390, 330, 90)
        self.rect_sair = pygame.Rect(235, 490, 330, 90)

    def desenha(self):
        self.window.blit(self.fundo, (0, 0))
        pygame.display.update()

    def update(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                if mouse_rect.colliderect(self.rect_modo_classico):
                    return TelaClassico()
                elif mouse_rect.colliderect(self.rect_modo_rapido):
                    pass
                elif mouse_rect.colliderect(self.rect_modo_escuro):
                    pass
                elif mouse_rect.colliderect(self.rect_sair):
                    pygame.quit()
                    quit()
        return self # Retorna a própria tela inicial

class TelaClassico(Jogo):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption(MODO_CLASSICO)
        self.cores_claras = [AZUL, AMARELO, VERDE, VERMELHO]
        self.cores = [AZUL_ESCURO, AMARELO_ESCURO, VERDE_ESCURO, VERMELHO_ESCURO]

        self.circulos = [
            Circulos(300, 270, AZUL_ESCURO),
            Circulos(500, 270, AMARELO_ESCURO),
            Circulos(300, 470, VERDE_ESCURO),
            Circulos(500, 470, VERMELHO_ESCURO)
        ]

        self.circulos_claros = [
            CirculosClaros(300, 270, AZUL),
            CirculosClaros(500, 270, AMARELO),
            CirculosClaros(300, 470, VERDE),
            CirculosClaros(500, 470, VERMELHO) 
        ]

        self.sorteia = True
        self.mostra_circulo = True
        self.cores_sorteadas = []
        self.tempo_start = pygame.time.get_ticks()

    def sorteia_circulos(self): # ACHO QUE ESSA FUNÇÃO TÁ CERTA!!!
        if self.sorteia:
            cor_sorteada = random.choice(self.cores)
            self.cores_sorteadas.append(cor_sorteada) # Sorteia e coloca a cor na lista das sorteadas
            print(self.cores_sorteadas)

    def desenha(self):
        self.window.blit(self.fundo_modo_classico, (0, 0))
        for circulo_claro in self.circulos_claros: # Desenha os circulos claros
            circulo_claro.desenha(self.window)
        for circulo in self.circulos: # Desenha os circulos escuros depois
            circulo.desenha(self.window)

        # AQUI SERLF.SORTEIA VIRA FALSE E O CIRCULO ESCURO SOME DA LISTA DOS SORTEADOS 

    def update(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for circulo in self.circulos:
                    if circulo.clicou(mouse_x, mouse_y) == True:
                        self.botao_clicado = circulo.cor
        return self 
    
    def tempo(self):  
        self.tempo_passado = pygame.time.get_ticks() - self.tempo_start
        if self.tempo_passado > 1000:
            self.mostra_circulo = not self.mostra_circulo
            self.tempo_start = pygame.time.get_ticks()
            if self.mostra_circulo:
                self.indice_circulo+=1

class TelaGameOver(Jogo):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption(GAME_OVER)
        self.game_over = pygame.image.load('img/Game-Over-Pattern-Pursuit.png')
        self.rect_tentar_de_novo = pygame.Rect(235, 282, 330, 90)
        self.rect_voltar_inicio = pygame.Rect(235, 382, 330, 90)
        self.rect_sair = pygame.Rect(235, 482, 330, 90)

    def desenha(self):
        self.window.blit(self.game_over, (0, 0))
        pygame.display.update()

    def update(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                if mouse_rect.colliderect(self.rect_tentar_de_novo):
                    return TelaClassico() # GUARDAR EM UMA VARIAVEL A ULTIMA TELA USADA, PARA ASSIM RETORNÁ-LA AQUI
                elif mouse_rect.colliderect(self.rect_voltar_inicio):
                    return TelaInicial()
                elif mouse_rect.colliderect(self.rect_sair):
                    pygame.quit()
                    quit()
        return self 